import pandas as pd
import numpy as np
from pathlib import Path


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "preprocessed_data.csv"
OUTPUT_FILE = BASE_DIR / "data" / "processed" / "performance_stability_results.csv"


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Data loaded successfully.")
print("Input records:", len(df))


# ---------------------------------------------------------
# Sort data
# ---------------------------------------------------------

df = df.sort_values(
    by=["Astronaut_ID", "Mission_Day"]
).reset_index(drop=True)


# ---------------------------------------------------------
# Create Performance Indicator
# ---------------------------------------------------------
# Higher value = better performance.
#
# Tasks completed      -> higher is better
# Errors                -> lower is better
# Reaction time         -> lower is better

df["Performance_Indicator"] = (
    df["Tasks_Completed_Normalized"] * 0.40
    + (1 - df["Errors_Normalized"]) * 0.30
    + (1 - df["Reaction_Time_Normalized"]) * 0.30
)


# ---------------------------------------------------------
# Calculate rolling performance variation
# ---------------------------------------------------------
# A 3-day window is used.
#
# Higher standard deviation means more variation.
# Lower standard deviation means more stable performance.

df["Performance_Rolling_STD"] = (
    df.groupby("Astronaut_ID")["Performance_Indicator"]
      .transform(
          lambda x: x.rolling(window=3, min_periods=2).std()
      )
)


# ---------------------------------------------------------
# Handle first available values
# ---------------------------------------------------------

df["Performance_Rolling_STD"] = (
    df["Performance_Rolling_STD"].fillna(0)
)


# ---------------------------------------------------------
# Convert variation into stability
# ---------------------------------------------------------
# Higher variation -> lower stability
# Lower variation -> higher stability

maximum_variation = df["Performance_Rolling_STD"].max()

if maximum_variation == 0:
    df["Performance_Stability_Score"] = 100
else:
    df["Performance_Stability_Score"] = (
        1
        - (
            df["Performance_Rolling_STD"]
            / maximum_variation
        )
    ) * 100


# ---------------------------------------------------------
# Stability Classification
# ---------------------------------------------------------

def classify_stability(score):

    if score < 40:
        return "Unstable"

    elif score < 70:
        return "Moderately Stable"

    else:
        return "Stable"


df["Stability_Level"] = (
    df["Performance_Stability_Score"]
    .apply(classify_stability)
)


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\nPerformance Stability Analysis Completed.")

print("\nStability Results:")

print(
    df[
        [
            "Mission_Day",
            "Astronaut_ID",
            "Performance_Indicator",
            "Performance_Rolling_STD",
            "Performance_Stability_Score",
            "Stability_Level"
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

average_stability = (
    df["Performance_Stability_Score"].mean()
)

highest_stability = df.loc[
    df["Performance_Stability_Score"].idxmax()
]

lowest_stability = df.loc[
    df["Performance_Stability_Score"].idxmin()
]


print("\n----------------------------------------")

print(
    "Average Performance Stability:",
    round(average_stability, 2)
)

print(
    "Highest Stability:",
    highest_stability["Astronaut_ID"],
    "Day",
    highest_stability["Mission_Day"],
    "Score:",
    round(
        highest_stability["Performance_Stability_Score"],
        2
    )
)

print(
    "Lowest Stability:",
    lowest_stability["Astronaut_ID"],
    "Day",
    lowest_stability["Mission_Day"],
    "Score:",
    round(
        lowest_stability["Performance_Stability_Score"],
        2
    )
)

print("----------------------------------------")

print("\nOutput saved to:")
print(OUTPUT_FILE)
