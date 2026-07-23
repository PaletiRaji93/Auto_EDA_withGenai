# Auto EDA with GenAI

This project is built to explore a sales dataset quickly with Python. It generates visual reports using Sweetviz, and it can also create an optional YData profile report when the profiling dependencies are available.

## What is included

- `automated_eda_sales.py` — runs automated EDA, generates `sweetviz_report.html`, and attempts YData profiling when possible
- `dtale_eda.py` — opens the dataset in D-Tale for interactive data inspection in your browser
- `data/sales_data.csv` — sample data used by both scripts
- `sweetviz_report.html` — generated report file
- `ydata_report.html` — generated only if YData Profiling works correctly

## What this project does

- checks required packages and versions
- loads the sales dataset from root or `data/` folder
- detects the main sales column automatically (`Sales`, `revenue`, or similar)
- creates a Sweetviz HTML report
- optionally creates a YData Profiling report when `setuptools` and profiling libraries are installed
- lets you inspect the same dataset in D-Tale with `dtale_eda.py`

## Setup

If you are using a conda environment with Python 3.11, run the following from the project folder:

```powershell
conda activate autoeda
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If you want YData Profiling to work reliably, also install or upgrade these packages:

```powershell
python -m pip install --upgrade setuptools platformdirs
python -m pip install --upgrade ydata-profiling fg-data-profiling
```

If `pkg_resources` is missing, the command below will fix it:

```powershell
python -m pip install --upgrade setuptools
```

## Running the EDA report

From the project root:

```powershell
python automated_eda_sales.py
```

Expected behavior:

- `sweetviz_report.html` should be created every time
- `ydata_report.html` is created only when profiling dependencies are available
- the script prints status messages and warns if it uses `Sales` instead of `revenue`

## Opening the report

After the script finishes, open `sweetviz_report.html` in your browser.

If YData Profiling succeeds, `ydata_report.html` will also be available.

## Using D-Tale

To inspect the dataset interactively:

```powershell
python dtale_eda.py
```

That script will launch D-Tale and print a local URL. Open the URL in your browser and press ENTER in the terminal when you are done.

## Dataset location

The project looks for the dataset in one of these places:

- `sales_data.csv` in the project root
- `data/sales_data.csv`

Your file should include a sales metric column such as `Sales`, `revenue`, `amount`, or `total`.

## Notes

- If Sweetviz runs successfully, `sweetviz_report.html` is ready to view.
- YData Profiling may fail if `setuptools` or `pkg_resources` is missing.
- Because you are using Python 3.11, this setup is a good fit for the profiling tools.
- If profiling still does not work, the main analysis is still available via Sweetviz and D-Tale.
