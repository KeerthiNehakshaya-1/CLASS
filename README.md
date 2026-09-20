# Cognitive Load Analytics System for Long-Duration Space Missions (CLASS)

## 1. Project Overview

The Cognitive Load Analytics System for Long-Duration Space Missions (CLASS) is a data analytics and decision-support prototype designed to analyze factors that may influence astronaut cognitive workload, fatigue, performance, and mission readiness during long-duration space missions.

The system combines physiological, behavioral, task-related, and mission-related parameters to generate multiple analytical scores and identify potentially high-risk mission conditions.

CLASS is designed as a prototype analytical system and is not intended to replace medical diagnosis, astronaut certification, or operational mission-control procedures.

---

## 2. Problem Statement

During long-duration space missions, astronauts may experience increased cognitive workload due to factors such as reduced sleep, complex tasks, communication delays, stress, errors, and prolonged mission demands.

Monitoring individual parameters separately may not provide a unified view of the astronaut's overall cognitive and performance condition.

CLASS addresses this problem by combining multiple mission and astronaut parameters into a unified analytical workflow.

---

## 3. Objectives

The main objectives of CLASS are:

* Analyze astronaut physiological and mission-related data.
* Identify factors associated with increased cognitive workload.
* Calculate a Cognitive Load Index.
* Estimate fatigue recovery.
* Measure performance stability.
* Evaluate decision efficiency.
* Calculate mission readiness.
* Identify potential risk conditions.
* Provide a mission scenario simulator.
* Present analytical results through visualizations and an interactive dashboard.

---

## 4. Input Parameters

The system uses the following parameters:

| Parameter               | Description                   |
| ----------------------- | ----------------------------- |
| Mission_Day             | Day of the mission            |
| Astronaut_ID            | Unique astronaut identifier   |
| Sleep_Hours             | Daily sleep duration          |
| Reaction_Time_ms        | Reaction time in milliseconds |
| Heart_Rate              | Heart rate measurement        |
| Tasks_Completed         | Number of completed tasks     |
| Task_Complexity         | Complexity of assigned tasks  |
| Errors                  | Number of errors              |
| Radiation_Exposure      | Radiation exposure value      |
| Communication_Delay_sec | Communication delay           |
| Stress_Level            | Stress measurement            |

---

## 5. System Workflow

The overall processing pipeline is:

Raw Data

↓

Data Cleaning

↓

Data Preprocessing

↓

Exploratory Data Analysis

↓

Correlation Analysis

↓

Cognitive Load Analysis

↓

Fatigue Recovery Analysis

↓

Performance Stability Analysis

↓

Decision Efficiency Analysis

↓

Mission Readiness Analysis

↓

Risk Analysis

↓

Scenario Simulation

↓

Visualization

↓

Interactive Dashboard

---

## 6. Analytical Metrics

### 6.1 Cognitive Load Index

The Cognitive Load Index (CLI) combines normalized indicators associated with cognitive workload.

The prototype considers:

* Sleep fatigue
* Reaction time
* Heart rate
* Task complexity
* Errors
* Communication delay
* Stress
* Radiation exposure

The resulting score is represented on a 0–100 scale.

---

### 6.2 Fatigue Recovery Score

The Fatigue Recovery Score estimates recovery using sleep duration and reaction-time-based indicators.

The prototype uses:

* Sleep recovery
* Reaction recovery

The resulting score is represented on a 0–100 scale.

---

### 6.3 Performance Stability Index

The Performance Stability Index evaluates variation in a combined performance indicator over a rolling three-day window.

It considers:

* Tasks completed
* Errors
* Reaction time

Lower variation indicates greater performance stability within this prototype.

---

### 6.4 Decision Efficiency Score

The Decision Efficiency Score combines:

* Task completion
* Error performance
* Reaction time

It provides a normalized 0–100 prototype score representing decision-related performance efficiency.

---

### 6.5 Mission Readiness Score

The Mission Readiness Score combines:

* Cognitive readiness
* Fatigue recovery
* Performance stability
* Decision efficiency

The result provides an overall analytical representation of mission readiness.

---

### 6.6 Risk Analysis

The risk-analysis stage combines the generated metrics using transparent threshold-based rules.

Potential risk indicators include:

* High cognitive load
* Poor recovery
* Unstable performance
* Low decision efficiency
* Low mission readiness

The system categorizes records into Low, Moderate, and High Risk levels.

---

## 7. Scenario Simulator

CLASS includes a Mission Scenario Simulator.

The simulator allows changes to selected mission conditions such as:

* Sleep duration
* Communication delay
* Task complexity
* Stress level

