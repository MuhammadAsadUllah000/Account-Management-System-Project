import tkinter as tk
from tkinter import ttk, simpledialog
import datetime


# Counter for generating unique 1-digit IDs
id_counter = 0

# Dictionary to store employee information
employees = {}

# Counter for generating unique 1-digit IDs for timetables
timetable_id_counter = 0

# Dictionary to store employee timetables
timetables = {}

attendance_records = {}

def generate_unique_id():
    global id_counter
    id_counter += 1
    return id_counter

def add_employee():
    global name_entry, experience_entry, designation_entry, salary_entry, address_entry, contact_entry, email_entry, result_display

    name = name_entry.get()
    experience = experience_entry.get()
    designation = designation_entry.get()
    salary = salary_entry.get()
    home_address = address_entry.get()
    contact_number = contact_entry.get()
    email = email_entry.get()

    if not all([name, experience, designation, salary, home_address, contact_number, email]):
        result_display.delete(1.0, tk.END)
        result_display.insert(tk.END, "All fields are required!")
        return

    id = generate_unique_id()  # Generate a unique ID
    employees[id] = {
        'Name': name,
        'Experience': experience,
        'Designation': designation,
        'Salary': salary,
        'Personal Information': {
            'Home Address': home_address,
            'Contact Number': contact_number,
            'Email': email
        }
    }

    # Clear entry fields after adding employee
    name_entry.delete(0, tk.END)
    experience_entry.delete(0, tk.END)
    designation_entry.delete(0, tk.END)
    salary_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    contact_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)

def search_employee_by_name():
    global result_display

    name_to_search = simpledialog.askstring("Search Employee", "Enter employee name:")
    if name_to_search:
        found = False
        for emp_id, emp_info in employees.items():
            if emp_info['Name'] == name_to_search:
                display_employee_info(emp_id, emp_info)
                found = True
                break
        if not found:
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, f"No employee found with the name '{name_to_search}'\n")

def search_employee_by_id():
    global result_display

    id_to_search = simpledialog.askinteger("Search Employee", "Enter employee ID:")
    if id_to_search:
        emp_info = employees.get(id_to_search)
        if emp_info:
            display_employee_info(id_to_search, emp_info)
        else:
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, f"No employee found with the ID '{id_to_search}'\n")

def display_employee_info(emp_id, emp_info):
    global result_display

    result_display.delete(1.0, tk.END)
    result_display.insert(tk.END, f"ID: {emp_id}\n")
    for key, value in emp_info.items():
        if key == 'Personal Information':
            result_display.insert(tk.END, f"{key}:\n")
            for info_key, info_value in value.items():
                result_display.insert(tk.END, f"\t{info_key}: {info_value}\n")
        else:
            result_display.insert(tk.END, f"{key}: {value}\n")

