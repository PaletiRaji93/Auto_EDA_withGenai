# Auto EDA with GenAI

This project performs automated exploratory data analysis on a sales dataset using Python.
It uses Sweetviz for generating a visual HTML report and can optionally use YData Profiling if the required dependency is available.

## Features

- Verifies required library versions before running
- Loads `sales_data.csv` from the workspace root or from the `data/` folder
- Detects the sales target column automatically (`revenue` or `Sales`)
- Generates `sweetviz_report.html` with rich EDA visuals
- Attempts YData Profiling when `setuptools` and `ydata-profiling` are installed

## Setup

1. Create and activate your virtual environment:
   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```
2. Install required packages:
   ```powershell
   pip install -r requirements.txt
   ```
3. If YData Profiling fails with import errors, install or upgrade its packaging dependencies:
   ```powershell
   .\.venv\Scripts\python.exe -m pip install --upgrade setuptools platformdirs
   .\.venv\Scripts\python.exe -m pip install ydata-profiling
   ```

4. If you use Python 3.13 and `ydata-profiling` still fails, install `fg-data-profiling` instead or use Python 3.11/3.12:
   ```powershell
   .\.venv\Scripts\python.exe -m pip install fg-data-profiling
   ```

> Note: Python 3.13 often has compatibility issues with `pkg_resources` and YData Profiling packages. For best results, use Python 3.11 or 3.12 for profile generation.

## Usage

Run the script from the project root:

```powershell
python automated_eda_sales.py
```

The script will print status messages and create the report files.

## Output

- `sweetviz_report.html` — main generated report
- `ydata_report.html` — generated only when YData Profiling is available

Open `sweetviz_report.html` in a browser to review the EDA results.

## Dataset

Place the dataset file as either:

- `sales_data.csv` in the project root, or
- `data/sales_data.csv`   

The CSV should contain a sales metric column such as `Sales` or `revenue`.
