# Import dependencies module
import dep

__version__ = 1.0

my_url = 'https://github.com/soldiers-son/simple-stock'

# Handle database PATH
def resource_path(relative_path):
    try:
        base_path = dep.sys._MEIPASS
    except Exception:
        base_path = dep.os.path.abspath(".")
    return dep.os.path.join(base_path, relative_path)

# Connect to database
if dep.os.path.exists("farm.db"):
    db_path = "farm.db"
else:
    db_path = resource_path("farm.db")

# Create cursor in database
conn = dep.sqlite3.connect(db_path)
c = conn.cursor()

# Login Session File
SESSION_FILE = "session.json"

# Current date and time
timestamp = dep.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#########################
# Main Functions
#########################

# Raise frame function
def show_frame(frame):
    frame.tkraise()

# Create login session file
def save_session(username):
    with open(SESSION_FILE, "w") as f:
        dep.json.dump({"username": username}, f)

# Keep current user logged in by loading the session file if exists, even after closing and reopening app
def load_session():
    if dep.os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            data = dep.json.load(f)
            return data.get("username")
    return None

# Clears session file when logged out
def clear_session():
    if dep.os.path.exists(SESSION_FILE):
        dep.os.remove(SESSION_FILE)

# Login validation, scans database for login credentials.
def login_validation():
    
    try:
        global current_user
        U = userl.get()
        P = passwordl.get()

        # check for empty fields first
        if len(U) == 0:
            dep.messagebox.showerror("ERROR", "Please enter a Username.")
            return
        if len(P) == 0:
            dep.messagebox.showerror("ERROR", "Please enter a Password.")
            return

        # query only for the username
        find_user = 'SELECT password_hash FROM users WHERE username = ?'
        c.execute(find_user, (U,))
        result = c.fetchone()

        if result:
            stored_hash = result[0]  # this should already be bytes
            if dep.bcrypt.checkpw(P.encode(), stored_hash):
                current_user = U
                save_session(U)
                userl.delete(0, 'end')
                passwordl.delete(0, 'end')
                dep.messagebox.showinfo("Welcome", f"Welcome back, {U}.")
                show_frame(main)
            else:
                dep.messagebox.showerror("ERROR", "Invalid username or password.")
        else:
            dep.messagebox.showerror("ERROR", "Username not found.")

        # clear input fields after any attempt
        userl.delete(0, 'end')
        passwordl.delete(0, 'end')
    except Exception as e:
        dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")

# Logs user out, deletes session file 
def logout():
    global current_user
    current_user = None
    clear_session()
    show_frame(login)

# Creates new user, uses dep.bcrypt HASH for password encryption when inserted into database 
def create_user():
    try:
        find_user = 'SELECT * FROM users WHERE username = ?'
        find_password = 'SELECT * FROM users WHERE password_hash = ?'
        c.execute(find_user, [(userc.get())])
        c.execute(find_password, [(passwordc.get())])
        result=c.fetchall()
        if(len(userc.get()) == 0):
                dep.messagebox.showerror(
                    "ERROR", "Please enter a Username.")
        elif(len(passwordc.get()) == 0):
                dep.messagebox.showerror(
                    "ERROR", "Please enter a Password.")
        elif result:
            passwordc.delete(0, dep.END)
            dep.messagebox.showerror(
                    "ERROR", "Password already exists.")
        else:
            N =userc.get()
            P =passwordc.get()
            hashed = dep.bcrypt.hashpw(P.encode(), dep.bcrypt.gensalt())
            c.execute("""
                INSERT INTO users(username, password_hash)
                VALUES(?,?)
                """, (N, hashed))
            conn.commit()
            userc.delete(0, dep.END)
            passwordc.delete(0, dep.END)
            show_frame(login)
            dep.messagebox.showinfo('Congrats!', 'Account Created!')
    except Exception as e:
        dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")


#########################
# MAIN Menu Bar Items
#########################
# About the app
def show_about():
        info = ("Project: 🌿Simple Stock\n"
                f"Version: {__version__}\n"
                "Author: soldiers_son\n"
                "Github: https://github.com/soldiers-son\n\n")
        dep.messagebox.showinfo("About", info)

