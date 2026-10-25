import os
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak
)


# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

OUTPUT_FILE = os.path.join(
    REPORT_DIR,
    "CLASS_Mission_Analysis_Report.pdf"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

cli_df = pd.read_csv(
    os.path.join(DATA_DIR, "cognitive_load_results.csv")
)

frs_df = pd.read_csv(
    os.path.join(DATA_DIR, "fatigue_recovery_results.csv")
)

psi_df = pd.read_csv(
    os.path.join(DATA_DIR, "performance_stability_results.csv")
)

des_df = pd.read_csv(
    os.path.join(DATA_DIR, "decision_efficiency_results.csv")
)

mrs_df = pd.read_csv(
    os.path.join(DATA_DIR, "mission_readiness_results.csv")
)

risk_df = pd.read_csv(
    os.path.join(DATA_DIR, "risk_analysis_results.csv")
)


# ---------------------------------------------------------
# MERGE RESULTS
# ---------------------------------------------------------

keys = ["Mission_Day", "Astronaut_ID"]

report_df = cli_df.merge(
    frs_df,
    on=keys,
    suffixes=("", "_FRS")
)

report_df = report_df.merge(
    psi_df,
    on=keys,
    suffixes=("", "_PSI")
)

report_df = report_df.merge(
    des_df,
    on=keys,
    suffixes=("", "_DES")
)

report_df = report_df.merge(
    mrs_df,
    on=keys,
    suffixes=("", "_MRS")
)

report_df = report_df.merge(
    risk_df,
    on=keys,
    suffixes=("", "_RISK")
)


# ---------------------------------------------------------
# FIND COLUMN NAMES
# ---------------------------------------------------------

def find_column(df, possible_names):
    for name in possible_names:
        if name in df.columns:
            return name

    return None


cli_column = find_column(
    report_df,
    ["CLI"]
)

frs_column = find_column(
    report_df,
    ["Fatigue_Recovery_Score"]
)

psi_column = find_column(
    report_df,
    ["Performance_Stability_Score"]
)

des_column = find_column(
    report_df,
    ["Decision_Efficiency_Score"]
)

mrs_column = find_column(
    report_df,
    ["Mission_Readiness_Score"]
)

risk_column = find_column(
    report_df,
    ["Risk_Level"]
)


# ---------------------------------------------------------
# PDF SETUP
# ---------------------------------------------------------

os.makedirs(REPORT_DIR, exist_ok=True)

doc = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    rightMargin=15 * mm,
    leftMargin=15 * mm,
    topMargin=15 * mm,
    bottomMargin=15 * mm
)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "ReportTitle",
    parent=styles["Title"],
    fontSize=20,
    leading=24,
    alignment=TA_CENTER,
    spaceAfter=8
)

subtitle_style = ParagraphStyle(
    "Subtitle",
    parent=styles["Normal"],
    fontSize=10,
    leading=14,
    alignment=TA_CENTER,
    spaceAfter=18
)

heading_style = ParagraphStyle(
    "Heading",
    parent=styles["Heading2"],
    fontSize=14,
    leading=18,
    spaceBefore=12,
    spaceAfter=8
)

normal_style = ParagraphStyle(
    "NormalText",
    parent=styles["Normal"],
    fontSize=9,
    leading=13
)


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def format_value(value):
    if pd.isna(value):
        return "N/A"

    if isinstance(value, (int, float)):
        return f"{value:.2f}"

    return str(value)


def create_table(data, column_widths=None):

    table = Table(
        data,
        colWidths=column_widths,
        repeatRows=1
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

            ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 8),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),

            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
             [colors.white, colors.HexColor("#EAF2F8")])
        ])
    )

    return table


# ---------------------------------------------------------
# BUILD REPORT
# ---------------------------------------------------------

story = []


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

story.append(
    Paragraph(
        "CLASS Mission Analysis Report",
        title_style
    )
)

story.append(
    Paragraph(
        "Cognitive Load Analytics System for Long-Duration Space Missions",
        subtitle_style
    )
)

story.append(
    Paragraph(
        "Post-Mission Analytical Assessment",
        heading_style
    )
)


# ---------------------------------------------------------
# MISSION INFORMATION
# ---------------------------------------------------------

astronauts = sorted(
    report_df["Astronaut_ID"].dropna().unique()
)

mission_days = sorted(
    report_df["Mission_Day"].dropna().unique()
)

mission_info = [
    ["Parameter", "Value"],
    ["System", "CLASS"],
    ["Number of Astronauts", str(len(astronauts))],
    ["Astronaut IDs", ", ".join(map(str, astronauts))],
    ["Mission Days", f"{min(mission_days)} - {max(mission_days)}"],
    ["Total Records", str(len(report_df))]
]

story.append(
    Paragraph(
        "1. Mission Information",
        heading_style
    )
)

story.append(
    create_table(
        mission_info,
        [60 * mm, 110 * mm]
    )
)

story.append(Spacer(1, 10))


# ---------------------------------------------------------
# DAILY ANALYTICAL RESULTS
# ---------------------------------------------------------

story.append(
    Paragraph(
        "2. Daily Analytical Results",
        heading_style
    )
)

daily_headers = [
    "Day",
    "Astronaut",
    "CLI",
    "FRS",
    "PSI",
    "DES",
    "MRS",
    "Risk"
]

