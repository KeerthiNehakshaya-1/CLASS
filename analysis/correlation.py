import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ---------------------------------------------------------
# Load data
# ---------------------------------------------------------

INPUT_FILE = Path("data/processed/preprocessed_data.csv")

df = pd.read_csv(INPUT_FILE)


# ---------------------------------------------------------
# Select important cognitive indicators
# ---------------------------------------------------------

columns = [
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


data = df[columns]


# ---------------------------------------------------------
# Pearson Correlation Matrix
# ---------------------------------------------------------

correlation_matrix = data.corr(method="pearson")


print("=" * 60)
print("CLASS - CORRELATION ANALYSIS")
print("=" * 60)

print("\nCorrelation Matrix:\n")

print(correlation_matrix.round(2))


# ---------------------------------------------------------
# Save correlation matrix
# ---------------------------------------------------------

OUTPUT_FILE = Path("data/processed/correlation_matrix.csv")

correlation_matrix.to_csv(OUTPUT_FILE)

print("\nCorrelation matrix saved at:")
print(OUTPUT_FILE)


# ---------------------------------------------------------
# Find strongest relationships
# ---------------------------------------------------------

print("\n" + "=" * 60)
print("STRONGEST CORRELATIONS")
print("=" * 60)


# Remove self-correlations
correlation_pairs = correlation_matrix.unstack()

correlation_pairs = correlation_pairs[
    correlation_pairs.index.get_level_values(0)
    != correlation_pairs.index.get_level_values(1)
]


# Remove duplicate pairs
correlation_pairs = correlation_pairs[
    correlation_pairs.index.map(
        lambda x: x[0] < x[1]
    )
]


# Sort by absolute correlation
strongest = correlation_pairs.reindex(
    correlation_pairs.abs().sort_values(
        ascending=False
    ).index
)


print("\nTop relationships:")

print(strongest.head(10).round(3))


# ---------------------------------------------------------
# Correlation Heatmap using Matplotlib
# ---------------------------------------------------------

plt.figure(figsize=(11, 8))

plt.imshow(
    correlation_matrix,
    interpolation="nearest",
    aspect="auto"
)

plt.colorbar(label="Correlation")

plt.xticks(
    range(len(columns)),
    columns,
    rotation=90
)

plt.yticks(
    range(len(columns)),
    columns
)

plt.title("CLASS Cognitive Indicator Correlation Matrix")

plt.tight_layout()

plt.show()


print("\nCorrelation analysis completed successfully.")