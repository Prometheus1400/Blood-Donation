import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

class BloodDonationSystem:
    DATA_FILE = "donors.json"
    
    def __init__(self, root):
        self.root = root
        self.root.title("Blood Donation Management System")
        self.root.geometry("600x400")
        
        # Load existing data
        self.donors = self.load_data()
        self.appointments = []
        
        # Create main frames
        self.main_frame = tk.Frame(self.root, padx=20, pady=20)
        self.main_frame.pack(fill="both", expand=True)
        
        # Welcome label
        welcome = tk.Label(
            self.main_frame, 
            text="Blood Donation Management System",
            font=("Helvetica", 16, "bold")
        )
        welcome.pack(pady=10)
        
        # Stats frame
        stats_frame = tk.LabelFrame(self.main_frame, text="Statistics", padx=10, pady=10)
        stats_frame.pack(fill="x", pady=10)
        
        self.stats_label = tk.Label(stats_frame, text=self.get_stats_text())
        self.stats_label.pack()
        
        # Button frame
        btn_frame = tk.Frame(self.main_frame)
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Register Donor", command=self.donor_registration, width=20).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Schedule Appointment", command=self.schedule_appointment, width=20).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="View Donors", command=self.view_donor_info, width=20).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Search Donors", command=self.search_donors, width=20).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(btn_frame, text="Blood Availability", command=self.view_blood_availability, width=20).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(btn_frame, text="Save & Exit", command=self.save_and_exit, width=20, bg="#ff6b6b").grid(row=2, column=1, padx=5, pady=5)
    
    def load_data(self):
        """Load donors from JSON file."""
        if os.path.exists(self.DATA_FILE):
            try:
                with open(self.DATA_FILE, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def save_data(self):
        """Save donors to JSON file."""
        with open(self.DATA_FILE, 'w') as f:
            json.dump(self.donors, f, indent=2)
    
    def get_stats_text(self):
        """Get summary statistics."""
        total = len(self.donors)
        return f"Total Donors: {total}"
    
    def update_stats(self):
        """Update the stats display."""
        self.stats_label.config(text=self.get_stats_text())
    
    def donor_registration(self):
        """Open donor registration form."""
        form = tk.Toplevel(self.root)
        form.title("Donor Registration")
        form.geometry("300x250")
        form.transient(self.root)
        form.grab_set()
        
        tk.Label(form, text="Name:").pack(anchor="w", padx=10, pady=(10, 0))
        name_entry = tk.Entry(form, width=30)
        name_entry.pack(fill="x", padx=10)
        
        tk.Label(form, text="Email:").pack(anchor="w", padx=10, pady=(10, 0))
        email_entry = tk.Entry(form, width=30)
        email_entry.pack(fill="x", padx=10)
        
        tk.Label(form, text="Phone:").pack(anchor="w", padx=10, pady=(10, 0))
        phone_entry = tk.Entry(form, width=30)
        phone_entry.pack(fill="x", padx=10)
        
        tk.Label(form, text="Blood Type:").pack(anchor="w", padx=10, pady=(10, 0))
        blood_var = tk.StringVar(value="O+")
        blood_combo = ttk.Combobox(form, textvariable=blood_var, values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], state="readonly", width=27)
        blood_combo.pack(fill="x", padx=10)
        
        def submit():
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            blood_type = blood_var.get()
            
            if not all([name, email, phone]):
                messagebox.showerror("Error", "Please fill out all fields", parent=form)
                return
            
            donor = {
                "id": len(self.donors) + 1,
                "name": name,
                "email": email,
                "phone": phone,
                "blood_type": blood_type,
                "registered_at": datetime.now().isoformat(),
                "donations": []
            }
            
            self.donors.append(donor)
            self.save_data()
            self.update_stats()
            
            messagebox.showinfo("Success", f"Donor {name} registered successfully!", parent=form)
            form.destroy()
        
        tk.Button(form, text="Submit", command=submit, bg="#4CAF50", fg="white").pack(pady=20)
    
    def schedule_appointment(self):
        """Open appointment scheduling form."""
        if not self.donors:
            messagebox.showinfo("Info", "No donors registered yet. Please register a donor first.")
            return
        
        form = tk.Toplevel(self.root)
        form.title("Schedule Appointment")
        form.geometry("300x300")
        form.transient(self.root)
        form.grab_set()
        
        tk.Label(form, text="Select Donor:").pack(anchor="w", padx=10, pady=(10, 0))
        donor_names = [f"{d['id']}: {d['name']} ({d['blood_type']})" for d in self.donors]
        donor_var = tk.StringVar()
        donor_combo = ttk.Combobox(form, textvariable=donor_var, values=donor_names, state="readonly", width=30)
        donor_combo.pack(fill="x", padx=10)
        
        tk.Label(form, text="Date (YYYY-MM-DD):").pack(anchor="w", padx=10, pady=(10, 0))
        date_entry = tk.Entry(form, width=30)
        date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        date_entry.pack(fill="x", padx=10)
        
        tk.Label(form, text="Time:").pack(anchor="w", padx=10, pady=(10, 0))
        time_var = tk.StringVar(value="09:00")
        time_combo = ttk.Combobox(form, textvariable=time_var, values=["09:00", "10:00", "11:00", "13:00", "14:00", "15:00"], state="readonly", width=27)
        time_combo.pack(fill="x", padx=10)
        
        tk.Label(form, text="Location:").pack(anchor="w", padx=10, pady=(10, 0))
        location_entry = tk.Entry(form, width=30)
        location_entry.insert(0, "Main Blood Bank")
        location_entry.pack(fill="x", padx=10)
        
        def submit():
            if not donor_var.get():
                messagebox.showerror("Error", "Please select a donor", parent=form)
                return
            
            donor_id = int(donor_var.get().split(":")[0])
            date = date_entry.get().strip()
            time = time_var.get()
            location = location_entry.get().strip()
            
            if not all([date, location]):
                messagebox.showerror("Error", "Please fill out all fields", parent=form)
                return
            
            # Find donor and add appointment
            for donor in self.donors:
                if donor["id"] == donor_id:
                    appointment = {
                        "date": date,
                        "time": time,
                        "location": location,
                        "scheduled_at": datetime.now().isoformat()
                    }
                    donor["donations"].append(appointment)
                    break
            
            self.save_data()
            messagebox.showinfo("Success", "Appointment scheduled successfully!", parent=form)
            form.destroy()
        
        tk.Button(form, text="Schedule", command=submit, bg="#4CAF50", fg="white").pack(pady=20)
    
    def view_donor_info(self):
        """Display all donors in a list view."""
        if not self.donors:
            messagebox.showinfo("Info", "No donors registered yet.")
            return
        
        view = tk.Toplevel(self.root)
        view.title("Donor Information")
        view.geometry("500x300")
        view.transient(self.root)
        
        # Create treeview
        columns = ("ID", "Name", "Blood Type", "Email", "Donations")
        tree = ttk.Treeview(view, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=80 if col != "Name" and col != "Email" else 120)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(view, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Populate data
        for donor in self.donors:
            tree.insert("", "end", values=(
                donor["id"],
                donor["name"],
                donor["blood_type"],
                donor["email"],
                len(donor.get("donations", []))
            ))
        
        tk.Button(view, text="Close", command=view.destroy).pack(pady=10)
    
    def search_donors(self):
        """Search donors by name or blood type."""
        if not self.donors:
            messagebox.showinfo("Info", "No donors registered yet.")
            return
        
        form = tk.Toplevel(self.root)
        form.title("Search Donors")
        form.geometry("400x300")
        form.transient(self.root)
        form.grab_set()
        
        tk.Label(form, text="Search by name or blood type:").pack(anchor="w", padx=10, pady=(10, 0))
        search_entry = tk.Entry(form, width=40)
        search_entry.pack(fill="x", padx=10)
        
        # Results frame
        result_frame = tk.Frame(form)
        result_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("Name", "Blood Type", "Phone")
        tree = ttk.Treeview(result_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        
        scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)
        
        def do_search():
            query = search_entry.get().lower()
            
            # Clear existing results
            for item in tree.get_children():
                tree.delete(item)
            
            # Search
            for donor in self.donors:
                if query in donor["name"].lower() or query in donor["blood_type"].lower():
                    tree.insert("", "end", values=(
                        donor["name"],
                        donor["blood_type"],
                        donor["phone"]
                    ))
            
            if not tree.get_children():
                messagebox.showinfo("No Results", "No donors found matching your search.", parent=form)
        
        tk.Button(form, text="Search", command=do_search, bg="#2196F3", fg="white").pack(pady=5)
        search_entry.bind("<Return>", lambda e: do_search())
        
        # Initial population
        for donor in self.donors:
            tree.insert("", "end", values=(
                donor["name"],
                donor["blood_type"],
                donor["phone"]
            ))
    
    def view_blood_availability(self):
        """Show blood type inventory."""
        view = tk.Toplevel(self.root)
        view.title("Blood Availability")
        view.geometry("300x250")
        view.transient(self.root)
        
        # Calculate inventory
        inventory = {}
        for donor in self.donors:
            bt = donor["blood_type"]
            inventory[bt] = inventory.get(bt, 0) + len(donor.get("donations", []))
        
        tk.Label(view, text="Blood Type Inventory", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        for bt in ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]:
            count = inventory.get(bt, 0)
            color = "#4CAF50" if count > 0 else "#f44336"
            frame = tk.Frame(view)
            frame.pack(fill="x", padx=20, pady=2)
            tk.Label(frame, text=bt, width=8, anchor="w").pack(side="left")
            tk.Label(frame, text=str(count), fg=color, font=("Helvetica", 10, "bold")).pack(side="right")
        
        tk.Button(view, text="Close", command=view.destroy).pack(pady=20)
    
    def save_and_exit(self):
        """Save data and close the application."""
        self.save_data()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = BloodDonationSystem(root)
    root.mainloop()
