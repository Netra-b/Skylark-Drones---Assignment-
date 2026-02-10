import pandas as pd
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
REPORT_PATH = Path("operations_status_report.md")

PRIORITY_ORDER = {
    "Urgent": 1,
    "High": 2,
    "Standard": 3
}


class Coordinator:
    def __init__(self):
        self.assignments = []
        self.decision_notes = []

    def assign_missions(self):
        self.assignments = []
        self.decision_notes = []

        drones = pd.read_csv(DATA_DIR / "drone_fleet.csv")
        missions = pd.read_csv(DATA_DIR / "missions.csv")
        pilots = pd.read_csv(DATA_DIR / "pilot_roster.csv")

        # ---- SORT BY PRIORITY ----
        missions["priority_rank"] = missions["priority"].map(PRIORITY_ORDER)
        missions = missions.sort_values("priority_rank")

        available_drones = drones[drones["status"] == "AVAILABLE"].to_dict("records")
        available_pilots = pilots[pilots["status"] == "AVAILABLE"].to_dict("records")

        for _, mission in missions.iterrows():
            assigned = False

            required_skills = {
                s.strip().lower()
                for s in str(mission["required_skills"]).split(",")
            }

            required_certs = {
                s.strip().lower()
                for s in str(mission["required_certs"]).split(",")
            }

            for pilot in available_pilots:
                pilot_skills = {
                    s.strip().lower()
                    for s in str(pilot["skills"]).split(",")
                }

                if not required_skills.issubset(pilot_skills):
                    continue

                if pilot["location"] != mission["location"]:
                    continue

                for drone in available_drones:
                    drone_certs = {
                        s.strip().lower()
                        for s in str(drone["certifications"]).split(",")
                    }

                    if not required_certs.issubset(drone_certs):
                        continue

                    # ✅ ASSIGN
                    self.assignments.append({
                        "Project ID": mission["project_id"],
                        "Client": mission["client"],
                        "Priority": mission["priority"],
                        "Location": mission["location"],
                        "Required Skills": mission["required_skills"],
                        "Pilot": pilot["name"],
                        "Drone": drone["drone_id"],
                        "Status": "Assigned"
                    })

                    self.decision_notes.append(
                        f"{mission['project_id']} assigned to {pilot['name']} "
                        f"in {mission['location']} using drone {drone['drone_id']}."
                    )

                    available_pilots.remove(pilot)
                    available_drones.remove(drone)
                    assigned = True
                    break

                if assigned:
                    break

            if not assigned:
                reason = (
                    f"{mission['project_id']} blocked because no AVAILABLE pilot in "
                    f"{mission['location']} with skills {mission['required_skills']} "
                    f"and drone with certifications {mission['required_certs']}."
                )

                self.assignments.append({
                    "Project ID": mission["project_id"],
                    "Client": mission["client"],
                    "Priority": mission["priority"],
                    "Location": mission["location"],
                    "Required Skills": mission["required_skills"],
                    "Pilot": "N/A",
                    "Drone": "N/A",
                    "Status": "Blocked"
                })

                self.decision_notes.append(reason)

        return self.assignments

    def generate_report(self):
        lines = [
            "# Drone Operations Status Report\n",
            f"Generated on: {datetime.now()}\n",
            "## Assignments\n"
        ]

        for a in self.assignments:
            lines.append(
                f"- **{a['Project ID']}** ({a['Priority']}) → {a['Status']} "
                f"| Pilot: {a['Pilot']} | Drone: {a['Drone']}"
            )

        lines.append("\n## Decision Notes\n")
        for note in self.decision_notes:
            lines.append(f"- {note}")

        REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
        return REPORT_PATH