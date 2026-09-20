import pandas as pd
import numpy as np
from pathlib import Path


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "processed" / "preprocessed_data.csv"
METRICS_FILE = BASE_DIR / "data" / "processed" / "mission_readiness_results.csv"

# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)
metrics_df = pd.read_csv(METRICS_FILE)

df = df.merge(
    metrics_df[
        [
            "Mission_Day",
            "Astronaut_ID",
            "Performance_Stability_Score"
        ]
    ],
    on=["Mission_Day", "Astronaut_ID"],
    how="left"
)

# ---------------------------------------------------------
# Select astronaut and mission day
# ---------------------------------------------------------

astronaut_id = input(
    "\nEnter Astronaut ID (example: A01): "
).strip()

mission_day = int(
    input("Enter Mission Day (1-30): ")
)


# ---------------------------------------------------------
# Find selected record
# ---------------------------------------------------------

selected = df[
    (df["Astronaut_ID"] == astronaut_id)
    &
    (df["Mission_Day"] == mission_day)
]


if selected.empty:

    print("\nRecord not found.")

    print(
        "Please check the Astronaut ID "
        "and Mission Day."
    )

    exit()


# Convert selected row to dictionary

record = selected.iloc[0].copy()


print("\nSelected Mission Record")
print("----------------------------------------")

print(
    "Astronaut:",
    record["Astronaut_ID"]
)

print(
    "Mission Day:",
    record["Mission_Day"]
)

print(
    "Sleep:",
    record["Sleep_Hours"],
    "hours"
)

print(
    "Reaction Time:",
    record["Reaction_Time_ms"],
    "ms"
)

print(
    "Task Complexity:",
    record["Task_Complexity"]
)

print(
    "Communication Delay:",
    record["Communication_Delay_sec"],
    "seconds"
)

print(
    "Stress:",
    record["Stress_Level"]
)


# ---------------------------------------------------------
# Scenario modifications
# ---------------------------------------------------------

print("\n----------------------------------------")
print("SCENARIO MODIFICATIONS")
print("----------------------------------------")

print(
    "Enter 0 if you do not want to modify "
    "a parameter."
)


sleep_change = float(
    input(
        "\nChange Sleep Hours "
        "(example: -2 or +1): "
    )
)

communication_change = float(
    input(
        "Change Communication Delay "
        "(example: +5 or -2): "
    )
)

complexity_change = float(
    input(
        "Change Task Complexity "
        "(example: +2 or -1): "
    )
)

stress_change = float(
    input(
        "Change Stress Level "
        "(example: +10 or -5): "
    )
)


# ---------------------------------------------------------
# Apply modifications
# ---------------------------------------------------------

scenario = record.copy()

scenario["Sleep_Hours"] = max(
    0,
    scenario["Sleep_Hours"] + sleep_change
)

scenario["Communication_Delay_sec"] = max(
    0,
    scenario["Communication_Delay_sec"]
    + communication_change
)

scenario["Task_Complexity"] = np.clip(
    scenario["Task_Complexity"]
    + complexity_change,
    1,
    10
)

scenario["Stress_Level"] = np.clip(
    scenario["Stress_Level"]
    + stress_change,
    0,
    100
)


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------

def normalize_value(value, minimum, maximum):

    if maximum == minimum:
        return 0

    return (
        (value - minimum)
        / (maximum - minimum)
    )


# ---------------------------------------------------------
# Calculate scenario normalized values
# ---------------------------------------------------------

scenario["Sleep_Fatigue_Normalized"] = (
    1
    - normalize_value(
        scenario["Sleep_Hours"],
        df["Sleep_Hours"].min(),
        df["Sleep_Hours"].max()
    )
)

scenario["Reaction_Time_Normalized"] = (
    record["Reaction_Time_Normalized"]
)

scenario["Heart_Rate_Normalized"] = (
    record["Heart_Rate_Normalized"]
)

scenario["Task_Complexity_Normalized"] = (
    normalize_value(
        scenario["Task_Complexity"],
        df["Task_Complexity"].min(),
        df["Task_Complexity"].max()
    )
)

scenario["Errors_Normalized"] = (
    record["Errors_Normalized"]
)

scenario["Communication_Delay_Normalized"] = (
    normalize_value(
        scenario["Communication_Delay_sec"],
        df["Communication_Delay_sec"].min(),
        df["Communication_Delay_sec"].max()
    )
)

scenario["Stress_Normalized"] = (
    normalize_value(
        scenario["Stress_Level"],
        df["Stress_Level"].min(),
        df["Stress_Level"].max()
    )
)

scenario["Radiation_Normalized"] = (
    record["Radiation_Normalized"]
)


# ---------------------------------------------------------
# Calculate Scenario CLI
# ---------------------------------------------------------

