import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from pathlib import Path


# =========================================================
# PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RISK_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "risk_analysis_results.csv"
)

PREPROCESSED_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "preprocessed_data.csv"
)

METRICS_FILE = (
    BASE_DIR
    / "data"
    / "processed"
    / "mission_readiness_results.csv"
)


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = pd.read_csv(RISK_FILE)
    preprocessed_df = pd.read_csv(PREPROCESSED_FILE)
    metrics_df = pd.read_csv(METRICS_FILE)

except FileNotFoundError as e:

    messagebox.showerror(
        "Required File Missing",
        f"Required file was not found:\n\n{e.filename}\n\n"
        "Please run:\n"
        "python main.py"
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
    "1050x900"
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
    pady=(0, 10)
)


# =========================================================
# SELECTION FRAME
# =========================================================

selection_frame = tk.Frame(root)

selection_frame.pack(
    pady=8
)


# ---------------------------------------------------------
# Astronaut
# ---------------------------------------------------------

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
    ),
    width=10
)

astronaut_dropdown.grid(
    row=0,
    column=1,
    padx=5
)

astronaut_dropdown.current(0)


# ---------------------------------------------------------
# Mission Day
# ---------------------------------------------------------

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
    width=10
)

day_dropdown.grid(
    row=0,
    column=3,
    padx=5
)


# =========================================================
# METRICS FRAME
# =========================================================

metrics_frame = tk.LabelFrame(
    root,
    text="Mission Analytics",
    padx=20,
    pady=10
)

metrics_frame.pack(
    padx=30,
    pady=8,
    fill="x"
)


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
    pady=5
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
    pady=5
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
    pady=5
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
    pady=5
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
    pady=5
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
    pady=5
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
    pady=8
)

risk_frame.pack(
    padx=30,
    pady=5,
    fill="x"
)


tk.Label(
    risk_frame,
    textvariable=factors_var,
    wraplength=900,
    justify="left"
).pack(
    anchor="w"
)


# =========================================================
# UPDATE DAY LIST
# =========================================================

def update_day_list(event=None):

    astronaut = astronaut_var.get()

    available_days = sorted(
        df[
            df["Astronaut_ID"] == astronaut
        ]["Mission_Day"].unique()
    )

    day_dropdown["values"] = [
        str(day)
        for day in available_days
    ]

    if available_days:

        day_dropdown.current(0)


# =========================================================
# UPDATE DASHBOARD
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
    # Update current metrics
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
    pady=6
)

update_button.pack(
    pady=7
)


# =========================================================
# SCENARIO SIMULATOR
# =========================================================

scenario_frame = tk.LabelFrame(
    root,
    text="MISSION SCENARIO SIMULATOR",
    padx=15,
    pady=10
)

scenario_frame.pack(
    padx=30,
    pady=8,
    fill="x"
)


# ---------------------------------------------------------
# Scenario variables
# ---------------------------------------------------------

sleep_change_var = tk.StringVar(value="0")
communication_change_var = tk.StringVar(value="0")
complexity_change_var = tk.StringVar(value="0")
stress_change_var = tk.StringVar(value="0")


# ---------------------------------------------------------
# Scenario input labels
# ---------------------------------------------------------

tk.Label(
    scenario_frame,
    text="Sleep Change (-2 to +2 hours):"
).grid(
    row=0,
    column=0,
    sticky="w",
    padx=8,
    pady=5
)

tk.Entry(
    scenario_frame,
    textvariable=sleep_change_var,
    width=10
).grid(
    row=0,
    column=1,
    padx=8
)


tk.Label(
    scenario_frame,
    text="Communication Delay Change (-5 to +5 sec):"
).grid(
    row=0,
    column=2,
    sticky="w",
    padx=8,
    pady=5
)

tk.Entry(
    scenario_frame,
    textvariable=communication_change_var,
    width=10
).grid(
    row=0,
    column=3,
    padx=8
)


tk.Label(
    scenario_frame,
    text="Task Complexity Change (-2 to +2):"
).grid(
    row=1,
    column=0,
    sticky="w",
    padx=8,
    pady=5
)

