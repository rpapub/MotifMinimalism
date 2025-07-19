#!/usr/bin/env python3

import argparse
import json
import os
from pathlib import Path
from jsonschema import Draft202012Validator
from genson import SchemaBuilder


def normalize_type(input_type: str) -> str:
    """
    Converts dash-case to snake_case for internal JSON keys.
    """
    return input_type.replace("-", "_")


def load_json(filepath: str) -> dict:
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(filepath: Path, content: dict):
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(content, f, indent=2)


def build_pattern_properties_schema(items: dict) -> dict:
    builder = SchemaBuilder(schema_uri="https://json-schema.org/draft/2020-12/schema")
    for value in items.values():
        builder.add_object(value)
    schema = builder.to_schema()

    # Patch only inside the Projects array
    try:
        projects_schema = schema["properties"]["solution"]["properties"]["Projects"]["items"]["properties"]
        for key in ["inputs", "outputs"]:
            if key in projects_schema:
                projects_schema[key] = {
                    "type": "object",
                    "additionalProperties": True
                }
    except KeyError:
        pass  # Projects array not found or malformed

    return {
        "type": "object",
        "patternProperties": {
            "^[a-f0-9\\-]{36}$": schema
        },
        "additionalProperties": False
    }


def build_root_schema(data_key: str, inner_schema: dict, version: str) -> dict:
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"https://rpapub.github.io/MotifMinimalism/schemas/{data_key.replace('_', '-')}/{version}.schema.json",
        "title": data_key.replace("_", " ").title(),
        "type": "object",
        "properties": {
            "schema_version": {"type": "string"},
            data_key: inner_schema
        },
        "required": ["schema_version", data_key]
    }


def main():
    parser = argparse.ArgumentParser(description="Generate a JSON Schema from data")
    parser.add_argument("input_file", help="Path to input JSON data file")
    parser.add_argument("--type", required=True, help="Data type (e.g., 'solution-examples')")
    parser.add_argument("--version", required=True, help="Schema version (e.g., 'v0.0.2')")
    args = parser.parse_args()

    folder_name = args.type  # dash-case for output folders
    data_key = normalize_type(args.type)  # snake_case for internal JSON

    data = load_json(args.input_file)

    if data_key not in data:
        raise KeyError(f"Top-level key '{data_key}' not found in data")

    # Extract UUID-keyed entries
    entries = data[data_key]
    inner_schema = build_pattern_properties_schema(entries)

    schema = build_root_schema(data_key, inner_schema, args.version)

    # Validate schema is itself valid
    Draft202012Validator.check_schema(schema)

    out_dir = Path("webpage/collections/_schemas") / folder_name
    version_path = out_dir / f"{args.version}.schema.json"
    latest_path = out_dir / "latest.schema.json"

    write_json(version_path, schema)
    write_json(latest_path, schema)

    print("✅ Schema written to:")
    print(f"- {version_path}")
    print(f"- {latest_path}")


if __name__ == "__main__":
    main()
