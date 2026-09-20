# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose

The purpose of the Cognitive Load Analytics System for Long-Duration Space Missions (CLASS) is to provide a prototype data analytics and decision-support system for analyzing astronaut cognitive workload, fatigue, performance, and mission readiness.

The system integrates multiple physiological, behavioral, and mission-related parameters and converts them into analytical indicators that can be explored through visualizations and an interactive dashboard.

### 1.2 Scope

CLASS covers:

* Astronaut data input
* Data cleaning
* Data preprocessing
* Exploratory data analysis
* Correlation analysis
* Cognitive load analysis
* Fatigue recovery analysis
* Performance stability analysis
* Decision efficiency analysis
* Mission readiness analysis
* Risk identification
* Mission scenario simulation
* Data visualization
* Interactive dashboard presentation

The current system is a prototype and does not replace medical diagnosis, clinical assessment, or operational mission-control procedures.

---

## 2. Functional Requirements

### FR1: Data Input

The system shall accept astronaut and mission-related data in CSV format.

### FR2: Data Validation

The system shall check the input data for:

* Missing values
* Duplicate records
* Invalid numerical values
* Values outside defined prototype ranges

### FR3: Data Preprocessing

The system shall normalize selected numerical parameters to prepare them for analytical calculations.

### FR4: Exploratory Data Analysis

The system shall provide statistical summaries including:

* Mean
* Median
* Variance
* Standard deviation
* Percentiles
* Mission-level summaries
* Astronaut-level summaries

### FR5: Correlation Analysis

The system shall calculate correlations between selected mission and astronaut parameters.

### FR6: Cognitive Load Analysis

The system shall calculate a Cognitive Load Index using weighted normalized parameters.

### FR7: Fatigue Recovery Analysis

The system shall calculate a prototype Fatigue Recovery Score using sleep and reaction-time indicators.

### FR8: Performance Stability Analysis

The system shall calculate a Performance Stability Index using a rolling performance measure.

### FR9: Decision Efficiency Analysis

The system shall calculate a Decision Efficiency Score using task completion, errors, and reaction time.

### FR10: Mission Readiness Analysis

The system shall combine the analytical scores to calculate a Mission Readiness Score.

### FR11: Risk Analysis

The system shall identify potential risk conditions using defined analytical thresholds and generate risk factors.

### FR12: Scenario Simulation

The system shall allow users to modify selected mission conditions and compare the resulting scenario metrics with the original condition.

### FR13: Visualization

The system shall generate graphical representations of important trends, relationships, and risk distributions.

### FR14: Dashboard

The system shall provide an interactive dashboard for viewing analytical results for a selected astronaut and mission day.

---

## 3. Non-Functional Requirements

### NFR1: Usability

The system should provide a simple interface that allows users to access analytical results without interacting directly with Python code.

### NFR2: Performance

The system should process the prototype dataset within a reasonable amount of time on the specified minimum hardware.

### NFR3: Reliability

The system should validate input data and report processing errors instead of silently producing invalid results.

### NFR4: Maintainability

The system should use modular Python files so that preprocessing, analytics, visualization, and dashboard components can be modified independently.

### NFR5: Reproducibility

The system should use a requirements file so that the required Python environment can be recreated.

### NFR6: Portability

The system should be capable of running on a standard Windows computer with Python installed.

### NFR7: Data Integrity

The original raw dataset should remain unchanged during processing. Processed datasets should be stored separately.

### NFR8: Security

If real astronaut or physiological data are used in a future implementation, appropriate access control, encryption, and data-protection mechanisms should be applied.

---

## 4. Hardware Requirements

Minimum hardware requirements:

* Intel Core i3 or equivalent processor
* 4 GB RAM
* At least 2 GB available storage
* Display resolution of 1366 × 768 or higher

---

## 5. Software Requirements

* Python 3.x
* Visual Studio Code or compatible Python IDE
* Pandas
* NumPy
* Matplotlib
* Tkinter
* Windows operating system or another Python-compatible operating system

---

## 6. Input Requirements

The system requires the following fields:

* Mission_Day
* Astronaut_ID
* Sleep_Hours
* Reaction_Time_ms
* Heart_Rate
* Tasks_Completed
* Task_Complexity
* Errors
* Radiation_Exposure
* Communication_Delay_sec
* Stress_Level

---

## 7. Output Requirements

The system shall produce:

* Cleaned dataset
* Preprocessed dataset
* Correlation matrix
* Cognitive Load results
* Fatigue Recovery results
* Performance Stability results
* Decision Efficiency results
* Mission Readiness results
* Risk analysis results
* Analytical visualizations
* Dashboard-based mission condition summary

---

## 8. Constraints

The current prototype has the following constraints:

* The development dataset is constructed for demonstration.
* Analytical weights are prototype choices.
* Risk thresholds are prototype rules.
* The system does not perform medical diagnosis.
* The system does not independently make mission decisions.
* Real-world validation would be required before operational use.
* Performance stability requires multiple observations because it uses a rolling window.

---

## 9. Assumptions

The system assumes that:

* Input records contain valid astronaut identifiers.
* Numerical measurements are represented using consistent units.
* Mission-day information is available.
* The input dataset contains the required fields.
* The selected analytical weights are appropriate for prototype demonstration.
