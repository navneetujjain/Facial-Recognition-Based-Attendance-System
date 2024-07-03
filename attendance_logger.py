import datetime

class AttendanceLogger:
    def __init__(self, filename):
        self.filename = filename

    def log_attendance(self, attendance_list):
        with open(self.filename, "a") as f:
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{current_datetime} - Attendance: {', '.join(attendance_list)}\n")