import customtkinter as ctk

class PointsFromOthersPanel(ctk.CTkToplevel):
    row_data = []
    task_data = []
    def __init__(self, rd, td):
        super().__init__()
        global rows_data, task_data
        rows_data = rd
        task_data = td
        self.geometry("500x600")
        self.resizable(False, False)
        self.title("My Score")

        self.label = ctk.CTkLabel(self, text="Main Table", font=("Arial", 24))
        self.label.pack(pady=20)

        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.pack(pady=10, fill="both", expand=True)

        
        self.display_main_table()

    def display_main_table(self):
        global rows_data, task_data
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        headers_frame = ctk.CTkFrame(self.table_frame)
        headers_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        headers = ["Date", "Phase", "Score", "Action"]
        for i, header_text in enumerate(headers):
            header_label = ctk.CTkLabel(headers_frame, text=header_text, font=("Arial", 12, "bold"))
            header_label.grid(row=0, column=i, sticky="nsew", padx=5)
            headers_frame.grid_columnconfigure(i, weight=1)
        for row_data in rows_data:
            row_frame = ctk.CTkFrame(self.table_frame, corner_radius=5)
            row_frame.pack(fill="x", padx=10, pady=5)

            for i, item in enumerate(row_data):
                label = ctk.CTkLabel(row_frame, text=item, font=("Arial", 12), anchor="center")
                label.grid(row=0, column=i, sticky="nsew", padx=5)
                row_frame.grid_columnconfigure(i, weight=1) 
            action_button = ctk.CTkButton(
                row_frame, 
                text="View Phase", 
                command=lambda data=row_data: self.display_detail_table(row_data, task_data[rows_data.index(row_data)])
            )
            action_button.grid(row=0, column=3, sticky="nsew", padx=0)

            row_frame.grid_columnconfigure(3, weight=1)


    def display_detail_table(self, row_data, td):       
        self.clear_screen()

        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(1, weight=1)
        self.table_frame.grid_rowconfigure(0, weight=1)

        self.table_frame.grid_columnconfigure(0, minsize=200)
        self.table_frame.grid_columnconfigure(1, minsize=200)

        detail_label = ctk.CTkLabel(self.table_frame, text=f"Details for {row_data[1]}", font=("Arial", 18))
        detail_label.grid(row=0, column=0, columnspan=2, pady=(10, 20), sticky="nsew")
        task_data = td
        
        header_task = ctk.CTkLabel(self.table_frame, text="Task", font=("Arial", 14, "bold"))
        header_task.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        header_grade = ctk.CTkLabel(self.table_frame, text="Grade", font=("Arial", 14, "bold"))
        header_grade.grid(row=1, column=1, padx=10, pady=5, sticky="nsew")

        total = 0
        for i, (task, grade) in enumerate(task_data, start=2): 
            task_label = ctk.CTkLabel(self.table_frame, text=task, font=("Arial", 12))
            task_label.grid(row=i, column=0, padx=10, pady=5, sticky="nsew")
            
            grade_label = ctk.CTkLabel(self.table_frame, text=str(grade), font=("Arial", 12))
            grade_label.grid(row=i, column=1, padx=10, pady=5, sticky="nsew")
            
            total += grade

        average = total / len(task_data)

        total_label = ctk.CTkLabel(self.table_frame, text="Total", font=("Arial", 14, "bold"))
        total_label.grid(row=len(task_data) + 2, column=0, padx=10, pady=5, sticky="nsew")

        average_label = ctk.CTkLabel(self.table_frame, text=f"{total} / Avg: {average:.2f}", font=("Arial", 14, "bold"))
        average_label.grid(row=len(task_data) + 2, column=1, padx=10, pady=5, sticky="nsew")


        back_button = ctk.CTkButton(self.table_frame, text="Back", command=self.display_main_table)
        back_button.grid(row=len(task_data) + 3, column=0, columnspan=2, pady=20, sticky="nsew")
    def clear_screen(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton) and widget.cget("text") == "Back":
                widget.pack_forget()