# Basic guide and info
def show_help():
        help = ("Login if you already have an account.\n"
                "Create an account if a new user\n\n"
                "How to use(Main):\n"
                "- Click 'Data Logs' to input data.\n"
                "- Click 'Inventory' to input inventory items.\n\n"
                "Menu Bar\n"
                "-Tools -- Click to view tools.(Weight Converter)\n"
                "-View Data -- Click to view data entries.(Plant, Harvest, Tasks)\n"
                "-View Inv -- Click to view Inventory.(Tools, Farm Supplies, Animal Supplies)\n")
        dep.messagebox.showinfo("About", help)


# Opens GitHub
def open_source():
    dep.webbrowser.open_new(my_url)

# Shows plants database treeview
def show_plant():
    if not current_user:
        dep.messagebox.showerror('Error', 'Please login to view data.')
        return
    try:
        c.execute("SELECT * FROM plant")
        rows = c.fetchall()
        
        plant_window = dep.tk.Toplevel(root)
        plant_window.title('Plant Logs')
        plant_window.geometry('565x350')
        plant_window.configure(bg="#1F1F1F")
        
        dep.ctk.CTkLabel(plant_window, font=("Default", 16, "bold"), text="View Data").pack(pady=10)
        
        # Create a frame to hold the Treeview and scrollbar
        tree_frame = dep.tk.Frame(plant_window)
        tree_frame.pack(fill="both", expand=True)
        
        # Create the Treeview
        tree = dep.ttk.Treeview(tree_frame, columns=("col1", "col2", "col3"), show="headings")
        tree.heading("col1", text="Type")
        tree.heading("col2", text="Amount")
        tree.heading("col3", text="Date/Time")
        tree.pack(side="left", fill="both", expand=True)
        
        # Create the vertical scrollbar
        scrollbar = dep.ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        
        # Attach scrollbar to Treeview
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Insert data
        for row in rows:
            tree.insert("", dep.tk.END, values=row)
    except Exception as e:
        dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")

# Shows harvest database treeview
def show_harvest():       
    if not current_user:
        dep.messagebox.showerror('Error', 'Please login to view data.')
        return
    try:
        c.execute("SELECT * FROM harvest")
        rows = c.fetchall()
        
        harvest_window = dep.tk.Toplevel(root)
        harvest_window.title('Harvest Logs')
        harvest_window.geometry('565x350')
        harvest_window.configure(bg="#1F1F1F")
        
        dep.ctk.CTkLabel(harvest_window, font=("Default", 16, "bold"), text="View Data").pack(pady=10)
        
        # Create a frame to hold the Treeview and scrollbar
        tree_frame = dep.tk.Frame(harvest_window)
        tree_frame.pack(fill="both", expand=True)
        
        # Create the Treeview
        tree = dep.ttk.Treeview(tree_frame, columns=("col1", "col2", "col3"), show="headings")
        tree.heading("col1", text="Type")
        tree.heading("col2", text="Amount")
        tree.heading("col3", text="Date/Time")
        tree.pack(side="left", fill="both", expand=True)
        
        # Create the vertical scrollbar
        scrollbar = dep.ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        
        # Attach scrollbar to Treeview
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Insert data
        for row in rows:
            tree.insert("", dep.tk.END, values=row)
    except Exception as e:
        dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")

# Shows task completed entries
def show_task():
    if not current_user:
        dep.messagebox.showerror('Error', 'Please login to view data.')
        return
    try:
        c.execute("SELECT * FROM task_complete")
        rows = c.fetchall()

        task_window = dep.tk.Toplevel(root)
        task_window.title('Task Logs')
        task_window.geometry('565x350')
        task_window.configure(bg="#1F1F1F")
        
        dep.ctk.CTkLabel(task_window, font=("Default", 16, "bold"), text="View Data").pack(pady=10)
        
        # Create a frame to hold the Treeview and scrollbar
        tree_frame = dep.tk.Frame(task_window)
        tree_frame.pack(fill="both", expand=dep.TRUE)
        
        # Create the Treeview
        tree = dep.ttk.Treeview(tree_frame, columns=("col1", "col2", "col3"), show="headings")
        tree.heading("col1", text="Name")
        tree.heading("col2", text="Date/Time")
        tree.heading("col3", text="Task")
        tree.pack(side="left", fill="both", expand=True)
        
        # Create the vertical scrollbar
        scrollbar = dep.ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        
        # Attach scrollbar to Treeview
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Insert data
        for row in rows:
            tree.insert("", dep.tk.END, values=row)
    except Exception as e:
        dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")

