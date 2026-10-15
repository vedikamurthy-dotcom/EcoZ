# EcoZ
EcoZ is a carbon aware workload schedular for enterprise batch processing system and recommends better execution times without violating their deadlines.

PROJECT OVERVIEW 

EcoZ sits at the intersection of three important areas: sustainable computing, enterprise workload scheduling, and electricity carbon-intensity forecasting.
A. Enterprise batch processing
Banks and other enterprises run jobs such as reporting, reconciliation, risk calculations and payroll processing. Some have strict deadlines, while others have execution windows in which they can be moved. EcoZ focuses on the flexible jobs.
B. Carbon-aware computing
The emissions associated with a unit of electricity vary by grid, location and time. The Green Software Foundation's Carbon Aware SDK describes ways to use emissions information to choose when or where software workloads run. 
C. Scheduling and decision support
The application combines a job's permitted execution window with hourly carbon-intensity estimates. It chooses a lower-carbon feasible time, then shows the original schedule, proposed schedule and estimated emissions difference.

PROBLEM STATEMENT 

Problem Statement — EcoZ: Carbon-Aware Enterprise Workload Scheduler
Enterprise systems execute batch-processing workloads according to predefined schedules that are primarily designed around business deadlines and operational requirements. However, flexible workloads may be executed during periods when the electricity grid has relatively high carbon intensity, resulting in avoidable electricity-related emissions.
Traditional fixed-time scheduling does not necessarily account for changes in grid carbon intensity. At the same time, postponing workloads without considering deadlines, execution duration, priority and dependencies can create operational risks.
The proposed EcoZ system aims to develop an interactive, carbon-aware scheduling dashboard that evaluates eligible enterprise jobs against hourly electricity carbon-intensity data and recommends lower-carbon execution windows.
The system will estimate baseline and proposed emissions, identify potential carbon savings, and enforce configurable execution-window and deadline constraints. It will provide visual analytics to help users understand the environmental benefits and scheduling trade-offs.
The prototype will first use clearly identified simulated data and will be designed to support integration with real carbon-intensity APIs and enterprise scheduling systems in future versions.