scenario_cli = (
    scenario["Sleep_Fatigue_Normalized"] * 0.20
    + scenario["Reaction_Time_Normalized"] * 0.15
    + scenario["Heart_Rate_Normalized"] * 0.10
    + scenario["Task_Complexity_Normalized"] * 0.15
    + scenario["Errors_Normalized"] * 0.15
    + scenario["Communication_Delay_Normalized"] * 0.10
    + scenario["Stress_Normalized"] * 0.10
    + scenario["Radiation_Normalized"] * 0.05
) * 100


# ---------------------------------------------------------
# Calculate Scenario Fatigue Recovery
# ---------------------------------------------------------

scenario_sleep_recovery = (
    min(scenario["Sleep_Hours"] / 8, 1)
    * 100
)

scenario_reaction_recovery = (
    1 - scenario["Reaction_Time_Normalized"]
) * 100

scenario_fatigue_recovery = (
    scenario_sleep_recovery * 0.60
    + scenario_reaction_recovery * 0.40
)


# ---------------------------------------------------------
# Calculate Scenario Decision Efficiency
# ---------------------------------------------------------

scenario_decision_efficiency = (
    scenario["Tasks_Completed_Normalized"] * 0.40
    + (1 - scenario["Errors_Normalized"]) * 0.30
    + (1 - scenario["Reaction_Time_Normalized"]) * 0.30
) * 100


# ---------------------------------------------------------
# Performance Stability
# ---------------------------------------------------------
# Stability cannot be reliably recalculated from a single
# modified record, so the original stability score is kept.

scenario_stability = (
    record.get(
        "Performance_Stability_Score",
        np.nan
    )
)

if pd.isna(scenario_stability):

    scenario_stability = 100


# ---------------------------------------------------------
# Calculate Scenario Mission Readiness
# ---------------------------------------------------------

scenario_cognitive_readiness = (
    100 - scenario_cli
)

scenario_readiness = (
    scenario_cognitive_readiness * 0.30
    + scenario_fatigue_recovery * 0.25
    + scenario_stability * 0.20
    + scenario_decision_efficiency * 0.25
)


# ---------------------------------------------------------
# Original metric values
# ---------------------------------------------------------

original_cli = (
    record["Sleep_Fatigue_Normalized"] * 0.20
    + record["Reaction_Time_Normalized"] * 0.15
    + record["Heart_Rate_Normalized"] * 0.10
    + record["Task_Complexity_Normalized"] * 0.15
    + record["Errors_Normalized"] * 0.15
    + record["Communication_Delay_Normalized"] * 0.10
    + record["Stress_Normalized"] * 0.10
    + record["Radiation_Normalized"] * 0.05
) * 100


original_fatigue = (
    min(record["Sleep_Hours"] / 8, 1)
    * 100
    * 0.60
    +
    (1 - record["Reaction_Time_Normalized"])
    * 100
    * 0.40
)


original_efficiency = (
    record["Tasks_Completed_Normalized"] * 0.40
    + (1 - record["Errors_Normalized"]) * 0.30
    + (1 - record["Reaction_Time_Normalized"]) * 0.30
) * 100


original_stability = (
    record.get(
        "Performance_Stability_Score",
        100
    )
)

if pd.isna(original_stability):

    original_stability = 100


original_readiness = (
    (100 - original_cli) * 0.30
    + original_fatigue * 0.25
    + original_stability * 0.20
    + original_efficiency * 0.25
)


# ---------------------------------------------------------
# Display comparison
# ---------------------------------------------------------

print("\n========================================")
print("SCENARIO RESULTS")
print("========================================")

print("\nMetric                  Original     Scenario")
print("----------------------------------------")

print(
    f"CLI                     "
    f"{original_cli:8.2f}     "
    f"{scenario_cli:8.2f}"
)

print(
    f"Fatigue Recovery        "
    f"{original_fatigue:8.2f}     "
    f"{scenario_fatigue_recovery:8.2f}"
)

print(
    f"Decision Efficiency     "
    f"{original_efficiency:8.2f}     "
    f"{scenario_decision_efficiency:8.2f}"
)

print(
    f"Performance Stability   "
    f"{original_stability:8.2f}     "
    f"{scenario_stability:8.2f}"
)

print(
    f"Mission Readiness       "
    f"{original_readiness:8.2f}     "
    f"{scenario_readiness:8.2f}"
)


# ---------------------------------------------------------
# Changes
# ---------------------------------------------------------

print("\n========================================")
print("CHANGES")
print("========================================")

print(
    "CLI Change:",
    round(scenario_cli - original_cli, 2)
)

print(
    "Recovery Change:",
    round(
        scenario_fatigue_recovery
        - original_fatigue,
        2
    )
)

print(
    "Efficiency Change:",
    round(
        scenario_decision_efficiency
        - original_efficiency,
        2
    )
)

print(
    "Readiness Change:",
    round(
        scenario_readiness
        - original_readiness,
        2
    )
)

print("========================================")