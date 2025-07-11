import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt

class StudentResultAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Result Analyzer")
        self.root.geometry("800x600")

        self.create_widgets()
        self.df = None

    def create_widgets(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        load_btn = tk.Button(frame, text="Load CSV File", command=self.load_csv)
        load_btn.pack(side=tk.LEFT, padx=10)

        export_btn = tk.Button(frame, text="Export Updated CSV", command=self.export_csv)
        export_btn.pack(side=tk.LEFT, padx=10)

        chart_btn = tk.Button(frame, text="Show Performance Chart", command=self.show_chart)
        chart_btn.pack(side=tk.LEFT, padx=10)

        self.table = ttk.Treeview(self.root)
        self.table.pack(fill=tk.BOTH, expand=True)

    def load_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            try:
                self.df = pd.read_csv(file_path)
                if 'Total' not in self.df.columns:
                    self.df['Total'] = self.df.iloc[:, 1:].sum(axis=1)
                if 'Average' not in self.df.columns:
                    self.df['Average'] = self.df['Total'] / (self.df.shape[1]-3)
                if 'Grade' not in self.df.columns:
                    self.df['Grade'] = self.df['Average'].apply(self.assign_grade)
                self.display_table()
                messagebox.showinfo("Success", "CSV Loaded and Processed Successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load CSV: {e}")

    def display_table(self):
        self.table.delete(*self.table.get_children())
        self.table["columns"] = list(self.df.columns)
        self.table["show"] = "headings"
        for col in self.df.columns:
            self.table.heading(col, text=col)
            self.table.column(col, width=100)
        for _, row in self.df.iterrows():
            self.table.insert("", tk.END, values=list(row))

    def export_csv(self):
        if self.df is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                self.df.to_csv(file_path, index=False)
                messagebox.showinfo("Success", "CSV exported successfully!")
        else:
            messagebox.showwarning("Warning", "Please load a CSV file first.")

    def show_chart(self):
        if self.df is not None:
            plt.figure(figsize=(10,6))
            plt.bar(self.df.iloc[:,0], self.df['Total'], color='skyblue')
            plt.xlabel('Student')
            plt.ylabel('Total Marks')
            plt.title('Student Performance')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showwarning("Warning", "Please load a CSV file first.")

    def assign_grade(self, avg):
        if avg >= 90:
            return 'A'
        elif avg >= 75:
            return 'B'
        elif avg >= 60:
            return 'C'
        elif avg >= 50:
            return 'D'
        else:
            return 'F'

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentResultAnalyzer(root)
    root.mainloop()
