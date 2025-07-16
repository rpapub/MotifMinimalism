#!/usr/bin/env python3
import os
import re
import shutil
import sys
import zipfile
import json
from pathlib import Path

def sanitize_filename(filename):
    name = re.sub(r'[_\-]v?\d[\w\.\-]*$', '', filename)
    name = re.sub(r'_+$', '', name)
    return name

def main(zip_path_str):
    zip_path = Path(zip_path_str).resolve()
    if not zip_path.is_file():
        print(f"File not found: {zip_path}")
        sys.exit(1)

    static_target = Path.cwd() / "static" / "Invocation"
    static_target.mkdir(parents=True, exist_ok=True)
    shutil.copy2(zip_path, static_target / zip_path.name)

    base_name = zip_path.stem
    stripped = sanitize_filename(base_name)
    prefix = stripped.split('_')[0]

    target_folder = Path.cwd() / prefix / stripped
    print(f"Target folder: {target_folder}")
    target_folder.mkdir(parents=True, exist_ok=True)
    for item in target_folder.glob("**/*"):
        try:
            if item.is_file():
                item.unlink()
            elif item.is_dir():
                shutil.rmtree(item)
        except Exception as e:
            print(f"Error deleting {item}: {e}")

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(target_folder)
        print(f"Extracted to {target_folder}")

    metadata = {}

    # 1. Parse .uipx file
    uipx_files = list(target_folder.glob("*.uipx"))
    print(f"[DEBUG] Found {len(uipx_files)} .uipx files")
    if len(uipx_files) == 1:
        try:
            with open(uipx_files[0], "r", encoding="utf-8") as f:
                data = json.load(f)
                metadata["StudioMinVersion"] = data.get("StudioMinVersion")
                metadata["SolutionId"] = data.get("SolutionId")
        except Exception as e:
            print(f"[ERROR] Failed to parse uipx: {e}")
    else:
        metadata["StudioMinVersion"] = None
        metadata["SolutionId"] = None

    # 2. Parse solutionResourcesDefinition.json
    resources_path = target_folder / "solutionResourcesDefinition.json"
    print(f"[DEBUG] Checking for file: {resources_path}")
    if resources_path.is_file():
        try:
            with open(resources_path, "r", encoding="utf-8") as f:
                solution_data = json.load(f)
                resources = solution_data.get("Resources", [])
                print(f"[DEBUG] Resources array length: {len(resources)}")
                if resources:
                    res = resources[0]
                    spec = res.get("Spec", {})
                    metadata["ProjectKey"] = res.get("ProjectKey")
                    metadata["name"] = spec.get("name")
                    metadata["description"] = spec.get("description")
                    metadata["targetFrameworkValue"] = spec.get("targetFrameworkValue")
        except Exception as e:
            print(f"[ERROR] Failed to parse solutionResourcesDefinition.json: {e}")

    # 3. Locate and extract all project.json files
    metadata["Projects"] = []
    project_jsons = []

    root_pj = target_folder / "project.json"
    if root_pj.exists():
        project_jsons.append(root_pj)

    for sub in target_folder.iterdir():
        if sub.is_dir():
            pj = sub / "project.json"
            if pj.exists():
                project_jsons.append(pj)

    print(f"[DEBUG] Found {len(project_jsons)} project.json files")
    for pj_path in project_jsons:
        try:
            with open(pj_path, "r", encoding="utf-8") as f:
                pj_data = json.load(f)
                metadata["Projects"].append({
                    "path": str(pj_path.relative_to(target_folder)),
                    "name": pj_data.get("name"),
                    "description": pj_data.get("description"),
                    "dependencies": pj_data.get("dependencies", {}),
                    "studioVersion": pj_data.get("studioVersion"),
                    "projectVersion": pj_data.get("projectVersion")
                })
        except Exception as e:
            print(f"[ERROR] Failed to parse {pj_path}: {e}")

    # 4. Locate and extract all project.uiproj files
    metadata["ProjectUiproj"] = []
    uiproj_files = []

    for sub in target_folder.iterdir():
        if sub.is_dir():
            candidate = sub / "project.uiproj"
            if candidate.exists():
                uiproj_files.append(candidate)

    print(f"[DEBUG] Found {len(uiproj_files)} project.uiproj files")
    for up_path in uiproj_files:
        try:
            with open(up_path, "r", encoding="utf-8") as f:
                up_data = json.load(f)
                metadata["ProjectUiproj"].append({
                    "path": str(up_path.relative_to(target_folder)),
                    "ProjectType": up_data.get("ProjectType"),
                    "Name": up_data.get("Name"),
                    "Description": up_data.get("Description")
                })
        except Exception as e:
            print(f"[ERROR] Failed to parse {up_path}: {e}")

    print(json.dumps(metadata, indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_solution.py <path_to_zip_file>")
        sys.exit(1)
    main(sys.argv[1])
