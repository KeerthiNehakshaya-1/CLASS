import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

INPUT_FILE = Path("data/processed/cleaned_data.csv")
OUTPUT_FILE = Path("data/processed/preprocessed_data.csv")


# ---------------------------------------------------------
# Load cleaned dataset
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Loaded dataset:")
print(df.head())


# ---------------------------------------------------------
# Min-Max Normalization
# ---------------------------------------------------------

def normalize(series):
    minimum = series.min()
    maximum = series.max()

    if maximum == minimum:
        return 0

    return (series - minimum) / (maximum - minimum)


# ---------------------------------------------------------
# Parameters where HIGH value means HIGH cognitive load
# ---------------------------------------------------------

df["Reaction_Time_Normalized"] = normalize(
    df["Reaction_Time_ms"]
)

df["Heart_Rate_Normalized"] = normalize(
    df["Heart_Rate"]
)

df["Task_Complexity_Normalized"] = normalize(
    df["Task_Complexity"]
)

df["Errors_Normalized"] = normalize(
    df["Errors"]
)

df["Radiation_Normalized"] = normalize(
    df["Radiation_Exposure"]
)

df["Communication_Delay_Normalized"] = normalize(
    df["Communication_Delay_sec"]
)

df["Stress_Normalized"] = normalize(
    df["Stress_Level"]
)


# ---------------------------------------------------------
# Sleep normalization
# LOW sleep = HIGH cognitive load
#
# Therefore we reverse the normalized value.
# ---------------------------------------------------------

sleep_normalized = normalize(df["Sleep_Hours"])

df["Sleep_Fatigue_Normalized"] = 1 - sleep_normalized


# ---------------------------------------------------------
# Task performance
#
# More completed tasks = better performance.
# We normalize it for later metric calculations.
# ---------------------------------------------------------

df["Tasks_Completed_Normalized"] = normalize(
    df["Tasks_Completed"]
)


# ---------------------------------------------------------
# Save preprocessed dataset
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_FILE, index=False)


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\nNormalization completed.")

print("\nNormalized columns:")

print([
    "Reaction_Time_Normalized",
    "Heart_Rate_Normalized",
    "Task_Complexity_Normalized",
    "Errors_Normalized",
    "Radiation_Normalized",
    "Communication_Delay_Normalized",
    "Stress_Normalized",
    "Sleep_Fatigue_Normalized",
    "Tasks_Completed_Normalized"
])

print("\nSample normalized data:")

print(
    df[
        [
            "Mission_Day",
            "Astronaut_ID",
            "Sleep_Fatigue_Normalized",
            "Reaction_Time_Normalized",
            "Stress_Normalized",
            "Errors_Normalized"
        ]
    ].head()
)

print("\nPreprocessed dataset saved at:")
print(OUTPUT_FILE)