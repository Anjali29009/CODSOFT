import tkinter as tk
from tkinter import messagebox
import os

# Define the filename for storing tasks
TASKS_FILE = "tasks.txt"

def load_tasks():
    """Load tasks from file, returning a list of task dictionaries"""
    tasks = []
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as file:
            for line in file:
                line = line.strip()
                if line:  # Skip empty lines
                    # Tasks are stored as [x] or [ ] followed by description
                    completed = line.startswith('[x]')
                    tasks.append({
                        'text': line[4:],  # Remove the [x]/[ ] prefix
                        'completed': completed
                    })
    return tasks

def save_tasks(tasks):
    """Save tasks to file with completion status"""
    with open(TASKS_FILE, "w") as file:
        for task in tasks:
            prefix = "[x]" if task['completed'] else "[ ]"
            file.write(f"{prefix}{task['text']}\n")

class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List")
        master.geometry("500x600")
        master.resizable(False, False)
        master.configure(bg="#F0F0F0")
        
        # Load existing tasks
        self.tasks = load_tasks()
        
        # Create UI elements
        self.create_widgets()
        self.update_task_listbox()

    def create_widgets(self):
        """Create and layout all UI components"""
        # Title Label
        title_font = ("Helvetica", 24, "bold")
        tk.Label(self.master, text="To-Do List", font=title_font,
                 bg="#F0F0F0", fg="#333333").pack(pady=20)

        # Input Frame
        input_frame = tk.Frame(self.master, bg="#F0F0F0")
        input_frame.pack(padx=10)

        self.task_entry = tk.Entry(input_frame, width=40, font=("Helvetica", 12))
        self.task_entry.pack(side=tk.LEFT, padx=5)
        
        add_button = tk.Button(input_frame, text="Add", command=self.add_task,
                              bg="#4CAF50", fg="white", font=("Helvetica", 10, "bold"))
        add_button.pack(side=tk.LEFT)
        
        # Bind Enter key to add task
        self.task_entry.bind("<Return>", lambda e: self.add_task())

        # Task List Frame
        list_frame = tk.Frame(self.master)
        list_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.task_listbox = tk.Listbox(
            list_frame, 
            width=50, 
            height=15, 
            font=("Helvetica", 12),
            selectbackground="#a6d4ff"
        )
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_listbox.pack(fill=tk.BOTH, expand=True)
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Button Frame
        button_frame = tk.Frame(self.master, bg="#F0F0F0")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Toggle Complete", 
                 command=self.toggle_complete).pack(side=tk.LEFT, padx=5)
        
        tk.Button(button_frame, text="Delete Task", 
                 command=self.delete_task).pack(side=tk.LEFT, padx=5)

    def update_task_listbox(self):
        """Refresh the task display list"""
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✓ " if task['completed'] else "   "
            text = f"{status}{task['text']}"
            self.task_listbox.insert(tk.END, text)
            
            # Style completed tasks differently
            if task['completed']:
                self.task_listbox.itemconfig(tk.END, {'fg': '#888888'}) #Grey out completed tasks  
                #Ensure incomplete tasks are black

    def add_task(self):
        """Add a new task to the list"""
        text = self.task_entry.get().strip()
        if text:
            self.tasks.append({'text': text, 'completed': False})
            save_tasks(self.tasks)
            self.task_entry.delete(0, tk.END) #clear the entry field
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "Please enter a task description")

    def toggle_complete(self):
        """Toggle completion status of selected task"""
        try:
            index = self.task_listbox.curselection()[0] #Get index of selected item
            self.tasks[index]['completed'] = not self.tasks[index]['completed']
            save_tasks(self.tasks)
            self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task first")

    def delete_task(self):
        """Remove selected task from list"""
        try:
            index = self.task_listbox.curselection()[0]
            #Ask for confirmation before deleting
            if messagebox.askyesno("Confirm", "Delete this task?"):
                del self.tasks[index]
                save_tasks(self.tasks)
                self.update_task_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task first")
#Entry point for the Tkinter appliation
if __name__ == "__main__":
    root = tk.Tk() #Create the main Window
    app = TodoApp(root) #Create an instance of our To-DO app
    root.mainloop() #starts the tkinter event loop