# Shows tool type entries
def show_tool():
    if not current_user:
        dep.messagebox.showerror('Error', 'Please login to view data.')
        return
    try:
        c.execute("SELECT * FROM tools")
        rows = c.fetchall()

        tool_window = dep.tk.Toplevel(root)
        tool_window.title('Tools')
        tool_window.geometry('565x350')
        tool_window.configure(bg="#1F1F1F")
        
        dep.ctk.CTkLabel(tool_window, font=("Default", 16, "bold"), text="View Data").pack(pady=10)
        
        # Create a frame to hold the Treeview and scrollbar
        tree_frame = dep.tk.Frame(tool_window)
        tree_frame.pack(fill="both", expand=dep.TRUE)
        
        # Create the Treeview
        tree = dep.ttk.Treeview(tree_frame, columns=("col1", "col2"), show="headings")
        tree.heading("col1", text="Tool Type")
        tree.heading("col2", text="Quantity")
        tree.pack(side="left", fill="both", expand=True)
        
        # Create the vertical scrollbar
        scrollbar = dep.ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        
        # Attach scrollbar to Treeview
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Insert data
        for row in rows:
            tree.insert("", dep.tk.END, values=row)
    except Exception as e:
        dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")

# Shows farm supplyd entries
def show_farm_supply():
    if not current_user:
        dep.messagebox.showerror('Error', 'Please login to view data.')
        return
    try:
        c.execute("SELECT * FROM farm_supply")
        rows = c.fetchall()

        farm_supply_window = dep.tk.Toplevel(root)
        farm_supply_window.title('Tools')
        farm_supply_window.geometry('565x350')
        farm_supply_window.configure(bg="#1F1F1F")
        
        dep.ctk.CTkLabel(farm_supply_window, font=("Default", 16, "bold"), text="View Data").pack(pady=10)
        
        # Create a frame to hold the Treeview and scrollbar
        tree_frame = dep.tk.Frame(farm_supply_window)
        tree_frame.pack(fill="both", expand=dep.TRUE)
        
        # Create the Treeview
        tree = dep.ttk.Treeview(tree_frame, columns=("col1", "col2"), show="headings")
        tree.heading("col1", text="Item")
        tree.heading("col2", text="Quantity")
        tree.pack(side="left", fill="both", expand=True)
        
        # Create the vertical scrollbar
        scrollbar = dep.ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        
        # Attach scrollbar to Treeview
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Insert data
        for row in rows:
            tree.insert("", dep.tk.END, values=row)
    except Exception as e:
        dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")

# Shows animal supply entries
def show_animal_supply():
    if not current_user:
        dep.messagebox.showerror('Error', 'Please login to view data.')
        return
    try:
        c.execute("SELECT * FROM animal_supply")
        rows = c.fetchall()

        animal_supply_window = dep.tk.Toplevel(root)
        animal_supply_window.title('Animal Supply')
        animal_supply_window.geometry('565x350')
        animal_supply_window.configure(bg="#1F1F1F")
        
        dep.ctk.CTkLabel(animal_supply_window, font=("Default", 16, "bold"), text="View Data").pack(pady=10)
        
        # Create a frame to hold the Treeview and scrollbar
        tree_frame = dep.tk.Frame(animal_supply_window)
        tree_frame.pack(fill="both", expand=dep.TRUE)
        
        # Create the Treeview
        tree = dep.ttk.Treeview(tree_frame, columns=("col1", "col2", "col3"), show="headings")
        tree.heading("col1", text="Item")
        tree.heading("col2", text="Price")
        tree.heading("col3", text="Date Purchased")
        tree.pack(side="left", fill="both", expand=True)
        
        # Create the vertical scrollbar
        scrollbar = dep.ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        
        # Attach scrollbar to Treeview
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Insert data
        for row in rows:
            tree.insert("", dep.tk.END, values=row)
    except Exception as e:
        dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")

