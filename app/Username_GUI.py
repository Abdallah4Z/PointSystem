import customtkinter as ctk
import fileEd
from fileEd import update_username as uu

class UsernameEntryApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("300x200")
        self.title("Enter Username")

        self.label = ctk.CTkLabel(self, text="Please enter your username:")
        self.label.pack(pady=10)

        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack(pady=10)

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_username)
        self.submit_button.pack(pady=10)

        self.result_label = ctk.CTkLabel(self, text="")
        self.result_label.pack(pady=10)

    def submit_username(self):
        username = self.username_entry.get()
        if username:
            uu(username)
            self.destroy()
