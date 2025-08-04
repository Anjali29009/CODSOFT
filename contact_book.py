import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class ContactBook:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Book")
        self.root.geometry("400x600")
        self.root.config(bg="#f5f5f5")
        
        self.contacts_file = "contacts.json"
        self.load_contacts()
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root, 
            text="Contact Book", 
            font=("Helvetica", 18, "bold"), 
            bg="#f5f5f5"
        )
        title_label.pack(pady=10)

        # Input fields
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.address_var = tk.StringVar()

        input_frame = tk.Frame(self.root, bg="#f5f5f5")
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Name:", bg="#f5f5f5").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.name_var).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Phone:", bg="#f5f5f5").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.phone_var).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Email:", bg="#f5f5f5").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.email_var).grid(row=2, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Address:", bg="#f5f5f5").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(input_frame, textvariable=self.address_var).grid(row=3, column=1, padx=5, pady=5)

        # Buttons
        button_frame = tk.Frame(self.root, bg="#f5f5f5")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Contact", command=self.add_contact).pack(side="left", padx=5)
        tk.Button(button_frame, text="View Contacts", command=self.view_contacts).pack(side="left", padx=5)
        tk.Button(button_frame, text="Search Contact", command=self.search_contact).pack(side="left", padx=5)
        tk.Button(button_frame, text="Update Contact", command=self.update_contact).pack(side="left", padx=5)
        tk.Button(button_frame, text="Delete Contact", command=self.delete_contact).pack(side="left", padx=5)

        # Contact List
        self.contact_listbox = tk.Listbox(self.root, width=50)
        self.contact_listbox.pack(pady=10)

    def load_contacts(self):
        if os.path.exists(self.contacts_file):
            with open(self.contacts_file, "r") as f:
                self.contacts = json.load(f)
        else:
            self.contacts = []

    def save_contacts(self):
        with open(self.contacts_file, "w") as f:
            json.dump(self.contacts, f, indent=2)

    def add_contact(self):
        name = self.name_var.get()
        phone = self.phone_var.get()
        email = self.email_var.get()
        address = self.address_var.get()

        if not name or not phone:
            messagebox.showerror("Error", "Name and Phone are required fields.")
            return

        contact = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }
        self.contacts.append(contact)
        self.save_contacts()
        messagebox.showinfo("Success", "Contact added successfully!")
        self.clear_fields()

    def view_contacts(self):
        self.contact_listbox.delete(0, tk.END)
        for contact in self.contacts:
            self.contact_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def search_contact(self):
        search_term = self.name_var.get() or self.phone_var.get()
        if not search_term:
            messagebox.showerror("Error", "Please enter a name or phone number to search.")
            return

        found_contacts = [c for c in self.contacts if search_term in (c['name'], c['phone'])]
        self.contact_listbox.delete(0, tk.END)
        for contact in found_contacts:
            self.contact_listbox.insert(tk.END, f"{contact['name']} - {contact['phone']}")

    def update_contact(self):
        selected_index = self.contact_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a contact to update.")
            return

        contact = self.contacts[selected_index[0]]
        contact['name'] = self.name_var.get() or contact['name']
        contact['phone'] = self.phone_var.get() or contact['phone']
        contact['email'] = self.email_var.get() or contact['email']
        contact['address'] = self.address_var.get() or contact['address']

        self.save_contacts()
        messagebox.showinfo("Success", "Contact updated successfully!")
        self.clear_fields()
        self.view_contacts()

    def delete_contact(self):
        selected_index = self.contact_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Error", "Please select a contact to delete.")
            return

        del self.contacts[selected_index[0]]
        self.save_contacts()
        messagebox.showinfo("Success", "Contact deleted successfully!")
        self.view_contacts()

    def clear_fields(self):
        self.name_var.set("")
        self.phone_var.set("")
        self.email_var.set("")
        self.address_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactBook(root)
    root.mainloop()
