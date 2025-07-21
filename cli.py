import typer
from pathlib import Path
from coral8.core import connect_file, import_file, list_files, inject_symbol

app = typer.Typer()
DATA_DIR = Path(".coral8")
DATA_DIR.mkdir(exist_ok=True)

@app.command()
def connect(filename: str, alias: str = typer.Option(None, "--alias", "-a")):
    """
    Connect a file to your project. Supported: .json, .csv, .py, .txt, .yaml, .xlsx
    """
    try:
        connect_file(filename, alias)
    except FileNotFoundError as e:
        typer.echo(f"❌ {str(e)}")
        raise typer.Exit(code=1)
    except ValueError as e:
        typer.echo(f"❌ {str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {str(e)}")
        raise typer.Exit(code=1)

@app.command("import")
def import_(name: str):
    """
    Load and display metadata about a connected file.
    """
    try:
        result = import_file(name)
        typer.echo(f"✅ Loaded data of type {type(result).__name__} from '{name}'")
    except FileNotFoundError as e:
        typer.echo(f"❌ {str(e)}")
        raise typer.Exit(code=1)
    except ValueError as e:
        typer.echo(f"❌ {str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def list():
    """
    Show all connected files.
    """
    try:
        files = list_files()
        if not files:
            typer.echo("No files connected.")
            return
        for f in files:
            typer.echo(f"📎 {f}")
    except Exception as e:
        typer.echo(f"❌ Error listing files: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def inject(filename: str, symbol: str):
    """
    Extract and print a function or class from a Python file.
    """
    try:
        code = inject_symbol(filename, symbol)
        typer.echo(code)
    except FileNotFoundError as e:
        typer.echo(f"❌ {str(e)}")
        raise typer.Exit(code=1)
    except ValueError as e:
        typer.echo(f"❌ {str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {str(e)}")
        raise typer.Exit(code=1)

@app.command()
def clear(file: str = typer.Argument(..., help="File name to remove, or 'all' to clear everything")):
    """
    Remove a connected file or wipe all connections.
    """
    if not DATA_DIR.exists():
        typer.echo("❌ No files are currently connected.")
        raise typer.Exit()

    try:
        if file.lower() == "all":
            for f in DATA_DIR.iterdir():
                f.unlink()
            typer.echo("🧹 Cleared all connected files.")
        else:
            target = DATA_DIR / file
            if not target.exists():
                raise FileNotFoundError(f"File '{file}' not found in connected files.")
            target.unlink()
            typer.echo(f"✅ Removed: {file}")
    except FileNotFoundError as e:
        typer.echo(f"❌ {str(e)}")
        raise typer.Exit(code=1)
    except Exception as e:
        typer.echo(f"❌ Unexpected error: {str(e)}")
        raise typer.Exit(code=1)
