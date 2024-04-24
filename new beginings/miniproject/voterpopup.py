import tkinter as tk
from votersignup import VoterSignup
from voterlogin import VoterLogin

class VoterSignupPopup:
    def __init__(self, master):
        self.master = master
        self.popup = tk.Toplevel(master)
        self.popup.title("Voter Options")
        self.popup.geometry("300x150")
        self.popup.configure(background="white")

        screen_width = self.popup.winfo_screenwidth()
        screen_height = self.popup.winfo_screenheight()

        x = (screen_width - 300) // 2  
        y = (screen_height - 150) // 2  

        self.popup.geometry(f"300x150+{x}+{y}")

        label = tk.Label(self.popup, text="Choose an option:", font=("Helvetica", 12), bg="white")
        label.pack(pady=10)

        signup_button = tk.Button(self.popup, text="Signup", command=self.open_voter_signup, font=("Helvetica", 12))
        signup_button.pack(pady=5)

        login_button = tk.Button(self.popup, text="Login", command=self.open_voter_login, font=("Helvetica", 12))
        login_button.pack(pady=5)

    def open_voter_signup(self):
        self.popup.destroy() 
        voter_signup_window = VoterSignup(self.master)

    def open_voter_login(self):
     self.popup.destroy()
     voter_login_window = VoterLogin(self.master)



