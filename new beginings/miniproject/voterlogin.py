import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
from subprocess import Popen
import customtkinter as ctk
import os

class VoterLogin:
    def __init__(self, master):
        self.master = master
        self.root = master
        self.root.title("Voter Login")
        self.root.geometry("780x520")  
        self.background_image = Image.open("miniproject\\login.png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        self.root.configure(background="white")  



        self.label_pid = ctk.CTkLabel(self.root, text="PID Number:", font=("Helvetica", 12), bg_color="black")
        self.label_pid.place(relx=0.318, rely=0.35)  
        self.entry_pid = ctk.CTkEntry(self.root, font=("Helvetica", 12), bg_color="black")
        self.entry_pid.place(relx=0.43, rely=0.35)  

        self.label_email = ctk.CTkLabel(self.root, text="Password:", bg_color="black", font=("Helvetica", 12))
        self.label_email.place(relx=0.33,rely=0.48) 
        self.entry_email = ctk.CTkEntry(self.root, font=("Helvetica", 12), bg_color="black", show="*")
        self.entry_email.place(relx=0.43,rely=0.48) 

        self.submit_button = ctk.CTkButton(self.root, text="Submit", command=self.submit_form, font=("Helvetica", 12), bg_color="black")
        self.submit_button.place(relx=0.53,rely=0.7)

        self.back_button = ctk.CTkButton(self.root, text="Back", command=self.back_to_campus_voice, font=("Helvetica", 12), bg_color="black")
        self.back_button.place(relx=0.3 ,rely=0.7)
        
    def submit_form(self):
        pid = self.entry_pid.get()
        roll = self.entry_email.get()
        if not pid or not roll:
            messagebox.showerror("Error", "Please enter both PID and Password.")
            return

        # Connect to the SQLite database
        connection = sqlite3.connect("Kenny.db")
        cursor = connection.cursor()

        # Query the database for the provided PID and email
        cursor.execute("SELECT * FROM voters WHERE pid=? AND roll=?", (pid, roll))
        voter = cursor.fetchone()

        # Check if a matching record was found
        if voter:
            messagebox.showinfo("Success", "Login successful!")
            self.root.destroy()
            Popen(["python", "voterhome.py",   pid, roll])
        else:
            messagebox.showerror("Error", "Invalid PID or Password.")

        # Close the database connection
        connection.close()

    def back_to_campus_voice(self):
        try:
            # Destroy the current window
            self.master.destroy()
            # Adjust the path to splash.py accordingly
            splash_path = r"C:\Users\Charis\Desktop\new beginings\miniproject\splash.py"
            Popen(["python", splash_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open splash.py: {e}")