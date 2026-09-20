import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

INPUT_FILE = Path("data/processed/preprocessed_data.csv")
OUTPUT_FILE = Path("data/processed/cognitive_load_results.csv")


# ---------------------------------------------------------
# Load preprocessed data
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)


# ---------------------------------------------------------
# Weights for Cognitive Load Index
# ---------------------------------------------------------

WEIGHTS = {
    "Sleep_Fatigue_Normalized": 0.20,
    "Reaction_Time_Normalized": 0.15,
    "Heart_Rate_Normalized": 0.10,
    "Task_Complexity_Normalized": 0.15,
    "Errors_Normalized": 0.15,
    "Communication_Delay_Normalized": 0.10,
    "Stress_Normalized": 0.10,
    "Radiation_Normalized": 0.05
}


# ---------------------------------------------------------
# Calculate weighted Cognitive Load Index
# ---------------------------------------------------------

df["CLI"] = (
    df["Sleep_Fatigue_Normalized"]
    * WEIGHTS["Sleep_Fatigue_Normalized"]

    + df["Reaction_Time_Normalized"]
    * WEIGHTS["Reaction_Time_Normalized"]

    + df["Heart_Rate_Normalized"]
    * WEIGHTS["Heart_Rate_Normalized"]

    + df["Task_Complexity_Normalized"]
    * WEIGHTS["Task_Complexity_Normalized"]

    + df["Errors_Normalized"]
    * WEIGHTS["Errors_Normalized"]

    + df["Communication_Delay_Normalized"]
    * WEIGHTS["Communication_Delay_Normalized"]

    + df["Stress_Normalized"]
    * WEIGHTS["Stress_Normalized"]

    + df["Radiation_Normalized"]
    * WEIGHTS["Radiation_Normalized"]
)


# ---------------------------------------------------------
# Convert CLI from 0-1 to 0-100
# ---------------------------------------------------------

df["CLI"] = df["CLI"] * 100


# ---------------------------------------------------------
# Round CLI
# ---------------------------------------------------------

df["CLI"] = df["CLI"].round(2)


# ---------------------------------------------------------
# Assign cognitive load level
# ---------------------------------------------------------

def classify_load(cli):

    if cli < 25:
        return "Low"

    elif cli < 50:
        return "Moderate"

    elif cli < 75:
        return "High"

    else:
        return "Very High"


df["Cognitive_Load_Level"] = df["CLI"].apply(
    classify_load
)


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("=" * 60)
print("COGNITIVE LOAD INDEX RESULTS")
print("=" * 60)

print(
    df[
        [
            "Mission_Day",
            "Astronaut_ID",
            "CLI",
            "Cognitive_Load_Level"
        ]
    ].to_string(index=False)
)


print("\nAverage CLI:")

print(
    round(df["CLI"].mean(), 2)
)


print("\nHighest CLI:")

highest = df.loc[df["CLI"].idxmax()]

print(
    "Mission Day:",
    highest["Mission_Day"]
)

print(
    "Astronaut:",
    highest["Astronaut_ID"]
)

print(
    "CLI:",
    highest["CLI"]
)

print(
    "Level:",
    highest["Cognitive_Load_Level"]
)


print("\nResults saved at:")

print(OUTPUT_FILE)

print("\nCognitive Load Index calculation completed.")