def edit_employee():
    global result_display

    id_to_edit = simpledialog.askinteger("Edit Employee Data", "Enter employee ID:")
    if id_to_edit:
        emp_info = employees.get(id_to_edit)
        if emp_info:
            edit_employee_window = tk.Toplevel(root)
            edit_employee_window.title(f"Edit Employee Data {id_to_edit}")

            name_var = tk.StringVar(value=emp_info['Name'])
            experience_var = tk.StringVar(value=emp_info['Experience'])
            designation_var = tk.StringVar(value=emp_info['Designation'])
            salary_var = tk.StringVar(value=emp_info['Salary'])
            address_var = tk.StringVar(value=emp_info['Personal Information']['Home Address'])
            contact_var = tk.StringVar(value=emp_info['Personal Information']['Contact Number'])
            email_var = tk.StringVar(value=emp_info['Personal Information']['Email'])

            ttk.Label(edit_employee_window, text="Name:", font=font_style).grid(row=0, column=0, padx=5, pady=5, sticky='e')
            ttk.Entry(edit_employee_window, font=font_style, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)

            ttk.Label(edit_employee_window, text="Experience:", font=font_style).grid(row=1, column=0, padx=5, pady=5, sticky='e')
            ttk.Entry(edit_employee_window, font=font_style, textvariable=experience_var).grid(row=1, column=1, padx=5, pady=5)

            ttk.Label(edit_employee_window, text="Designation:", font=font_style).grid(row=2, column=0, padx=5, pady=5, sticky='e')
            ttk.Entry(edit_employee_window, font=font_style, textvariable=designation_var).grid(row=2, column=1, padx=5, pady=5)

            ttk.Label(edit_employee_window, text="Salary:", font=font_style).grid(row=3, column=0, padx=5, pady=5, sticky='e')
            ttk.Entry(edit_employee_window, font=font_style, textvariable=salary_var).grid(row=3, column=1, padx=5, pady=5)

            ttk.Label(edit_employee_window, text="Home Address:", font=font_style).grid(row=4, column=0, padx=5, pady=5, sticky='e')
            ttk.Entry(edit_employee_window, font=font_style, textvariable=address_var).grid(row=4, column=1, padx=5, pady=5)

            ttk.Label(edit_employee_window, text="Contact Number:", font=font_style).grid(row=5, column=0, padx=5, pady=5, sticky='e')
            ttk.Entry(edit_employee_window, font=font_style, textvariable=contact_var).grid(row=5, column=1, padx=5, pady=5)

            ttk.Label(edit_employee_window, text="Email Address:", font=font_style).grid(row=6, column=0, padx=5, pady=5, sticky='e')
            ttk.Entry(edit_employee_window, font=font_style, textvariable=email_var).grid(row=6, column=1, padx=5, pady=5)

            def save_changes():
                employees[id_to_edit]['Name'] = name_var.get()
                employees[id_to_edit]['Experience'] = experience_var.get()
                employees[id_to_edit]['Designation'] = designation_var.get()
                employees[id_to_edit]['Salary'] = salary_var.get()
                employees[id_to_edit]['Personal Information']['Home Address'] = address_var.get()
                employees[id_to_edit]['Personal Information']['Contact Number'] = contact_var.get()
                employees[id_to_edit]['Personal Information']['Email'] = email_var.get()
                edit_employee_window.destroy()

            save_button = ttk.Button(edit_employee_window, text="Save Changes", command=save_changes)
            save_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)

        else:
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, f"No employee found with the ID '{id_to_edit}'\n")

def generate_unique_timetable_id():
    global timetable_id_counter
    timetable_id_counter += 1
    return timetable_id_counter

def add_timetable():
    global id_entry, result_display, monday_var, tuesday_var, wednesday_var, thursday_var, friday_var

    emp_id = id_entry.get()
    working_hours = [monday_var.get(), tuesday_var.get(), wednesday_var.get(), thursday_var.get(), friday_var.get()]

    if not all([emp_id, *working_hours]):
        result_display.delete(1.0, tk.END)
        result_display.insert(tk.END, "Employee ID and all working hours are required!")
        return

    emp_id = int(emp_id)
    if emp_id not in employees:
        result_display.delete(1.0, tk.END)
        result_display.insert(tk.END, f"No employee found with ID '{emp_id}'")
        return

    if emp_id in timetables:
        timetables[emp_id].extend(working_hours)
    else:
        timetables[emp_id] = working_hours

    result_display.delete(1.0, tk.END)
    result_display.insert(tk.END, "Working hours added successfully!")

    # Clear entry fields
    id_entry.delete(0, tk.END)
    monday_var.delete(0, tk.END)
    tuesday_var.delete(0, tk.END)
    wednesday_var.delete(0, tk.END)
    thursday_var.delete(0, tk.END)
    friday_var.delete(0, tk.END)

    display_employee_timetable(emp_id)


