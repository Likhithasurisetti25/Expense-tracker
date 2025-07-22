import csv
from datetime import datetime
import os
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.file_path = "expenses.csv"
        self.load_expenses()
        self.setup_gui()

    def load_expenses(self):
        """Load expenses from CSV file if it exists"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', newline='') as file:
                    reader = csv.DictReader(file)
                    self.expenses = list(reader)
            except Exception:
                self.expenses = []

    def save_expenses(self):
        """Save expenses to CSV file"""
        with open(self.file_path, 'w', newline='') as file:
            if self.expenses:
                fieldnames = self.expenses[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.expenses)

    def setup_gui(self):
        """Create and configure the GUI"""
        self.root = tk.Tk()
        self.root.title("Personal Expense Tracker")
        self.root.geometry("800x600")
        
        # Configure style
        style = ttk.Style()
        style.configure('TButton', padding=6, font=('Arial', 10))
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TEntry', font=('Arial', 10))
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Add Expense Frame
        add_frame = ttk.LabelFrame(main_frame, text="Add Expense", padding="10")
        add_frame.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        ttk.Label(add_frame, text="Amount:").grid(row=0, column=0, padx=5, pady=5)
        self.amount_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.amount_var).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.category_var = tk.StringVar()
        categories = ['Food', 'Transport', 'Entertainment', 'Shopping', 'Bills', 'Other']
        ttk.Combobox(add_frame, textvariable=self.category_var, values=categories).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(add_frame, text="Date:").grid(row=2, column=0, padx=5, pady=5)
        self.date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        ttk.Entry(add_frame, textvariable=self.date_var).grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Button(add_frame, text="Add Expense", command=self.add_expense_gui).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Summary Frame
        summary_frame = ttk.LabelFrame(main_frame, text="Expense Summary", padding="10")
        summary_frame.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.summary_text = scrolledtext.ScrolledText(summary_frame, width=50, height=10)
        self.summary_text.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # Buttons Frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=2, column=0, padx=5, pady=5)
        
        ttk.Button(buttons_frame, text="View Summary", command=self.view_summary_gui).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Delete Expense", command=self.delete_expense_gui).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="Exit", command=self.root.quit).grid(row=0, column=2, padx=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Start the GUI
        self.root.mainloop()

    def save_expenses(self):
        """Save expenses to CSV file"""
        with open(self.file_path, 'w', newline='') as file:
            if self.expenses:
                fieldnames = self.expenses[0].keys()
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(self.expenses)

    def add_expense_gui(self):
        """Add expense using GUI"""
        try:
            amount = float(self.amount_var.get())
            category = self.category_var.get()
            date = self.date_var.get()
            
            if not all([amount, category, date]):
                messagebox.showerror("Error", "Please fill in all fields")
                return
            
            expense = {
                "amount": amount,
                "category": category,
                "date": date,
                "timestamp": datetime.now().isoformat()
            }
            
            self.expenses.append(expense)
            self.save_expenses()
            messagebox.showinfo("Success", f"Expense added successfully: ${amount} in {category} on {date}")
            
            # Clear input fields
            self.amount_var.set("")
            self.category_var.set("")
            self.date_var.set(datetime.now().strftime("%Y-%m-%d"))
            
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount as a number.")

    def get_category_summary(self, category):
        """Get total expenses for a specific category"""
        total = sum(float(expense["amount"]) for expense in self.expenses 
                    if expense["category"].lower() == category.lower())
        return total

    def get_overall_summary(self):
        """Get total overall expenses"""
        return sum(float(expense["amount"]) for expense in self.expenses)

    def get_time_summary(self, period='month'):
        """Get spending summary by time period (day, week, month)"""
        from collections import defaultdict
        
        summary = defaultdict(float)
        
        for expense in self.expenses:
            date = datetime.fromisoformat(expense["timestamp"]).date()
            
            if period == 'day':
                key = date.strftime("%Y-%m-%d")
            elif period == 'week':
                key = date.strftime("%Y-Week %U")
            else:  # month
                key = date.strftime("%Y-%m")
            
            summary[key] += float(expense["amount"])
        
        return dict(summary)

    def view_summary_gui(self):
        """Display expense summary in GUI"""
        if not self.expenses:
            messagebox.showinfo("Info", "No expenses recorded yet!")
            return

        summary = "=== Expense Summary ===\n\n"
        
        # Overall summary
        overall_total = self.get_overall_summary()
        summary += f"Total Expenses: ${overall_total:.2f}\n\n"
        
        # Category-wise summary
        summary += "Expenses by Category:\n"
        categories = set(expense["category"] for expense in self.expenses)
        for category in sorted(categories):
            total = self.get_category_summary(category)
            summary += f"{category}: ${total:.2f}\n"
        
        summary += "\nExpenses by Month:\n"
        monthly_summary = self.get_time_summary()
        for month, amount in sorted(monthly_summary.items()):
            summary += f"{month}: ${amount:.2f}\n"
        
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.insert(tk.END, summary)

    def delete_expense_gui(self):
        """Delete expense using GUI"""
        if not self.expenses:
            messagebox.showinfo("Info", "No expenses to delete!")
            return

        # Create a new window for expense selection
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Expense")
        delete_window.geometry("400x300")
        
        # Create a listbox to show expenses
        listbox = tk.Listbox(delete_window, width=50, height=15)
        listbox.pack(padx=10, pady=10)
        
        # Add expenses to listbox
        for expense in self.expenses:
            listbox.insert(tk.END, f"${expense['amount']} - {expense['category']} - {expense['date']}")
        
        def delete_selected():
            selected_index = listbox.curselection()
            if not selected_index:
                messagebox.showerror("Error", "Please select an expense to delete")
                return
            
            index = selected_index[0]
            deleted_expense = self.expenses.pop(index)
            self.save_expenses()
            messagebox.showinfo("Success", f"Expense deleted: ${deleted_expense['amount']} - {deleted_expense['category']}")
            delete_window.destroy()
            
        ttk.Button(delete_window, text="Delete Selected", command=delete_selected).pack(pady=5)
        ttk.Button(delete_window, text="Cancel", command=delete_window.destroy).pack(pady=5)

    def run(self):
        """Start the GUI application"""
        self.setup_gui()
if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.run()