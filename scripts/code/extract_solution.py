import argparse
import json
import os
import zipfile
from pathlib import Path
from dotenv import load_dotenv


def extract_solution_id(uis_zip_path):
    with zipfile.ZipFile(uis_zip_path, 'r') as zipf:
        uipx_files = [f for f in zipf.namelist() if f.endswith(".uipx") and '/' not in f]
        if len(uipx_files) != 1:
            raise ValueError("Expected exactly one .uipx file at root of zip.")
        with zipf.open(uipx_files[0]) as f:
            content = json.load(f)
            return content["SolutionId"]

# Extract initial Projects array from .uipx file
def extract_projects(uis_path):
    with zipfile.ZipFile(uis_path, 'r') as zipf:
        uipx_name = [f for f in zipf.namelist() if f.endswith(".uipx") and '/' not in f][0]
        with zipf.open(uipx_name) as f:
            uipx_data = json.load(f)
            return uipx_data.get("Projects", [])



def build_defaults(schema):
    t = schema.get("type")

    if t == "object":
        props = schema.get("properties", {})
        required = schema.get("required", [])
        return {
            k: build_defaults(props[k])
            for k in required if k in props
        }

    elif t == "array":
        items_schema = schema.get("items", {})
        if items_schema.get("type") == "object":
            return [build_defaults(items_schema)]
        else:
            return []

    elif t == "string":
        return ""
    elif t == "integer":
        return 0
    elif t == "number":
        return 0.0
    elif t == "boolean":
        return False

    return None

def apply_env_defaults(data, schema, prefix="DEFAULT__"):
    for key, value in os.environ.items():
        if not key.startswith(prefix):
            continue

        path_parts = key[len(prefix):].split("__")
        schema_cursor = schema["properties"]["solution_examples"]["patternProperties"]["^[a-f0-9\\-]{36}$"]
        data_cursor = next(iter(data["solution_examples"].values()))

        for i, part in enumerate(path_parts):
            is_last = i == len(path_parts) - 1

            # If array index
            if part.isdigit():
                index = int(part)
                if not isinstance(data_cursor, list):
                    break
                while len(data_cursor) <= index:
                    item_schema = schema_cursor.get("items", {})
                    data_cursor.append(build_defaults(item_schema))
                if is_last:
                    data_cursor[index] = cast_value(value, item_schema.get("type"))
                else:
                    data_cursor = data_cursor[index]
                    schema_cursor = item_schema
            else:
                # Match key case-insensitively
                key_match = next((k for k in data_cursor if k.lower() == part.lower()), None)
                if not key_match:
                    break  # key doesn't exist in schema/data
                if is_last:
                    t = schema_cursor["properties"][key_match].get("type")
                    data_cursor[key_match] = cast_value(value, t)
                else:
                    data_cursor = data_cursor[key_match]
                    schema_cursor = schema_cursor["properties"][key_match]



def cast_value(value, typ):
    if typ == "integer":
        return int(value)
    elif typ == "number":
        return float(value)
    elif typ == "boolean":
        return value.lower() in ("1", "true", "yes")
    return value  # string or unknown


def build_structure_from_schema(schema, solution_id):
    root = {
        "schema_version": "",
        "solution_examples": {}
    }

    pattern_schema = schema["properties"]["solution_examples"]["patternProperties"]["^[a-f0-9\\-]{36}$"]
    root["solution_examples"][solution_id] = build_defaults(pattern_schema)

    return root


