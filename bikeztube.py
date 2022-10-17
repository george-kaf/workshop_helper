from tkinter import *
from tkinter import ttk
import tkcalendar as cal
import sqlite3
from tkinter import font
import messagebox
from itertools import count
from tkinter.scrolledtext import ScrolledText


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
    work text,
    total text
)
""")

c.execute("""CREATE TABLE IF NOT EXISTS history (
    name text,
    phone text,
    bike text,
    id integer,
    date text,
    work text,
    total text
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
    c.execute("INSERT INTO bikes VALUES (:name, :phone, :bike, :id, :date , :work, :total, :ready)",
            {
                'name':name_entry.get(),
                'phone':phone_entry.get(),
                'bike':bike_entry.get(),
                'id':id_entry.get(),
                'date':date_entry.get(),
                'work':work_entry.get('1.0', END),
                'total':'£'+total_price_entry.get(),
                'ready' : ''
            })

    conn.commit()
    conn.close()

    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    bike_entry.delete(0, END)
    id_entry.delete(0, END)
    date_entry.delete(0, END)
    work_entry.delete('1.0', END)
    total_price_entry.delete(0, END)
    
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
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[8], record[1], record[2], record[3], record[0], record[5], record[6], record[7]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[8], record[1], record[2], record[3], record[0], record[5], record[6], record[7]), tags=('oddrow',))
        #increment counter
        count +=1

    conn.commit()
    conn.close()


def clear_entries():

    name_entry.delete(0, END)
    phone_entry.delete(0, END)
    bike_entry.delete(0, END)
    id_entry.delete(0, END)
    work_entry.delete('1.0', END)
    total_price_entry.delete(0, END)

    

def update_bike():

    selected = my_tree.focus()
    my_tree.item(selected, text='', values=(name_entry.get(),phone_entry.get(), bike_entry.get(), id_entry.get(), date_entry.get(), work_entry.get('1.0', END), total_price_entry.get()))

    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute("""UPDATE bikes SET
        name = :name,
        phone = :phone,
        bike = :bike,
        date = :date,
        work = :work,
        total = :total
        WHERE oid = :oid""",
        {
                'name':name_entry.get(),
                'phone':phone_entry.get(),
                'bike':bike_entry.get(),
                'oid':id_entry.get(),
                'date':date_entry.get(),
                'work':work_entry.get('1.0', END),
                'total':total_price_entry.get()

        }
    )

    conn.commit()
    conn.close()

    my_tree.delete(*my_tree.get_children())
    query_database()

def fixed_ready():

    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute('SELECT Ready from bikes WHERE oid=?', (id_entry.get(),))
    res = c.fetchall()
    res_str = list(res[0])

    conn.commit()
    conn.close()
    if res_str[0] == '':
        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()        
        c.execute("""UPDATE bikes SET
            Ready = :ready
            WHERE oid = :oid""",
            {
                    'ready':'✓',
                    'oid':id_entry.get(),

            }
        )

        conn.commit()
        conn.close()
        my_tree.delete(*my_tree.get_children())
        query_database()

    if res_str[0] == '✓' :
        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute("""UPDATE bikes SET
                    Ready = :ready
                    WHERE oid = :oid""",
                    {
                            'ready':'',
                            'oid':id_entry.get(),

                    }
                )

        conn.commit()
        conn.close()
        my_tree.delete(*my_tree.get_children())
        query_database()

def delete_bike():
    x = my_tree.selection()[0]
    my_tree.delete(x)

    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute("DELETE from bikes WHERE oid=" + id_entry.get())
    conn.commit()
    conn.close()
    clear_entries()

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

    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute("INSERT INTO history VALUES (:name, :phone, :bike, :id, :date, :work, :total)",
            {
                'name':name_entry.get(),
                'phone':phone_entry.get(),
                'bike':bike_entry.get(),
                'id':id_entry.get(),
                'date':date_entry.get(),
                'work':work_entry.get('1.0', END),
                'total':total_price_entry.get()

            })
    c.execute("DELETE from bikes WHERE oid=" + id_entry.get())
    conn.commit()
    conn.close()

    clear_entries()

    messagebox.showinfo("Done!", "Service Record Saved !")



