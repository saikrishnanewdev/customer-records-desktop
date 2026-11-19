# Customer Records — Windows Desktop App (Python + PySide6)

A small starter Windows app: add a customer (name, phone, notes), save it
into a local SQLite database, see all saved records in a table, delete one.

## Run it (from source)

```bash
pip install -r requirements.txt
python main.py
```

Records are stored in `records.db` next to the app.

## Build the Windows .exe (on your Windows PC)

```bash
pip install -r requirements.txt
pip install pyinstaller
pyinstaller app.spec
```

The .exe appears at `dist/CustomerRecords.exe`. Give that single file to
anyone — no Python needed on their PC. The database file (`records.db`) is
created next to the .exe on first run.

## Build the .exe automatically (GitHub Actions)

Every push to `main` builds the .exe on a Windows machine in the cloud:

1. Push this project to a GitHub repo.
2. Open the repo → **Actions** tab → **Build Windows .exe** → the latest run.
3. Download the **CustomerRecords-windows** artifact — it contains the .exe.

## Files

| File | What it does |
| --- | --- |
| `main.py` | The window, form, table and buttons (PySide6) |
| `db.py` | SQLite: create table, add, list, delete |
| `requirements.txt` | Python packages needed |
| `app.spec` | PyInstaller recipe for the single-file .exe |
| `.github/workflows/build-windows.yml` | Auto-builds the .exe on every push |