tk.Entry(
    scenario_frame,
    textvariable=complexity_change_var,
    width=10
).grid(
    row=1,
    column=1,
    padx=8
)


tk.Label(
    scenario_frame,
    text="Stress Change(-10 to +10):"
).grid(
    row=1,
    column=2,
    sticky="w",
    padx=8,
    pady=5
)

tk.Entry(
    scenario_frame,
    textvariable=stress_change_var,
    width=10
).grid(
    row=1,
    column=3,
    padx=8
)


# =========================================================
# SCENARIO RESULTS
# =========================================================

scenario_result_frame = tk.LabelFrame(
    root,
    text="Scenario Results",
    padx=15,
    pady=8
)

scenario_result_frame.pack(
    padx=30,
    pady=5,
    fill="x"
)


# Header

tk.Label(
    scenario_result_frame,
    text="Metric",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=0,
    padx=30,
    pady=3
)

tk.Label(
    scenario_result_frame,
    text="Original",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=1,
    padx=30,
    pady=3
)

tk.Label(
    scenario_result_frame,
    text="Scenario",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=2,
    padx=30,
    pady=3
)

tk.Label(
    scenario_result_frame,
    text="Change",
    font=("Arial", 10, "bold")
).grid(
    row=0,
    column=3,
    padx=30,
    pady=3
)


scenario_cli_var = tk.StringVar(value="--")
scenario_fatigue_var = tk.StringVar(value="--")
scenario_stability_var = tk.StringVar(value="--")
scenario_efficiency_var = tk.StringVar(value="--")
scenario_readiness_var = tk.StringVar(value="--")


# ---------------------------------------------------------
# Helper to create scenario rows
# ---------------------------------------------------------

def create_scenario_row(
    row_number,
    name,
    original,
    scenario,
    change
):

    tk.Label(
        scenario_result_frame,
        text=name
    ).grid(
        row=row_number,
        column=0,
        sticky="w",
        padx=15,
        pady=3
    )

    tk.Label(
        scenario_result_frame,
        textvariable=original
    ).grid(
        row=row_number,
        column=1
    )

    tk.Label(
        scenario_result_frame,
        textvariable=scenario
    ).grid(
        row=row_number,
        column=2
    )

    tk.Label(
        scenario_result_frame,
        textvariable=change
    ).grid(
        row=row_number,
        column=3
    )


scenario_original_cli = tk.StringVar(value="--")
scenario_original_fatigue = tk.StringVar(value="--")
scenario_original_stability = tk.StringVar(value="--")
scenario_original_efficiency = tk.StringVar(value="--")
scenario_original_readiness = tk.StringVar(value="--")

scenario_cli_change = tk.StringVar(value="--")
scenario_fatigue_change = tk.StringVar(value="--")
scenario_stability_change = tk.StringVar(value="--")
scenario_efficiency_change = tk.StringVar(value="--")
scenario_readiness_change = tk.StringVar(value="--")


create_scenario_row(
    1,
    "Cognitive Load",
    scenario_original_cli,
    scenario_cli_var,
    scenario_cli_change
)

create_scenario_row(
    2,
    "Fatigue Recovery",
    scenario_original_fatigue,
    scenario_fatigue_var,
    scenario_fatigue_change
)

create_scenario_row(
    3,
    "Performance Stability",
    scenario_original_stability,
    scenario_stability_var,
    scenario_stability_change
)

create_scenario_row(
    4,
    "Decision Efficiency",
    scenario_original_efficiency,
    scenario_efficiency_var,
    scenario_efficiency_change
)

create_scenario_row(
    5,
    "Mission Readiness",
    scenario_original_readiness,
    scenario_readiness_var,
    scenario_readiness_change
)


# =========================================================
# SCENARIO CALCULATION
# =========================================================