def display_employee_timetable():
    global result_display

    emp_id = simpledialog.askinteger("Display Timetable", "Enter employee ID:")
    if emp_id:
        if emp_id in employees:
            emp_info = employees[emp_id]
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, f"\nEmployee Name: {emp_info['Name']}\n")
            if emp_id in timetables:
                result_display.insert(tk.END, f"Timetable for Employee ID {emp_id}:\n")
                days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
                timetable = timetables[emp_id]
                for day, hours in zip(days, timetable):
                    result_display.insert(tk.END, f"{day}: {hours}\n")
            else:
                result_display.insert(tk.END, f"No timetable found for Employee ID {emp_id}\n")
        else:
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, f"No employee found with the ID '{emp_id}'\n")
def open_attendance_window():
    record_attendance()

def record_attendance():
    global id_entry, present_var, absent_var, result_display

    attendance_window = tk.Toplevel(root)
    attendance_window.title("Record Attendance")

    ttk.Label(attendance_window, text="Enter Employee ID*:", font=font_style).grid(row=0, column=0, padx=(5, 2), pady=5, sticky='e')
    id_entry = ttk.Entry(attendance_window, font=font_style)
    id_entry.grid(row=0, column=1, padx=(2, 5), pady=5)
    ttk.Label(attendance_window, text="*", font=font_style, foreground="red").grid(row=0, column=2, padx=5, pady=5, sticky='w')

    present_var = tk.BooleanVar(value=False)  # Initialize as False
    absent_var = tk.BooleanVar(value=False)   # Initialize as False

    ttk.Checkbutton(attendance_window, text="Present", variable=present_var).grid(row=1, column=0, padx=5, pady=5, sticky='w')
    ttk.Checkbutton(attendance_window, text="Absent", variable=absent_var).grid(row=2, column=0, padx=5, pady=5, sticky='w')

    def display_attendance():
        emp_id = id_entry.get()
        if emp_id:
            emp_id = int(emp_id)
            if emp_id in employees:
                result_display.delete(1.0, tk.END)
                if emp_id in attendance_records:
                    result_display.insert(tk.END, f"Attendance Record for Employee ID {emp_id}:\n")
                    for date, status in attendance_records[emp_id].items():
                        result_display.insert(tk.END, f"Date: {date}, Status: {status}\n")
                else:
                    result_display.insert(tk.END, f"No attendance record found for Employee ID {emp_id}\n")
            else:
                result_display.delete(1.0, tk.END)
                result_display.insert(tk.END, f"No employee found with ID '{emp_id}'\n")
        else:
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, "Please enter Employee ID\n")

    display_button = ttk.Button(attendance_window, text="Display Attendance", command=display_attendance)
    display_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    result_display = tk.Text(attendance_window, height=5, width=40)
    result_display.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    def save_attendance():
        emp_id = id_entry.get()
        present = present_var.get()
        absent = absent_var.get()

        if emp_id and (present or absent):
            emp_id = int(emp_id)
            if emp_id in employees:
                attendance = "Present" if present else "Absent"
                result_display.delete(1.0, tk.END)
                result_display.insert(tk.END, f"Attendance for Employee ID {emp_id}: {attendance}\n")
                # Add attendance record
                if emp_id not in attendance_records:
                    attendance_records[emp_id] = {}
                today = datetime.date.today().isoformat()
                attendance_records[emp_id][today] = "Present" if present else "Absent"
            else:
                result_display.delete(1.0, tk.END)
                result_display.insert(tk.END, f"No employee found with ID '{emp_id}'\n")
        else:
            result_display.delete(1.0, tk.END)
            result_display.insert(tk.END, "Please enter Employee ID and select either 'Present' or 'Absent'\n")

    save_button = ttk.Button(attendance_window, text="Save Attendance", command=save_attendance)
    save_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    
