from tkinter import *
from tkinter import ttk
import tkcalendar as cal
import sqlite3
from tkinter import font
from tkinter import messagebox 
from itertools import count
from tkinter.scrolledtext import ScrolledText
from datetime import date

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
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[8], record[1], record[2], record[3], record[0], record[5], record[7]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[8], record[1], record[2], record[3], record[0], record[5], record[7]), tags=('oddrow',))
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
    date_entry.delete(0, END)
    date_entry.set_date(date.today())

    

def update_bike():
    MsgBox = messagebox.askquestion ('Update bike','Are you sure?')
    if MsgBox == 'yes':
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
        clear_entries()
        query_database()
    else:
        pass

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
    MsgBox = messagebox.askquestion ('Update bike','Are you sure?')
    if MsgBox == 'yes':
        x = my_tree.selection()[0]
        my_tree.delete(x)

        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute("DELETE from bikes WHERE oid=" + id_entry.get())
        conn.commit()
        conn.close()
        clear_entries()

        messagebox.showinfo("Deleted!", "Your Bike Has Been Deleted!")
    else:
        pass


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
    pass

    
def parts_add_to_comments():
    pass


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
    
    def reset():
        my_hist_tree.delete(*my_hist_tree.get_children())
        global count
        count = 0
        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute('SELECT rowid, * FROM history')

        name_entry2.delete(0, END)
        phone_entry2.delete(0, END)
        bike_entry2.delete(0, END)
        id_entry2.delete(0, END)
        date_entry2.delete(0, END)
        work_entry2.delete('1.0', END)
        total_price_entry2.delete(0, END)

        results = c.fetchall()

        records = sorted(results, key=lambda tup: tup[0], reverse=True)

        for record in records:
            if count % 2 ==0:
                my_hist_tree.insert(parent='', index='end', iid=count, text='', values=(str(record[1]), str(record[2]), str(record[3]), record[0], str(record[5]), str(record[6]), str(record[7])), tags=('evenrow',))
            else:
                my_hist_tree.insert(parent='', index='end', iid=count, text='', values=(str(record[1]), str(record[2]), str(record[3]), record[0], str(record[5]), str(record[6]), str(record[7])), tags=('oddrow',))
            #increment counter
            count +=1

        conn.commit()
        conn.close() 


    def searcht():
        query = searchbox_entry.get()
        selections = []
        for child in my_hist_tree.get_children():
                selections.append(my_hist_tree.item(child)['values'])
        my_hist_tree.delete(*my_hist_tree.get_children())

        s_results = []
        for i in selections:
            if query.lower() in (str(i)).lower(): 
                s_results.append(i)

        for l in s_results:
            global count
            my_hist_tree.insert(parent='', index='end', iid=count, text='', values=(l[0], str(l[1]), l[2], l[3], l[4], l[5], l[6]))
            count +=1
   


    def query_history():

        global count
        count = 0
        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute('SELECT rowid, * FROM history')

        results = c.fetchall()
        records = sorted(results, key=lambda tup: tup[0], reverse=True)

        for record in records:
            if count % 2 ==0:
                my_hist_tree.insert(parent='', index='end', iid=count, text='', values=(str(record[1]), str(record[2]), str(record[3]), record[0], str(record[5]), str(record[6]), str(record[7])), tags=('evenrow',))
            else:
                my_hist_tree.insert(parent='', index='end', iid=count, text='', values=(str(record[1]), str(record[2]), str(record[3]), record[0], str(record[5]), str(record[6]), str(record[7])), tags=('oddrow',))
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
    my_hist_tree.column("Work", anchor=CENTER, width=300)
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
    searchbox_label.pack(anchor=W, padx=10)

    searchbox_entry = Entry(search_frame)
    searchbox_entry.pack( padx=10, pady=0, side=LEFT)

    reset_button = Button(search_frame, text='Reset', command=reset, background='yellowgreen')
    reset_button.pack(side=RIGHT)

    search_button = Button(search_frame, text='Go', command=searcht, background='yellowgreen')
    search_button.pack(padx=5, side=RIGHT, ipadx=7)

    entries_frame2 = Frame(entries_frame, pady=10)
    entries_frame2.pack(pady=10)

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

    work_entry2 = ScrolledText(entries_frame2, font=('Verdana', 12, 'bold'), height=7, width=17, wrap=WORD)
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
        total_price_entry.insert(0, values[6])

        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute('SELECT work FROM bikes WHERE oid=?', (id_entry.get(),))
        res = c.fetchall()

        for i in res:
            work_entry.insert('1.0', i[0])

    except:
        pass    



cust_frame = Frame(root)
cust_frame.pack(fill='both', expand=True, padx=20, pady=20)

upper_frame = Frame(cust_frame)
upper_frame.pack(fill='both', expand=1)

lower_frame = Frame(cust_frame)
lower_frame.pack(fill='both', expand=1)

my_tree_frame = Frame(lower_frame)
my_tree_frame.pack(pady=0, padx=0, side=LEFT, expand=True, fill='both')

my_tree = ttk.Treeview(my_tree_frame, selectmode='extended')
my_tree.pack(fill='both', expand=True)

second_but_frame = Frame(my_tree_frame)
second_but_frame.pack(fill='x', expand=1)

ready_button = Button(second_but_frame, text="Ready ✓", font=('Verdana',12, 'bold'), bg="yellowgreen",width=18 , command=fixed_ready)
ready_button.pack(side=LEFT)

get_hist_button = Button(second_but_frame, text="Service History ⇆", font=('Verdana', 12, 'bold'),  bg="yellowgreen",width=18 , command=get_history)
get_hist_button.pack(side=LEFT, padx=10, pady=10)