def ser_add_to_comments():
    x = ser_combo.get()
    x = x + ' +  '
    work_entry.insert(END,x)

    
def parts_add_to_comments():
    x = parts_combo.get()
    x = x + ' +  '
    work_entry.insert(END,x)   


def get_history():

    top = Toplevel(root) 
    top.state('zoomed') 

    def update_bike():

        selected = my_hist_tree.focus()
        my_hist_tree.item(selected, text='', values=(name_entry2.get(),phone_entry2.get(), bike_entry2.get(), id_entry2.get(), date_entry2.get(), work_entry2.get('1.0', END), total_price_entry2.get()))

        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute("""UPDATE history SET
            name = :name,
            phone = :phone,
            bike = :bike,
            date = :date,
            work = :work,
            total = :total
            WHERE oid = :oid""",
            {
                    'name':name_entry2.get(),
                    'phone':phone_entry2.get(),
                    'bike':bike_entry2.get(),
                    'oid':id_entry2.get(),
                    'date':date_entry2.get(),
                    'work':work_entry2.get('1.0', END),
                    'total':total_price_entry2.get()

            }
        )

        conn.commit()
        conn.close()

        my_hist_tree.delete(*my_hist_tree.get_children())
        query_history()


    def clear_entries():
        name_entry2.delete(0, END)
        phone_entry2.delete(0, END)
        bike_entry2.delete(0, END)
        id_entry2.delete(0, END)
        work_entry2.delete('1.0', END)
        total_price_entry2.delete(0, END)

    def delete_bike():
        x = my_hist_tree.selection()[0]
        my_hist_tree.delete(x)

        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute("DELETE from history WHERE oid=" + id_entry2.get())
        conn.commit()
        conn.close()
        clear_entries()

        messagebox.showinfo("Deleted!", "Your Bike Service Has Been Deleted!")

    def select_record(e):
        try:
            name_entry2.delete(0, END)
            phone_entry2.delete(0, END)
            bike_entry2.delete(0, END)
            id_entry2.delete(0, END)
            date_entry2.delete(0, END)
            work_entry2.delete('1.0', END)
            total_price_entry2.delete(0, END)

            selected = my_hist_tree.focus()
            values = my_hist_tree.item(selected, "values")

            name_entry2.insert(0, values[0])
            phone_entry2.insert(0, values[1])
            bike_entry2.insert(0, values[2])
            id_entry2.insert(0, values[3])
            date_entry2.insert(0, values[4])
            work_entry2.insert('1.0', values[5])
            total_price_entry2.insert(0, values[6])
        except:
            pass   

    def query_history():
        global count
        count = 0
        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute('SELECT rowid, * FROM history')

        records = c.fetchall()

        for record in records:
            if count % 2 ==0:
                my_hist_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[3], record[0], record[5], record[6], record[7]), tags=('evenrow',))
            else:
                my_hist_tree.insert(parent='', index='end', iid=count, text='', values=(record[1], record[2], record[3], record[0], record[5], record[6], record[7]), tags=('oddrow',))
            #increment counter
            count +=1

        conn.commit()
        conn.close() 

    hist_frame = LabelFrame(top, pady=10, text="Service History", padx=15,)
    hist_frame.pack(fill='both', expand=True, padx=20, pady=20)

    my_hist_tree_frame = Frame(hist_frame)
    my_hist_tree_frame.pack(pady=0, padx=0, side=LEFT, expand=True, fill='both')

    buttons_hist_frame = Frame(hist_frame)
    buttons_hist_frame.pack(side=RIGHT, expand=True, fill='both')

    my_hist_tree = ttk.Treeview(my_hist_tree_frame, selectmode='extended')
    my_hist_tree.pack(fill='both', expand=True)

    my_hist_tree['columns'] = ('Name', 'Phone', 'Bike', 'ID', 'Date', 'Work', 'Total')

    my_hist_tree.column('#0', width=0, stretch=NO)
    my_hist_tree.column("Name", anchor=CENTER, width=120)
    my_hist_tree.column("Phone", anchor=CENTER, width=120)
    my_hist_tree.column("Bike", anchor=CENTER, width=200)
    my_hist_tree.column("ID", anchor=CENTER, width=90)
    my_hist_tree.column("Date", anchor=CENTER, width=110)
    my_hist_tree.column("Work", anchor=CENTER, width=700)
    my_hist_tree.column("Total", anchor=CENTER, width=80)

    my_hist_tree.heading("#0", text="", anchor=CENTER)
    my_hist_tree.heading("Name", text="Name", anchor=CENTER)
    my_hist_tree.heading("Phone", text="Phone", anchor=CENTER)
    my_hist_tree.heading("Bike", text="Bike", anchor=CENTER)
    my_hist_tree.heading("ID", text="ID", anchor=CENTER)
    my_hist_tree.heading("Date", text="Date", anchor=CENTER)
    my_hist_tree.heading("Work", text="Work", anchor=CENTER)
    my_hist_tree.heading("Total", text="Total", anchor=CENTER)

    my_hist_tree.tag_configure('oddrow', background= 'white')
    my_hist_tree.tag_configure('evenrow',background='lightgrey', foreground='black')

    s = ttk.Style()
    s.theme_use('clam')
    s.configure('Treeview.Heading', background="yellowgreen", foreground='black', font=('Verdana', 15), height=15)
    s.configure('Treeview', rowheight=40, font=('Verdana' ,11))

    entries_frame = Frame(buttons_hist_frame)
    entries_frame.pack(fill='y', expand=True, side=RIGHT)

    search_frame = Frame(entries_frame)
    search_frame.pack(fill='x')

    searchbox_label = Label(search_frame, text='Search :')
    searchbox_label.pack(fill='x')

    searchbox_entry = Entry(search_frame)
    searchbox_entry.pack(fill='x', pady=10)

    entries_frame2 = Frame(entries_frame, pady=10)
    entries_frame2.pack(pady=20)

    date_entry2 = cal.DateEntry(entries_frame2, width=17, date_pattern='dd/MM/yyyy')
    date_entry2.grid(row=0, column=0, padx=10)

    id_label2 = Label(entries_frame2, text="ID (Always Leave Empty!)")
    id_label2.grid(row=1, column=0, pady=2, padx=10)

    id_entry2 = Entry(entries_frame2, font=('Verdana',12), width=20)
    id_entry2.grid(row=2, column=0, pady=2, padx=10)

    name_label2 = Label(entries_frame2, text="Name")
    name_label2.grid(row=3, column=0, pady=2, padx=10)

    name_entry2 = Entry(entries_frame2, font=('Verdana',12), width=20)
    name_entry2.grid(row=4, column=0, pady=2, padx=10)

    phone_label2 = Label(entries_frame2, text="Phone")
    phone_label2.grid(row=5, column=0, pady=2, padx=10)

    phone_entry2 = Entry(entries_frame2, font=('Verdana',12), width=20)
    phone_entry2.grid(row=6, column=0, pady=2, padx=10)

    bike_label2 = Label(entries_frame2, text="Bike")
    bike_label2.grid(row=7, column=0, pady=2, padx=10)

    bike_entry2 = Entry(entries_frame2, font=('Verdana',12), width=20)
    bike_entry2.grid(row=8, column=0, pady=2, padx=10)

    work_label2 = Label(entries_frame2, text="Work")
    work_label2.grid(row=9, column=0, pady=2, padx=10)

    work_entry2 = ScrolledText(entries_frame2, font=('Times New Roman', 12, 'bold'), height=7, width=22, wrap=WORD)
    work_entry2.grid(row=10, column=0, pady=2, padx=10)

    total_price_label2 = Label(entries_frame2, text="Total")
    total_price_label2.grid(row=11, column=0, pady=2, padx=10)

    total_price_entry2 = Entry(entries_frame2, font=('Verdana',12, 'bold'), width=18)
    total_price_entry2.grid(row=12, column=0, pady=2, padx=10)

    buttons_hist = Frame(entries_frame)
    buttons_hist.pack()

    del_button2 = Button(buttons_hist, text="Delete Service",  bg="yellow green",width=25 , command=delete_bike)
    del_button2.grid(row=13, column=0, padx=10, pady=5)

    update_bike_button2 = Button(buttons_hist, text="Update Service",  bg="yellow green",width=25 , command=update_bike)
    update_bike_button2.grid(row=14, column=0, padx=10, pady=5)



    my_hist_tree.bind("<ButtonRelease-1>", select_record)
    query_history()

    top.mainloop()