#########################
### Button Functions
#########################

# Submits plant frame entries
def plant_submit():

    T =plant1.get()
    A = plant2.get()
    if len(T) == 0:
        dep.messagebox.showerror("ERROR", "Please enter Plant Type.")
        return
    if len(A) == 0:
        dep.messagebox.showerror("ERROR", "Please enter Amount")
        return
    try:
        c.execute("""
        INSERT INTO plant(type, amount, date)
        VALUES(?,?,?)
        """, (T, A, timestamp))
        conn.commit()
        dep.messagebox.showinfo('Congrats!', 'Data entry successful.')
        plant1.delete(0, dep.END)
        plant2.delete(0, dep.END)
    except Exception as e:
        dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")
    
# Submits harvest frame entries
def harvest_submit():
    T = h1.get()
    A = h2.get()
    if len(T) == 0:
        dep.messagebox.showerror("ERROR", "Please enter Plant Type.")
        return
    if len(A) == 0:
        dep.messagebox.showerror("ERROR", "Please enter Amount")
        return
    try:
        c.execute("""
        INSERT INTO harvest(type, amount, date)
        VALUES(?,?,?)
        """, (T, A, timestamp))
        conn.commit()
        dep.messagebox.showinfo('Congrats!', 'Data entry successful.')
        h1.delete(0, dep.END)
        h2.delete(0, dep.END)
    except Exception as e:
            dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")

# Submits task frame entries
def task_submit():
    T = tasks.get()
    if not T:
        dep.messagebox.showerror("ERROR", "Please enter Task Completed.")
        return
    try:
        c.execute("""
            INSERT INTO task_complete(name, date, task)
            VALUES(?,?,?)
        """, (current_user, timestamp, T))
        conn.commit()
        dep.messagebox.showinfo('Congrats!', 'Data entry successful.')
        tasks.delete(0, dep.END)
    except Exception as e:
        dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")

# Submits tool frame entries
def tool_submit():
    T1 = t1.get()
    T2 = t2.get()
    if not T1:
        dep.messagebox.showerror("ERROR", "Please enter Tool Type.")
        return
    if not T2:
        dep.messagebox.showerror("ERROR", "Please enter Quantity.")
        return
    try:
        c.execute("""
            INSERT INTO tools(tool, quantity)
            VALUES(?,?)
        """, (T1, T2))
        conn.commit()
        dep.messagebox.showinfo('Congrats!', 'Data entry successful.')
        t1.delete(0, dep.END)
        t2.delete(0, dep.END)
    except Exception as e:
        dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")

# Submits Farm Supply frame entries
def farm_supply_submit():
    F1 = f1.get()
    F2 = f2.get()
    if not F1:
        dep.messagebox.showerror("ERROR", "Please enter Item.")
        return
    if not F2:
        dep.messagebox.showerror("ERROR", "Please enter Quantity.")
        return
    try:
        c.execute("""
            INSERT INTO farm_supply(item, quantity)
            VALUES(?,?)
        """, (F1, F2))
        conn.commit()
        dep.messagebox.showinfo('Congrats!', 'Data entry successful.')
        f1.delete(0, dep.END)
        f2.delete(0, dep.END)
    except Exception as e:
        dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")


# Submits Animal Supply frame entries
def animal_supply_submit():
    A1 = a1.get()
    A2 = a2.get()
    if not A1:
        dep.messagebox.showerror("ERROR", "Please enter Item.")
        return
    if not A2:
        dep.messagebox.showerror("ERROR", "Please enter Quantity.")
        return
    try:
        c.execute("""
            INSERT INTO animal_supply(item, price, date)
            VALUES(?,?, ?)
        """, (A1, A2, timestamp))
        conn.commit()
        dep.messagebox.showinfo('Congrats!', 'Data entry successful.')
        a1.delete(0, dep.END)
        a2.delete(0, dep.END)
    except Exception as e:
        dep.messagebox.showerror("Database Error", f"An error occurred:\n{e}")

#########################
# End of Main Functions  
#########################

