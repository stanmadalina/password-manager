from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    password_list = password_letters + password_numbers + password_symbols

    random.shuffle(password_list)

    password = "".join(password_list)
    pyperclip.copy(password)
    password_entry.delete(0, END)
    password_entry.insert(0, password)

    # print(f"Your password is: {password}")


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    site = web_entry.get()
    email = cred_entry.get()
    password = password_entry.get()

    # validate data
    data = {site: {
        "email": email,
        "password": password
    }
    }

    if len(site) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning!", message="Some fields are empty!")
    else:
        try:
            with open("passwords.json", "r") as f:
                # get data
                json_data = json.load(f)
        except FileNotFoundError:
            # messagebox.showerror(title="Error!", message="The file doesn't exist")
            with open("passwords.json", "w") as f:
                # write update data
                json.dump(data, f, indent=4)
        except json.decoder.JSONDecodeError:
            with open("passwords.json", "w") as f:
                json.dump(data, f, indent=4)
        else:
            # update data
            json_data.update(data)
            with open("passwords.json", "w") as f:
                # write update data
                json.dump(json_data, f, indent=4)
        finally:
            web_entry.delete(0, END)
            cred_entry.delete(0, END)
            password_entry.delete(0, END)
        messagebox.showinfo(message="Data was saved successfully!")


# ---------------------------- SEARCH ------------------------------- #


def search():
    website = web_entry.get()
    clear_fields()
    web_entry.insert(0, website)
    if len(website) > 0:
        try:
            with open("passwords.json", "r") as file:
                data = json.load(file)
            password = data[website]["password"]
            email = data[website]["email"]
        except FileNotFoundError:
            save()
        except KeyError:
            messagebox.showerror(title="Error!", message="No details for the website are saved.")
        except json.decoder.JSONDecodeError:
            messagebox.showerror(title="Error!", message="No data saved just yet!")
        else:
            cred_entry.insert(0, email)
            password_entry.config(show="")
            password_entry.insert(0, password)
            pyperclip.copy(password)
    else:
        messagebox.showwarning(message="No website entered!")


# ---------------------------- DELETE FILE ------------------------------- #
def delete_file():
    mes = "This operation will delete all saved passwords. Are you sure?"
    ok = messagebox.showwarning(message=mes)
    if ok.lower() == "ok":
        open("passwords.json", "w").close()


# ---------------------------- CLEAR SITE DATA ------------------------------- #


def clear_site():
    website = web_entry.get()
    print(website)
    if len(website) > 0:
        try:
            with open("passwords.json", "r") as file:
                data = json.load(file)
                print(data[website])
                data.pop(website, None)
            with open("passwords.json", "w") as file:
                json.dump(data, file, indent=4)
                messagebox.showinfo(message="Site data successfully removed!")
        except:
            messagebox.showwarning(message="The password file is empty or does not exist. Enter data and click \"Add\"")
    else:
        messagebox.showwarning(message="Please enter the website you want to clear data from.")


def tutorial():
    messagebox.showinfo(title="Tutorial", message='''
    Welcome to the password manager! 
    This is a quick guide to the functionalities of this app.
    
    Search button
        -enter the website you wish to see the email and password to
        
    Clear site data
        -enter the website you wish to clear data from
    
    Generate password
        -automatically generates a strong password
    
    Add
        -saves the credentials
    
    Delete
        -deletes all the saved credentials
        
    Hope you find this useful!
    ''')


def clear_fields():
    web_entry.delete(0, 'end')
    password_entry.delete(0, 'end')
    cred_entry.delete(0, 'end')

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password manager")
window.config(padx=20, pady=20)
LOCK = r'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'
canvas = Canvas(width=200, height=200)
lock = PhotoImage(data=LOCK)
canvas.create_image(100, 100, image=lock)
canvas.grid(column=2, row=0)

# website label:
web = Label(text="Website")
web.grid(column=1, row=1)
web.config(padx=5, pady=10)

# password label
password_label = Label(text="Password")
password_label.grid(column=1, row=3)
password_label.config(padx=5, pady=10)

# credentials label
cred = Label(text="Email")
cred.grid(column=1, row=2)
cred.config(padx=5, pady=10)

# website entry
web_entry = Entry(width=38)
web_entry.focus()
web_entry.grid(column=2, row=1)

# credentials entry
cred_entry = Entry(width=38)
cred_entry.grid(column=2, row=2)

# password entry
password_entry = Entry(width=38, show="*")
password_entry.grid(column=2, row=3)


# add button
add = Button(text="Add", command=save)
add.grid(column=2, row=4)
add.config(width=30)

# search button
search = Button(text="Search", command=search)
search.grid(column=4, row=1)
search.config(width=18)

# clear site data
clear = Button(text="Clear site data", command=clear_site)
clear.grid(column=4, row=4)
clear.config(width=18)

# generate password button
gen = Button(text="Generate password", command=generate_password)
gen.grid(column=4, row=3)
gen.config(width=18)


# delete file data button
delete_button = Button(text="Delete", command=delete_file)
delete_button.grid(column=2, row=6)
delete_button.config(width=10, bg="red")

# clear fields
clear = Button(text="Clear fields", command=clear_fields)
clear.grid(column=4, row=2)
clear.config(width=18)

# tutorial button
tut = Button(text="Tutorial", command=tutorial)
tut.grid(column=0, row=6)
tut.config(width=10)
window.mainloop()
