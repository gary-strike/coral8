 **coral8** is a zero-config CLI tool that lets you register, inspect, and inject data or code files in Python projects. It’s minimal, modular, and built for local workflows.

---

##  Features

- `coral8 bridge` — register any `.csv`,`.xlsx`,`.yaml`, `.json`, or `.txt` file
- `coral8 peek` — preview the data via command line
- `coral8 graft` — copy Python functions across `.py` files safely via AST
- `coral8 vault` — see what you’ve registered
- `--alias` support — avoid filename collisions with ease
- `coral8 scrub all` - declutter your coral8 space

Coral8 is NOT a data parser. It’s the layer that makes parsing possible.

Modern projects rely on multiple file formats—CSV, JSON, YAML, TXT, and more. But bridging them across tools, scripts, and notebooks often leads to:

Redundant loaders for each format

Hardcoded paths scattered across files

Confusion over which data files are in use

Coral8 provides a consistent interface to register, manage, and access data files across your entire project.

Use Coral8 to:
Register multiple files from different formats in one step

Safely alias filenames to avoid collisions

Preview connected files directly from the command line

Load registered files into Python with consistent logic

Inject shared functions across .py files using AST-based replacement

Plays well with:
Data analysis tools like pandas, polars, or dask

Machine learning pipelines with mixed input sources

Jupyter notebooks and research workflows

Lightweight CLI-based ETL pipelines
---

##  Installation

You can now install **coral8** directly from PyPI:

```bash
pip install coral8

---

##  Example

python

from coral8.loader import parse_file

sales = parse_file("sales_2022.csv")
config = parse_file("model.yaml")
logdata = parse_file("clickstream.json")

# Use with pandas, or pass directly into other tooling
Once a file is registered, Coral8 handles the rest—no boilerplate, no guesswork.
