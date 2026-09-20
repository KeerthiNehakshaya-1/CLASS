import pandas as pd
import numpy as np
from pathlib import Path


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "preprocessed_data.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "fatigue_recovery_results.csv"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Data loaded successfully.")
print("Input records:", len(df))


# ---------------------------------------------------------
# Sleep Recovery Component
# ---------------------------------------------------------
# 8 hours is used as the reference sleep duration.
# Values above 8 hours are capped at 100%.

df["Sleep_Recovery_Score"] = (
    df["Sleep_Hours"] / 8
).clip(0, 1) * 100


# ---------------------------------------------------------
# Reaction Performance Component
# ---------------------------------------------------------
# Lower reaction time indicates better performance.
#
# Reaction_Time_Normalized:
# 0 = lowest reaction time
# 1 = highest reaction time
#
# Therefore:
# 1 - normalized value = better performance

df["Reaction_Recovery_Score"] = (
    1 - df["Reaction_Time_Normalized"]
) * 100


# ---------------------------------------------------------
# Fatigue Recovery Score
# ---------------------------------------------------------
# Sleep contributes 60%
# Reaction performance contributes 40%

df["Fatigue_Recovery_Score"] = (
    df["Sleep_Recovery_Score"] * 0.60
    + df["Reaction_Recovery_Score"] * 0.40
)


# ---------------------------------------------------------
# Recovery Level
# ---------------------------------------------------------

def classify_recovery(score):

    if score < 40:
        return "Poor Recovery"

    elif score < 70:
        return "Moderate Recovery"

    else:
        return "Good Recovery"


df["Recovery_Level"] = df["Fatigue_Recovery_Score"].apply(
    classify_recovery
)


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\nFatigue Recovery Analysis Completed.")

print("\nRecovery Results:")
print(
    df[
        [
            "Mission_Day",
            "Astronaut_ID",
            "Sleep_Hours",
            "Reaction_Time_ms",
            "Fatigue_Recovery_Score",
            "Recovery_Level"
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

average_recovery = df["Fatigue_Recovery_Score"].mean()

highest_recovery = df.loc[
    df["Fatigue_Recovery_Score"].idxmax()
]

lowest_recovery = df.loc[
    df["Fatigue_Recovery_Score"].idxmin()
]


print("\n----------------------------------------")
print("Average Fatigue Recovery Score:",
      round(average_recovery, 2))

print(
    "Highest Recovery:",
    highest_recovery["Astronaut_ID"],
    "Day",
    highest_recovery["Mission_Day"],
    "Score:",
    round(highest_recovery["Fatigue_Recovery_Score"], 2)
)

print(
    "Lowest Recovery:",
    lowest_recovery["Astronaut_ID"],
    "Day",
    lowest_recovery["Mission_Day"],
    "Score:",
    round(lowest_recovery["Fatigue_Recovery_Score"], 2)
)

print("----------------------------------------")

print("\nOutput saved to:")
print(OUTPUT_FILE)