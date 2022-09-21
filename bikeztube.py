from tkinter import *
from tkinter import ttk
import tkcalendar as cal
import sqlite3
from tkinter import font
import messagebox
from itertools import count

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
    phone text,
    bike text,
    id integer,
    date text,
    work text
)
""")

c.execute("""CREATE TABLE IF NOT EXISTS history (
    name text,
    phone text,
    bike text,
    id integer,
    date text,
    work text
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
    c.execute("INSERT INTO bikes VALUES (:name, :phone, :bike, :id, :date , :work)",
            {
                'name':name_entry.get(),
                'phone':phone_entry.get(),
                'bike':bike_entry.get(),
                'id':id_entry.get(),
                'date':date_entry.get(),
                'work':work_entry.get()
            })

    conn.commit()
    conn.close()

    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    bike_entry.delete(0, END)
    id_entry.delete(0, END)
    date_entry.delete(0, END)
    work_entry.delete(0, END)
    
    my_tree.delete(*my_tree.get_children())
    query_database()


def query_database():
    global count
    count = 0
    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute('SELECT rowid, * FROM bikes')

    records = c.fetchall()

    for record in records:
        if count % 2 ==0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[3], record[0], record[5], record[6]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[3], record[0], record[5], record[6]), tags=('oddrow',))
        #increment counter
        count +=1

    conn.commit()
    conn.close()

def clear_entries():
    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    bike_entry.delete(0, END)
    id_entry.delete(0, END)
    work_entry.delete(0, END)

def delete_bike():

    x = my_tree.selection()[0]
    my_tree.delete(x)

        #create or connect to database
    conn = sqlite3.connect('bikes.db')

    #create a cursor
    c = conn.cursor()

    #delete from database
    c.execute("DELETE from bikes WHERE oid=" + id_entry.get())
    
    #commit changes
    conn.commit()

    #close connection
    conn.close()

    #clear entry boxes
    clear_entries()

    #add a little message box for fun
    messagebox.showinfo("Deleted!", "Your Bike Has Been Deleted!")


def grab_phone():

    phone = phone_entry.get()

    root.clipboard_clear()
    root.clipboard_append(phone)

def copy_ready_text():

    rtext = str('Hello. This is Bikeztube. Your bicycle is ready for collection. We are open till 17:00 on weekdays and 16:00 on Saturdays. Please pick it up at your earliest convenience. Thank you!')

    root.clipboard_clear()
    root.clipboard_append(rtext)    

def fixed_bike():

    x = my_tree.selection()[0]
    my_tree.delete(x)

        #create or connect to database
    conn = sqlite3.connect('bikes.db')

    #create a cursor
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (:name, :phone, :bike, :id, :date, :work)",
            {
                'name':name_entry.get(),
                'phone':phone_entry.get(),
                'bike':bike_entry.get(),
                'id':id_entry.get(),
                'date':date_entry.get(),
                'work':work_entry.get()

            })
    #delete from database
    c.execute("DELETE from bikes WHERE oid=" + id_entry.get())
    
    conn.commit()
    conn.close()
    clear_entries()
    messagebox.showinfo("Deleted!", "Your Bike Has Been Deleted!")



def ser_add_to_comments():
    x = ser_combo.get()
    x = x + ', '
    work_entry.insert(END,x)
    
def parts_add_to_comments():
    x = parts_combo.get()
    x = x + ', '
    work_entry.insert(END,x)   

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

def select_record(e):

    #clear entry boxes
    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    bike_entry.delete(0, END)
    id_entry.delete(0, END)
    date_entry.delete(0, END)
    work_entry.delete(0, END)

    #grab record number
    selected = my_tree.focus()
    #grab record values
    values = my_tree.item(selected, "values")

    #output to entry boxes
    name_entry.insert(0, values[0])
    phone_entry.insert(0, values[1])
    bike_entry.insert(0, values[2])
    id_entry.insert(0, values[3])
    date_entry.insert(0, values[4])
    work_entry.insert(0, values[5])
    
#frame for listbox and entries
cust_frame = Frame(root)
cust_frame.pack(fill='both', expand=True, padx=20, pady=20)



#create a treeview scrollbar
tree_scroll = Scrollbar(cust_frame)
#tree_scroll.pack(side=RIGHT, fill='y', pady=0)