del_button = Button(second_but_frame, text="Delete x", font=('Verdana', 12, 'bold'),  bg="yellowgreen",width=18 , command=delete_bike)
del_button.pack(side=LEFT, padx=0, pady=0)


my_tree['columns'] = ('Ready', 'Name', 'Phone', 'Bike', 'ID', 'Date','Total')

my_tree.column('#0', width=0, stretch=NO)
my_tree.column("Ready", anchor=CENTER, width=40)
my_tree.column("Name", anchor=CENTER, width=120)
my_tree.column("Phone", anchor=CENTER, width=90)
my_tree.column("Bike", anchor=CENTER, width=200)
my_tree.column("ID", anchor=CENTER, width=90)
my_tree.column("Date", anchor=CENTER, width=70)
my_tree.column("Total", anchor=CENTER, width=40)

my_tree.heading("#0", text="", anchor=CENTER)
my_tree.heading("Ready", text="Ready", anchor=CENTER)
my_tree.heading("Name", text="Name", anchor=CENTER)
my_tree.heading("Phone", text="Phone", anchor=CENTER)
my_tree.heading("Bike", text="Bike", anchor=CENTER)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Date", text="Date", anchor=CENTER)
my_tree.heading("Total", text="Total", anchor=CENTER)

my_tree.tag_configure('oddrow', background= 'white')
my_tree.tag_configure('evenrow',background='lightgrey', foreground='black')

s = ttk.Style()
s.theme_use('clam')
s.configure('Treeview.Heading', background="yellowgreen", foreground='black', font=('Verdana', 15), height=8)
s.configure('Treeview', rowheight=40, font=('Verdana' ,11))

entries_frame = Frame(upper_frame, pady=10)
entries_frame.pack(fill='x', expand=True, side=LEFT)

entries_frame_top = Frame(entries_frame)
entries_frame_top.pack(fill='x', expand=True)

date_label = Label(entries_frame_top, text="Date : ", font=('Verdana', 14, 'bold'))
date_label.grid(row=0, column=0)

date_entry = cal.DateEntry(entries_frame_top, width=17, date_pattern='dd/MM/yyyy', font=('Verdana', 11))
date_entry.grid(row=0, column=1, padx=(0,40))

id_label = Label(entries_frame_top, text="ID (Leave Empty!) : ", font=('Verdana', 14, 'bold'))
id_label.grid(row=0, column=2)

id_entry = ttk.Entry(entries_frame_top, font=('Verdana', 14), width=15)
id_entry.grid(row=0, column=3)

entries_frame_middle = Frame(entries_frame)
entries_frame_middle.pack(fill='x', expand=True)

name_label = Label(entries_frame_middle, text="Name : ", font=('Verdana', 14, 'bold'))
name_label.grid(row=0, column=0)

name_entry = ttk.Entry(entries_frame_middle, font=('Verdana',14), width=20)
name_entry.grid(row=0, column=1, pady=20)

phone_label = Label(entries_frame_middle, text="Phone : ", font=('Verdana', 14, 'bold'))
phone_label.grid(row=0, column=2, padx=(30,10))

phone_entry = ttk.Entry(entries_frame_middle, font=('Verdana',14), width=20)
phone_entry.grid(row=0, column=3)

entries_frame_bottom = Frame(entries_frame)
entries_frame_bottom.pack(fill='x', expand=True, side=RIGHT)

bike_label = Label(entries_frame_bottom, text="Bike : ", font=('Verdana', 14, 'bold'))
bike_label.grid(row=0, column=0)

bike_entry = ttk.Entry(entries_frame_bottom, font=('Verdana',14 ), width=20)
bike_entry.grid(row=0, column=1, padx=(10,0))

total_price_label = Label(entries_frame_bottom, text="Total : ", font=('Verdana', 14, 'bold'))
total_price_label.grid(row=0, column=2, padx=(30,10))

total_price_entry = ttk.Entry(entries_frame_bottom, font=('Verdana',14), width=20)
total_price_entry.grid(row=0, column=3, padx=(10,0))

# combo_frame = Frame(entries_frame_right)
# combo_frame.grid(row=11, column=0, pady=2, padx=20)

# main_but_frame = Frame(entries_frame_right)
# main_but_frame.grid(row=14, column=0, padx=12, pady=15)

# clear_but = Button(main_but_frame, text="Clear  -",  bg="yellow green", font=('Verdana', 11, 'bold'), command=clear_entries, width=25)
# clear_but.pack(pady=0)

# add_button = Button(main_but_frame, text="Add  +",  bg="yellow green", font=('Verdana', 11, 'bold'), command=add_bike, width=25)
# add_button.pack(pady=0)

# update_bike_button = Button(main_but_frame, text="Update  ↺ ", font=('Verdana', 11, 'bold'),  bg="yellow green", width=25 , command=update_bike)
# update_bike_button.pack(pady=0)

# fixed_button = Button(main_but_frame, text="Fixed  👍", font=('Verdana', 11, 'bold'),  bg="yellow green", width=25 , command=fixed_bike)
# fixed_button.pack(pady=0)

lower_widg_frame = Frame(upper_frame)
lower_widg_frame.pack(fill='x', expand=1, pady=0)

work_frame_top = Frame(lower_widg_frame)
work_frame_top.pack(fill='y', expand=1, side=RIGHT)

work_label = Label(work_frame_top, text="Work (Εξαρτημα κενο τιμη κενο, F=front, R=rear, αμα ειναι δυο x κενο 2 κενο)", font=('Verdana', 11))
work_label.pack(pady=5, anchor=W,fill='y', expand=1)

work_entry = Text(work_frame_top, font=('Verdana', 12, 'bold'), wrap=WORD, height=7)
work_entry.pack(fill='y', expand=1)

my_tree.bind("<ButtonRelease-1>", select_record)

query_database()

root.mainloop()
