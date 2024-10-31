import customtkinter as ctk
from datetime import datetime 
from DataBase import db as database

class TaskTable(ctk.CTkToplevel):
    username = ""

    def __init__(self, members, tasks, use):
        super().__init__()
        global username 
        username = use
        self.geometry("750x500")
        self.title("Task Table")

        self.member_names = members
        self.tasks = tasks
        self.table_entries = {}

        # Phase Number Entry at the Top
        ctk.CTkLabel(self, text="Phase Number:").grid(row=0, column=0, padx=10, pady=5)
        self.phase_entry = ctk.CTkEntry(self, width=100)
        self.phase_entry.grid(row=0, column=1, columnspan=len(self.member_names), padx=10, pady=5)

        # Header row
        ctk.CTkLabel(self, text="Task Name").grid(row=1, column=0, padx=10, pady=5)
        for col, member in enumerate(self.member_names, start=1):
            ctk.CTkLabel(self, text=member).grid(row=1, column=col, padx=10, pady=5)
        ctk.CTkLabel(self, text="Notes").grid(row=1, column=len(self.member_names) + 1, padx=10, pady=5)

        for row, task in enumerate(self.tasks, start=2):
            ctk.CTkLabel(self, text=task).grid(row=row, column=0, padx=10, pady=5)
            
            self.table_entries[row] = {}
            for col in range(1, len(self.member_names) + 1):
                entry = ctk.CTkEntry(self, width=50)
                entry.grid(row=row, column=col, padx=10, pady=5)
                entry.bind("<KeyRelease>", lambda event, r=row, c=col: self.calculate_totals())
                self.table_entries[row][col] = entry
            
            notes_entry = ctk.CTkEntry(self, width=150)
            notes_entry.grid(row=row, column=len(self.member_names) + 1, padx=10, pady=5)
            self.table_entries[row]["notes"] = notes_entry

        # Total row
        ctk.CTkLabel(self, text="Total").grid(row=len(self.tasks) + 2, column=0, padx=10, pady=5)
        self.total_labels = {}
        for col in range(1, len(self.member_names) + 1):
            total_label = ctk.CTkLabel(self, text="0")
            total_label.grid(row=len(self.tasks) + 2, column=col, padx=10, pady=5)
            self.total_labels[col] = total_label

        submit_button = ctk.CTkButton(self, text="Submit", command=self.on_submit)
        submit_button.grid(row=len(self.tasks) + 3, column=0, columnspan=len(self.member_names) + 2, pady=10)
        self.notes_label = ctk.CTkLabel(self, text="* Please enter scores between 0 and 10. \n dont forget to fill phase number (1, 2, 3, etc..)")
        self.notes_label.grid(row=len(self.tasks) + 4, column=0, columnspan=len(self.member_names) + 2, pady=10)

    def calculate_totals(self):
        for col in range(1, len(self.member_names) + 1):
            total = 0
            for row in range(2, len(self.tasks) + 2):  # Starts from row 2 for tasks
                entry = self.table_entries.get(row, {}).get(col)
                if entry:
                    try:
                        score = int(entry.get() or 0)
                    except ValueError:
                        score = 0  # Handle non-integer input gracefully
                    total += score
            self.total_labels[col].configure(text=str(total))

    def on_submit(self):
        global username
        names = ["Abdallah", "Ahmed", "Belal", "Eyad", "Mahmoud", "Mazen"]
        names = [i for i in names if i.lower() != username.lower()]
        
        table_data = []
        for row in range(2, len(self.tasks) + 2): 
            task_data = []
            for col in range(1, len(self.member_names) + 1):
                value = self.table_entries[row][col].get()
                try:
                    grade = float(value)  

                except ValueError:
                    grade = 0  # Default to 0 if conversion fails
                task_data.append(grade)
            notes = self.table_entries[row]["notes"].get()
            task_data.append(notes)
            table_data.append(task_data)

        current_date = datetime.now()
        formatted_date = current_date.strftime("%d-%m-%Y")
        
        db = database.DatabaseHandler()
        t = db.get_tasks_name()
        
        for i in range(len(t)):
            for jj in range(len(self.member_names)):
                grade = table_data[i][jj]  
                note = table_data[i][-1] 
                task = str(t[i])   
                
                print(f"Inserting into DB: username={username}, member={self.member_names[jj]}, task={t[i]}, grade={grade}, phase={self.phase_entry.get()}, date={formatted_date}, note={note}")
                db.add_record(username, self.member_names[jj], task, grade, self.phase_entry.get(), formatted_date, note)
        
        db.close()
        self.clear_table()


    def clear_table(self):
        for row in range(2, len(self.tasks) + 2):  
            for col in range(1, len(self.member_names) + 1):
                self.table_entries[row][col].delete(0, "end")
            self.table_entries[row]["notes"].delete(0, "end")
        for col in self.total_labels:
            self.total_labels[col].configure(text="0")
