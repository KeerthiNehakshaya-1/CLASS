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
    / "mission_readiness_results.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "risk_analysis_results.csv"
)


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

df = pd.read_csv(INPUT_FILE)

print("Mission readiness data loaded successfully.")
print("Input records:", len(df))


# ---------------------------------------------------------
# Risk Identification
# ---------------------------------------------------------
# Risk is identified using the existing analytical metrics.
#
# High CLI                  -> higher risk
# Low Fatigue Recovery      -> higher risk
# Low Performance Stability -> higher risk
# Low Decision Efficiency  -> higher risk
# Low Mission Readiness     -> higher risk


def identify_risk(row):

    risk_points = 0

    # Cognitive load
    if row["CLI"] >= 75:
        risk_points += 2
    elif row["CLI"] >= 50:
        risk_points += 1

    # Fatigue recovery
    if row["Fatigue_Recovery_Score"] < 40:
        risk_points += 2
    elif row["Fatigue_Recovery_Score"] < 70:
        risk_points += 1

    # Performance stability
    if row["Performance_Stability_Score"] < 40:
        risk_points += 2
    elif row["Performance_Stability_Score"] < 70:
        risk_points += 1

    # Decision efficiency
    if row["Decision_Efficiency_Score"] < 40:
        risk_points += 2
    elif row["Decision_Efficiency_Score"] < 70:
        risk_points += 1

    # Mission readiness
    if row["Mission_Readiness_Score"] < 40:
        risk_points += 2
    elif row["Mission_Readiness_Score"] < 60:
        risk_points += 1

    return risk_points


df["Risk_Points"] = df.apply(
    identify_risk,
    axis=1
)


# ---------------------------------------------------------
# Risk Level
# ---------------------------------------------------------

def classify_risk(points):

    if points >= 7:
        return "High Risk"

    elif points >= 4:
        return "Moderate Risk"

    else:
        return "Low Risk"


df["Risk_Level"] = df["Risk_Points"].apply(
    classify_risk
)


# ---------------------------------------------------------
# Identify contributing factors
# ---------------------------------------------------------

def identify_factors(row):

    factors = []

    if row["CLI"] >= 75:
        factors.append("High Cognitive Load")

    if row["Fatigue_Recovery_Score"] < 40:
        factors.append("Poor Recovery")

    if row["Performance_Stability_Score"] < 40:
        factors.append("Unstable Performance")

    if row["Decision_Efficiency_Score"] < 40:
        factors.append("Low Decision Efficiency")

    if row["Mission_Readiness_Score"] < 40:
        factors.append("Low Mission Readiness")

    if not factors:
        factors.append("No Major Risk Indicator")

    return ", ".join(factors)


df["Risk_Factors"] = df.apply(
    identify_factors,
    axis=1
)


# ---------------------------------------------------------
# Sort by risk
# ---------------------------------------------------------

df = df.sort_values(
    by=["Risk_Points", "Mission_Readiness_Score"],
    ascending=[False, True]
).reset_index(drop=True)


# ---------------------------------------------------------
# Save results
# ---------------------------------------------------------

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ---------------------------------------------------------
# Display risk results
# ---------------------------------------------------------

print("\nRisk Analysis Completed.")

print("\nRisk Results:")

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
            "Risk_Points",
            "Risk_Level",
            "Risk_Factors"
        ]
    ].to_string(index=False)
)


# ---------------------------------------------------------
# Risk Summary
# ---------------------------------------------------------

print("\n----------------------------------------")
print("RISK SUMMARY")
print("----------------------------------------")

risk_counts = df["Risk_Level"].value_counts()

print(risk_counts)


# ---------------------------------------------------------
# Highest Risk Records
# ---------------------------------------------------------

print("\nTop Risk Records:")

top_risk = df.head(10)

print(
    top_risk[
        [
            "Mission_Day",
            "Astronaut_ID",
            "Mission_Readiness_Score",
            "Risk_Points",
            "Risk_Level",
            "Risk_Factors"
        ]
    ].to_string(index=False)
)


print("\n----------------------------------------")

print("Output saved to:")
print(OUTPUT_FILE)

print("----------------------------------------")