def select_record(e):

    try:
        name_entry.delete(0, END)
        phone_entry.delete(0, END)
        bike_entry.delete(0, END)
        id_entry.delete(0, END)
        date_entry.delete(0, END)
        work_entry.delete('1.0', END)
        total_price_entry.delete(0, END)

        selected = my_tree.focus()
        values = my_tree.item(selected, "values")

        name_entry.insert(0, values[1])
        phone_entry.insert(0, values[2])
        bike_entry.insert(0, values[3])
        id_entry.insert(0, values[4])
        date_entry.insert(0, values[5])
        work_entry.insert('1.0', values[6])
        total_price_entry.insert(0, values[7])
    except:
        pass    



cust_frame = Frame(root)
cust_frame.pack(fill='both', expand=True, padx=20, pady=20)

my_tree_frame = Frame(cust_frame)
my_tree_frame.pack(pady=0, padx=0, side=LEFT, expand=True, fill='both')

my_tree = ttk.Treeview(my_tree_frame, selectmode='extended')
my_tree.pack(fill='both', expand=True)

my_tree['columns'] = ('Ready', 'Name', 'Phone', 'Bike', 'ID', 'Date', 'Work', 'Total')

my_tree.column('#0', width=0, stretch=NO)
my_tree.column("Ready", anchor=CENTER, width=60)
my_tree.column("Name", anchor=CENTER, width=120)
my_tree.column("Phone", anchor=CENTER, width=120)
my_tree.column("Bike", anchor=CENTER, width=200)
my_tree.column("ID", anchor=CENTER, width=90)
my_tree.column("Date", anchor=CENTER, width=110)
my_tree.column("Work", anchor=CENTER, width=700)
my_tree.column("Total", anchor=CENTER, width=80)