def load_schema():
    schema_path = Path.cwd() / "webpage/collections/_schemas/solution-examples/latest.schema.json"
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Generate solution_examples structure from schema and .uis file.")
    parser.add_argument("uis_path", type=str, help="Path to the .uis file")
    args = parser.parse_args()

    uis_path = Path(args.uis_path)
    if not uis_path.exists() or uis_path.suffix != ".uis":
        print("Error: Provide a valid .uis file.")
        return

    env_path = Path.cwd() / ".env"
    if env_path.exists():
        load_dotenv(env_path)
    else:
        print("Warning: .env file not found.")

    try:
        solution_id = extract_solution_id(uis_path)
    except Exception as e:
        print(f"Error extracting SolutionId: {e}")
        return

    schema = load_schema()
    output_data = build_structure_from_schema(schema, solution_id)
    apply_env_defaults(output_data, schema)


    projects_from_uipx = extract_projects(uis_path)

    # Inject into structure
    projects_array = output_data["solution_examples"][solution_id]["solution"]["Projects"]

    # Replace the array with entries containing only basic fields from uipx
    projects_array.clear()
    for proj in projects_from_uipx:
        projects_array.append({
            "Type": proj.get("Type", ""),
            "ProjectRelativePath": proj.get("ProjectRelativePath", ""),
            "Id": proj.get("Id", ""),
            "Name": "",  # to be filled later
            "Description": "",
            "images": []
        })

    # Populate Name and Description for ProcessOrchestration projects
    with zipfile.ZipFile(uis_path, 'r') as zipf:
        for project in projects_array:
            rel_path = project["ProjectRelativePath"]

            if project["Type"] == "ProcessOrchestration" and rel_path.endswith(".uiproj"):
                try:
                    with zipf.open(rel_path) as f:
                        project_data = json.load(f)
                        if "Name" in project_data:
                            project["Name"] = project_data["Name"]
                        if "Description" in project_data and project_data["Description"] is not None:
                            project["Description"] = project_data["Description"]
                except Exception as e:
                    print(f"Warning: Failed to read project file '{rel_path}': {e}")

                # Handle entry-points.json and BPMN as before
                entry_path = str(Path(rel_path).parent / "entry-points.json").replace("\\", "/")
                if entry_path in zipf.namelist():
                    try:
                        with zipf.open(entry_path) as ef:
                            entry_data = json.load(ef)
                            entrypoints = entry_data.get("entryPoints", [])
                            if entrypoints:
                                ep = entrypoints[0]
                                if "input" in ep:
                                    project["inputs"] = ep["input"]
                                if "output" in ep:
                                    project["outputs"] = ep["output"]
                                if "filePath" in ep:
                                    bpmn_path = ep["filePath"].split("#")[0].lstrip("/content/")
                                    bpmn_full_path = str(Path(rel_path).parent / bpmn_path).replace("\\", "/")

                                    if bpmn_full_path in zipf.namelist():
                                        try:
                                            with zipf.open(bpmn_full_path) as bpmn_file:
                                                from xml.etree import ElementTree as ET
                                                tree = ET.parse(bpmn_file)
                                                root = tree.getroot()
                                                ns = {'bpmn': 'http://www.omg.org/spec/BPMN/20100524/MODEL'}
                                                doc = root.find('.//bpmn:documentation', ns)
                                                if doc is not None and doc.text and project["Description"] == "":
                                                    project["Description"] = doc.text.strip()
                                        except Exception as e:
                                            print(f"Warning: Failed to parse BPMN file '{bpmn_full_path}': {e}")
                    except Exception as e:
                        print(f"Warning: Failed to read entry-points.json for '{rel_path}': {e}")

            elif project["Type"] == "Process":
                folder = str(Path(rel_path).parent)
                project_json_path = f"{folder}/project.json".replace("\\", "/")

                if project_json_path in zipf.namelist():
                    try:
                        with zipf.open(project_json_path) as pf:
                            project_data = json.load(pf)
                            if "name" in project_data:
                                project["Name"] = project_data["name"]
                            if "description" in project_data and project_data["description"] is not None:
                                project["Description"] = project_data["description"]
                    except Exception as e:
                        print(f"Warning: Failed to read project.json for '{folder}': {e}")



    output_dir = Path.cwd() / "webpage/_data/solution_examples"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_filename = uis_path.stem + ".json"
    output_path = output_dir / output_filename

    if output_path.exists():
        confirm = input(f"File '{output_path}' exists. Overwrite? [y/N]: ").strip().lower()
        if confirm != "y":
            print("Cancelled.")
            return

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2)

    print(f"File written to {output_path}")


if __name__ == "__main__":
    main()
