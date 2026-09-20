import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------
# File paths
# ---------------------------------------------------------

INPUT_FILE = Path("data/processed/preprocessed_data.csv")

df = pd.read_csv(INPUT_FILE)


# ---------------------------------------------------------
# Basic dataset information
# ---------------------------------------------------------

print("=" * 60)
print("CLASS - EXPLORATORY DATA ANALYSIS")
print("=" * 60)

print("\nDataset Shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 Records:")
print(df.head())


# ---------------------------------------------------------
# Statistical Analysis
# ---------------------------------------------------------

numeric_columns = [
    "Sleep_Hours",
    "Reaction_Time_ms",
    "Heart_Rate",
    "Tasks_Completed",
    "Task_Complexity",
    "Errors",
    "Radiation_Exposure",
    "Communication_Delay_sec",
    "Stress_Level"
]

print("\n" + "=" * 60)
print("DESCRIPTIVE STATISTICS")
print("=" * 60)

print(df[numeric_columns].describe())


# ---------------------------------------------------------
# Mean
# ---------------------------------------------------------

print("\nMean:")
print(df[numeric_columns].mean())


# ---------------------------------------------------------
# Median
# ---------------------------------------------------------

print("\nMedian:")
print(df[numeric_columns].median())


# ---------------------------------------------------------
# Variance
# ---------------------------------------------------------

print("\nVariance:")
print(df[numeric_columns].var())


# ---------------------------------------------------------
# Standard Deviation
# ---------------------------------------------------------

print("\nStandard Deviation:")
print(df[numeric_columns].std())


# ---------------------------------------------------------
# Percentiles
# ---------------------------------------------------------

print("\nPercentiles:")

percentiles = df[numeric_columns].quantile(
    [0.25, 0.50, 0.75]
)

print(percentiles)


# ---------------------------------------------------------
# Mission Day Summary
# ---------------------------------------------------------

print("\nMission Day Summary:")

print(
    df.groupby("Mission_Day")[
        [
            "Sleep_Hours",
            "Reaction_Time_ms",
            "Heart_Rate",
            "Errors",
            "Stress_Level"
        ]
    ].mean()
)


# ---------------------------------------------------------
# Astronaut Summary
# ---------------------------------------------------------

print("\nAstronaut Summary:")

print(
    df.groupby("Astronaut_ID")[
        [
            "Sleep_Hours",
            "Reaction_Time_ms",
            "Errors",
            "Stress_Level"
        ]
    ].mean()
)


# ---------------------------------------------------------
# Correlation Matrix
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("CORRELATION MATRIX")
print("=" * 60)

correlation_matrix = df[numeric_columns].corr()

print(correlation_matrix)


# ---------------------------------------------------------
# Plot 1: Sleep vs Reaction Time
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.scatter(
    df["Sleep_Hours"],
    df["Reaction_Time_ms"]
)

plt.xlabel("Sleep Duration (Hours)")
plt.ylabel("Reaction Time (ms)")
plt.title("Sleep Duration vs Reaction Time")

plt.grid(True)

plt.show()


# ---------------------------------------------------------
# Plot 2: Stress Level Distribution
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.hist(
    df["Stress_Level"],
    bins=8
)

plt.xlabel("Stress Level")
plt.ylabel("Frequency")
plt.title("Stress Level Distribution")

plt.grid(True)

plt.show()


# ---------------------------------------------------------
# Plot 3: Reaction Time Distribution
# ---------------------------------------------------------

plt.figure(figsize=(8, 5))

plt.hist(
    df["Reaction_Time_ms"],
    bins=8
)

plt.xlabel("Reaction Time (ms)")
plt.ylabel("Frequency")
plt.title("Reaction Time Distribution")

plt.grid(True)

plt.show()


# ---------------------------------------------------------
# Plot 4: Stress over Mission Days
# ---------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.plot(
    df["Mission_Day"],
    df["Stress_Level"],
    marker="o"
)

plt.xlabel("Mission Day")
plt.ylabel("Stress Level")
plt.title("Stress Level Over Mission Days")

plt.grid(True)

plt.show()


# ---------------------------------------------------------
# Plot 5: Reaction Time over Mission Days
# ---------------------------------------------------------

plt.figure(figsize=(9, 5))

plt.plot(
    df["Mission_Day"],
    df["Reaction_Time_ms"],
    marker="o"
)

plt.xlabel("Mission Day")
plt.ylabel("Reaction Time (ms)")
plt.title("Reaction Time Over Mission Days")

plt.grid(True)

plt.show()


print("\nEDA completed successfully.")