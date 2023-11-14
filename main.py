from tkinter import *
from tkmacosx import Button
from tkinter import messagebox
import random
import pyperclip
import json

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)


# ---------------------------- SEARCH SAVED WEBSITE ----------------------------- #

def find_password():
    website_input = website_entry.get()
    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website_input in data:
            email = data[website_input]['email']
            password = data[website_input]['password']
            messagebox.showinfo(title=website_input, message=f"Email: {email}\n"
                                                             f"Password: {password}")
        else:
            messagebox.showinfo(title="Error", message="No details for the website exists")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for letter in range(nr_letters)]
    password_list += [random.choice(symbols) for symbol in range(nr_symbols)]
    password_list += [random.choice(numbers) for number in range(nr_numbers)]

    random.shuffle(password_list)
    password = "".join(password_list)
    pyperclip.copy(password)
    password_entry.delete(0, END)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website_input = website_entry.get()
    email_input = user_entry.get()
    password_input = password_entry.get()
    new_data = {
        website_input: {
            "email": email_input,
            "password": password_input,
        }
    }
    if len(website_input) == 0 or len(email_input) == 0 or len(password_input) == 0:
        messagebox.showinfo(title="oopps", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", mode="r") as data_file:
                data = json.load(data_file)
                print(data)
        except FileNotFoundError:
            with open("data.json", mode="w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #

canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

user_label = Label(text="Email/Username:")
user_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

website_entry = Entry(width=20)
website_entry.grid(column=1, row=1)
website_entry.focus()

search_btn = Button(text="Search", bg="grey", width=135, borderless=1, command=find_password)
search_btn.grid(column=2, row=1)

user_entry = Entry(width=35)
user_entry.grid(column=1, row=2, columnspan=2)
user_entry.insert(0, "example@gmail.com")

password_entry = Entry(width=20)
password_entry.grid(column=1, row=3)

generate_btn = Button(text="Generate Password", bg="grey", width=135, borderless=1, command=generate_password)
generate_btn.grid(column=2, row=3)

add_btn = Button(text="Add", width=329, bg="grey", borderless=1, command=save_password)
add_btn.grid(column=1, row=4, columnspan=2)

window.mainloop()