#########################
# Simple Stock GUI
#########################

root = dep.tk.Tk()
root.title("Simple Stock")
root.geometry('350x300')

container = dep.tk.Frame(root)
container.pack(side="top", fill='both', expand=True)
container.grid_rowconfigure(0, weight=1)
container.grid_columnconfigure(0, weight=1)
container.tk_setPalette("#1F1F1F")

title_font = dep.font.Font(root, family="Arial", size=12, underline=True)

current_user = None

# LOGIN

login = dep.tk.Frame(container)

dep.tk.Label(login, padx=10, pady=10, text="Login", font=title_font).pack()

label_1 = dep.tk.Label(login, text="Username:")
label_1.pack(pady=5)

userl = dep.ctk.CTkEntry(login)
userl.pack(pady=5)

label_1 = dep.tk.Label(login, text="Password:")
label_1.pack(pady=5)

passwordl = dep.ctk.CTkEntry(login, show="*")
passwordl.pack(pady=5)

dep.ctk.CTkButton(login, 
                text_color="black", 
                fg_color="white", 
                hover_color="gray94", 
                command=login_validation, 
                text="Enter",).pack(pady=5)

dep.ctk.CTkButton(login, text="Create User",
                text_color="black",
                fg_color="white", 
                hover_color="gray94", 
                command=lambda: show_frame(create)).pack(pady=5)

# CREATE_USER
create = dep.tk.Frame(container)

dep.tk.Label(create, padx=10, pady=10, text="Create User", font=title_font).pack()

label_1 = dep.tk.Label(create, text="Create Username:")
label_1.pack(pady=5)

userc = dep.ctk.CTkEntry(create)
userc.pack(pady=5)

label_1 = dep.tk.Label(create, text="Create Password:")
label_1.pack(pady=5)

passwordc = dep.ctk.CTkEntry(create)
passwordc.pack(pady=5)

dep.ctk.CTkButton(create, text_color="black", 
              fg_color="white", 
              hover_color="gray94", 
              command=create_user, text="Submit",).pack(pady=5)

dep.ctk.CTkButton(create, text="Back to Login", 
              text_color="black", 
              fg_color="white", 
              hover_color="gray94", 
              command=lambda: show_frame(login)).pack(pady=5)

################
# MAIN
################
main = dep.tk.Frame(container)

dep.tk.Label(main, padx=10, text="Main", font=title_font).pack(pady=(20, 10))

menubar = dep.tk.Menu(root, bg='white')
root.config(menu=menubar)

view_data = dep.tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='View Data', menu=view_data)
view_data.add_command(label='Plant', command=show_plant)
view_data.add_command(label='Harvest', command=show_harvest)
view_data.add_command(label='Task Log', command=show_task)

view_inv = dep.tk.Menu(menubar,tearoff=0)
menubar.add_cascade(label='View Inv', menu=view_inv)
view_inv.add_command(label='Tools', command=show_tool)
view_inv.add_command(label='Farm Supply', command=show_farm_supply)
view_inv.add_command(label='Animal Supply', command=show_animal_supply)

help_menu = dep.tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label='Help', command=show_help)
help_menu.add_command(label='About', command=show_about)
help_menu.add_command(label='Source Code', command=open_source)

datalogging = dep.ctk.CTkButton(main, 
                            text="Data Logging", 
                            text_color="black", 
                            fg_color="white", 
                            hover_color="gray94", 
                            command=lambda: show_frame(data_logging))
datalogging.pack(padx=10, pady=10)

inventory = dep.ctk.CTkButton(main, 
                      text ="Inventory", 
                      text_color="black", 
                      fg_color="white", 
                      hover_color="gray94", 
                      command=lambda: show_frame(farm_inventory))
inventory.pack(padx=10, pady=10)


dep.ctk.CTkButton(main, 
              text="Logout", 
              text_color="black", 
              fg_color="white", 
              hover_color="gray94", 
              command=logout).pack(padx=10, pady=10)



# Data Logging

data_logging = dep.tk.Frame(container)

dep.tk.Label(data_logging, padx=10, text="Data Logging", font=title_font).pack(pady=(20,10))

