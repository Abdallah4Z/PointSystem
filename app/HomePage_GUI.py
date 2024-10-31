import customtkinter as ctk
import History_GUI
import PointsTable_GUI
import Score_GUI
import fileEd 
import Username_GUI
from fileEd import username as u
from DataBase import db as database

class HomePage(ctk.CTk):
    def __init__(self, username):
        super().__init__()
        self.geometry("500x500")
        self.title("Home Page")

        self.username = username
        db = database.DatabaseHandler()
        phases = db.get_all_phases_data()
        rows_data = []
        for phase in phases:
            if phase[1] == username:
                phasee = (phase[3])
                rows_data.append(phasee)
        if rows_data: 
            average = sum(rows_data) / len(rows_data) 

        print("Average:", average)
        db.close()        

        
        header = ctk.CTkLabel(self, text=f"Welcome, {self.username}", font=("Arial", 24))
        header.pack(pady=20)

        
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=20)

        new_point_button = ctk.CTkButton(button_frame, text="Create New Point View", command=self.open_new_point_view)
        new_point_button.grid(row=0, column=0, padx=10, pady=10)

        history_button = ctk.CTkButton(button_frame, text="View History", command=self.open_history)
        history_button.grid(row=0, column=1, padx=10, pady=10)

        points_button = ctk.CTkButton(button_frame, text="View Points from Others", command=self.open_points_from_others)
        points_button.grid(row=0, column=2, padx=10, pady=10)

    
        canvas = ctk.CTkCanvas(self, width=200, height=200, bg="lightblue", highlightthickness=0)
        canvas.pack(pady=20)
        canvas.create_oval(50, 50, 150, 150, outline="gray", width=4)
        canvas.create_text(100, 100, text=f"{average*10}", font=("Arial", 32), fill="black")

        note_label = ctk.CTkLabel(self, text="Progress towards goal", font=("Arial", 14))
        note_label.pack(pady=10)

  
    def open_new_point_view(self):
        mem = ["Abdallah", "Ahmed", "Belal", "Eyad", "Mahmoud", "Mazen"]
        mem = [i for i in mem if i.lower() != username.lower()]
        db = database.DatabaseHandler()
        t = db.get_tasks_name()
        db.close()
        PointsTable_GUI.TaskTable(mem, t, username)

    def open_history(self):
        db = database.DatabaseHandler()
        phases = db.get_all_phases_data()
        rows_data = []
        for phase in phases:
            if phase[1] == username:
                phasee = (phase[2], phase[0])
                rows_data.append(phasee)

        tasks = db.get_all_records()
        tasks_data = []
        for i in range(1, len(rows_data)+1):
            tt  = []
            for task in tasks:
                if task[6] == i and task[1] == username:
                    tt.append((task[3] +" - "+task[2], task[4]))    
            tasks_data.append(tt)  

        print(tasks_data)           
        db.close()                   
        History_GUI.HistoryPanel(rows_data, tasks_data)

    def open_points_from_others(self):
        db = database.DatabaseHandler()
        phases = db.get_all_phases_data()
        rows_data = []
        for phase in phases:
            if phase[1] == username:
                phasee = (phase[2], phase[0], phase[3])
                rows_data.append(phasee)

        tasks = db.get_all_records()
        tasks_data = []
        for i in range(1, len(rows_data)+1):
            tt  = []
            for task in tasks:
                if task[6] == i and task[2] == username:
                    tt.append((task[3], task[4])) 
            tasks_data.append(tt)  

        print(tasks_data)           
        db.close()                   
        Score_GUI.PointsFromOthersPanel(rows_data, tasks_data)

if __name__ == "__main__":
    username = u()
    if username == "user":
        Username_GUI.UsernameEntryApp().mainloop()

    username = u()
    app = HomePage(username)
    app.mainloop()
