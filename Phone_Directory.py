#note- tree=table in the code
import os           #os a module that is responsible for interacting with operating system, in this case to interact with contact file saved on computer
from tkinter import Tk, Label, Entry, Button, messagebox, Toplevel, filedialog      #to import required component in GUI
from tkinter.ttk import Treeview            #is a more advanced version of the standard `tkinter` `Treeview`

def insert_data():      #function called when pressed insert button by the user
    name = entry_name.get().strip()         
    email = entry_email.get().strip()       #strip= to remove whitespaces                
    contact = entry_contact.get().strip()           #get gets the data and save it in the table
    gender = entry_gender.get().strip()

    if not name:
        messagebox.showerror("Error", "Please enter a name.")
        return                  #Restriction for name

    if not email or "@" not in email:
        messagebox.showerror("Error", "Please enter a valid email address.")
        return          #Restriction for phone number

    if not contact.isdigit() or len(contact) != 11:
        messagebox.showerror("Error", "Please enter a valid 11-digit contact number.")
        return                  #Restriction for contact

    if gender.lower() not in ("male", "female", "other"):
        messagebox.showerror("Error", "Please enter a valid gender (Male, Female, Other).")         #Restriction for gender
        return

    with open("contacts.txt", "a") as file:
        file.write(f"Name: {name}\n")
        file.write(f"Email: {email}\n")             #File handling: Writes the email into the file, prefixed with "Email: " and then insert data from a newline.
        file.write(f"Contact: {contact}\n")
        file.write(f"Gender: {gender}\n")
        file.write("\n")

    messagebox.showinfo("Success", "Contact data inserted successfully.")       #messagebox displayed on successfull insertion if user passes all the restriction

    entry_name.delete(0, "end")
    entry_email.delete(0, "end")
    entry_contact.delete(0, "end")              #Clears the text in the selected widget.
    entry_gender.delete(0, "end")

def open_contact_info():                #Function called on clicking the button
    contact_window = Toplevel()         #toplevel-Creates a new window
    contact_window.title("Phone Directory")     #title of window
    tree = Treeview(contact_window, columns=("name", "email", "contact", "gender"), show="headings")            #Creates a `Treeview` widget with columns for displaying the contact data



    tree.heading("name", text="Name")
    tree.heading("email", text="Email")
    tree.heading("contact", text="Contact Number")          #Sets the heading of the "contact" column in the `tree` widget to "Contact Number" n others respectively
    tree.heading("gender", text="Gender")

    file_path = "contacts.txt"          #filepath definition
    if os.path.exists(file_path):               #use of os module- checks the file existence
        with open(file_path, "r") as file:              #opens file & Reads all the lines from the file and stores them in the `lines` list.
            lines = file.readlines()
            
            


#Use of bubble sorting to sort data
        sorted_data = []            #Initializes an empty list `sorted_data` to store the sorted contact data.
        person_data = {}               #empty dictionary-to store the data for a single contact.
        for line in lines:      #iterating in terms of lines
            line = line.strip()         #removes extra lines
            if line.startswith("Name:"):                #Checks if the line starts with "Name:".
                person_data["name"] = line.replace("Name:", "").strip()                     #Extracts the name from the line and assigns it to the "name" key in the `person_data` dictionary.
            elif line.startswith("Email:"):
                person_data["email"] = line.replace("Email:", "").strip()
            elif line.startswith("Contact:"):
                person_data["contact"] = line.replace("Contact:", "").strip()
            elif line.startswith("Gender:"):
                person_data["gender"] = line.replace("Gender:", "").strip()
                sorted_data.append(person_data)
                person_data = {}

