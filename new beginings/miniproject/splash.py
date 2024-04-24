import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from votersignup import *
from votersignup import VoterSignup
from voterlogin import VoterLogin


class CampusVoice:
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(background="white")

        window_width = 780
        window_height = 520
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.root.title("CampusVoice")

        self.image = Image.open(r'miniproject\Frame 3 (1).png')
        self.photo = ImageTk.PhotoImage(self.image)

        self.label_image = tk.Label(self.root, image=self.photo)
        self.label_image.place(x=0, y=0)


        button_width = 15
        button_height = 2
        button_padding = 20
        button_y = 0.9 * window_height

        self.button_candidate = tk.Button(self.root, text="Signup", width=button_width, height=button_height, bg="#856cbf", fg="black", font=("Helvetica", 14, "bold"), relief=RAISED, borderwidth=3, command=self.open_signup)
        self.button_candidate.place(relx=0.3, rely=button_y/window_height, anchor=CENTER)

        self.button_voter = tk.Button(self.root, text="Login", width=button_width, height=button_height, bg="#856cbf", fg="black", font=("Helvetica", 14, "bold"), relief=RAISED, borderwidth=3, command=self.open_login)
        self.button_voter.place(relx=0.7, rely=button_y/window_height, anchor=CENTER)

        self.root.mainloop()

    def open_signup(self):
        self.voter_signup= VoterSignup(self.root)
        

    def open_login(self):
        self.voter_login = VoterLogin(self.root)
        
        

if __name__ == "__main__":
    app = CampusVoice()
 