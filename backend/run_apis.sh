#!/bin/bash
fastapi dev hr/employees/api_manage.py --host 0.0.0.0 --port 8000 &
fastapi dev hr/Attendance/api_manage.py --host 0.0.0.0 --port 8001
wait