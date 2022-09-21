from tkinter import *
from tkinter import ttk
import tkcalendar as cal
import sqlite3
from tkinter import font
from PIL import Image, ImageTk


root = Tk()
root.title("Bikeztube")
root.state("zoomed")


#CREATE DATABASE TABLE or CONNECT
conn = sqlite3.connect('bikes.db')
#create cursor
c = conn.cursor()
#create table
c.execute("""CREATE TABLE IF NOT EXISTS bikes (
    name text,
    bike text,
    phone text,
    date text,
    comments text
)
""")

c.execute("""CREATE TABLE IF NOT EXISTS history (
    name text
    )
""")
#COMMIT CHANGES
conn.commit()
#CLOSE CONNECTION
conn.close()


#ADD BIKES FUNCTION
def add_bike():

    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute("INSERT INTO bikes VALUES (:name, :bike, :phone, :date , :comments)",
            {
                'name':name_entry.get(),
                'bike':bike_entry.get(),
                'phone':phone_entry.get(),
                'date':date_entry.get(),
                'comments':comments_entry.get("1.0",END)
            })

    conn.commit()
    conn.close()

    name_entry.delete(0, END)
    bike_entry.delete(0, END)
    phone_entry.delete(0, END)
    comments_entry.delete("1.0", END)
    cust_list.delete(0, END)
    query_database()


def query_database():

    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute('SELECT rowid, date, name, bike, phone, comments FROM bikes')

    records = c.fetchall()
    cust_list_from_sql = []

    for record in records:
        cust_list_from_sql.append(str(record[0])+".  "+record[1]+"-"+record[2]+"-"+str(record[3]+" | "+str(record[5])+" no~"+str(record[4])))

    for i in cust_list_from_sql:
        x=0
        cust_list.insert(x, i)
        x+1

    conn.commit()
    conn.close()


def delete_bike():

    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()

    id_to_delete = cust_list.get(cust_list.curselection())
    id_to_delete2 = id_to_delete.split('.')
    id_to_delete3 = id_to_delete2[0]

    c.execute("DELETE FROM bikes WHERE rowid=?", (id_to_delete3,))
    conn.commit()
    conn.close()

    cust_list.delete(0, END)
    query_database()


def grab_phone():

    phone = cust_list.get(cust_list.curselection())
    phone2 = phone.split('no~')
    ph = phone2[1] 

    root.clipboard_clear()
    root.clipboard_append(ph)

def copy_ready_text():

    rtext = str('Hello. This is Bikeztube. Your bicycle is ready for collection. We are open till 17:00 on weekdays and 16:00 on Saturdays. Please pick it up at your earliest convenience. Thank you!')

    root.clipboard_clear()
    root.clipboard_append(rtext)    

def fixed_bike():

    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()

    fixedBikeDetails = cust_list.get(cust_list.curselection())
    id_to_delete2 = fixedBikeDetails.split('.')

    id_to_delete = id_to_delete2[0]

    c.execute("DELETE FROM bikes WHERE rowid=?", (id_to_delete,))
    c.execute("INSERT INTO history VALUES (:name)",
            {
                'name':fixedBikeDetails
            })
    conn.commit()
    conn.close()

    cust_list.delete(0, END)
    query_database()


def ser_add_to_comments():
    x = ser_combo.get()
    x = x + ', '
    comments_entry.insert(END,x)
    
def parts_add_to_comments():
    x = parts_combo.get()
    x = x + ', '
    comments_entry.insert(END,x)   

def get_history():

    top = Toplevel(root) 
    top.state('zoomed') 

    hist_frame = LabelFrame(top, pady=10, text="Service History", padx=15,)
    hist_frame.pack(fill='both', expand=True, padx=20, pady=20)

    hist_list = Listbox(hist_frame, width=40, height=10, font=('Verdana', 15))
    hist_list.pack(side=LEFT, pady=0, fill='both', expand=True)

    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute('SELECT * FROM history')

    records = c.fetchall()
    hist_list_from_sql = []

    for record in records:
        hist_list_from_sql.append(record[0])

    for i in hist_list_from_sql:
        x=0
        hist_list.insert(x, i)
        x+1

    conn.commit()
    conn.close()

    top.mainloop()
    
