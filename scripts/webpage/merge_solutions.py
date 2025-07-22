import argparse
import json
import yaml
from pathlib import Path
from jsonschema import Draft202012Validator, RefResolver, ValidationError

# --- Config ---
OUTPUT_FILENAME = "merged.json"
SCHEMA_PATH = Path("webpage/collections/_schemas/solution-examples/v0.0.4.schema.json")
DEFS_DIR = SCHEMA_PATH.parent.parent / "definitions"

# --- Args ---
parser = argparse.ArgumentParser(description="Merge solution_examples from multiple JSON files.")
parser.add_argument("--index", required=True, help="Path to index.yml file")
parser.add_argument("--output-dir", help="Directory to write merged JSON (defaults to index file's folder)")
args = parser.parse_args()

index_path = Path(args.index)
input_folder = index_path.parent
output_dir = Path(args.output_dir) if args.output_dir else input_folder
output_path = output_dir / OUTPUT_FILENAME

# --- Read index.yml ---
with open(index_path, "r", encoding="utf-8") as f:
    index_data = yaml.safe_load(f)

# --- Merge all solution_examples ---
merged = {}
for file_key in index_data.get("files", []):
    json_path = input_folder / f"{file_key}.json"
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as jf:
            data = json.load(jf)
            examples = data.get("solution_examples", {})
            merged.update(examples)

# --- Wrap with top-level structure
final_output = {
    "schema_version": "1.0.0",
    "solution_examples": merged
}

# --- Load schema and all local definitions ---
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema = json.load(f)

store = {schema.get("$id", ""): schema}

# Load local definition files
for def_file in DEFS_DIR.glob("*.schema.json"):
    with open(def_file, "r", encoding="utf-8") as f:
        def_schema = json.load(f)
        if "$id" in def_schema:
            store[def_schema["$id"]] = def_schema

# --- Validate using RefResolver
resolver = RefResolver(base_uri=SCHEMA_PATH.resolve().as_uri(), referrer=schema, store=store)
validator = Draft202012Validator(schema, resolver=resolver)

try:
    errors = sorted(validator.iter_errors(final_output), key=lambda e: list(e.path))
    if errors:
        print("❌ Validation failed:")
        for err in errors:
            print(f"{list(err.path)}: {err.message}")
        exit(1)
    else:
        print(f"✅ Validation passed using schema: {SCHEMA_PATH}")
except ValidationError as ve:
    print(f"❌ Schema validation error:\n{ve}")
    exit(1)

# --- Write output
output_dir.mkdir(parents=True, exist_ok=True)
with open(output_path, "w", encoding="utf-8") as out_file:
    json.dump(final_output, out_file, indent=2)

print(f"✅ Merged {len(merged)} entries → {output_path}")