def open_add_staffing_window():
    global name_entry, experience_entry, designation_entry, salary_entry, address_entry, contact_entry, email_entry, result_display

    add_staffing_window = tk.Toplevel(root)
    add_staffing_window.title("Add Staffing")

    # Labels and Entry fields with red asterisks
    ttk.Label(add_staffing_window, text="Name*:", font=font_style).grid(row=0, column=0, padx=5, pady=5, sticky='e')
    name_entry = ttk.Entry(add_staffing_window, font=font_style)
    name_entry.grid(row=0, column=1, padx=5, pady=5)
    ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=0, column=2, padx=5, pady=5, sticky='w')

    ttk.Label(add_staffing_window, text="Experience*:", font=font_style).grid(row=1, column=0, padx=5, pady=5, sticky='e')
    experience_entry = ttk.Entry(add_staffing_window, font=font_style)
    experience_entry.grid(row=1, column=1, padx=5, pady=5)
    ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=1, column=2, padx=5, pady=5, sticky='w')

    ttk.Label(add_staffing_window, text="Designation*:", font=font_style).grid(row=2, column=0, padx=5, pady=5, sticky='e')
    designation_entry = ttk.Entry(add_staffing_window, font=font_style)
    designation_entry.grid(row=2, column=1, padx=5, pady=5)
    ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=2, column=2, padx=5, pady=5, sticky='w')

    ttk.Label(add_staffing_window, text="Salary*:", font=font_style).grid(row=3, column=0, padx=5, pady=5, sticky='e')
    salary_entry = ttk.Entry(add_staffing_window, font=font_style)
    salary_entry.grid(row=3, column=1, padx=5, pady=5)
    ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=3, column=2, padx=5, pady=5, sticky='w')

    personal_info_label = ttk.Label(add_staffing_window, text="Personal Information")
    personal_info_label.grid(row=4, column=0, columnspan=3, pady=5, sticky='w', padx=5)

    ttk.Label(add_staffing_window, text="Home Address*:", font=font_style).grid(row=5, column=0, padx=5, pady=5, sticky='e')
    address_entry = ttk.Entry(add_staffing_window, font=font_style)
    address_entry.grid(row=5, column=1, padx=5, pady=5)
    ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=5, column=2, padx=5, pady=5, sticky='w')

    ttk.Label(add_staffing_window, text="Contact Number*:", font=font_style).grid(row=6, column=0, padx=5, pady=5, sticky='e')
    contact_entry = ttk.Entry(add_staffing_window, font=font_style)
    contact_entry.grid(row=6, column=1, padx=5, pady=5)
    ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=6, column=2, padx=5, pady=5, sticky='w')

    ttk.Label(add_staffing_window, text="Email Address*:", font=font_style).grid(row=7, column=0, padx=5, pady=5, sticky='e')
    email_entry = ttk.Entry(add_staffing_window, font=font_style)
    email_entry.grid(row=7, column=1, padx=5, pady=5)
    ttk.Label(add_staffing_window, text="*", font=font_style, foreground="red").grid(row=7, column=2, padx=5, pady=5, sticky='w')

    add_button = ttk.Button(add_staffing_window, text="Add Employee", command=add_employee)
    add_button.grid(row=8, column=0, columnspan=3, padx=5, pady=5)

    search_by_name_button = ttk.Button(add_staffing_window, text="Search by Name", command=search_employee_by_name)
    search_by_name_button.grid(row=9, column=0, padx=5, pady=5)

    search_by_id_button = ttk.Button(add_staffing_window, text="Search by ID", command=search_employee_by_id)
    search_by_id_button.grid(row=9, column=1, padx=5, pady=5)

    result_display = tk.Text(add_staffing_window, height=10, width=40)
    result_display.grid(row=10, column=0, columnspan=3, padx=5, pady=5)