plant = dep.ctk.CTkButton(data_logging, 
                      text="Plant Log", 
                      text_color="black", 
                      fg_color="white", 
                      hover_color="gray94", 
                      command=lambda: show_frame(plant))
plant.pack(padx=10, pady=10,)

harvest_log = dep.ctk.CTkButton(data_logging, 
                            text="Harvest Log", 
                            text_color="black", 
                            fg_color="white", 
                            hover_color="gray94", 
                            command=lambda: show_frame(harvest))
harvest_log.pack(padx=10, pady=10,)

task_log  = dep.ctk.CTkButton(data_logging, 
                          text="Task Log", 
                          text_color="black", 
                          fg_color="white", 
                          hover_color="gray94", 
                          command=lambda: show_frame(task))
task_log.pack(padx=10, pady=10,)

dep.ctk.CTkButton(data_logging, 
              text="Back To Main", 
              text_color="black", 
              fg_color="white", 
              hover_color="gray94", 
              command=lambda: show_frame(main)).pack(pady=10)

# Plant Log

plant = dep.tk.Frame(container)

dep.tk.Label(plant, text="Plant Log", font=title_font).pack(pady=(20, 10))

label_1 = dep.tk.Label(plant, text="Plant Type:")
label_1.pack(pady=5)

plant1 = dep.ctk.CTkEntry(plant)
plant1.pack(pady=5)

label_1 = dep.tk.Label(plant, text="Quantity:")
label_1.pack(pady=5)

plant2 = dep.ctk.CTkEntry(plant)
plant2.pack(pady=5)

dep.ctk.CTkButton(plant, 
                              text_color="black", 
                              fg_color="white", 
                              hover_color="gray94",
                              command=plant_submit, 
                              text="Submit",).pack(pady=5)

dep.ctk.CTkButton(plant, 
              text="Back",
              text_color="black", 
              fg_color="white", 
              hover_color="gray94", 
              command=lambda: show_frame(data_logging)).pack()

# Harvest Log

harvest = dep.tk.Frame(container)

dep.tk.Label(harvest, text="Harvest Log", font=title_font).pack(pady=(20, 10))

label_1 = dep.tk.Label(harvest, text="Item:")
label_1.pack(pady=5)

h1 = dep.ctk.CTkEntry(harvest)
h1.pack(pady=5)

label_1 = dep.tk.Label(harvest, text="Quantity:")
label_1.pack(pady=5)

h2 = dep.ctk.CTkEntry(harvest)
h2.pack(pady=5)

dep.ctk.CTkButton(harvest, 
                              text_color="black", 
                              fg_color="white", 
                              hover_color="gray94", 
                              command=harvest_submit, 
                              text="Submit",).pack(pady=5)

dep.ctk.CTkButton(harvest, 
              text="Back", 
              text_color="black", 
              fg_color="white", 
              hover_color="gray94", 
              command=lambda: show_frame(data_logging)).pack()

# Task Log
task = dep.tk.Frame(container)

dep.tk.Label(task, text="Task Log", font=title_font).pack(pady=(20, 10))

dep.tk.Label(task, text="Task Complete:").pack(pady=5)

tasks = dep.ctk.CTkEntry(task)
tasks.pack(pady=5)

dep.ctk.CTkButton(task, 
                              text_color="black", 
                              fg_color="white", 
                              hover_color="gray94", 
                              command=task_submit, 
                              text="Submit",).pack(pady=5)

dep.ctk.CTkButton(task, 
              text="Back", 
              text_color="black", 
              fg_color="white", 
              hover_color="gray94", 
              command=lambda: show_frame(data_logging)).pack()

################
# Farm Inventory
################

farm_inventory = dep.tk.Frame(container)

dep.tk.Label(farm_inventory, text="Farm_Inventory", font=title_font).pack(pady=(20, 10))

tool_frame = dep.ctk.CTkButton(farm_inventory, 
                            text="Tools", 
                            text_color="black", 
                            fg_color="white", 
                            hover_color="gray94", 
                            command=lambda: show_frame(tool_supply))
tool_frame.pack(padx=10, pady=10)