my_tree.heading("#0", text="", anchor=CENTER)
my_tree.heading("Ready", text="Ready", anchor=CENTER)
my_tree.heading("Name", text="Name", anchor=CENTER)
my_tree.heading("Phone", text="Phone", anchor=CENTER)
my_tree.heading("Bike", text="Bike", anchor=CENTER)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Date", text="Date", anchor=CENTER)
my_tree.heading("Work", text="Work", anchor=CENTER)
my_tree.heading("Total", text="Total", anchor=CENTER)

my_tree.tag_configure('oddrow', background= 'white')
my_tree.tag_configure('evenrow',background='lightgrey', foreground='black')

s = ttk.Style()
s.theme_use('clam')
s.configure('Treeview.Heading', background="yellowgreen", foreground='black', font=('Verdana', 15), height=15)
s.configure('Treeview', rowheight=40, font=('Verdana' ,11))

entries_frame = Frame(cust_frame, pady=10)
entries_frame.pack(fill='y', expand=True, side=RIGHT)

date_entry = cal.DateEntry(entries_frame, width=17, date_pattern='dd/MM/yyyy')
date_entry.grid(row=0, column=0, padx=10)

id_label = Label(entries_frame, text="ID (Always Leave Empty!)")
id_label.grid(row=1, column=0, pady=2, padx=10)

id_entry = Entry(entries_frame, font=('Verdana',12), width=20)
id_entry.grid(row=2, column=0, pady=2, padx=10)

name_label = Label(entries_frame, text="Name")
name_label.grid(row=3, column=0, pady=2, padx=10)

name_entry = Entry(entries_frame, font=('Verdana',12), width=20)
name_entry.grid(row=4, column=0, pady=2, padx=10)

phone_label = Label(entries_frame, text="Phone")
phone_label.grid(row=5, column=0, pady=2, padx=10)

phone_entry = Entry(entries_frame, font=('Verdana',12), width=20)
phone_entry.grid(row=6, column=0, pady=2, padx=10)

bike_label = Label(entries_frame, text="Bike")
bike_label.grid(row=7, column=0, pady=2, padx=10)

bike_entry = Entry(entries_frame, font=('Verdana',12), width=20)
bike_entry.grid(row=8, column=0, pady=2, padx=10)

