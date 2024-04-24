import tkinter as tk
from tkinter import messagebox, filedialog
import sqlite3
from PIL import Image, ImageTk
import re
from subprocess import Popen
import customtkinter as ctk
from customtkinter import *
import string
import os

class VoterSignup:
    def __init__(self, master):
        
        self.master = master
        self.root = master
        self.root.title("Voter Signup")
        self.root.geometry("780x520")  
        self.background_image = Image.open("miniproject\\register (1).png")
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self.root, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)
        
        self.signup_frame = tk.Frame(self.root, bg="black")
        self.signup_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.label_name = ctk.CTkLabel(self.signup_frame, text="Name:", font=("Helvetica", 12))
        self.label_name.grid(row=0, column=0, padx=10, pady=10)
        self.entry_name = ctk.CTkEntry(self.signup_frame, font=("Helvetica", 12))
        self.entry_name.grid(row=0, column=1, padx=10, pady=10)
        
        self.label_roll = ctk.CTkLabel(self.signup_frame, text="Password:", font=("Helvetica", 12))
        self.label_roll.grid(row=0, column=2, padx=10, pady=10)
        self.entry_roll = ctk.CTkEntry(self.signup_frame, font=("Helvetica", 12))
        self.entry_roll.grid(row=0, column=3, padx=10, pady=10)
        
        self.label_pid = ctk.CTkLabel(self.signup_frame, text="PID:", font=("Helvetica", 12))
        self.label_pid.grid(row=1, column=0, padx=10, pady=10)
        self.entry_pid = ctk.CTkEntry(self.signup_frame, font=("Helvetica", 12))
        self.entry_pid.grid(row=1, column=1, padx=10, pady=10)
        
        self.label_class = ctk.CTkLabel(self.signup_frame, text="Year:", font=("Helvetica", 12))
        self.label_class.grid(row=2, column=2, padx=10, pady=10)
        self.class_options = ["FE","SE","TE","BE"]
        self.class_var = tk.StringVar(master)
        self.class_var.set(self.class_options[0]) 
        self.class_dropdown = tk.OptionMenu(self.signup_frame, self.class_var, *self.class_options)
        self.class_dropdown.config(font=("Helvetica", 12), bg= "grey")
        self.class_dropdown.grid(row=2, column=3, padx=10, pady=10)
        
        self.label_email = ctk.CTkLabel(self.signup_frame, text="Email:", font=("Helvetica", 12))
        self.label_email.grid(row=1, column=2, padx=10, pady=10)
        self.entry_email = ctk.CTkEntry(self.signup_frame, font=("Helvetica", 12))
        self.entry_email.grid(row=1, column=3, padx=10, pady=10)
        
        self.label_branch = ctk.CTkLabel(self.signup_frame, text="Branch:", font=("Helvetica", 12))
        self.label_branch.grid(row=2, column=0, padx=10, pady=10)
        self.branch_options = ["INFT", "CMPN", "MECH", "EXTC", "ELEC"]
        self.branch_var = tk.StringVar(master)
        self.branch_var.set(self.branch_options[0]) 
        self.branch_dropdown = tk.OptionMenu(self.signup_frame, self.branch_var, *self.branch_options)
        self.branch_dropdown.config(font=("Helvetica", 12), bg="grey")
        self.branch_dropdown.grid(row=2, column=1, padx=2, pady=2)
        
        
        self.image_preview_label = ctk.CTkLabel(self.signup_frame, text="Image Preview:", font=("Helvetica", 12))
        self.image_preview_label.grid(row=3, column=0, padx=10, pady=10)
        self.image_preview = tk.Label(self.signup_frame, bg="black")
        self.image_preview.grid(row=3, column=1, columnspan=1, padx=1, pady=10)
        
        self.submit_button = ctk.CTkButton(self.signup_frame, text="Submit", command=self.submit_form, font=("Helvetica", 12))
        self.submit_button.grid(row=4, column=2, padx=10, pady=10, sticky="e")
        
        self.back_button = ctk.CTkButton(self.signup_frame, text="Back", command=self.back_to_campus_voice, font=("Helvetica", 12))
        self.back_button.grid(row=4, column=1, padx=10, pady=10, sticky="e")
        
        self.add_image_button = ctk.CTkButton(self.signup_frame, text="Add Image", command=self.add_image, font=("Helvetica", 12))
        self.add_image_button.grid(row=4, column=3, padx=10, pady=10, sticky="e")
        
        self.root.mainloop()

    def submit_form(self):
        name = self.entry_name.get().strip()
        roll = self.entry_roll.get().strip()
        pid = self.entry_pid.get().strip()
        class_ = self.class_var.get().strip().upper() 
        branch = self.branch_var.get().strip()
        email = self.entry_email.get().strip()

        error_messages = []

        if not name.replace(" ", "").isalpha():
           error_messages.append("Name can only contain alphabetic characters and spaces.")
        if not (len(roll) >= 6 and any(char.isdigit() for char in roll) and any(char in string.ascii_letters for char in roll)):
            error_messages.append("Password must be at least 6 digits with a combination of numbers and letters.")

        if not (pid.isdigit() and len(pid) == 6):
           error_messages.append("Password must contain exactly six digits.")
        if not email.endswith('@student.sfit.ac.in'):
           error_messages.append("Email must contain the domain '@student.sfit.ac.in'.")

        if error_messages:
           messagebox.showerror("Error", "\n".join(error_messages))
           return

        try:
            connection = sqlite3.connect("Kenny.db")
            cursor = connection.cursor()

            cursor.execute("PRAGMA table_info(voters)")
            table_info = cursor.fetchall()
            image_column_exists = any(column[1] == "image" for column in table_info)
            if not image_column_exists:
                cursor.execute("ALTER TABLE voters ADD COLUMN image BLOB")

            cursor.execute("INSERT INTO voters (name, roll, pid, class_, branch, email, image) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (name, roll, pid, class_, branch, email, self.image_data))
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Signup successful!")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def back_to_campus_voice(self):
        try:
            # Destroy the current window
            self.master.destroy()
            current_directory = os.getcwd()
            # Append the relative path to splash.py
            splash_path = os.path.join(current_directory, "miniproject", "splash.py")
            Popen(["python", splash_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open splash.py: {e}")
        
    def add_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            with open(file_path, "rb") as file:
                self.image_data = file.read()
            self.load_image_preview(file_path)

    def load_image_preview(self, file_path):
        image = Image.open(file_path)
        image.thumbnail((100, 100))  
        photo = ImageTk.PhotoImage(image)
        self.image_preview.config(image=photo)
        self.image_preview.image = photo  