def run_scenario():

    astronaut = astronaut_var.get()

    try:

        day = int(
            day_var.get()
        )

        sleep_change = float(
            sleep_change_var.get()
        )

        communication_change = float(
            communication_change_var.get()
        )

        complexity_change = float(
            complexity_change_var.get()
        )

        stress_change = float(
            stress_change_var.get()
        )

    except ValueError:

        messagebox.showerror(
            "Invalid Input",
            "Please enter valid numeric values for all scenario changes."
        )

        return


    # -----------------------------------------------------
    # Find selected record
    # -----------------------------------------------------

    selected = preprocessed_df[
        (preprocessed_df["Astronaut_ID"] == astronaut)
        &
        (preprocessed_df["Mission_Day"] == day)
    ]


    if selected.empty:

        messagebox.showwarning(
            "No Data",
            "No preprocessed record found for the selected astronaut and day."
        )

        return


    record = selected.iloc[0].copy()


    # -----------------------------------------------------
    # Get original Performance Stability
    # -----------------------------------------------------

    stability_result = metrics_df[
        (metrics_df["Astronaut_ID"] == astronaut)
        &
        (metrics_df["Mission_Day"] == day)
    ]


    if stability_result.empty:

        messagebox.showwarning(
            "Missing Metric",
            "Performance Stability value was not found."
        )

        return


    original_stability = (
        stability_result.iloc[0]
        ["Performance_Stability_Score"]
    )


    # -----------------------------------------------------
    # Apply scenario modifications
    # -----------------------------------------------------

    scenario = record.copy()


    scenario["Sleep_Hours"] = max(
        0,
        scenario["Sleep_Hours"]
        + sleep_change
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


    # =====================================================
    # NORMALIZATION HELPER
    # =====================================================

    def normalize_value(
        value,
        minimum,
        maximum
    ):

        if maximum == minimum:
            return 0

        return (
            (value - minimum)
            / (maximum - minimum)
        )


    # =====================================================
    # SCENARIO NORMALIZED VALUES
    # =====================================================

    scenario["Sleep_Fatigue_Normalized"] = (
        1
        -
        normalize_value(
            scenario["Sleep_Hours"],
            preprocessed_df["Sleep_Hours"].min(),
            preprocessed_df["Sleep_Hours"].max()
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
            preprocessed_df["Task_Complexity"].min(),
            preprocessed_df["Task_Complexity"].max()
        )
    )


    scenario["Errors_Normalized"] = (
        record["Errors_Normalized"]
    )


    scenario["Communication_Delay_Normalized"] = (
        normalize_value(
            scenario["Communication_Delay_sec"],
            preprocessed_df["Communication_Delay_sec"].min(),
            preprocessed_df["Communication_Delay_sec"].max()
        )
    )


    scenario["Stress_Normalized"] = (
        normalize_value(
            scenario["Stress_Level"],
            preprocessed_df["Stress_Level"].min(),
            preprocessed_df["Stress_Level"].max()
        )
    )


    scenario["Radiation_Normalized"] = (
        record["Radiation_Normalized"]
    )


    # =====================================================
    # SCENARIO CLI
    # =====================================================

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


    # =====================================================
    # SCENARIO FATIGUE RECOVERY
    # =====================================================

    scenario_sleep_recovery = (
        min(
            scenario["Sleep_Hours"] / 8,
            1
        )
        * 100
    )


    scenario_reaction_recovery = (
        1
        -
        scenario["Reaction_Time_Normalized"]
    ) * 100


    scenario_fatigue = (
        scenario_sleep_recovery * 0.60
        +
        scenario_reaction_recovery * 0.40
    )


    # =====================================================
    # SCENARIO DECISION EFFICIENCY
    # =====================================================

    scenario_efficiency = (
        scenario["Tasks_Completed_Normalized"] * 0.40
        +
        (1 - scenario["Errors_Normalized"]) * 0.30
        +
        (1 - scenario["Reaction_Time_Normalized"]) * 0.30
    ) * 100


    # =====================================================
    # PERFORMANCE STABILITY
    # =====================================================

    # PSI is kept unchanged because it is calculated
    # using a 3-day rolling performance measure.

    scenario_stability = original_stability


    # =====================================================
    # SCENARIO MISSION READINESS
    # =====================================================

    scenario_cognitive_readiness = (
        100 - scenario_cli
    )


    scenario_readiness = (
        scenario_cognitive_readiness * 0.30
        +
        scenario_fatigue * 0.25
        +
        scenario_stability * 0.20
        +
        scenario_efficiency * 0.25
    )


    # =====================================================
    # ORIGINAL VALUES
    # =====================================================

    original_cli = (
        record["Sleep_Fatigue_Normalized"] * 0.20
        +
        record["Reaction_Time_Normalized"] * 0.15
        +
        record["Heart_Rate_Normalized"] * 0.10
        +
        record["Task_Complexity_Normalized"] * 0.15
        +
        record["Errors_Normalized"] * 0.15
        +
        record["Communication_Delay_Normalized"] * 0.10
        +
        record["Stress_Normalized"] * 0.10
        +
        record["Radiation_Normalized"] * 0.05
    ) * 100


    original_fatigue = (
        min(
            record["Sleep_Hours"] / 8,
            1
        )
        * 100
        * 0.60
        +
        (1 - record["Reaction_Time_Normalized"])
        * 100
        * 0.40
    )


    original_efficiency = (
        record["Tasks_Completed_Normalized"] * 0.40
        +
        (1 - record["Errors_Normalized"]) * 0.30
        +
        (1 - record["Reaction_Time_Normalized"]) * 0.30
    ) * 100


    original_readiness = (
        (100 - original_cli) * 0.30
        +
        original_fatigue * 0.25
        +
        original_stability * 0.20
        +
        original_efficiency * 0.25
    )


    # =====================================================
    # DISPLAY RESULTS
    # =====================================================

    scenario_original_cli.set(
        f"{original_cli:.2f}"
    )

    scenario_cli_var.set(
        f"{scenario_cli:.2f}"
    )

    scenario_cli_change.set(
        f"{scenario_cli - original_cli:+.2f}"
    )


    scenario_original_fatigue.set(
        f"{original_fatigue:.2f}"
    )

    scenario_fatigue_var.set(
        f"{scenario_fatigue:.2f}"
    )

    scenario_fatigue_change.set(
        f"{scenario_fatigue - original_fatigue:+.2f}"
    )


    scenario_original_stability.set(
        f"{original_stability:.2f}"
    )

    scenario_stability_var.set(
        f"{scenario_stability:.2f}"
    )

    scenario_stability_change.set(
        f"{scenario_stability - original_stability:+.2f}"
    )


    scenario_original_efficiency.set(
        f"{original_efficiency:.2f}"
    )

    scenario_efficiency_var.set(
        f"{scenario_efficiency:.2f}"
    )

    scenario_efficiency_change.set(
        f"{scenario_efficiency - original_efficiency:+.2f}"
    )


    scenario_original_readiness.set(
        f"{original_readiness:.2f}"
    )

    scenario_readiness_var.set(
        f"{scenario_readiness:.2f}"
    )

    scenario_readiness_change.set(
        f"{scenario_readiness - original_readiness:+.2f}"
    )


# =========================================================
# RUN SCENARIO BUTTON
# =========================================================

scenario_button = tk.Button(
    scenario_frame,
    text="RUN SCENARIO",
    command=run_scenario,
    padx=25,
    pady=6
)

scenario_button.grid(
    row=2,
    column=0,
    columnspan=4,
    pady=8
)


# =========================================================
# INFORMATION FRAME
# =========================================================

info_frame = tk.LabelFrame(
    root,
    text="CLASS Interpretation",
    padx=20,
    pady=8
)

info_frame.pack(
    padx=30,
    pady=7,
    fill="x"
)


info_text = tk.Label(
    info_frame,
    text=(
        "CLASS combines cognitive load, fatigue recovery, "
        "performance stability, decision efficiency, and "
        "mission readiness to support mission monitoring. "
        "The scenario simulator provides what-if analysis "
        "by modifying selected mission conditions."
    ),
    wraplength=900,
    justify="left"
)

info_text.pack(
    anchor="w"
)


# =========================================================
# EVENTS
# =========================================================

astronaut_dropdown.bind(
    "<<ComboboxSelected>>",
    update_day_list
)


# =========================================================
# INITIALIZE
# =========================================================

update_day_list()

update_dashboard()


# =========================================================
# START DASHBOARD
# =========================================================

root.mainloop()