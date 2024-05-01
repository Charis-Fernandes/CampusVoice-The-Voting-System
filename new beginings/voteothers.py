import tkinter as tk
from tkinter import messagebox
import sqlite3
import sys

WIDTH = 780
HEIGHT = 520

class VoteOthersWindow:
    def __init__(self, master, user_pid):
        self.master = master
        self.user_pid = user_pid
        self.master.title("Vote Others")
        self.master.geometry(f"{WIDTH}x{HEIGHT}")

        self.scrollable_frame = tk.Frame(master)
        self.scrollable_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.scrollable_frame)
        self.scrollbar = tk.Scrollbar(self.scrollable_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)

        self.frame = tk.Frame(self.canvas)

        self.canvas.create_window((0, 0), window=self.frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.load_candidates()

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def on_canvas_configure(self, event):
        self.canvas.itemconfig(self.scrollable_frame, width=event.width)

    def load_candidates(self):
        try:
            connection = sqlite3.connect("Kenny.db")
            cursor = connection.cursor()

            cursor.execute("SELECT name, pid FROM candidates")
            candidates = cursor.fetchall()

            for candidate in candidates:
                name, pid = candidate
                if pid == self.user_pid:
                    continue  # Skip the current user from the list of candidates

                frame = tk.Frame(self.frame)
                frame.pack(fill=tk.X, padx=10, pady=10)

                tk.Label(frame, text=name).pack(side=tk.LEFT)
                vote_button = tk.Button(frame, text="Vote", command=lambda p=pid: self.vote(p))
                vote_button.pack(side=tk.RIGHT)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to load candidates. Error: {e}")

    def vote(self, candidate_pid):
        try:
            connection = sqlite3.connect("Kenny.db")
            cursor = connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM votes WHERE user_pid=?", (self.user_pid,))
            vote_count = cursor.fetchone()[0]

            if vote_count > 0:
                messagebox.showinfo("Information", "You have already voted.")
                return

            cursor.execute("INSERT INTO votes (user_pid, candidate_pid) VALUES (?, ?)", (self.user_pid, candidate_pid))
            connection.commit()
            connection.close()

            messagebox.showinfo("Success", "Vote registered successfully!")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Failed to vote. Error: {e}")


def main():
    # Fetch user's PID from command line arguments
    if len(sys.argv) >= 2:
        user_pid = sys.argv[1]
    else:
        print("User PID is missing.")
        return

    root = tk.Tk()
    app = VoteOthersWindow(root, user_pid)
    root.mainloop()


if __name__ == "__main__":
    main()