#bubble sorting the data
        n = len(sorted_data)        #Assigns the number of contact entries in `sorted_data` to the variable `n`.
        for i in range(n - 1):          #Outer loop-iterates n-1 times
            for j in range(0, n - i - 1):           #Inner loop-iterates from 0 to `n-i-1`.
                if sorted_data[j]["name"] > sorted_data[j + 1]["name"]:             #Compares the names of adjacent contact entries in `sorted_data`
                    sorted_data[j], sorted_data[j + 1] = sorted_data[j + 1], sorted_data[j]                 #Swaps the positions of the contact entries if the names are out of order.-bubble sort work

        for person_data in sorted_data:                 #Iterates over the sorted contact data in `sorted_data`.
            tree.insert("", "end", values=(person_data["name"], person_data["email"], person_data["contact"], person_data["gender"]))           #Inserts a row in the `tree` widget

    tree.pack()         #Displays the `tree` widget in the `contact_window`

    def delete_person():            #delete dunction called when clicked delete
        selected_item = tree.selection()                #Gets the currently selected item in the tree
        if not selected_item:
            messagebox.showerror("Error", "Please select a person to delete.")
            return      #if row not selected error msg

        person_data = tree.item(selected_item)["values"]        
        name = person_data[0]

        for i, data in enumerate(sorted_data):
            if data["name"] == name:            #deleting the value from sorted data
                sorted_data.pop(i)
                break

        with open(file_path, "w") as file:
            for person_data in sorted_data:
                file.write(f"Name: {person_data['name']}\n")
                file.write(f"Email: {person_data['email']}\n")
                file.write(f"Contact: {person_data['contact']}\n")
                file.write(f"Gender: {person_data['gender']}\n")
                file.write("\n")

        tree.delete(selected_item)
        messagebox.showinfo("Success", "Person's data deleted successfully!")

    def save_data():
        if not sorted_data:
            messagebox.showerror("Error", "No contact data to save.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if save_path:
            with open(save_path, "w") as file:
                for person_data in sorted_data:
                    file.write(f"Name: {person_data['name']}\n")
                    file.write(f"Email: {person_data['email']}\n")
                    file.write(f"Contact: {person_data['contact']}\n")
                    file.write(f"Gender: {person_data['gender']}\n")
                    file.write("\n")

            messagebox.showinfo("Success", "Contact data saved successfully.")
#edit button-same work as delete button
    def edit_person():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a person to edit.")
            return

        person_data = tree.item(selected_item)["values"]
        name = person_data[0]

        for i, data in enumerate(sorted_data):
            if data["name"] == name:
                edit_window = Toplevel()
                edit_window.title("EDIT CONTACT INFO")   #window defining that display on clicking edit button

                Label(edit_window, text="Name:", font="8").grid(row=0, column=0, sticky="w")
                Label(edit_window, text="Email:", font="8").grid(row=1, column=0, sticky="w")
                Label(edit_window, text="Contact Number:", font="8").grid(row=2, column=0, sticky="w")
                Label(edit_window, text="Gender:", font="8").grid(row=3, column=0, sticky="w")

                entry_name = Entry(edit_window, font="10", width=30)
                entry_name.grid(row=0, column=1)
                entry_name.insert(0, data["name"])

                entry_email = Entry(edit_window, font="10", width=30)
                entry_email.grid(row=1, column=1)
                entry_email.insert(0, data["email"])

                entry_contact = Entry(edit_window, font="10", width=30)
                entry_contact.grid(row=2, column=1)
                entry_contact.insert(0, data["contact"])

                entry_gender = Entry(edit_window, font="10", width=30)
                entry_gender.grid(row=3, column=1)
                entry_gender.insert(0, data["gender"])

                def save_edit():
                    new_name = entry_name.get().strip()
                    new_email = entry_email.get().strip()
                    new_contact = entry_contact.get().strip()
                    new_gender = entry_gender.get().strip()

                    if not new_name:
                        messagebox.showerror("Error", "Please enter a name.")
                        return

                    if not new_email or "@" not in new_email:
                        messagebox.showerror("Error", "Please enter a valid email address.")
                        return

                    if not new_contact.isdigit() or len(new_contact) != 11:
                        messagebox.showerror("Error", "Please enter a valid 11-digit contact number.")
                        return

                    if new_gender.lower() not in ("male", "female", "other"):
                        messagebox.showerror("Error", "Please enter a valid gender (Male, Female, Other).")
                        return

                    sorted_data[i]["name"] = new_name           #Updates the name in the sorted data
                    sorted_data[i]["email"] = new_email
                    sorted_data[i]["contact"] = new_contact
                    sorted_data[i]["gender"] = new_gender

                    tree.item(selected_item, values=(new_name, new_email, new_contact, new_gender))         #Updates the values of the selected item in the `tree` widget with the edited contact data

                    with open(file_path, "w") as file:
                        for person_data in sorted_data:
                            file.write(f"Name: {person_data['name']}\n")
                            file.write(f"Email: {person_data['email']}\n")
                            file.write(f"Contact: {person_data['contact']}\n")
                            file.write(f"Gender: {person_data['gender']}\n")
                            file.write("\n")

                    messagebox.showinfo("Success", "Person's data updated successfully!")
                    edit_window.destroy()       #Closes the edit window.

                save_button = Button(edit_window, text="Save", font="6", command=save_edit)
                save_button.grid(row=4, column=1, pady=10)

                break

    delete_button = Button(contact_window, text="Delete", command=delete_person)
    delete_button.pack(side="left", padx=5, pady=10)

    save_button = Button(contact_window, text="Save", command=save_data)
    save_button.pack(side="right", padx=5, pady=10)

    edit_button = Button(contact_window, text="Edit", command=edit_person)
    edit_button.pack(side="top", anchor="center", padx=8, pady=10)

window = Tk()
window.title("Insert Contact Data")
window.geometry("600x500")
window.resizable(False, False)

Label(window, text="\nTelecom Registry\n", font="ariel 24 bold", fg="black").pack(fill="both")
label_name = Label(window, text="Name:", font="8")
label_name.pack()

entry_name = Entry(window, font="10", width=30)
entry_name.pack()

label_email = Label(window, text="Email:", font="8")
label_email.pack()

entry_email = Entry(window, font="10", width=30)
entry_email.pack()

label_contact = Label(window, text="Contact Number:", font="8")
label_contact.pack()

entry_contact = Entry(window, font="10", width=30)
entry_contact.pack()

label_gender = Label(window, text="Gender:", font="8")
label_gender.pack()

entry_gender = Entry(window, font="10", width=30)
entry_gender.pack()

button_insert = Button(window, text="Insert", font="6", command=insert_data)
button_insert.pack(pady=10)

button_view = Button(window, text="View Contacts", font="6", command=open_contact_info)
button_view.pack(pady=10)

window.mainloop()   #main event on loop so that user can interact