daily_data = [daily_headers]

for _, row in report_df.iterrows():

    daily_data.append([
        str(row["Mission_Day"]),
        str(row["Astronaut_ID"]),
        format_value(row[cli_column]) if cli_column else "N/A",
        format_value(row[frs_column]) if frs_column else "N/A",
        format_value(row[psi_column]) if psi_column else "N/A",
        format_value(row[des_column]) if des_column else "N/A",
        format_value(row[mrs_column]) if mrs_column else "N/A",
        str(row[risk_column]) if risk_column else "N/A"
    ])


story.append(
    create_table(
        daily_data,
        [
            15 * mm,
            25 * mm,
            20 * mm,
            20 * mm,
            20 * mm,
            20 * mm,
            20 * mm,
            25 * mm
        ]
    )
)


# ---------------------------------------------------------
# SUMMARY STATISTICS
# ---------------------------------------------------------

story.append(PageBreak())

story.append(
    Paragraph(
        "3. Overall Mission Summary",
        heading_style
    )
)

summary_data = [
    ["Metric", "Average", "Minimum", "Maximum"]
]


def add_summary_row(label, column):

    if column is None:
        return

    summary_data.append([
        label,
        f"{report_df[column].mean():.2f}",
        f"{report_df[column].min():.2f}",
        f"{report_df[column].max():.2f}"
    ])


add_summary_row("Cognitive Load Index", cli_column)
add_summary_row("Fatigue Recovery Score", frs_column)
add_summary_row("Performance Stability Index", psi_column)
add_summary_row("Decision Efficiency Score", des_column)
add_summary_row("Mission Readiness Score", mrs_column)


story.append(
    create_table(
        summary_data,
        [65 * mm, 35 * mm, 35 * mm, 35 * mm]
    )
)


# ---------------------------------------------------------
# RISK ANALYSIS
# ---------------------------------------------------------

story.append(
    Paragraph(
        "4. Risk Analysis",
        heading_style
    )
)

if risk_column:

    risk_counts = (
        report_df[risk_column]
        .value_counts()
        .reset_index()
    )

    risk_counts.columns = [
        "Risk Level",
        "Number of Records"
    ]

    risk_data = [
        ["Risk Level", "Number of Records"]
    ]

    for _, row in risk_counts.iterrows():
        risk_data.append([
            str(row["Risk Level"]),
            str(row["Number of Records"])
        ])

    story.append(
        create_table(
            risk_data,
            [70 * mm, 70 * mm]
        )
    )

else:

    story.append(
        Paragraph(
            "Risk information was not available in the processed results.",
            normal_style
        )
    )


# ---------------------------------------------------------
# HIGH-RISK EVENTS
# ---------------------------------------------------------

story.append(
    Paragraph(
        "5. Important Mission Events",
        heading_style
    )
)

if risk_column:

    high_risk = report_df[
        report_df[risk_column].astype(str).str.contains(
            "High",
            case=False,
            na=False
        )
    ]

    if len(high_risk) > 0:

        event_data = [
            ["Mission Day", "Astronaut", "Risk Level"]
        ]

        for _, row in high_risk.iterrows():

            event_data.append([
                str(row["Mission_Day"]),
                str(row["Astronaut_ID"]),
                str(row[risk_column])
            ])

        story.append(
            create_table(
                event_data,
                [50 * mm, 50 * mm, 60 * mm]
            )
        )

    else:

        story.append(
            Paragraph(
                "No high-risk records were identified in the processed results.",
                normal_style
            )
        )


# ---------------------------------------------------------
# ANALYTICAL INTERPRETATION
# ---------------------------------------------------------

story.append(
    Paragraph(
        "6. Analytical Interpretation",
        heading_style
    )
)

interpretation = (
    "CLASS integrates cognitive load, fatigue recovery, "
    "performance stability, decision efficiency, and mission "
    "readiness indicators into a unified analytical report. "
    "The results provide a structured view of astronaut-related "
    "mission conditions across the recorded mission days."
)

story.append(
    Paragraph(
        interpretation,
        normal_style
    )
)

story.append(Spacer(1, 8))

story.append(
    Paragraph(
        "The generated indicators are intended as prototype "
        "decision-support measures based on the constructed "
        "demonstration dataset. They are not medical diagnoses "
        "or operational certification measures.",
        normal_style
    )
)


# ---------------------------------------------------------
# ANALYST NOTES
# ---------------------------------------------------------

story.append(
    Paragraph(
        "7. Analyst Notes",
        heading_style
    )
)

notes = [
    ["Notes / Observations"],
    [" "],
    [" "],
    [" "],
    [" "]
]

story.append(
    create_table(
        notes,
        [170 * mm]
    )
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

story.append(Spacer(1, 20))

story.append(
    Paragraph(
        "Generated by CLASS | Cognitive Load Analytics System",
        subtitle_style
    )
)


# ---------------------------------------------------------
# GENERATE PDF
# ---------------------------------------------------------

doc.build(story)

print()
print("=" * 60)
print("CLASS MISSION REPORT GENERATED SUCCESSFULLY")
print("=" * 60)
print()
print("Report:")
print(OUTPUT_FILE)
print()