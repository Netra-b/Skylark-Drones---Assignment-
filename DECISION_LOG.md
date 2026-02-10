# Decision Log — Drone Operations Coordinator

## Assumptions
- Input CSVs live in the `data/` folder by default. This can be changed via the `DATA_DIR` environment variable.
- CSV columns may vary; the loader tolerates missing non-essential columns. Recommended columns:
  - `pilot_roster.csv`: `pilot_id`, `name`, `status`, `skills` (semicolon-separated), `certifications` (semicolon-separated), `location_lat`, `location_lon`.
  - `drone_fleet.csv`: `drone_id`, `model`, `status`, `payload_capacity_kg`, `maintenance_due`, `location_lat`, `location_lon`.
  - `missions.csv`: `mission_id`, `status` (PENDING), `priority` (HIGH/MEDIUM/LOW), `start`, `end`, `required_skills`, `required_certifications`, `required_payload_kg`, `location_lat`, `location_lon`.

## Tradeoffs
- Scheduling logic is greedy and deterministic: it prefers earliest/ highest-priority missions, picks the first compatible pilot/drone pair, and uses simple preemption for HIGH-priority missions. This keeps the implementation understandable and maintainable.
- No external geolocation packages are used; a Haversine implementation is included to avoid extra dependencies.
- Time-window conflict detection requires valid `start`/`end` timestamps in `missions.csv`. Missions missing timestamps will be skipped for conflict checks but may still be assigned.

## Future Improvements
- Add weighted scoring to prefer closest pilots/drones and to balance utilization.
- Support shift schedules and pilot duty-time limits.
- Add an optimization step (ILP / MIP) for global optimal assignments.
- Add unit tests and CI integration.
