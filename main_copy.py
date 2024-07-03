import cv2
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, Toplevel, Label
from best_frame import choose_best_frame
from simpleFace import SimpleFacerec
from attendance_logger import AttendanceLogger
from datetime import datetime
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = "C:/Users/navne/OneDrive/Desktop/Project New Environemt/attendance_system-main/sonorous-mix-422222-k4-76584c592ca8.json"
SPREADSHEET_ID = "1KByMC6oXpKZRI-N0L3SGprBoLlY2lxAmfmJbKA2AWFE"



class FaceRecognitionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Department of Electronics and Telecommunication")

        self.current_camera_index = 0
        self.attendance_started = False
        self.attendance_list = []
        
        self.sfr = SimpleFacerec()
        self.sfr.load_encoding_images("C:/Users/navne/OneDrive/Desktop/Project New Environemt/attendance_system-main/faces_database/")
        
        self.cap = cv2.VideoCapture(self.current_camera_index)

        self.label = tk.Label(root)
        self.label.pack(side=tk.TOP, pady=10)

        self.frame_buttons = tk.Frame(root)
        self.frame_buttons.pack(side=tk.BOTTOM, pady=10)

        self.quit_button = tk.Button(self.frame_buttons, text="Quit", command=self.quit, bg="#C850C0", fg="white", padx=10, pady=5)  # Custom-styled button
        self.quit_button.pack(side=tk.LEFT, padx=10)

        self.switch_camera_button = tk.Button(self.frame_buttons, text="Switch Camera", command=self.switch_camera, bg="#C850C0", fg="white", padx=10, pady=5)  # Custom-styled button
        self.switch_camera_button.pack(side=tk.LEFT, padx=10)

        self.add_student_button = tk.Button(self.frame_buttons, text="Add Student", command=self.add_student, bg="#C850C0", fg="white", padx=10, pady=5)  # Custom-styled button
        self.add_student_button.pack(side=tk.LEFT, padx=10)

        self.start_attendance_button = tk.Button(self.frame_buttons, text="Start Attendance", command=self.start_attendance, bg="#C850C0", fg="white", padx=10, pady=5)  # Custom-styled button
        self.start_attendance_button.pack(side=tk.LEFT, padx=10)

        self.stop_attendance_button = tk.Button(self.frame_buttons, text="Stop Attendance", command=self.stop_attendance, state=tk.DISABLED, bg="#C850C0", fg="white", padx=10, pady=5)  # Custom-styled button
        self.stop_attendance_button.pack(side=tk.LEFT, padx=10)

        #self.copy_names_button = tk.Button(self.frame_buttons, text="Copy Names", command=self.copy_names, state=tk.DISABLED, bg="#C850C0", fg="white", padx=10, pady=5)  # Custom-styled button
        #self.copy_names_button.pack(side=tk.LEFT, padx=10)

        self.attendees_label = tk.Label(root, text="Attendance: ", bg="lightgray", padx=10, pady=5)  # Custom-styled label
        self.attendees_label.pack(side=tk.BOTTOM, pady=10)

        # Frame for name and ID inputs
        self.student_info_frame = tk.Frame(root)
        self.student_info_frame.pack(side=tk.BOTTOM, pady=10)

        self.name_label = tk.Label(self.student_info_frame, text="Enter student's name: ", bg="lightgray")  # Custom-styled label
        self.name_label.pack(side=tk.LEFT)

        self.name_entry = tk.Entry(self.student_info_frame)
        self.name_entry.pack(side=tk.LEFT)

        self.id_label = tk.Label(self.student_info_frame, text="Enter student's ID: ", bg="lightgray")  # Custom-styled label
        self.id_label.pack(side=tk.LEFT)

        self.id_entry = tk.Entry(self.student_info_frame)
        self.id_entry.pack(side=tk.LEFT)

        self.update_frame()

    def update_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if self.attendance_started:
            face_locations, face_names = self.sfr.detect_known_faces(frame)

            for name in face_names:
                if name not in self.attendance_list:
                    self.attendance_list.append(name)

            self.update_attendees_label()

        # Resize image to fit window
        height, width, _ = frame.shape
        if height > 500 or width > 700:
            frame = cv2.resize(frame, (700, 500))

        img = Image.fromarray(frame)
        img = ImageTk.PhotoImage(image=img)
        self.label.img = img
        self.label.config(image=img)
        
        self.root.after(10, self.update_frame)

    def switch_camera(self):
        self.cap.release()
        self.current_camera_index = (self.current_camera_index + 1) % 2
        self.cap = cv2.VideoCapture(self.current_camera_index)

    def start_attendance(self):
        self.attendance_started = True
        self.start_attendance_button.config(state=tk.DISABLED)
        self.stop_attendance_button.config(state=tk.NORMAL)
        #self.copy_names_button.config(state=tk.DISABLED)
        self.attendance_list = []


    def stop_attendance(self):
        self.attendance_started = False
        self.start_attendance_button.config(state=tk.NORMAL)
        self.stop_attendance_button.config(state=tk.DISABLED)
        #self.copy_names_button.config(state=tk.NORMAL)

    
        attendance_logger = AttendanceLogger("C:/Users/navne/OneDrive/Desktop/Project New Environemt/attendance_system-main/attendance.log")

    # Log the attendance
        attendance_logger.log_attendance(self.attendance_list)

        self.update_google_sheet(self.attendance_list)

    def copy_names(self):
        names_str = ", ".join(self.attendance_list)
        self.root.clipboard_clear()
        self.root.clipboard_append(names_str)

    def add_student(self):
        
        video_path = filedialog.askopenfilename(title="Select Video File", filetypes=[("Video files", "*.mp4")])
        if not video_path:
            return  # User canceled the selection

        
        student_name = self.name_entry.get()
        student_id = self.id_entry.get()

        
        choose_best_frame(video_path, student_id, student_name)

        


    def update_attendees_label(self):
        names_str = ", ".join(self.attendance_list)
        self.attendees_label.config(text="Attendance: " + names_str)

    def quit(self):
        self.cap.release()
        self.root.destroy()
    
    def update_google_sheet(self, names_list):
        credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)

        
        data = {
            'values': [
                [datetime.now().strftime('%Y-%m-%d'), datetime.now().strftime('%H:%M:%S')] + name.split('_')
                for name in names_list if name != "Unknown"
            ]
        }

        sheet = service.spreadsheets()
        result = sheet.values().append(spreadsheetId=SPREADSHEET_ID, range='Sheet1!A1', valueInputOption='USER_ENTERED', body=data).execute()
        self.show_dialog("Attendance Data updated successfully in the sheet.")
        self.attendees_label.config(text="Attendance: ")

    def show_dialog(self, message):
        dialog = Toplevel(self.root)
        dialog.title("Update Status")

        label = Label(dialog, text=message)
        label.pack(pady=20, padx=20)

        def close_dialog():
            dialog.destroy()

        self.root.after(5000, close_dialog)
        
        dialog.protocol("WM_DELETE_WINDOW", close_dialog)



def main():
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
