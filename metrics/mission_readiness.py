import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

CLI_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "cognitive_load_results.csv"
)

FRS_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "fatigue_recovery_results.csv"
)

PSI_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "performance_stability_results.csv"
)

DES_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "decision_efficiency_results.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "mission_readiness_results.csv"
)


# ---------------------------------------------------------
# Load metric files
# ---------------------------------------------------------

cli = pd.read_csv(CLI_FILE)

frs = pd.read_csv(FRS_FILE)

psi = pd.read_csv(PSI_FILE)

des = pd.read_csv(DES_FILE)

print("All metric files loaded successfully.")


# ---------------------------------------------------------
# Select required columns
# ---------------------------------------------------------

cli = cli[
    [
        "Mission_Day",
        "Astronaut_ID",
        "CLI"
    ]
]

frs = frs[
    [
        "Mission_Day",
        "Astronaut_ID",
        "Fatigue_Recovery_Score"
    ]
]

psi = psi[
    [
        "Mission_Day",
        "Astronaut_ID",
        "Performance_Stability_Score"
    ]
]

des = des[
    [
        "Mission_Day",
        "Astronaut_ID",
        "Decision_Efficiency_Score"
    ]
]


# ---------------------------------------------------------
# Merge all metrics
# ---------------------------------------------------------

df = cli.merge(
    frs,
    on=["Mission_Day", "Astronaut_ID"],
    how="inner"
)

df = df.merge(
    psi,
    on=["Mission_Day", "Astronaut_ID"],
    how="inner"
)

df = df.merge(
    des,
    on=["Mission_Day", "Astronaut_ID"],
    how="inner"
)


# ---------------------------------------------------------
# Convert Cognitive Load into a Readiness Component
# ---------------------------------------------------------
# Higher cognitive load = lower readiness.
#
# Therefore:
#
# Cognitive Readiness = 100 - CLI

df["Cognitive_Readiness"] = 100 - df["CLI"]


# ---------------------------------------------------------
# Mission Readiness Score
# ---------------------------------------------------------
#
# Cognitive Readiness       -> 30%
# Fatigue Recovery          -> 25%
# Performance Stability     -> 20%
# Decision Efficiency       -> 25%

df["Mission_Readiness_Score"] = (
    df["Cognitive_Readiness"] * 0.30
    + df["Fatigue_Recovery_Score"] * 0.25
    + df["Performance_Stability_Score"] * 0.20
    + df["Decision_Efficiency_Score"] * 0.25
)


# ---------------------------------------------------------
# Readiness Classification
# ---------------------------------------------------------

def classify_readiness(score):

    if score < 40:
        return "Low Readiness"

    elif score < 60:
        return "Moderate Readiness"

    elif score < 80:
        return "Good Readiness"

    else:
        return "High Readiness"


df["Readiness_Level"] = (
    df["Mission_Readiness_Score"]
    .apply(classify_readiness)
)


# ---------------------------------------------------------
# Sort results
# ---------------------------------------------------------

df = df.sort_values(
    by=["Astronaut_ID", "Mission_Day"]
).reset_index(drop=True)


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

print("\nMission Readiness Analysis Completed.")

print("\nMission Readiness Results:")

print(
    df[
        [
            "Mission_Day",
            "Astronaut_ID",
            "CLI",
            "Fatigue_Recovery_Score",
            "Performance_Stability_Score",
            "Decision_Efficiency_Score",
            "Mission_Readiness_Score",
            "Readiness_Level"
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

average_readiness = (
    df["Mission_Readiness_Score"].mean()
)

highest_readiness = df.loc[
    df["Mission_Readiness_Score"].idxmax()
]

lowest_readiness = df.loc[
    df["Mission_Readiness_Score"].idxmin()
]


print("\n----------------------------------------")

print(
    "Average Mission Readiness:",
    round(average_readiness, 2)
)

print(
    "Highest Readiness:",
    highest_readiness["Astronaut_ID"],
    "Day",
    highest_readiness["Mission_Day"],
    "Score:",
    round(
        highest_readiness["Mission_Readiness_Score"],
        2
    )
)

print(
    "Lowest Readiness:",
    lowest_readiness["Astronaut_ID"],
    "Day",
    lowest_readiness["Mission_Day"],
    "Score:",
    round(
        lowest_readiness["Mission_Readiness_Score"],
        2
    )
)

print("----------------------------------------")

print("\nOutput saved to:")
print(OUTPUT_FILE)