The system recalculates the affected analytical metrics and compares the scenario with the original condition.

This allows users to explore hypothetical mission conditions without modifying the original dataset.

---

## 8. Visualization

The system generates visualizations including:

* Cognitive Load Trend
* Mission Readiness Trend
* Sleep vs Reaction Time
* Average Analytics Metrics
* Risk Distribution
* Stress Trend

These visualizations help identify trends and relationships in the dataset.

---

## 9. Dashboard

CLASS includes an interactive Tkinter dashboard.

The dashboard allows the user to select:

* Astronaut
* Mission Day

It displays:

* Cognitive Load
* Fatigue Recovery
* Performance Stability
* Decision Efficiency
* Mission Readiness
* Risk Level
* Risk Factors

---

## 10. Technology Stack

### Programming Language

Python

### Data Processing

* Pandas
* NumPy

### Data Visualization

* Matplotlib

### Dashboard

* Tkinter

### Development Environment

* Visual Studio Code

### Data Format

CSV

---

## 11. Project Structure

```text
CLASS/
│
├── README.md
├── main.py
│
├── analysis/
│   ├── eda.py
│   ├── correlation.py
│   ├── risk_analysis.py
│   ├── scenario_simulator.py
│   └── visualization.py
│
├── dashboard/
│   └── dashboard.py
│
├── data/
│   ├── raw/
│   │   └── astronaut_data.csv
│   │
│   └── processed/
│       ├── cleaned_data.csv
│       ├── preprocessed_data.csv
│       ├── correlation_matrix.csv
│       ├── cognitive_load_results.csv
│       ├── fatigue_recovery_results.csv
│       ├── performance_stability_results.csv
│       ├── decision_efficiency_results.csv
│       ├── mission_readiness_results.csv
│       └── risk_analysis_results.csv
│
├── metrics/
│   ├── cognitive_load.py
│   ├── fatigue_recovery.py
│   ├── performance_stability.py
│   ├── decision_efficiency.py
│   └── mission_readiness.py
│
├── preprocessing/
│   ├── data_cleaning.py
│   └── data_preprocessing.py
│
└── visualizations/
    ├── cognitive_load_trend.png
    ├── mission_readiness_trend.png
    ├── sleep_vs_reaction_time.png
    ├── average_metrics.png
    ├── risk_distribution.png
    └── stress_trend.png
```

---

## 12. How to Run

Open the terminal inside the `CLASS` project folder.

Run the complete analytical pipeline:

```bash
python main.py
```

After the pipeline finishes, start the dashboard:

```bash
python dashboard/dashboard.py
```

To run the scenario simulator separately:

```bash
python analysis/scenario_simulator.py
```

---

## 13. Minimum Hardware Requirements

* Intel Core i3 / AMD equivalent or above
* 4 GB RAM
* At least 2 GB available storage
* Display resolution of 1366 × 768 or higher

---

## 14. Software Requirements

* Python 3.x
* Visual Studio Code or another Python-compatible IDE
* Pandas
* NumPy
* Matplotlib
* Tkinter

Tkinter is normally included with standard Python installations on Windows.

---

## 15. Limitations

The current system is a prototype analytical implementation.

The dataset used for development is constructed for demonstration and testing purposes.

The analytical weights and thresholds used in the scoring models are prototype design choices and have not been clinically or operationally validated.

The system should therefore not be interpreted as a medical diagnostic system or as an autonomous mission-control decision system.

Performance Stability is estimated using a rolling three-day window, and the scenario simulator does not independently recalculate the rolling stability metric from a single modified record.

---

## 16. Future Scope

Potential future extensions include:

* Real-time astronaut data ingestion
* Integration with wearable sensors
* Real physiological datasets
* Advanced machine-learning models
* Time-series forecasting
* Anomaly detection
* Explainable AI
* More sophisticated mission simulations
* Real-time mission-control dashboards
* Secure cloud-based data processing
* Integration with NASA, ESA, or ISRO-compatible research datasets where appropriate
* Validation using expert-defined physiological and operational criteria

---

## 17. Conclusion

CLASS provides an integrated analytical workflow for studying cognitive workload, fatigue, performance, decision efficiency, mission readiness, and potential risk conditions during long-duration space missions.

By combining data preprocessing, statistical analysis, custom analytical metrics, scenario simulation, visualization, and an interactive dashboard, the system demonstrates how data analytics can support human-factor analysis in aerospace environments.

The current implementation serves as a prototype foundation that can be extended with real-world datasets, advanced machine-learning techniques, domain validation, and real-time monitoring capabilities.