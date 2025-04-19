import tkinter as tk
from tkinter import messagebox
import json

class FoodTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Food Tracker")
        self.root.geometry("500x700")
        
        # Load data from file
        self.food_list = self.load_data()

        # Create GUI elements
        self.food_name_label = tk.Label(root, text="Food Name:", font=('Arial', 12))
        self.food_name_label.grid(row=0, column=0, pady=10, padx=10)

        self.food_name_entry = tk.Entry(root, font=('Arial', 12))
        self.food_name_entry.grid(row=0, column=1, pady=10, padx=10)

        self.calories_label = tk.Label(root, text="Calories:", font=('Arial', 12))
        self.calories_label.grid(row=1, column=0, pady=10, padx=10)

        self.calories_entry = tk.Entry(root, font=('Arial', 12))
        self.calories_entry.grid(row=1, column=1, pady=10, padx=10)

        self.add_button = tk.Button(root, text="Add Food", command=self.add_food, font=('Arial', 12), bg='green', fg='white')
        self.add_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.clear_button = tk.Button(root, text="Clear Fields", command=self.clear_fields, font=('Arial', 12), bg='lightgray')
        self.clear_button.grid(row=2, column=2, pady=20)

        # Search Section
        self.search_label = tk.Label(root, text="Search by Name:", font=('Arial', 12))
        self.search_label.grid(row=3, column=0, pady=10, padx=10)

        self.search_entry = tk.Entry(root, font=('Arial', 12))
        self.search_entry.grid(row=3, column=1, pady=10, padx=10)
        self.search_entry.bind("<KeyRelease>", self.update_food_list)

        # Listbox with Scrollbar to show foods
        self.food_listbox_frame = tk.Frame(root)
        self.food_listbox_frame.grid(row=4, column=0, columnspan=3, pady=10, padx=10)

        self.food_listbox = tk.Listbox(self.food_listbox_frame, width=50, height=10, font=('Arial', 12))
        self.food_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.food_listbox_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.food_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.food_listbox.yview)

        self.total_calories_label = tk.Label(root, text="Total Calories: 0", font=('Arial', 12))
        self.total_calories_label.grid(row=5, column=0, columnspan=3, pady=10)

        self.food_item_count_label = tk.Label(root, text="Total Items: 0", font=('Arial', 12))
        self.food_item_count_label.grid(row=6, column=0, columnspan=3, pady=10)

        self.edit_button = tk.Button(root, text="Edit", command=self.edit_food, font=('Arial', 12), bg='yellow')
        self.edit_button.grid(row=7, column=0, pady=5)

        self.delete_button = tk.Button(root, text="Delete", command=self.delete_food, font=('Arial', 12), bg='red', fg='white')
        self.delete_button.grid(row=7, column=1, pady=5)

        # Sort by Name / Calories
        self.sort_by_name_button = tk.Button(root, text="Sort by Name", command=self.sort_by_name, font=('Arial', 12))
        self.sort_by_name_button.grid(row=8, column=0, pady=5)

        self.sort_by_calories_button = tk.Button(root, text="Sort by Calories", command=self.sort_by_calories, font=('Arial', 12))
        self.sort_by_calories_button.grid(row=8, column=1, pady=5)

        self.update_food_list()
        self.update_total_calories()
        self.update_food_item_count()

    def add_food(self):
        food_name = self.food_name_entry.get().strip()
        calories = self.calories_entry.get().strip()

        if not food_name or not calories:
            messagebox.showwarning("Input Error", "Please enter both food name and calories.")
            return

        if food_name in [food[0] for food in self.food_list]:
            messagebox.showwarning("Duplicate Entry", "This food item is already in the list.")
            return

        try:
            calories = int(calories)
            if calories <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Input Error", "Calories must be a positive integer.")
            return

        self.food_list.append((food_name, calories))
        self.update_food_list()
        self.update_total_calories()
        self.update_food_item_count()
        self.save_data()

        # Clear input fields
        self.food_name_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)

    def update_food_list(self, event=None):
        search_query = self.search_entry.get().lower()

        self.food_listbox.delete(0, tk.END)
        for index, food in enumerate(self.food_list):
            food_name, calories = food
            if search_query in food_name.lower():
                self.food_listbox.insert(tk.END, f"{index + 1}. {food_name} - {calories} kcal")

    def update_total_calories(self):
        total_calories = sum([food[1] for food in self.food_list])
        self.total_calories_label.config(text=f"Total Calories: {total_calories}")

    def update_food_item_count(self):
        item_count = len(self.food_list)
        self.food_item_count_label.config(text=f"Total Items: {item_count}")

    def clear_fields(self):
        self.food_name_entry.delete(0, tk.END)
        self.calories_entry.delete(0, tk.END)

    def edit_food(self):
        try:
            selected_index = self.food_listbox.curselection()[0]
            selected_food = self.food_list[selected_index]

            self.food_name_entry.delete(0, tk.END)
            self.food_name_entry.insert(0, selected_food[0])

            self.calories_entry.delete(0, tk.END)
            self.calories_entry.insert(0, selected_food[1])

            # Remove the selected food item for editing
            self.delete_food()

        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a food item to edit.")

    def delete_food(self):
        try:
            selected_index = self.food_listbox.curselection()[0]
            if messagebox.askyesno("Delete Confirmation", "Are you sure you want to delete this item?"):
                del self.food_list[selected_index]
                self.update_food_list()
                self.update_total_calories()
                self.update_food_item_count()
                self.save_data()
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a food item to delete.")

    def sort_by_name(self):
        self.food_list.sort(key=lambda x: x[0].lower())  # Sort by food name (case insensitive)
        self.update_food_list()
        self.save_data()

    def sort_by_calories(self):
        self.food_list.sort(key=lambda x: x[1])  # Sort by calories
        self.update_food_list()
        self.save_data()

    def save_data(self):
        try:
            with open("food_data.json", "w") as f:
                json.dump(self.food_list, f)
        except Exception as e:
            messagebox.showerror("Save Error", f"An error occurred while saving the data: {e}")

    def load_data(self):
        try:
            with open("food_data.json", "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

# Create the main Tkinter window and pass it to the FoodTrackerApp
root = tk.Tk()
app = FoodTrackerApp(root)

# Run the application
root.mainloop()