#frame for listbox and entries
cust_frame = LabelFrame(root, pady=10, text="Bikes For Service", padx=15,)
cust_frame.pack(fill='both', expand=True, padx=20, pady=20)
cust_list = Listbox(cust_frame, width=40, height=10, font=('Verdana', 15))
cust_list.pack(side=LEFT, pady=0, fill='both', expand=True)

#Frame for all the entries
entries_frame = Frame(cust_frame, pady=10)
entries_frame.pack(fill='both', expand=True)

date_entry = cal.DateEntry(entries_frame, width=17, date_pattern='dd/MM/yyyy')
date_entry.grid(row=0, column=0, padx=10, pady=10)

name_label = Label(entries_frame, text="Name")
name_label.grid(row=1, column=0, pady=2, padx=10)

name_entry = Entry(entries_frame, font=(21))
name_entry.grid(row=2, column=0, pady=2, padx=10)

phone_label = Label(entries_frame, text="Phone")
phone_label.grid(row=3, column=0, pady=2, padx=10)

phone_entry = Entry(entries_frame, font=(21))
phone_entry.grid(row=4, column=0, pady=2, padx=10)

bike_label = Label(entries_frame, text="Bike")
bike_label.grid(row=5, column=0, pady=2, padx=10)

bike_entry = Entry(entries_frame, font=(21))
bike_entry.grid(row=6, column=0, pady=2, padx=10)

comments_label = Label(entries_frame, text="Comments")
comments_label.grid(row=7, column=0, pady=2, padx=10)

comments_frame = Frame(entries_frame)
comments_frame.grid(row=8, column=0, pady=2, padx=10)
comments_entry = Text(comments_frame, width=20, height=10, font=(21))

comments_entry.pack(fill='both', expand=True)

combo_frame = Frame(entries_frame)
combo_frame.grid(row=9, column=0, pady=2, padx=20)

comboValuesServices = ['+Basic Service', '+Second Service', '+Full Service']
comboValuesParts = ['+Inner tube R', '+Inner tube F', '+Tyre R', '+Tyre F', 
'+Brake Pads R', '+Brake Pads F', '+Chain', '+Cassette', '+Drivetrain', '+Derailleur R', 
'+Derailleur F', '+G. Shifter R', '+G. Shifter F', '+Cable(s)', '+Hanger', '+Brake Lever(s)',
'+Wheel R', '+Wheel F', '+Bleed', '+Other: ']


ser_frame = Frame(combo_frame)
ser_frame.pack(pady=15)

parts_frame = Frame(combo_frame)
parts_frame.pack()

bigfont = font.Font(family="Verdana",size=12)
root.option_add("*TCombobox*Listbox*Font", bigfont)

ser_combo = ttk.Combobox(ser_frame, values =comboValuesServices, state='readonly', font=('Verdana',10))
ser_combo.set('Basic Service')
ser_combo.grid(row=0, column=0)

add_button_plus = Button(ser_frame, text='+', command=ser_add_to_comments,  bg="yellow green", font=('Verdana',12, 'bold'), width=2)
add_button_plus.grid(row=1, column=0, sticky=W, pady=5)

parts_combo = ttk.Combobox(parts_frame, values =comboValuesParts, state='readonly', font=('Verdana',10))
parts_combo.set('Inner tube R')
parts_combo.grid(row=2, column=0)

add_button_plus = Button(parts_frame, text='+', command=parts_add_to_comments,  bg="yellow green", font=('Verdana',12, 'bold'), width=2)
add_button_plus.grid(row=3, column=0, sticky=W, pady=5)

add_button = Button(entries_frame, text="Add Bike",  bg="yellow green", command=add_bike, width=25)
add_button.grid(row=10, column=0, padx=10, pady=10)

fixed_button = Button(entries_frame, text="Bike Fixed",  bg="yellow green",width=25 , command=fixed_bike)
fixed_button.grid(row=11, column=0, padx=10, pady=10)

phone_button = Button(entries_frame, text="Copy Phone Number",  bg="yellow green",width=25 , command=grab_phone)
phone_button.grid(row=12, column=0, padx=10, pady=10)

del_button = Button(entries_frame, text="Delete Bike",  bg="yellow green",width=25 , command=delete_bike)
del_button.grid(row=13, column=0, padx=10, pady=10)

hist_button = Button(entries_frame, text="Service History",  bg="yellow green",width=25 , command=get_history)
hist_button.grid(row=14, column=0, padx=10, pady=10)

query_database()

root.mainloop()
