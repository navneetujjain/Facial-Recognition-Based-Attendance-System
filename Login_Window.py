import tkinter as tk
from main_copy import FaceRecognitionApp
from PIL import Image, ImageTk
import tkinter.messagebox as tmsg
import tkinter.ttk as ttk



class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("600x500")
        self.root.configure(bg="#333333")

        self.background_image = ImageTk.PhotoImage(Image.open("C:/Users/navne/OneDrive/Desktop/Project New Environemt/attendance_system-main/background.jpg"))
        self.background_label = tk.Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Add logo
        self.logo = ImageTk.PhotoImage(Image.open("C:/Users/navne/OneDrive/Desktop/Project New Environemt/attendance_system-main/logo.png"))
        self.logo_label = tk.Label(self.root, image=self.logo, bg="#333333")
        self.logo_label.pack(pady=(30, 0))

        # Add label
        self.label = tk.Label(self.root, text="Department of Electronics and Telecommunication", font=("Roboto", 16, "bold"), fg="white", bg="#333333")
        self.label.pack(pady=(10, 0))

        self.id_frame = tk.Frame(self.root, bg="#444444")
        self.id_frame.pack(pady=(20, 0))

        self.id_label = tk.Label(self.id_frame, text="Enter ID:", font=("Arial", 14), fg="white", bg="#444444")
        self.id_label.pack(side="left", padx=(20, 0))

        self.id_entry = tk.Entry(self.id_frame, font=("Arial", 14))
        self.id_entry.pack(side="left", padx=(10, 0))

        self.password_frame = tk.Frame(self.root, bg="#444444")
        self.password_frame.pack(pady=(20, 0))

        self.password_label = tk.Label(self.password_frame, text="Enter Password:", font=("Arial", 14), fg="white", bg="#444444")
        self.password_label.pack(side="left", padx=(20, 0))

        self.password_entry = tk.Entry(self.password_frame, font=("Arial", 14), show="*")
        self.password_entry.pack(side="left", padx=(10, 0))

        self.login_button = tk.Button(self.root, text="Login", font=("Roboto", 14), command=self.check_credentials, bg="#555555", fg="white", bd=0, cursor="hand2")
        self.login_button.pack(pady=(20, 0))

        #self.progress = ttk.Progressbar(self.root, length=200, mode='indeterminate')
        #self.progress.pack(pady=(20, 0))
        #self.progress.place_forget()

    

        self.login_button.bind("<Enter>", self.on_enter)
        self.login_button.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.login_button.config(bg="#666666")

    def on_leave(self, e):
        self.login_button.config(bg="#555555")

        #self.progress.place(x=150, y=200)
        #self.progress.start(10)


        

    def check_credentials(self):
        id = self.id_entry.get()
        password = self.password_entry.get()

        #self.progress.place(x=150, y=200)
        #self.progress.start(10)

        
        if id == "Navneet" and password == "Tce@123":
            #self.progress.stop()
            #self.progress.place_forget()
            self.root.destroy()
            main()
        else:
            #self.progress.stop()
            #self.progress.place_forget()
            self.id_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            #self.id_label.config(text="Invalid ID or Password. Try again:", fg="red")
            #self.password_label.config(text="Invalid ID or Password. Try again:", fg="red")
            invalid_label = tk.Label(self.root, text="Invalid ID or Password. Please try again.", font=("Arial", 12), fg="red", bg="#333333")
            invalid_label.pack(pady=(10, 0))  # Adjust padding as needed

def main():
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()

if __name__ == "__main__":
    login_root = tk.Tk()
    login_window = LoginWindow(login_root)
    login_root.mainloop()