def open_timetable_window():
    global id_entry, result_display, monday_var, tuesday_var, wednesday_var, thursday_var, friday_var

    timetable_window = tk.Toplevel(root)
    timetable_window.title("Employee Timetable")

    ttk.Label(timetable_window, text="Enter Employee ID*:", font=font_style).grid(row=0, column=0, padx=(5, 2), pady=5, sticky='e')
    id_entry = ttk.Entry(timetable_window, font=font_style)
    id_entry.grid(row=0, column=1, padx=(2, 5), pady=5)
    ttk.Label(timetable_window, text="*", font=font_style, foreground="red").grid(row=0, column=2, padx=5, pady=5, sticky='w')

    ttk.Label(timetable_window, text="Working Hours:", font=font_style).grid(row=1, column=0, padx=(5, 2), pady=5, sticky='e')

    ttk.Label(timetable_window, text="Monday*:", font=font_style).grid(row=1, column=1, padx=(2, 5), pady=5, sticky='w')
    monday_var = ttk.Entry(timetable_window, font=font_style, width=8)
    monday_var.grid(row=1, column=2, padx=(2, 5), pady=5)
    ttk.Label(timetable_window, text="*", font=font_style, foreground="red").grid(row=1, column=3, padx=5, pady=5, sticky='w')

    ttk.Label(timetable_window, text="Tuesday*:", font=font_style).grid(row=1, column=4, padx=(2, 5), pady=5, sticky='w')
    tuesday_var = ttk.Entry(timetable_window, font=font_style, width=8)
    tuesday_var.grid(row=1, column=5, padx=(2, 5), pady=5)
    ttk.Label(timetable_window, text="*", font=font_style, foreground="red").grid(row=1, column=6, padx=5, pady=5, sticky='w')

    ttk.Label(timetable_window, text="Wednesday*:", font=font_style).grid(row=1, column=7, padx=(2, 5), pady=5, sticky='w')
    wednesday_var = ttk.Entry(timetable_window, font=font_style, width=8)
    wednesday_var.grid(row=1, column=8, padx=(2, 5), pady=5)
    ttk.Label(timetable_window, text="*", font=font_style, foreground="red").grid(row=1, column=9, padx=5, pady=5, sticky='w')

    ttk.Label(timetable_window, text="Thursday*:", font=font_style).grid(row=1, column=10, padx=(2, 5), pady=5, sticky='w')
    thursday_var = ttk.Entry(timetable_window, font=font_style, width=8)
    thursday_var.grid(row=1, column=11, padx=(2, 5), pady=5)
    ttk.Label(timetable_window, text="*", font=font_style, foreground="red").grid(row=1, column=12, padx=5, pady=5, sticky='w')

    ttk.Label(timetable_window, text="Friday*:", font=font_style).grid(row=1, column=13, padx=(2, 5), pady=5, sticky='w')
    friday_var = ttk.Entry(timetable_window, font=font_style, width=8)
    friday_var.grid(row=1, column=14, padx=(2, 5), pady=5)
    ttk.Label(timetable_window, text="*", font=font_style, foreground="red").grid(row=1, column=15, padx=5, pady=5, sticky='w')

    add_button = ttk.Button(timetable_window, text="Add Timetable", command=add_timetable)
    add_button.grid(row=2, column=0, columnspan=16, padx=5, pady=5)

    display_button = ttk.Button(timetable_window, text="Display Timetable", command=display_employee_timetable)
    display_button.grid(row=3, column=0, columnspan=16, padx=5, pady=5)

    result_display = tk.Text(timetable_window, height=10, width=60)
    result_display.grid(row=4, column=0, columnspan=16, padx=5, pady=5)


# Create main window
root = tk.Tk()
root.title("Employee Management System")

# Create font style
font_style = ('Arial', 12)

# Create menu bar
menu_bar = tk.Menu(root)

# Create File menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)

# Create Employee menu
employee_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Employee", menu=employee_menu)
employee_menu.add_command(label="Add Staffing", command=open_add_staffing_window)
employee_menu.add_command(label="Edit Staffing", command=edit_employee)

# Create Timetable menu
timetable_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Timetable", menu=timetable_menu)
timetable_menu.add_command(label="Employee Timetable", command=open_timetable_window)

# Create Attendance menu
attendance_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Attendance", menu=attendance_menu)
attendance_menu.add_command(label="Record Attendance", command=open_attendance_window)


# Set menu bar
root.config(menu=menu_bar)

# Start main event loop
root.mainloop()
