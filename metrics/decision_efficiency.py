import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "preprocessed_data.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "decision_efficiency_results.csv"
)


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Data loaded successfully.")
print("Input records:", len(df))


# ---------------------------------------------------------
# Decision Efficiency Components
# ---------------------------------------------------------

# 1. Task Completion
# Higher number of completed tasks = better efficiency

task_component = (
    df["Tasks_Completed_Normalized"]
)


# 2. Error Performance
# Fewer errors = better efficiency

error_component = (
    1 - df["Errors_Normalized"]
)


# 3. Reaction Performance
# Lower reaction time = better efficiency

reaction_component = (
    1 - df["Reaction_Time_Normalized"]
)


# ---------------------------------------------------------
# Decision Efficiency Score
# ---------------------------------------------------------

df["Decision_Efficiency_Score"] = (
    task_component * 0.40
    + error_component * 0.30
    + reaction_component * 0.30
) * 100


# ---------------------------------------------------------
# Classification
# ---------------------------------------------------------

def classify_efficiency(score):

    if score < 40:
        return "Low Efficiency"

    elif score < 70:
        return "Moderate Efficiency"

    else:
        return "High Efficiency"


df["Decision_Efficiency_Level"] = (
    df["Decision_Efficiency_Score"]
    .apply(classify_efficiency)
)


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

df.to_csv(OUTPUT_FILE, index=False)


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\nDecision Efficiency Analysis Completed.")

print("\nDecision Efficiency Results:")

print(
    df[
        [
            "Mission_Day",
            "Astronaut_ID",
            "Tasks_Completed",
            "Errors",
            "Reaction_Time_ms",
            "Decision_Efficiency_Score",
            "Decision_Efficiency_Level"
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

average_efficiency = (
    df["Decision_Efficiency_Score"].mean()
)

highest_efficiency = df.loc[
    df["Decision_Efficiency_Score"].idxmax()
]

lowest_efficiency = df.loc[
    df["Decision_Efficiency_Score"].idxmin()
]


print("\n----------------------------------------")

print(
    "Average Decision Efficiency:",
    round(average_efficiency, 2)
)

print(
    "Highest Efficiency:",
    highest_efficiency["Astronaut_ID"],
    "Day",
    highest_efficiency["Mission_Day"],
    "Score:",
    round(
        highest_efficiency["Decision_Efficiency_Score"],
        2
    )
)

print(
    "Lowest Efficiency:",
    lowest_efficiency["Astronaut_ID"],
    "Day",
    lowest_efficiency["Mission_Day"],
    "Score:",
    round(
        lowest_efficiency["Decision_Efficiency_Score"],
        2
    )
)

print("----------------------------------------")

print("\nOutput saved to:")
print(OUTPUT_FILE)