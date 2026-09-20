import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

RESULT_FILE = BASE_DIR / "data" / "processed" / "mission_readiness_results.csv"
RISK_FILE = BASE_DIR / "data" / "processed" / "risk_analysis_results.csv"
PREPROCESSED_FILE = BASE_DIR / "data" / "processed" / "preprocessed_data.csv"

OUTPUT_DIR = BASE_DIR / "visualizations"

OUTPUT_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

df = pd.read_csv(RESULT_FILE)
risk_df = pd.read_csv(RISK_FILE)
raw_df = pd.read_csv(PREPROCESSED_FILE)


print("Data loaded successfully.")
print("Mission readiness records:", len(df))


# ---------------------------------------------------------
# 1. Cognitive Load Trend
# ---------------------------------------------------------

plt.figure(figsize=(10, 5))

for astronaut in df["Astronaut_ID"].unique():

    astronaut_data = df[df["Astronaut_ID"] == astronaut]

    plt.plot(
        astronaut_data["Mission_Day"],
        astronaut_data["CLI"],
        marker="o",
        label=astronaut
    )

plt.xlabel("Mission Day")
plt.ylabel("Cognitive Load Index")
plt.title("Cognitive Load Trend")
plt.legend()
plt.grid(True)

plt.savefig(OUTPUT_DIR / "cognitive_load_trend.png")
plt.show()
plt.close()


# ---------------------------------------------------------
# 2. Mission Readiness Trend
# ---------------------------------------------------------

plt.figure(figsize=(10, 5))

for astronaut in df["Astronaut_ID"].unique():

    astronaut_data = df[df["Astronaut_ID"] == astronaut]

    plt.plot(
        astronaut_data["Mission_Day"],
        astronaut_data["Mission_Readiness_Score"],
        marker="o",
        label=astronaut
    )

plt.xlabel("Mission Day")
plt.ylabel("Mission Readiness Score")
plt.title("Mission Readiness Trend")
plt.legend()
plt.grid(True)

plt.savefig(OUTPUT_DIR / "mission_readiness_trend.png")
plt.show()
plt.close()


# ---------------------------------------------------------
# 3. Sleep vs Reaction Time
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    raw_df["Sleep_Hours"],
    raw_df["Reaction_Time_ms"]
)

plt.xlabel("Sleep Hours")
plt.ylabel("Reaction Time (ms)")
plt.title("Sleep vs Reaction Time")
plt.grid(True)

plt.savefig(OUTPUT_DIR / "sleep_vs_reaction_time.png")
plt.show()
plt.close()


# ---------------------------------------------------------
# 4. Average Metrics
# ---------------------------------------------------------

average_values = [
    df["CLI"].mean(),
    df["Fatigue_Recovery_Score"].mean(),
    df["Performance_Stability_Score"].mean(),
    df["Decision_Efficiency_Score"].mean(),
    df["Mission_Readiness_Score"].mean()
]

metric_names = [
    "Cognitive Load",
    "Fatigue Recovery",
    "Performance Stability",
    "Decision Efficiency",
    "Mission Readiness"
]

plt.figure(figsize=(10, 5))

plt.bar(metric_names, average_values)

plt.ylabel("Score")
plt.title("Average Mission Analytics Metrics")
plt.xticks(rotation=20)
plt.grid(axis="y")

plt.savefig(OUTPUT_DIR / "average_metrics.png")
plt.show()
plt.close()


# ---------------------------------------------------------
# 5. Risk Distribution
# ---------------------------------------------------------

risk_counts = risk_df["Risk_Level"].value_counts()

plt.figure(figsize=(8, 5))

plt.bar(
    risk_counts.index,
    risk_counts.values
)

plt.xlabel("Risk Level")
plt.ylabel("Number of Records")
plt.title("Risk Level Distribution")
plt.grid(axis="y")

plt.savefig(OUTPUT_DIR / "risk_distribution.png")
plt.show()
plt.close()


# ---------------------------------------------------------
# 6. Stress Trend
# ---------------------------------------------------------

plt.figure(figsize=(10, 5))

for astronaut in raw_df["Astronaut_ID"].unique():

    astronaut_data = raw_df[
        raw_df["Astronaut_ID"] == astronaut
    ]

    plt.plot(
        astronaut_data["Mission_Day"],
        astronaut_data["Stress_Level"],
        marker="o",
        label=astronaut
    )

plt.xlabel("Mission Day")
plt.ylabel("Stress Level")
plt.title("Stress Trend")
plt.legend()
plt.grid(True)

plt.savefig(OUTPUT_DIR / "stress_trend.png")
plt.show()
plt.close()


print()
print("All visualizations generated successfully.")
print("Saved in:", OUTPUT_DIR)