#create the treeview
my_tree = ttk.Treeview(cust_frame, yscrollcommand=tree_scroll.set, selectmode='extended', height=25)
my_tree.pack(pady=0, padx=0, side=LEFT, expand=True, fill='both')

#configure scrollbar
tree_scroll.config(command=my_tree.yview)

#define our columns
my_tree['columns'] = ('Name', 'Phone', 'Bike', 'ID', 'Date', 'Work')

#format our columns
my_tree.column('#0', width=0, stretch=NO)
my_tree.column("Name", anchor=W)
my_tree.column("Phone", anchor=W)
my_tree.column("Bike", anchor=W)
my_tree.column("ID", anchor=CENTER, width=70)
my_tree.column("Date", anchor=W, width=100)
my_tree.column("Work", anchor=W, width=350)

#create headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Phone", text="Phone", anchor=W)
my_tree.heading("Bike", text="Bike", anchor=CENTER)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Date", text="Date", anchor=CENTER)
my_tree.heading("Work", text="Work", anchor=CENTER)

# create  striped row tags
my_tree.tag_configure('oddrow', background= 'white')
my_tree.tag_configure('evenrow',background='lightgrey', foreground='black')


#Frame for all the entries
entries_frame = Frame(cust_frame, pady=10)
entries_frame.pack(fill='both', expand=True, side=RIGHT)

date_entry = cal.DateEntry(entries_frame, width=17, date_pattern='dd/MM/yyyy')
date_entry.grid(row=0, column=0, padx=10)

id_label = Label(entries_frame, text="ID (Always Leave Empty!)")
id_label.grid(row=1, column=0, pady=2, padx=10)

id_entry = Entry(entries_frame, font=(21))
id_entry.grid(row=2, column=0, pady=2, padx=10)

name_label = Label(entries_frame, text="Name")
name_label.grid(row=3, column=0, pady=2, padx=10)

name_entry = Entry(entries_frame, font=(21))
name_entry.grid(row=4, column=0, pady=2, padx=10)

phone_label = Label(entries_frame, text="Phone")
phone_label.grid(row=5, column=0, pady=2, padx=10)

phone_entry = Entry(entries_frame, font=(21))
phone_entry.grid(row=6, column=0, pady=2, padx=10)

bike_label = Label(entries_frame, text="Bike")
bike_label.grid(row=7, column=0, pady=2, padx=10)

bike_entry = Entry(entries_frame, font=(21))
bike_entry.grid(row=8, column=0, pady=2, padx=10)

work_label = Label(entries_frame, text="Work")
work_label.grid(row=9, column=0, pady=2, padx=10)

work_entry = Entry(entries_frame, font=(21))
work_entry.grid(row=10, column=0, pady=2, padx=10)

combo_frame = Frame(entries_frame)
combo_frame.grid(row=11, column=0, pady=2, padx=20)

comboValuesServices = ['Basic Service', 'Second Service', 'Full Service']
comboValuesParts = ['Inner tube R', 'Inner tube F', 'Tyre R', 'Tyre F', 
'Brake Pads R', 'Brake Pads F', 'Chain', 'Cassette', 'Drivetrain', 'Derailleur R', 
'Derailleur F', 'G. Shifter R', 'G. Shifter F', 'Cable(s)', 'Hanger', 'Brake Lever(s)',
'Wheel R', 'Wheel F', 'Bleed', 'Other: ']


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
add_button.grid(row=12, column=0, padx=10, pady=5)

fixed_button = Button(entries_frame, text="Bike Fixed",  bg="yellow green",width=25 , command=fixed_bike)
fixed_button.grid(row=13, column=0, padx=10, pady=5)

phone_button = Button(entries_frame, text="Copy Phone Number",  bg="yellow green",width=25 , command=grab_phone)
phone_button.grid(row=14, column=0, padx=10, pady=5)

del_button = Button(entries_frame, text="Delete Bike",  bg="yellow green",width=25 , command=delete_bike)
del_button.grid(row=15, column=0, padx=10, pady=5)

hist_button = Button(entries_frame, text="Service History",  bg="yellow green",width=25 , command=get_history)
hist_button.grid(row=16, column=0, padx=10, pady=5)

my_tree.bind("<ButtonRelease-1>", select_record)

query_database()

root.mainloop()
