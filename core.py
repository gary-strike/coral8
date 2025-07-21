import json
import csv
import yaml         # YAML support
import openpyxl     # Excel support
from pathlib import Path
import ast

DATA_DIR = Path(".coral8")
DATA_DIR.mkdir(exist_ok=True)

def connect_file(source_path: str, alias: str = None):
    src = Path(source_path)
    if not src.exists():
        raise FileNotFoundError(f"File '{source_path}' not found. Please check the path.")

    name = alias or src.name

    # Sanitize alias (block traversal/nesting)
    if "/" in name or "\\" in name or ".." in name:
        raise ValueError(f"Invalid alias name '{name}'. Nested paths are not allowed.")

    dst = DATA_DIR / name
    try:
        dst.write_bytes(src.read_bytes())  # Copy file to DATA_DIR
        print(f"✅ Connected: {name}")
    except Exception as e:
        raise RuntimeError(f"Failed to connect file '{name}': {e}")

def import_file(name: str):
    file_path = DATA_DIR / name
    if not file_path.exists():
        raise FileNotFoundError(f"File '{name}' not found in connected files.")
    
    ext = file_path.suffix.lower()
    try:
        if ext == ".json":
            return json.loads(file_path.read_text())
        elif ext == ".csv":
            with file_path.open(newline="") as f:
                return list(csv.DictReader(f))
        elif ext in [".yml", ".yaml"]:
            with open(file_path, "r") as f:
                return yaml.safe_load(f)
        elif ext == ".xlsx":
            wb = openpyxl.load_workbook(file_path)
            sheet = wb.active
            data = []
            for row in sheet.iter_rows(values_only=True):
                data.append(row)
            return data
        elif ext == ".txt":
            return file_path.read_text()
        elif ext == ".py":
            return file_path.read_text()
        else:
            raise ValueError(f"Unsupported file type '{ext}' for file '{name}'.")
    except Exception as e:
        raise ValueError(f"Error loading file '{name}': {str(e)}")

def list_files():
    return [f.name for f in DATA_DIR.iterdir() if f.is_file()]

def inject_symbol(filename: str, symbol: str):
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"File '{filename}' not found.")
    if path.suffix != ".py":
        raise ValueError("Inject only works on Python files.")

    source = path.read_text()
    tree = ast.parse(source)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name == symbol:
            return ast.unparse(node)

    raise ValueError(f"Symbol '{symbol}' not found in {filename}.")


