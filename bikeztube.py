from tkinter import *
from tkinter import ttk
import tkcalendar as cal
import sqlite3

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


#frame for listbox and entries
cust_frame = LabelFrame(root, pady=10, text="Bikes For Service", padx=15,)
cust_frame.pack(fill='both', expand=True, padx=20, pady=20)
cust_list = Listbox(cust_frame, width=40, height=10, font=('Verdana', 15))
cust_list.pack(side=LEFT, pady=0, fill='both', expand=True)

#Frame for all the entries
entries_frame = Frame(cust_frame, pady=10)
entries_frame.pack(fill='both', expand=True)

date_entry = cal.DateEntry(entries_frame, width=17)
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

add_button = Button(entries_frame, text="Add Bike",  bg="yellow green", command=add_bike, width=25)
add_button.grid(row=9, column=0, padx=10, pady=10)

fixed_button = Button(entries_frame, text="Bike Fixed",  bg="yellow green",width=25 , command=fixed_bike)
fixed_button.grid(row=10, column=0, padx=10, pady=10)

rtext_button = Button(entries_frame, text="Copy Ready Text",  bg="yellow green",width=25 , command=copy_ready_text)
rtext_button.grid(row=11, column=0, padx=10, pady=10)

phone_button = Button(entries_frame, text="Copy Phone Number",  bg="yellow green",width=25 , command=grab_phone)
phone_button.grid(row=12, column=0, padx=10, pady=10)

del_button = Button(entries_frame, text="Delete Bike",  bg="yellow green",width=25 , command=delete_bike)
del_button.grid(row=13, column=0, padx=10, pady=10)


query_database()

root.mainloop()