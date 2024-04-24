import tkinter as tk
from PIL import Image, ImageTk
import sys
import sqlite3
from io import BytesIO
from tkinter import messagebox
from subprocess import Popen
import sys, os
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import customtkinter as ctk


WIDTH = 780
HEIGHT = 520

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x_coordinate = int((screen_width / 2) - (width / 2))
    y_coordinate = int((screen_height / 2) - (height / 2))

    window.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")



class ProfileWindow:
    def __init__(self, master, reg_window, user_data):
        self.master = master
        self.reg_window = reg_window
        self.user_data = user_data  # Assign user_data attribute
        self.master.title("User Profile")
        self.master.geometry(f"{WIDTH}x{HEIGHT}")  # Set the geometry to match RegWindow
     
        
                # Set the initial window size
        width = 780
        height = 520

        # Set the geometry to center the window on the screen
        center_window(self.master, width, height)

        profile_frame = tk.Frame(master)
        profile_frame.pack(padx=0, pady=0)

        bg_image = Image.open("miniproject\\becomecandidate (2).png")
        bg_image = bg_image.resize((WIDTH, HEIGHT), Image.BICUBIC)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        canvas = tk.Canvas(profile_frame, width=WIDTH, height=HEIGHT)
        canvas.pack()
        canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        name, pid, class_, branch, image_data = user_data

        # Display user profile
        if image_data:
            image = Image.open(BytesIO(image_data))
            image.thumbnail((100, 100))
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(profile_frame, image=photo)
            image_label.image = photo
            image_label.place(x=80, y=150)  # Adjust the coordinates as needed
        else:
            image_label = tk.Label(profile_frame, text="No Image", font=("Times", 12), foreground="gray")
            image_label.place(x=80, y=150)  # Adjust the coordinates as needed

        tk.Label(profile_frame, text="Name:", font=("Inter", 14, "bold"), bg="black", fg="white").place(x=200, y=150)
        tk.Label(profile_frame, text=name, font=("Inter", 14), bg="black", fg="white").place(x=300, y=150)

        tk.Label(profile_frame, text="PID:", font=("Inter", 14, "bold"), bg="black", fg="white").place(x=200, y=200)
        tk.Label(profile_frame, text=pid, font=("Inter", 14), bg="black", fg="white").place(x=300, y=200)

        tk.Label(profile_frame, text="Class:", font=("Inter", 14, "bold"), bg="black", fg="white").place(x=200, y=250)
        tk.Label(profile_frame, text=class_, font=("Inter", 14), bg="black", fg="white").place(x=300, y=250)

        tk.Label(profile_frame, text="Branch:", font=("Inter", 14, "bold"), bg="black", fg="white").place(x=200, y=300)
        tk.Label(profile_frame, text=branch, font=("Inter", 14), bg="black", fg="white").place(x=300, y=300)


        become_candidate_button = ctk.CTkButton(profile_frame, text="Become a Candidate", command=self.become_candidate,bg_color="black")
        become_candidate_button.place(x=200, y=390)  # Adjust the coordinates as needed

        back_button = ctk.CTkButton(profile_frame, text="Back", command=self.back_to_reg_window, bg_color="black")
        back_button.place(x=500, y=390)  # Adjust the coordinates as needed
        
        self.defaulter_status = tk.BooleanVar()  # Variable to store defaulter status
        self.kt_status = tk.BooleanVar()  # Variable to store KT status

        # Checkboxes for defaulter and KT status
        ctk.CTkCheckBox(profile_frame, text="Yes, I have active defaulters", bg_color="black", variable=self.defaulter_status, onvalue=True, offvalue=False).place(x=200, y=350)
        ctk.CTkCheckBox(profile_frame, text="Yes, I have live KT", bg_color="black",variable=self.kt_status, onvalue=True, offvalue=False).place(x=405, y=350)

    def back_to_reg_window(self):
        self.master.destroy()
        self.reg_window.master.deiconify()

    def become_candidate(self):
        if self.defaulter_status.get() or self.kt_status.get():
            messagebox.showinfo("Information", "Sorry, you are ineligible to become a candidate.")
            return
        try:
            connection = sqlite3.connect("Kenny.db")
            cursor = connection.cursor()

            # Check if the user is already a candidate
            cursor.execute("SELECT COUNT(*) FROM candidates WHERE pid=? ", (self.user_data[1],))
            candidate_count = cursor.fetchone()[0]

            if candidate_count > 0:
                # If the user is already a candidate, show a message and return
                messagebox.showinfo("Information", "You are already a candidate.")
                return

            # Create candidates table if it doesn't exist
            cursor.execute('''CREATE TABLE IF NOT EXISTS candidates (
                            name TEXT,
                            pid TEXT,
                            class_ TEXT,
                            branch TEXT,
                            image BLOB
                        )''')

            # Insert user data into the candidates table
            cursor.execute('''INSERT INTO candidates (name, pid, class_, branch, image)
                          VALUES (?, ?, ?, ?, ?)''', self.user_data)

            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "You have successfully become a candidate!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to become a candidate. Error: {e}")

            
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % tuple(int(255 * x) for x in rgb[:3])

