import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from pathlib import Path


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "risk_analysis_results.csv"
)


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = pd.read_csv(DATA_FILE)

except FileNotFoundError:

    print("Risk analysis file not found.")

    print(
        "Please run:"
    )

    print(
        "python analysis/risk_analysis.py"
    )

    raise


# =========================================================
# MAIN WINDOW
# =========================================================

root = tk.Tk()

root.title(
    "CLASS - Cognitive Load Analytics System"
)

root.geometry(
    "1000x700"
)


# =========================================================
# TITLE
# =========================================================

title_label = tk.Label(
    root,
    text="CLASS",
    font=("Arial", 24, "bold")
)

title_label.pack(
    pady=(15, 2)
)


subtitle_label = tk.Label(
    root,
    text="Cognitive Load Analytics System for Long-Duration Space Missions",
    font=("Arial", 12)
)

subtitle_label.pack(
    pady=(0, 15)
)


# =========================================================
# SELECTION FRAME
# =========================================================

selection_frame = tk.Frame(root)

selection_frame.pack(
    pady=10
)


# Astronaut

tk.Label(
    selection_frame,
    text="Astronaut:"
).grid(
    row=0,
    column=0,
    padx=5
)


astronaut_var = tk.StringVar()

astronaut_dropdown = ttk.Combobox(
    selection_frame,
    textvariable=astronaut_var,
    state="readonly",
    values=sorted(
        df["Astronaut_ID"].unique()
    )
)

astronaut_dropdown.grid(
    row=0,
    column=1,
    padx=5
)

astronaut_dropdown.current(0)


# Mission Day

tk.Label(
    selection_frame,
    text="Mission Day:"
).grid(
    row=0,
    column=2,
    padx=5
)


day_var = tk.StringVar()

day_dropdown = ttk.Combobox(
    selection_frame,
    textvariable=day_var,
    state="readonly",
    values=[
        str(x)
        for x in sorted(
            df["Mission_Day"].unique()
        )
    ]
)

day_dropdown.grid(
    row=0,
    column=3,
    padx=5
)

day_dropdown.current(0)


# =========================================================
# METRICS FRAME
# =========================================================

metrics_frame = tk.LabelFrame(
    root,
    text="Mission Analytics",
    padx=20,
    pady=15
)

metrics_frame.pack(
    padx=30,
    pady=15,
    fill="x"
)


# Variables

cli_var = tk.StringVar(value="--")

recovery_var = tk.StringVar(value="--")

stability_var = tk.StringVar(value="--")

efficiency_var = tk.StringVar(value="--")

readiness_var = tk.StringVar(value="--")

risk_var = tk.StringVar(value="--")

factors_var = tk.StringVar(value="--")


# ---------------------------------------------------------
# Metric labels
# ---------------------------------------------------------

tk.Label(
    metrics_frame,
    text="Cognitive Load:"
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=10,
    pady=8
)

tk.Label(
    metrics_frame,
    textvariable=cli_var
).grid(
    row=0,
    column=1,
    sticky="w"
)


tk.Label(
    metrics_frame,
    text="Fatigue Recovery:"
).grid(
    row=1,
    column=0,
    sticky="w",
    padx=10,
    pady=8
)

tk.Label(
    metrics_frame,
    textvariable=recovery_var
).grid(
    row=1,
    column=1,
    sticky="w"
)


tk.Label(
    metrics_frame,
    text="Performance Stability:"
).grid(
    row=2,
    column=0,
    sticky="w",
    padx=10,
    pady=8
)

tk.Label(
    metrics_frame,
    textvariable=stability_var
).grid(
    row=2,
    column=1,
    sticky="w"
)


tk.Label(
    metrics_frame,
    text="Decision Efficiency:"
).grid(
    row=0,
    column=2,
    sticky="w",
    padx=10,
    pady=8
)

tk.Label(
    metrics_frame,
    textvariable=efficiency_var
).grid(
    row=0,
    column=3,
    sticky="w"
)


tk.Label(
    metrics_frame,
    text="Mission Readiness:"
).grid(
    row=1,
    column=2,
    sticky="w",
    padx=10,
    pady=8
)

tk.Label(
    metrics_frame,
    textvariable=readiness_var
).grid(
    row=1,
    column=3,
    sticky="w"
)


tk.Label(
    metrics_frame,
    text="Risk Level:"
).grid(
    row=2,
    column=2,
    sticky="w",
    padx=10,
    pady=8
)

tk.Label(
    metrics_frame,
    textvariable=risk_var
).grid(
    row=2,
    column=3,
    sticky="w"
)


# =========================================================
# RISK FACTORS
# =========================================================

risk_frame = tk.LabelFrame(
    root,
    text="Risk Factors",
    padx=20,
    pady=15
)

risk_frame.pack(
    padx=30,
    pady=10,
    fill="x"
)


tk.Label(
    risk_frame,
    textvariable=factors_var,
    wraplength=850,
    justify="left"
).pack(
    anchor="w"
)


# =========================================================
# UPDATE FUNCTION
# =========================================================

def update_dashboard():

    astronaut = astronaut_var.get()

    try:

        day = int(
            day_var.get()
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Mission Day",
            "Please select a valid mission day."
        )

        return


    result = df[
        (df["Astronaut_ID"] == astronaut)
        &
        (df["Mission_Day"] == day)
    ]


    if result.empty:

        messagebox.showwarning(
            "No Data",
            "No record found for the selected astronaut and day."
        )

        return


    row = result.iloc[0]


    # -----------------------------------------------------
    # Update metrics
    # -----------------------------------------------------

    cli_var.set(
        f"{row['CLI']:.2f} / 100"
    )

    recovery_var.set(
        f"{row['Fatigue_Recovery_Score']:.2f} / 100"
    )

    stability_var.set(
        f"{row['Performance_Stability_Score']:.2f} / 100"
    )

    efficiency_var.set(
        f"{row['Decision_Efficiency_Score']:.2f} / 100"
    )

    readiness_var.set(
        f"{row['Mission_Readiness_Score']:.2f} / 100"
    )

    risk_var.set(
        row["Risk_Level"]
    )

    factors_var.set(
        row["Risk_Factors"]
    )


# =========================================================
# UPDATE BUTTON
# =========================================================

update_button = tk.Button(
    root,
    text="Analyze Mission Condition",
    command=update_dashboard,
    padx=20,
    pady=8
)

update_button.pack(
    pady=15
)


# =========================================================
# INFORMATION FRAME
# =========================================================

info_frame = tk.LabelFrame(
    root,
    text="CLASS Interpretation",
    padx=20,
    pady=15
)

info_frame.pack(
    padx=30,
    pady=10,
    fill="x"
)


info_text = tk.Label(
    info_frame,
    text=(
        "CLASS combines cognitive load, fatigue recovery, "
        "performance stability, decision efficiency, "
        "and mission readiness to support mission monitoring."
    ),
    wraplength=850,
    justify="left"
)

info_text.pack(
    anchor="w"
)


# =========================================================
# START DASHBOARD
# =========================================================

update_dashboard()

root.mainloop()