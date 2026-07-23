import os
import pandas as pd
import dtale

# Get the project directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Dataset path
file_path = os.path.join(BASE_DIR, "data", "sales_data.csv")

try:
    df = pd.read_csv(file_path)
    print("Dataset loaded successfully.")
    print(f"Shape: {df.shape}")

except FileNotFoundError:
    print(f"ERROR: Dataset not found:\n{file_path}")
    exit()

except Exception as e:
    print(f"Error loading dataset:\n{e}")
    exit()

print("Launching D-Tale...")

d = dtale.show(df)

print("\nD-Tale launched successfully!")
print(f"Open this URL in your browser:\n{d._main_url}")

input("\nPress ENTER to close D-Tale...")

d.kill()