class ResultsPage:
    def __init__(self, master):
        self.master = master
        self.master.title("Results")
        self.master.geometry(f"{WIDTH}x{HEIGHT}")
                # Set the initial window size
        width = 780
        height = 520

        # Set the geometry to center the window on the screen
        center_window(self.master, width, height)

        self.bg_image = Image.open(r"miniproject\Results (5).png")
        self.bg_image = self.bg_image.resize((WIDTH, HEIGHT), Image.BICUBIC)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT)
        canvas.pack()

        canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)

        self.result_label = tk.Label(canvas, text="Winner:", font=("Segoe UI Semibold", 19), bg="black", fg="white")
        self.result_label.place(relx=0.28, rely=0.28, anchor=tk.CENTER)
        self.result_label = tk.Label(canvas, text="Pie Chart-", font=("Segoe UI Semibold", 19), bg="black", fg="white")
        self.result_label.place(relx=0.70, rely=0.28, anchor=tk.CENTER)

        self.result_frame = tk.Frame(canvas, bg="black")
        self.result_frame.place(relx=0.18, rely=0.5, anchor=tk.CENTER)

        self.fetch_most_voted_candidate()
        self.create_pie_chart()

        back_button = ctk.CTkButton(canvas, text="Back", bg_color="black",  command=self.back_to_homepage)
        back_button.place(relx=0.5, rely=0.94, anchor=tk.CENTER)

    def fetch_most_voted_candidate(self):
        try:
            connection = sqlite3.connect("Kenny.db")
            cursor = connection.cursor()

            # Query to get the candidate with the most votes
            cursor.execute("""
                SELECT candidates.name, candidates.pid, candidates.class_, candidates.branch, COUNT(results.candidate_pid) as vote_count, candidates.image
                FROM candidates
                JOIN results ON candidates.pid = results.candidate_pid
                GROUP BY candidates.pid
                ORDER BY vote_count DESC
                LIMIT 1
            """)
            result = cursor.fetchone()

            if result:
                name, pid, class_, branch, vote_count, image_data = result
                result_text = f"{name}\n{class_} {branch}\nLive Count: {vote_count}"
                tk.Label(self.result_frame, text=result_text, font=("Arial", 15), bg="black", fg="white").pack(pady=5)
            
                # Display the image of the winner on the canvas
                if image_data:
                    winner_image = Image.open(BytesIO(image_data))
                    winner_image = winner_image.resize((100, 100), Image.BICUBIC)
                    winner_photo = ImageTk.PhotoImage(winner_image)
                    winner_image_label = tk.Label(self.master, image=winner_photo)
                    winner_image_label.image = winner_photo
                    winner_image_label.place(relx=0.37, rely=0.51, anchor=tk.CENTER)
            
            else:
                tk.Label(self.result_frame, text="No results found", font=("Arial", 12), bg="black", fg="white").pack(pady=5)

            connection.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to fetch results. Error: {e}")


    def create_pie_chart(self):
        try:
            connection = sqlite3.connect("Kenny.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT candidates.name, COUNT(results.candidate_pid) as vote_count
                FROM candidates
                JOIN results ON candidates.pid = results.candidate_pid
                GROUP BY candidates.pid
                ORDER BY vote_count DESC
            """)
            results = cursor.fetchall()

            # Extract candidate names and vote counts
            candidate_names = [row[0] for row in results]
            vote_counts = [row[1] for row in results]

            # Create a pie chart
            fig = Figure(figsize=(2, 2),  facecolor='black')
            ax = fig.add_subplot(111)
            patches, _, autotexts = ax.pie(vote_counts, autopct='%1.1f%%', startangle=140)
            ax.axis('equal') 
            for autotext in autotexts:
                autotext.set_fontsize(6)  # Set the font size to your desired value


            # Embed the plot into the tkinter window
            canvas = FigureCanvasTkAgg(fig, master=self.master)
            canvas.draw()

            # Place the canvas with the pie chart over the background image
            canvas.get_tk_widget().place(relx=0.72, rely=0.55, anchor=tk.CENTER)

            # Create and place the legend frame
            # Create and place the legend frame
            legend_frame = tk.Frame(self.master, bg='black', bd=1, relief=tk.SOLID)
            legend_frame.place(relx=0.68, rely=0.84, anchor=tk.CENTER)

            # Add legend labels with slice colors
            for name, patch in reversed(list(zip(candidate_names, patches))):
                color = patch.get_facecolor()
                legend_label = tk.Label(legend_frame, text=name, bg=rgb_to_hex(color))
                legend_label.pack(side=tk.LEFT, padx=5)


            connection.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to create pie chart. Error: {e}")

    def back_to_homepage(self):
        self.master.destroy()



class Reg_window4:
    def __init__(self, master, pid=None, roll=None):
        self.master = master
        self.pid = pid  # Store pid as an instance attribute
        self.roll = roll  # Store roll as an instance attribute
        self.master.title("Vote Others")
        self.master.geometry(f"{WIDTH}x{HEIGHT}")
        self.voted_candidates = set()
                # Set the initial window size
        width = 780
        height = 520

        # Set the geometry to center the window on the screen
        center_window(self.master, width, height)

        self.bg_image = Image.open("miniproject\\h.png")
        self.bg_image = self.bg_image.resize((WIDTH, HEIGHT), Image.BICUBIC)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.canvas = tk.Canvas(master, width=WIDTH, height=HEIGHT , borderwidth=0, highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_photo)
  

        # Hamburger icon setup
        self.menu_visible = False
        self.hamburger_icon = tk.Button(master, text="☰", font=("Arial", 12), command=self.toggle_menu, bg="#070B32", fg="white")
        self.hamburger_icon.place(relx=0.98, rely=0.09, anchor=tk.NE)

        # About Us and Help options setup
        self.about_us_button = tk.Button(master, text="About Us", command=self.open_about_us, bg="#070B32", fg="white")
        self.help_button = tk.Button(master, text="Help", command=self.open_help, bg="#070B32", fg="white")
        self.logout_button = tk.Button(master, text="Logout", command=self.logout, bg="#070B32", fg="white")
        


        self.about_us_window = None
        self.help_window = None

        # Adding images to buttons
        image1 = Image.open("miniproject\\1.png")
        image1 = image1.resize((170, 230), Image.BICUBIC)
        image1 = ImageTk.PhotoImage(image1)

        image2 = Image.open("miniproject\\2.jpeg")
        image2 = image2.resize((170, 230), Image.BICUBIC)
        image2 = ImageTk.PhotoImage(image2)

        image3 = Image.open("miniproject\\3.jpeg")
        image3 = image3.resize((170, 230), Image.BICUBIC)
        image3 = ImageTk.PhotoImage(image3)

        # Adding three buttons side by side with images
        self.button1 = tk.Button(master, text="Button 1", image=image1, command=self.button1_action)
        self.button2 = tk.Button(master, text="Button 2", image=image2, command=self.button2_action)
        self.button3 = tk.Button(master, text="Button 3", image=image3, command=self.button3_action)

        # Pack the buttons
        self.button1.place(x=500, y=200)
        self.button2.place(x=100, y=200)
        self.button3.place(x=300, y=200)

        # Store references to the images to prevent them from being garbage collected
        self.button1.image = image1
        self.button2.image = image2
        self.button3.image = image3
        
        # Marquee Text
        self.marquee_text = " Join the 2024 Student Council Elections and Vote For Your Favourite Candidate! " * 2
        self.marquee_label = tk.Label(master, text=self.marquee_text, font=("Arial", 12), bg="#000000", fg="white")
        self.marquee_label.pack(fill=tk.X, pady=5) 
        self.scroll_marquee()
        self.marquee_label.bind("<Button-1>", lambda event: self.button2_action())

    def scroll_marquee(self):
        self.marquee_label.place(x=self.marquee_label.winfo_x() - 1, y=self.marquee_label.winfo_y())
        if self.marquee_label.winfo_x() < -self.marquee_label.winfo_width():
            self.marquee_label.place(x=WIDTH, y=self.marquee_label.winfo_y())
        self.master.after(30, self.scroll_marquee)

    def toggle_menu(self):
        if self.menu_visible:
            self.about_us_button.place_forget()
            self.help_button.place_forget()
            self.logout_button.place_forget()
            self.menu_visible = False
        else:
            self.about_us_button.place(relx=0.98, rely=0.15, anchor=tk.NE)
            self.help_button.place(relx=0.98, rely=0.2, anchor=tk.NE)
            self.logout_button.place(relx=0.98, rely=0.25, anchor=tk.NE)
            self.menu_visible = True

    def open_about_us(self):
        if self.about_us_window is None:
            self.about_us_window = tk.Toplevel(self.master)
            self.about_us_window.title("About Us")
            
            # Calculate the center coordinates of the screen
            screen_width = self.about_us_window.winfo_screenwidth()
            screen_height = self.about_us_window.winfo_screenheight()
            x_coordinate = (screen_width - WIDTH) // 2
            y_coordinate = (screen_height - HEIGHT) // 2
            
            # Set the window geometry
            self.about_us_window.geometry(f"{WIDTH}x{HEIGHT}+{x_coordinate}+{y_coordinate}")

            self.about_us_window.protocol("WM_DELETE_WINDOW", self.close_about_us)
            # Add content to the About Us window
            # (Your existing code for adding content)

            # Add content to the About Us window
            scrollable_frame = ctk.CTkScrollableFrame(self.about_us_window, width=780,height=520)
            scrollable_frame.pack()
            text_label = ctk.CTkLabel(scrollable_frame, text="About CampusVoice :",font=ctk.CTkFont(size=24, weight="bold"))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="CampusVoice is an online platform tailored for college elections, facilitating student",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="participation from joining the ballot to casting votes for candidates.",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="",font=ctk.CTkFont(size=16, weight="bold"))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="About the Creators :",font=ctk.CTkFont(size=24, weight="bold"))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="This project is created by the students of St. Francis Institute of Technology studying in",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="Second Year of IT Department.",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="Our group members are: Charis Fernandes, Alton Fernandes, Kennice Gonsalves and",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="Jeslyn Gonsalves",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            add_button = ctk.CTkButton(scrollable_frame, text="Back",command=self.close_about_us, width=120)
            add_button.pack(anchor='w')

            root.mainloop()

    def close_about_us(self):
        if self.about_us_window is not None:
            self.about_us_window.destroy()
            self.about_us_window = None

    def open_help(self):
        if self.help_window is None:
            self.help_window = tk.Toplevel(self.master)
            self.help_window.title("Help")
            
            # Calculate the center coordinates of the screen
            screen_width = self.help_window.winfo_screenwidth()
            screen_height = self.help_window.winfo_screenheight()
            x_coordinate = (screen_width - WIDTH) // 2
            y_coordinate = (screen_height - HEIGHT) // 2
            
            # Set the window geometry
            self.help_window.geometry(f"{WIDTH}x{HEIGHT}+{x_coordinate}+{y_coordinate}")

            self.help_window.protocol("WM_DELETE_WINDOW", self.close_help)
            # Add content to the Help window
            # (Your existing code for adding content)


            # Create the scrollable frame and content
            scrollable_frame = ctk.CTkScrollableFrame(self.help_window, width=780, height=520)
            scrollable_frame.pack()
            text_label = ctk.CTkLabel(scrollable_frame, text="How do I become a Candidate?",font=ctk.CTkFont(size=24, weight="bold"))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="❖Click join ballot button on the home page",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="❖All your details will be displayed on the screen",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="❖Click on 'become a candidate button'",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="❖Now you are a candidate",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="How do I vote?",font=ctk.CTkFont(size=24, weight="bold"))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="❖Press vote others on the home page ",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="❖A scrollable UI will pop up displaying all the details of other candidates",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="❖Choose your favourite candidate ",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="Note: You can vote only once so choose wisely",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="How do I see the results?",font=ctk.CTkFont(size=24,weight="bold"))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="",font=ctk.CTkFont(size=24,weight="bold"))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="❖Click on results button on Home page",font=ctk.CTkFont(size=16))
            text_label.pack(anchor='w')
            text_label = ctk.CTkLabel(scrollable_frame, text="❖And now your personalised result will be displayed",font=ctk.CTkFont(size=16,))
            text_label.pack(anchor='w')
            add_button = ctk.CTkButton(scrollable_frame, text="Back",command=self.close_help, width=120)
            add_button.pack(anchor='w')

            root.mainloop()
            

    def logout(self):
        try:
            # Destroy the current window
            self.master.destroy()
            # Adjust the path to splash.py accordingly
            splash_path = r"C:\Users\Charis\Desktop\new beginings\miniproject\splash.py"
            Popen(["python", splash_path])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open splash.py: {e}")

            

    def close_help(self):
        if self.help_window is not None:
            self.help_window.destroy()
            self.help_window = None


    def button1_action(self):
        if self.pid and self.roll:  # Check if pid and roll are not None
            # Fetch user data
            user_data = fetch_user_data(self.pid, self.roll)

            if user_data:
                # Hide the current window
                self.master.withdraw()
                # Create profile window
                profile_window = tk.Toplevel(self.master)
                ProfileWindow(profile_window, self, user_data)
            else:
                tk.messagebox.showerror("Error", "User data not found.")
        else:
            tk.messagebox.showerror("Error", "PID and roll are not provided.")
            
            
    def button2_action(self):
        try:
            
            # Create the results table if it doesn't exist
            self.create_results_table()

            connection = sqlite3.connect("Kenny.db")
            cursor = connection.cursor()

            cursor.execute("SELECT name, pid, class_, branch, image FROM candidates")
            candidates = cursor.fetchall()
            width = 780
            height = 520
            # Create a new window for displaying candidate profiles
            candidate_window = tk.Toplevel(self.master)
            center_window(candidate_window, width, height)
            candidate_window.title("Candidate Profiles")
            candidate_window.geometry(f"{WIDTH}x{HEIGHT}")
                    # Set the initial window size


            # Set the geometry to center the window on the screen
            

            # Load the background image
            background_image = Image.open(r"miniproject\\Vote others (6).png")
            background_photo = ImageTk.PhotoImage(background_image)
            background_label = tk.Label(candidate_window, image=background_photo)
            background_label.image = background_photo
            background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Ensure the background covers the entire window

            # Create a frame to contain the candidate profiles
            frame = tk.Frame(candidate_window, bg="black")  # Set the background color here
            frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

            # Create a canvas for scrolling
            canvas = tk.Canvas(frame, bg="black", highlightthickness=0)  # Set the canvas background color
            canvas.pack(side="left", fill="both", expand=True)

            # Add a scrollbar to the canvas
            scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview, bg="black", troughcolor="blue")
            scrollbar.pack(side="right", fill="y", padx=(210, 0), pady=10)
            canvas.configure(yscrollcommand=scrollbar.set)

            # Create another frame inside the canvas to contain the candidate profiles
            inner_frame = tk.Frame(canvas, bg="black")  # Set the inner frame background color
            canvas.create_window((0, 0), window=inner_frame, anchor="nw")

            # Display candidate profiles in the UI
            for candidate in candidates:
                name, pid, class_, branch, image_data = candidate

                # Create a frame for each candidate profile
                profile_frame = tk.Frame(inner_frame, bg="black")
                profile_frame.pack(fill=tk.X, padx=5, pady=10)

                # Display candidate information
                if image_data:
                    image = Image.open(BytesIO(image_data))
                    image.thumbnail((100, 100))
                    photo = ImageTk.PhotoImage(image)
                    image_label = tk.Label(profile_frame, image=photo, bg="black")
                    image_label.image = photo
                    image_label.pack(side=tk.LEFT, padx=10)
                else:
                    image_label = tk.Label(profile_frame, text="No Image", font=("Arial", 10), foreground="gray", fg="white", bg="black")
                    image_label.pack(side=tk.LEFT, padx=10)

                tk.Label(profile_frame, text=f"Name: {name}\nPID: {pid}\nClass: {class_}\nBranch: {branch}", font=("Arial", 10), fg="white", bg="black").pack(side=tk.LEFT)

                # Add vote button for each candidate
                if pid not in self.voted_candidates:  # Check if the user has not voted for this candidate
                    vote_button =ctk.CTkButton(profile_frame, text="Vote", command=lambda p=pid: self.vote_candidate(p), bg_color="black")
                    vote_button.pack(side=tk.RIGHT)
                else:
                    vote_button = ctk.CTkButton(profile_frame, text="Voted", state=tk.DISABLED, bg_color="black")
                    vote_button.pack(side=tk.RIGHT)

            # Update the scroll region
            inner_frame.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))

            connection.close()
            
                    # Add back button
            back_button = ctk.CTkButton(candidate_window, text="back", bg_color="black",  command=candidate_window.destroy)
            back_button.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to fetch candidate profiles. Error: {e}")



    def vote_candidate(self, candidate_pid):
        try:
            connection = sqlite3.connect("Kenny.db")
            cursor = connection.cursor()

            # Check if the user has already voted for any candidate
            cursor.execute("SELECT COUNT(*) FROM results WHERE user_pid=?", (self.pid,))
            vote_count = cursor.fetchone()[0]

            if vote_count > 0:
                messagebox.showinfo("Information", "You have already voted for a candidate.")
            else:
                # Insert the vote into the results table
                cursor.execute("INSERT INTO results (user_pid, candidate_pid) VALUES (?, ?)", (self.pid, candidate_pid))
                connection.commit()
                messagebox.showinfo("Success", "Vote registered successfully!")
                self.voted_candidates.add(candidate_pid)  # Add the voted candidate to the set

            connection.close()

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to vote. Error: {e}")

    def create_results_table(self):
        try:
            connection = sqlite3.connect("Kenny.db")
            cursor = connection.cursor()

            cursor.execute('''CREATE TABLE IF NOT EXISTS results (
                                user_pid TEXT,
                                candidate_pid TEXT,
                                UNIQUE(user_pid, candidate_pid)
                            )''')

            connection.commit()
            connection.close()
            

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to create results table. Error: {e}")
            
    def back_to_homepage(self):
        self.master.deiconify()


    def button3_action(self):
        results_window = tk.Toplevel(self.master)
        results_page = ResultsPage(results_window)
        print("Button 3 clicked")
        

    




# Print the number of command-line arguments
print("Number of command-line arguments:", len(sys.argv))

# Print the command-line arguments themselves
print("Command-line arguments:", sys.argv)

# Check if PID and roll arguments are provided
if len(sys.argv) >= 3:
    pid = sys.argv[1]
    roll = sys.argv[2]
    print("PID:", pid)
    print("Roll:", roll)
else:
    print("PID and roll are missing.")
    sys.exit()
    

# Fetch voter data for the current user
def fetch_user_data(pid, roll):
    try:
        connection = sqlite3.connect("Kenny.db")
        cursor = connection.cursor()

        # Fetch data for the current user based on PID and roll
        cursor.execute("SELECT name, pid, class_, branch, image FROM voters WHERE pid=? AND roll=?", (pid, roll))
        user_data = cursor.fetchone()

        connection.close()

        return user_data

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None


# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = Reg_window4(root, pid, roll)
    root.mainloop()