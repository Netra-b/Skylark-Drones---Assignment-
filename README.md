# Drone Operations Coordination System

## 📌 Project Overview

This project implements a **Drone Operations Coordination System** designed to automatically assign drones and pilots to client missions based on priority, availability, skills, certifications, and location constraints.

The system ensures that:

* High‑priority missions are handled first
* Only **AVAILABLE** pilots and drones are assigned
* Skill and certification mismatches are avoided
* Clear operational reports are generated for decision‑making

This project demonstrates practical use of **Python, Pandas, data‑driven decision logic, and report generation**, making it suitable for operations management and backend automation use cases.

---

## 🗂️ Project Structure

```
project_root/
│
├── coordinator.py                 # Core mission assignment logic
├── data/
│   ├── drone_fleet.csv             # Drone inventory and certifications
│   ├── pilot_roster.csv            # Pilot skills, location, availability
│   └── missions.csv                # Mission requirements and priorities
│
├── operations_status_report.md     # Auto‑generated output report
└── README.md                       # Project documentation
```

---

## 📊 Input Data Description

### `missions.csv`

Defines client missions and operational requirements.

| Column          | Description                      |
| --------------- | -------------------------------- |
| project_id      | Unique mission ID                |
| client          | Client name                      |
| priority        | Urgent / High / Standard         |
| location        | Mission location                 |
| required_skills | Skills required from pilot       |
| required_certs  | Certifications required on drone |

---

### `pilot_roster.csv`

Defines available pilots and their capabilities.

| Column   | Description             |
| -------- | ----------------------- |
| name     | Pilot name              |
| skills   | Pilot skill set         |
| location | Current base location   |
| status   | AVAILABLE / UNAVAILABLE |

---

### `drone_fleet.csv`

Defines drone inventory and certifications.

| Column         | Description             |
| -------------- | ----------------------- |
| drone_id       | Unique drone identifier |
| certifications | Drone certifications    |
| status         | AVAILABLE / MAINTENANCE |

---

## ⚙️ Assignment Logic

Missions are processed using the following logic:

1. Missions are **sorted by priority** (Urgent → High → Standard)
2. For each mission:

   * Find an AVAILABLE pilot
   * Pilot must:

     * Be in the same location
     * Have all required skills
   * Find an AVAILABLE drone
   * Drone must:

     * Have all required certifications
3. If all conditions are met → **Mission Assigned**
4. If any condition fails → **Mission Blocked with reason**

Each pilot and drone can only be assigned once per run.

---

## 🧠 Example Outcome

| Project | Priority | Status   | Reason                                  |
| ------- | -------- | -------- | --------------------------------------- |
| PRJ002  | Urgent   | Assigned | Matching pilot and drone found          |
| PRJ001  | High     | Assigned | Matching pilot and drone found          |
| PRJ003  | Standard | Blocked  | No compatible pilot + drone combination |

---

## 📝 Generated Report

After execution, the system automatically generates:

📄 **`operations_status_report.md`**

The report contains:

* Assignment summary
* Pilot and drone allocations
* Clear decision notes explaining every assignment or blockage

This ensures **auditability and operational transparency**.

---

## ▶️ How to Run

1. Ensure Python 3.9+ is installed
2. Install dependencies:

```bash
pip install pandas
```

3. Ensure the `data/` directory contains all CSV files
4. Run the coordinator logic (via UI or script)
5. View results in `operations_status_report.md`

---

## 🚀 Skills & Concepts Demonstrated

* Python OOP design
* Pandas data processing
* Priority‑based scheduling
* Constraint satisfaction logic
* Automated report generation
* Clean, maintainable backend code

---

## ✅ Conclusion

This Drone Operations Coordination System provides a scalable and transparent solution for managing complex operational constraints in mission‑critical environments. The modular design allows easy extension for future enhancements such as fuel constraints, weather checks, or real‑time availability updates.

---