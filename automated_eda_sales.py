#!/usr/bin/env python3
"""Automated Exploratory Data Analysis for a sales dataset."""

from __future__ import annotations

import re
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

MIN_VERSIONS = {
    "pandas": "2.0.0",
    "sweetviz": "2.3.0",
}
OPTIONAL_VERSIONS = {
    "ydata-profiling": "4.6.0",
    "fg-data-profiling": "4.19.0",
}


def parse_version(version_string: str) -> tuple[int, ...]:
    """Normalize a version string into a comparable tuple of integers."""
    return tuple(int(part) for part in re.findall(r"\d+", version_string))


def is_python_3_13_or_newer() -> bool:
    """Return True when running on Python 3.13 or newer."""
    return sys.version_info >= (3, 13)


def check_package_versions() -> bool:
    """Verify that the required libraries are installed with compatible versions."""
    print("Checking library versions...")

    if is_python_3_13_or_newer():
        print(
            "WARNING: Python 3.13+ may be incompatible with ydata-profiling/pkg_resources."
            " Use Python 3.11 or 3.12 for profiling support."
        )

    for package_name, minimum_version in MIN_VERSIONS.items():
        try:
            installed_version = version(package_name)
        except PackageNotFoundError:
            print(f"ERROR: {package_name} is not installed.")
            return False

        print(f"{package_name}: {installed_version}")

        if parse_version(installed_version) < parse_version(minimum_version):
            print(
                f"ERROR: {package_name} version {installed_version} is below the required minimum {minimum_version}."
            )
            return False

    for package_name, minimum_version in OPTIONAL_VERSIONS.items():
        try:
            installed_version = version(package_name)
        except PackageNotFoundError:
            print(
                f"WARNING: {package_name} is not installed. YData Profiling will be skipped."
            )
            continue

        print(f"{package_name}: {installed_version} (optional)")

        if parse_version(installed_version) < parse_version(minimum_version):
            print(
                f"WARNING: {package_name} version {installed_version} is below the optional minimum {minimum_version}."
            )
            print("YData Profiling may fail or be skipped.")

    print("All required library versions are compatible.")
    return True


def load_dataset(file_path: Path):
    """Load the sales dataset from CSV with basic error handling."""
    import pandas as pd

    try:
        df = pd.read_csv(file_path)
        print(f"Dataset loaded successfully from {file_path}.")
        return df
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        return None
    except pd.errors.ParserError as exc:
        print(f"WARNING: CSV parsing failed with the default parser: {exc}")
        try:
            df = pd.read_csv(file_path, sep=";", engine="python")
            print(
                f"Dataset loaded successfully from {file_path} using a fallback parser."
            )
            return df
        except Exception as exc2:
            print(f"ERROR: Could not parse dataset with fallback parser: {exc2}")
            return None
    except Exception as exc:  # pragma: no cover - defensive handling
        print(f"ERROR: Could not load dataset: {exc}")
        return None


def find_target_feature(df, preferred_targets: list[str]) -> str | None:
    """Choose a target feature from the dataset using case-insensitive matching."""
    lower_columns = {column.lower(): column for column in df.columns}
    for target in preferred_targets:
        if target.lower() in lower_columns:
            return lower_columns[target.lower()]
    return None


def generate_reports(df, target_feature: str):
    """Create YData Profiling and Sweetviz reports and save them as HTML files."""
    profile_report_cls = None

    try:
        from ydata_profiling import ProfileReport

        profile_report_cls = ProfileReport
    except Exception as exc:  # pragma: no cover - optional reporting
        try:
            from data_profiling import ProfileReport

            profile_report_cls = ProfileReport
            print("NOTE: Using data_profiling as a drop-in replacement for ydata_profiling.")
        except Exception as exc2:
            import importlib.util

            pkg_resources_installed = importlib.util.find_spec("pkg_resources") is not None
            print("ERROR: Failed to import ydata-profiling or data_profiling.")
            print(f"Details: {type(exc).__name__}: {exc}")
            print(f"Fallback details: {type(exc2).__name__}: {exc2}")
            if not pkg_resources_installed:
                print("The missing module 'pkg_resources' is provided by setuptools.")
                print(
                    "Install or upgrade it with:"
                    " .\\.venv\\Scripts\\python.exe -m pip install --upgrade setuptools platformdirs"
                )

            if is_python_3_13_or_newer():
                print(
                    "Python 3.13+ may still break profiling because pkg_resources compatibility is not stable."
                )
                print(
                    "For best results, create a Python 3.11 or 3.12 virtual environment and reinstall ydata-profiling."
                )
                print(
                    "If you want to try an alternative package, install:"
                    " .\\.venv\\Scripts\\python.exe -m pip install fg-data-profiling"
                )
            else:
                print(
                    "Install or upgrade optional profiling dependencies with:"
                    " .\\.venv\\Scripts\\python.exe -m pip install --upgrade ydata-profiling fg-data-profiling setuptools platformdirs"
                )
            print("Continuing with Sweetviz only.")

    try:
        import sweetviz as sv
    except ModuleNotFoundError as exc:
        print("ERROR: sweetviz is not installed. Install it with: python -m pip install sweetviz")
        return False

    if profile_report_cls is not None:
        try:
            ydata_report = profile_report_cls(df, minimal=True)
            ydata_report.to_file("ydata_report.html")
            print("YData Profiling report saved as ydata_report.html")
        except Exception as exc:  # pragma: no cover - defensive handling
            print(f"ERROR: Failed to create YData report: {exc}")
            print("Continuing with Sweetviz only.")

    try:
        sweetviz_report = sv.analyze(df, target_feat=target_feature)
        sweetviz_report.show_html("sweetviz_report.html")
        print("Sweetviz report saved as sweetviz_report.html")
    except Exception as exc:  # pragma: no cover - defensive handling
        print(f"ERROR: Failed to create Sweetviz report: {exc}")
        return False

    return True


def main() -> None:
    """Run the full EDA workflow."""
    if not check_package_versions():
        sys.exit(1)

    script_dir = Path(__file__).resolve().parent
    data_path = script_dir / "sales_data.csv"
    if not data_path.exists():
        data_path = script_dir / "data" / "sales_data.csv"

    df = load_dataset(data_path)

    if df is None:
        sys.exit(1)

    target_feature = find_target_feature(df, ["revenue", "sales", "amount", "total"])
    if target_feature is None:
        print("ERROR: The dataset does not contain a known target column.")
        print(f"Available columns: {', '.join(df.columns)}")
        sys.exit(1)

    if target_feature.lower() != "revenue":
        print(f"WARNING: Using '{target_feature}' as the target feature.")

    if generate_reports(df, target_feature):
        print("EDA workflow completed successfully.")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
