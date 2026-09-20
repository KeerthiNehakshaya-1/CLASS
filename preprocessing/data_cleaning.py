import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

INPUT_FILE = Path("data/raw/astronaut_data.csv")
OUTPUT_FILE = Path("data/processed/cleaned_data.csv")


# ---------------------------------------------------------
# Load dataset
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Original dataset shape:", df.shape)

print("\nOriginal columns:")
print(df.columns.tolist())


# ---------------------------------------------------------
# Check missing values
# ---------------------------------------------------------

print("\nMissing values:")
print(df.isnull().sum())


# ---------------------------------------------------------
# Remove duplicate records
# ---------------------------------------------------------

duplicate_count = df.duplicated().sum()

print("\nDuplicate records:", duplicate_count)

df = df.drop_duplicates()


# ---------------------------------------------------------
# Check data types
# ---------------------------------------------------------

print("\nData types:")
print(df.dtypes)


# ---------------------------------------------------------
# Check invalid values
# ---------------------------------------------------------

print("\nInvalid value checks:")

print("Sleep <= 0:",
      (df["Sleep_Hours"] <= 0).sum())

print("Reaction time <= 0:",
      (df["Reaction_Time_ms"] <= 0).sum())

print("Heart rate <= 0:",
      (df["Heart_Rate"] <= 0).sum())

print("Tasks completed < 0:",
      (df["Tasks_Completed"] < 0).sum())

print("Errors < 0:",
      (df["Errors"] < 0).sum())

print("Task complexity outside 1-10:",
      ((df["Task_Complexity"] < 1) |
       (df["Task_Complexity"] > 10)).sum())

print("Stress level outside 0-100:",
      ((df["Stress_Level"] < 0) |
       (df["Stress_Level"] > 100)).sum())


# ---------------------------------------------------------
# Handle missing values
# ---------------------------------------------------------

numeric_columns = df.select_dtypes(include="number").columns

df[numeric_columns] = df[numeric_columns].fillna(
    df[numeric_columns].median()
)


# ---------------------------------------------------------
# Save cleaned dataset
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)


# ---------------------------------------------------------
# Final information
# ---------------------------------------------------------

print("\nCleaned dataset shape:", df.shape)

print("\nCleaning completed successfully.")

print("\nCleaned file saved at:")
print(OUTPUT_FILE)