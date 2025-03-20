import pandas as pd
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk
import recipeBank as st



df = st.storage('recipes.csv')


def main_menu():
    window = tk.Tk()
    window.title("Menu")

    # Set the dimensions of the window (e.g., 400x300)
    window_width = 400
    window_height = 100

    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position to center the window
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    b1 = tk.Button(window, text="Redigera recept", command=lambda: editRecipes())
    b2 = tk.Button(window, text="Månadsplan", command=lambda: monthlyPlan())
    
    b1.pack(side="left", padx=20)
    b2.pack(side="left", expand=True)
    #b3.pack(side="left", padx=20)

    window.mainloop()
    #OPTIONS
    #ADD recipe
    #Show list of recipes
    #Start mouthly plan
    #

def addRecipe_GUI():

    def button_window():
        window  = tk.Tk()
        window.title("Recipes")

        # Set the dimensions of the window (e.g., 400x300)
        window_width = 400
        window_height = 100

        # Get the screen width and height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        # Calculate the position to center the window
        x_coordinate = (screen_width // 2) - (window_width // 2)
        y_coordinate = (screen_height // 2) - (window_height // 2)

        window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

        def button_clicked(button_text):
            global tag 
            tag = button_text
            window.destroy()

        b1 = tk.Button(window, text="Vardag", command=lambda: button_clicked("Vardag"))
        b2 = tk.Button(window, text="Storkok", command=lambda: button_clicked("Storkok"))
        b3 = tk.Button(window, text="Helg", command=lambda: button_clicked("Helg"))
    
        b1.pack(side="left", padx=20)
        b2.pack(side="left", expand=True)
        b3.pack(side="left", padx=20)

        window.mainloop()

    name = simpledialog.askstring("Input", "Enter recipe name")
    link = simpledialog.askstring("Input", "Enter link")
    button_window()


    if name and link and tag:
        # Add a new row to the DataFrame
        df.addRecepie(name, link, tag)
        print("Updated DataFrame:")
        print(df.toString())
    else:
        print("Input was canceled or invalid.")

def editRecipes():
    window = tk.Tk()
    window.title("Redigera recept")

    # Set the dimensions of the window (e.g., 400x300)
    window_width = 600
    window_height = 400

    # Get the screen width and height
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate the position to center the window
    x_coordinate = (screen_width // 2) - (window_width // 2)
    y_coordinate = (screen_height // 2) - (window_height // 2)

    window.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")

    tree = ttk.Treeview(window)
    tree["columns"] = list(df.getDataframe().columns) 
    tree["show"] = "headings"

    # Set the column headers
    for col in df.getDataframe().columns:
        tree.heading(col, text=col)  # Set the column heading
        tree.column(col, width=100)  # Set the column width

    # Add rows to the Treeview
    for _, row in df.getDataframe().iterrows():
        tree.insert("", "end", values=list(row))

    # Pack the Treeview into the window
    tree.pack(fill="both", expand=True)

    button_frame = tk.Frame(window)
    button_frame.pack(fill="x", pady=10)

    button_new = tk.Button(button_frame, text="Nytt recept", command=lambda: addRecipe_GUI())
    button_remove = tk.Button(button_frame, text="Ta bort recept", command=lambda: removeRecipe())
    button_EJVALD = tk.Button(button_frame, text="EJ VALD", command=lambda: removeRecipe())

    button_new.pack(side="left", padx=20)
    button_remove.pack(side="left", expand=True)
    button_EJVALD.pack(side="left", padx=20)


    window.mainloop()


def removeRecipe():
    print()

def monthlyPlan():
    print()
    
    
main_menu()





#For showing dataframe from menu later
'''
import tkinter as tk
import pandas as pd

# Sample DataFrame
data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [25, 30, 35],
    "City": ["New York", "Los Angeles", "Chicago"]
}
df = pd.DataFrame(data)

# Function to show DataFrame in terminal
def show_dataframe():
    print(df)

# Create the main window
root = tk.Tk()
root.title("DataFrame Example")

# Create a button to show the DataFrame
button = tk.Button(root, text="Show DataFrame", command=show_dataframe)
button.pack(pady=10)

root.mainloop()
'''