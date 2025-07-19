import argparse
import json
import yaml
from pathlib import Path
from jsonschema import validate, ValidationError

# --- Config ---
OUTPUT_FILENAME = "merged.json"
SCHEMA_PATH = Path("webpage/collections/_schemas/solution-examples/latest.schema.json")

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
with open(index_path, "r") as f:
    index_data = yaml.safe_load(f)

# --- Merge all solution_examples ---
merged = {}
for file_key in index_data.get("files", []):
    json_path = input_folder / f"{file_key}.json"
    if json_path.exists():
        with open(json_path, "r") as jf:
            data = json.load(jf)
            examples = data.get("solution_examples", {})
            merged.update(examples)

# --- Wrap with top-level structure
final_output = {
    "schema_version": "1.0.0",
    "solution_examples": merged
}

# --- Validate against schema
try:
    with open(SCHEMA_PATH, "r") as schema_file:
        schema = json.load(schema_file)
    validate(instance=final_output, schema=schema)
    print(f"✅ Validation passed using schema: {SCHEMA_PATH}")
except ValidationError as ve:
    print(f"❌ Validation failed:\n{ve.message}")
    exit(1)
except FileNotFoundError:
    print(f"❌ Schema file not found at: {SCHEMA_PATH}")
    exit(1)

# --- Write output
output_dir.mkdir(parents=True, exist_ok=True)
with open(output_path, "w") as out_file:
    json.dump(final_output, out_file, indent=2)

print(f"✅ Merged {len(merged)} entries → {output_path}")
