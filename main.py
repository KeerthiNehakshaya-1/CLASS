import subprocess
import sys
from pathlib import Path


# ---------------------------------------------------------
# Project directory
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent


# ---------------------------------------------------------
# Pipeline stages
# ---------------------------------------------------------

STAGES = [
    ("Data Cleaning", "preprocessing/data_cleaning.py"),
    ("Data Preprocessing", "preprocessing/data_preprocessing.py"),
    ("EDA", "analysis/eda.py"),
    ("Correlation Analysis", "analysis/correlation.py"),
    ("Cognitive Load Index", "metrics/cognitive_load.py"),
    ("Fatigue Recovery Score", "metrics/fatigue_recovery.py"),
    ("Performance Stability Index", "metrics/performance_stability.py"),
    ("Decision Efficiency Score", "metrics/decision_efficiency.py"),
    ("Mission Readiness Score", "metrics/mission_readiness.py"),
    ("Risk Analysis", "analysis/risk_analysis.py"),
    ("Visualization", "analysis/visualization.py")
]


# ---------------------------------------------------------
# Run pipeline
# ---------------------------------------------------------

print("=" * 60)
print("CLASS - COMPLETE ANALYTICS PIPELINE")
print("=" * 60)


for stage_name, script_path in STAGES:

    print()
    print("-" * 60)
    print("Running:", stage_name)
    print("-" * 60)

    script = BASE_DIR / script_path

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=BASE_DIR
    )

    if result.returncode != 0:

        print()
        print("ERROR")
        print("Pipeline stopped at:", stage_name)
        print("Check the error message above.")

        sys.exit(1)


print()
print("=" * 60)
print("CLASS PIPELINE COMPLETED SUCCESSFULLY")
print("=" * 60)

print()
print("Generated outputs:")
print("1. Cleaned data")
print("2. Preprocessed data")
print("3. Correlation analysis")
print("4. Cognitive Load Index")
print("5. Fatigue Recovery Score")
print("6. Performance Stability Index")
print("7. Decision Efficiency Score")
print("8. Mission Readiness Score")
print("9. Risk Analysis")
print("10. Visualizations")

print()
print("To open the dashboard, run:")
print("python dashboard/dashboard.py")