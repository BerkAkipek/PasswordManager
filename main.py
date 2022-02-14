from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 
            'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 
            'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    choosen_letters = [choice(letters) for _ in range(randint(8, 10))]
    choosen_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    choosen_numbers = [choice(numbers) for _ in range(randint(2, 4))]
    password_list = choosen_letters + choosen_symbols + choosen_numbers
    shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_data():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "Email": email,
            "Password": password
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't left any tab empty.")
    else:
        is_okay_to_save  = messagebox.askokcancel(title="Warning", message=f"Website: {website}\nEmail/Username: {email}\n"
                f"Password: {password}\nIs it okay to save?")
        if is_okay_to_save:
            try:
                with open(file="data.json", mode="r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open(file="data.json", mode="w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open(file="data.json", mode="w") as file:
                    json.dump(data, file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get().title()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="There is no data file exists.")
    else:
        if website in data:
            email = data[website]["Email"]
            password = data[website]["Password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"There is no entry about{website}")

# ---------------------------- UI SETUP ------------------------------- #
# Matrix[rows, columns, depth]
screen = Tk()
screen.title("Password Manager")
screen.config(padx=50, pady=50, bg="white")
# screen.geometry("500x400")

canvas = Canvas(bg="white", height=200, width=200, highlightthickness=0)
password_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=password_img)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website", bg="white")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username", bg="white")
email_label.grid(column=0, row=2)
password_label = Label(text="Password", bg="white")
password_label.grid(column=0, row=3)

# Entries
website_entry = Entry(width=21, highlightthickness=0)
website_entry.grid(column=1, row=1, sticky="ew")
website_entry.focus()
email_entry = Entry(width=32, highlightthickness=0)
email_entry.grid(column=1, row=2, columnspan=2, sticky="ew")
email_entry.insert(0, "example@email.com")
password_entry = Entry(width=21, highlightthickness=0)
password_entry.grid(column=1, row=3, sticky="ew")

# Buttons
search_button = Button(text="Search", bg="white", highlightthickness=0, command=find_password)
search_button.grid(column=2, row=1, sticky="EW")
generate_password_button = Button(text="Generate Password", bg="white", highlightthickness=0, command=password_generator)
generate_password_button.grid(column=2, row=3)
add_button = Button(text="Add", bg="white", highlightthickness=0, width=33, command=save_data)
add_button.grid(column=1, row=4, columnspan=2, sticky="ew")

screen.mainloop()