farm_supply_frame = dep.ctk.CTkButton(farm_inventory, 
                            text="Farm Supply", 
                            text_color="black", 
                            fg_color="white", 
                            hover_color="gray94", 
                            command=lambda: show_frame(farm_supply))
farm_supply_frame.pack(padx=10, pady=10)

animal_supply_frame = dep.ctk.CTkButton(farm_inventory, 
                            text="Animal Supply", 
                            text_color="black", 
                            fg_color="white", 
                            hover_color="gray94", 
                            command=lambda: show_frame(animal_supply))
animal_supply_frame.pack(padx=10, pady=10)

dep.ctk.CTkButton(farm_inventory, 
              text="Back To Main", 
              text_color="black", 
              fg_color="white", 
              hover_color="gray94", 
              command=lambda: show_frame(main)).pack(pady=10)

# Tool Supply entry Frame

tool_supply = dep.tk.Frame(container)

dep.tk.Label(tool_supply, text="Tool Supply", font=title_font).pack(pady=(20, 10))

dep.tk.Label(tool_supply, text="Tool Type").pack(pady=5)

t1 = dep.ctk.CTkEntry(tool_supply)
t1.pack(pady=5)

dep.tk.Label(tool_supply, text="Quantity").pack(pady=5)

t2 = dep.ctk.CTkEntry(tool_supply)
t2.pack(pady=5)

dep.ctk.CTkButton(tool_supply, 
                              text_color="black", 
                              fg_color="white", 
                              hover_color="gray94", 
                              text="Submit",
                              command=tool_submit).pack(pady=5)

dep.ctk.CTkButton(tool_supply, 
              text="Back", 
              text_color="black", 
              fg_color="white", 
              hover_color="gray94", 
              command=lambda: show_frame(farm_inventory)).pack()


# Farm Supply entry Frame

farm_supply = dep.tk.Frame(container)

dep.tk.Label(farm_supply, text="Farm Supply", font=title_font).pack(pady=(20, 10))

dep.tk.Label(farm_supply, text="Item").pack(pady=5)

f1 = dep.ctk.CTkEntry(farm_supply)
f1.pack(pady=5)

dep.tk.Label(farm_supply, text="Quantity").pack(pady=5)

f2 = dep.ctk.CTkEntry(farm_supply)
f2.pack(pady=5)

dep.ctk.CTkButton(farm_supply, 
                              text_color="black", 
                              fg_color="white", 
                              hover_color="gray94",
                              text="Submit",
                              command=farm_supply_submit).pack(pady=5)

dep.ctk.CTkButton(farm_supply, 
              text="Back", 
              text_color="black", 
              fg_color="white", 
              hover_color="gray94", 
              command=lambda: show_frame(farm_inventory)).pack()

# Animal Supply entry Frame

animal_supply = dep.tk.Frame(container)

dep.tk.Label(animal_supply, text="Animal Supply", font=title_font).pack(pady=(20, 10))

dep.tk.Label(animal_supply, text="Item").pack(pady=5)

a1 = dep.ctk.CTkEntry(animal_supply)
a1.pack(pady=5)

dep.tk.Label(animal_supply, text="Price").pack(pady=5)

a2 = dep.ctk.CTkEntry(animal_supply)
a2.pack(pady=5)

dep.ctk.CTkButton(animal_supply, 
                              text_color="black", 
                              fg_color="white", 
                              hover_color="gray94",
                              text="Submit",
                              command=animal_supply_submit).pack(pady=5)

dep.ctk.CTkButton(animal_supply, 
              text="Back", 
              text_color="black", 
              fg_color="white", 
              hover_color="gray94", 
              command=lambda: show_frame(farm_inventory)).pack()


###################
# Run time funtions
###################
for frame in (login, create, 
              main, data_logging, 
              plant, harvest, task, 
              farm_inventory, tool_supply, 
              farm_supply, animal_supply):
    frame.grid(row=0, column=0, sticky="nsew")
    
# Sets current user to load .json file
current_user = load_session()

# Checks for session file
if current_user:
    # If a session exists, skip login and go straight to main frame
    show_frame(main)
else:
    # Otherwise, stay on login frame
    show_frame(login)

conn.commit()
root.mainloop()
conn.close()