work_label = Label(entries_frame, text="Work")
work_label.grid(row=9, column=0, pady=2, padx=10)

work_entry = ScrolledText(entries_frame, font=('Times New Roman', 12, 'bold'), height=7, width=22, wrap=WORD)
work_entry.grid(row=10, column=0, pady=2, padx=10)

total_price_label = Label(entries_frame, text="Total")
total_price_label.grid(row=11, column=0, pady=2, padx=10)

total_price_entry = Entry(entries_frame, font=('Verdana',12, 'bold'), width=18)
total_price_entry.grid(row=12, column=0, pady=2, padx=10)

combo_frame = Frame(entries_frame)
combo_frame.grid(row=13, column=0, pady=2, padx=20)

comboValuesServices = ['Basic Service', 'Second Service', 'Full Service']
comboValuesParts = ['Inner tube R', 'Inner tube F', 'Tyre R', 'Tyre F', 
'Brake Pads R', 'Brake Pads F', 'Chain', 'Cassette', 'Drivetrain', 'Derailleur R', 
'Derailleur F', 'G. Shifter R', 'G. Shifter F', 'Cable(s)', 'Hanger', 'Brake Lever(s)',
'Wheel R', 'Wheel F', 'Bleed', 'Other: ']


ser_frame = Frame(combo_frame)
ser_frame.pack(pady=15)

parts_frame = Frame(combo_frame)
parts_frame.pack()

bigfont = font.Font(family="Times New Roman",size=13, weight='bold')
root.option_add("*TCombobox*Listbox*Font", bigfont)

ser_combo = ttk.Combobox(ser_frame, width=15, values =comboValuesServices, state='readonly', font=('Times New Roman',13, 'bold'))
ser_combo.set('Basic Service')
ser_combo.grid(row=0, column=0, padx=10)

add_button_plus = Button(ser_frame, text='+', command=ser_add_to_comments,  bg="yellow green", font=('Verdana',12, 'bold'))
add_button_plus.grid(row=0, column=1)

parts_combo = ttk.Combobox(parts_frame, width=15, values =comboValuesParts, state='readonly', font=('Times New Roman',13, 'bold'))
parts_combo.set('Inner tube R')
parts_combo.grid(row=1, column=0, padx=10)

add_button_plus = Button(parts_frame, text='+', command=parts_add_to_comments,  bg="yellow green", font=('Verdana',12, 'bold'))
add_button_plus.grid(row=1, column=1)

add_button = Button(entries_frame, text="Add Bike",  bg="yellow green", command=add_bike, width=25)
add_button.grid(row=14, column=0, padx=10, pady=5)

ready_button = Button(entries_frame, text="Bike Ready",  bg="yellow green",width=25 , command=fixed_ready)
ready_button.grid(row=15, column=0, padx=10, pady=5)

del_button = Button(entries_frame, text="Delete Bike",  bg="yellow green",width=25 , command=delete_bike)
del_button.grid(row=16, column=0, padx=10, pady=5)

update_bike_button = Button(entries_frame, text="Update Bike",  bg="yellow green",width=25 , command=update_bike)
update_bike_button.grid(row=17, column=0, padx=10, pady=5)

fixed_button = Button(entries_frame, text="Bike Fixed",  bg="yellow green",width=25 , command=fixed_bike)
fixed_button.grid(row=18, column=0, padx=10, pady=5)

buttons_left_frame = Frame(my_tree_frame)
buttons_left_frame.pack(fill='x', pady=20)

get_hist_button = Button(buttons_left_frame, text="Service History",  bg="yellow green",width=25 , command=get_history)
get_hist_button.pack(side=LEFT)

import_data = Button(buttons_left_frame, text="Import Data",  bg="lightgrey",width=25)
import_data.pack(side=LEFT, padx=20)

export_data = Button(buttons_left_frame, text="Export Data",  bg="lightgrey",width=25)
export_data.pack(side=LEFT)

phone_button = Button(buttons_left_frame, text="Copy Phone Number",  bg="lightgrey",width=25 , command=grab_phone)
phone_button.pack(side=LEFT, padx=20)

my_tree.bind("<ButtonRelease-1>", select_record)

query_database()

root.mainloop()
