from tkinter import *
from tkinter import ttk
import tkcalendar as cal
import sqlite3
from tkinter import font
from tkinter import messagebox 
from itertools import count
from tkinter.scrolledtext import ScrolledText
from customtkinter import *
from colorama import Fore, Back, Style


darkpurple = '#3B3355'
mediumpurple = '#5D5D81'   
lightpurple = '#909CC2'
lightgreen = '#CEEC97'
lightgreen2= '#DBE4CB'
darkgreen = '#909CC2'

root = CTk()
root.title("Bikeztube")

screen_width = root.winfo_screenwidth()
screen_height = int(root.winfo_screenheight()/1.05)
screen_resolution = str(screen_width)+'x'+str(screen_height)
print(screen_resolution)

root.geometry(screen_resolution+'+-10+-1')

set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

conn = sqlite3.connect('bikes.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS bikes (
    name text,
    phone text,
    bike text,
    id integer,
    date text,
    work text,
    total text,
    Ready text
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
conn.commit()
conn.close()

def add_bike():

    try:
        last = my_tree.get_children()[-1]
    except:
        last=0

    def add_bike_to_database():
        
        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute("INSERT INTO bikes VALUES (:name, :phone, :bike, :id, :date , :work, :total, :Ready)",
                {
                    'name':name_entry.get(),
                    'phone':phone_entry.get(),
                    'bike':bike_entry.get(),
                    'id': int(last)+1,
                    'date':date_entry.get(),
                    'work':work_entry.get('1.0', END),
                    'total':'£'+total_price_entry.get(),
                    'Ready' : ''
                })

        conn.commit()
        conn.close()

        add_level.destroy()
        my_tree.delete(*my_tree.get_children())
        query_database()

    add_level = CTkToplevel(root)
    add_level.title("Add Customer")

    add_level.wm_transient(root)    

    entries_buttons_and_work = CTkFrame(add_level)
    entries_buttons_and_work.pack(fill='both', expand=True)

    entries_frame = CTkFrame(entries_buttons_and_work)
    entries_frame.pack(padx=20, pady=20, ipadx=50)

    date_label = CTkLabel(entries_frame, text="Date : ", font=('roboto', 14, 'bold'))
    date_label.grid(row=0, column=0, sticky=W, padx=(button_width, 0))

    s.configure('DateEntry', fieldbackground='white')
    date_entry = cal.DateEntry(entries_frame, date_pattern='dd/MM/yyyy', font=('roboto', 11))
    date_entry.grid(row=0, column=1, sticky=W, pady=20)

    name_label = CTkLabel(entries_frame, text="Name : ", font=('roboto', 14, 'bold'))
    name_label.grid(row=1, column=0, sticky=W, padx=(button_width, 0))

    name_entry = CTkEntry(entries_frame, font=('roboto',14))
    name_entry.grid(row=1, column=1, sticky=W)

    phone_label = CTkLabel(entries_frame, text="Phone : ", font=('roboto', 14, 'bold'))
    phone_label.grid(row=1, column=2, padx=(button_width*1.3, 0))

    phone_entry = CTkEntry(entries_frame, font=('roboto',14))
    phone_entry.grid(row=1, column=3, sticky=W)

    bike_label = CTkLabel(entries_frame, text="Bike : ", font=('roboto', 14, 'bold'))
    bike_label.grid(row=2, column=0, sticky=W, padx=(button_width, 0))

    bike_entry = CTkEntry(entries_frame, font=('roboto',14 ))
    bike_entry.grid(row=2, column=1, sticky=W, pady=20)

    total_price_label = CTkLabel(entries_frame, text="Total : ", font=('roboto', 14, 'bold'))
    total_price_label.grid(row=2, column=2, padx=(button_width*1.3, 0))

    total_price_entry = CTkEntry(entries_frame, font=('roboto',14))
    total_price_entry.grid(row=2, column=3, sticky=W)

    work_label = CTkLabel(entries_frame, text="Work : ", font=('roboto', 14, 'bold'))
    work_label.grid(row=3, column=0, sticky=NW, padx=(button_width, 0))

    work_entry = CTkTextbox(entries_frame, font=('roboto',14), width=button_width*25)
    work_entry.grid(row=3, column=1, columnspan=3, sticky=W)

    add_but = CTkButton(entries_frame, text="Add", command=add_bike_to_database, font=('roboto', button_width), width=button_width*7)
    add_but.grid(row=4, column=3, sticky=E, pady=20)

    add_level.mainloop()

def update_bike():

    try:
        curItem = my_tree.focus()
        item_data = (my_tree.item(curItem))
        item_values = item_data['values']
        id_from_selection = str(item_values[4])


        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute('SELECT work from bikes WHERE oid=?', (int(id_from_selection),))
        work3 = c.fetchall()
        work2 = work3[0]
        work = work2[0]
        conn.commit()
        conn.close()

        def update_bike_in_database():
            MsgBox = messagebox.askquestion ('Update bike','Are you sure?')
            if MsgBox == 'yes':

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
                            'name':name_entry1.get(),
                            'phone':phone_entry1.get(),
                            'bike':bike_entry1.get(),
                            'oid':id_from_selection,
                            'date':date_entry1.get(),
                            'work':work_entry1.get('1.0', END),
                            'total':total_price_entry1.get()

                    }
                )

                conn.commit()
                conn.close()

                my_tree.delete(*my_tree.get_children())
                query_database()
                update_level.destroy()
            else:
                pass

        def insert_entries():
            date_entry1.set_date(item_values[5]),
            name_entry1.insert(0, item_values[1]),
            phone_entry1.insert(0, item_values[2]),
            bike_entry1.insert(0, item_values[3]),
            total_price_entry1.insert(0, item_values[6]),
            work_entry1.insert('1.0',  work)

        update_level = Toplevel(root)
        update_level.title("Update")

        update_level.wm_transient(root)    

        entries_buttons_and_work1 = CTkFrame(update_level)
        entries_buttons_and_work1.pack(fill='both', expand=True)

        entries_frame1 = CTkFrame(entries_buttons_and_work1)
        entries_frame1.pack(padx=20, pady=20, ipadx=50)

        date_label1 = CTkLabel(entries_frame1, text="Date : ", font=('roboto', 14, 'bold'))
        date_label1.grid(row=0, column=0, sticky=W, padx=(button_width, 0))

        date_entry1 = cal.DateEntry(entries_frame1, date_pattern='dd/MM/yyyy', font=('roboto', 11))
        date_entry1.grid(row=0, column=1, sticky=W, pady=20)

        name_label1 = CTkLabel(entries_frame1, text="Name : ", font=('roboto', 14, 'bold'))
        name_label1.grid(row=1, column=0, sticky=W, padx=(button_width, 0))

        name_entry1 = CTkEntry(entries_frame1, font=('roboto',14))
        name_entry1.grid(row=1, column=1, sticky=W)

        phone_label1 = CTkLabel(entries_frame1, text="Phone : ", font=('roboto', 14, 'bold'))
        phone_label1.grid(row=1, column=2, padx=(button_width*1.3, 0))

        phone_entry1 = CTkEntry(entries_frame1, font=('roboto',14))
        phone_entry1.grid(row=1, column=3, sticky=W)

        bike_label1 = CTkLabel(entries_frame1, text="Bike : ", font=('roboto', 14, 'bold'))
        bike_label1.grid(row=2, column=0, sticky=W, padx=(button_width, 0))

        bike_entry1 = CTkEntry(entries_frame1, font=('roboto',14 ))
        bike_entry1.grid(row=2, column=1, sticky=W, pady=20)

        total_price_label1 = CTkLabel(entries_frame1, text="Total : ", font=('roboto', 14, 'bold'))
        total_price_label1.grid(row=2, column=2, padx=(button_width*1.3, 0))

        total_price_entry1 = CTkEntry(entries_frame1, font=('roboto',14))
        total_price_entry1.grid(row=2, column=3, sticky=W)

        work_label1 = CTkLabel(entries_frame1, text="Work : ", font=('roboto', 14, 'bold'))
        work_label1.grid(row=3, column=0, sticky=NW, padx=(button_width, 0))

        work_entry1 = CTkTextbox(entries_frame1, font=('roboto',14), width=button_width*25)
        work_entry1.grid(row=3, column=1, columnspan=3, sticky=W)

        update_but1 = CTkButton(entries_frame1, text="Update", command=update_bike_in_database, font=('roboto', button_width), width=button_width*7)
        update_but1.grid(row=4, column=3, sticky=E, pady=20)

        insert_entries()

        update_level.mainloop()


    except:
        pass

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

def delete_bike():
    MsgBox = messagebox.askquestion ('Delete bike','Are you sure?')
    if MsgBox == 'yes':
        
        curItem = my_tree.focus()
        item_data = (my_tree.item(curItem))
        item_values = item_data['values']
        id_from_selection = str(item_values[4])

        x = my_tree.selection()[0]
        my_tree.delete(x)

        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute("DELETE from bikes WHERE oid=" + id_from_selection)
        conn.commit()
        conn.close()

        messagebox.showinfo("Deleted!", "Your Bike Has Been Deleted!")
    else:
        pass

def fixed():

    try :
        curItem = my_tree.focus()
        item_data = (my_tree.item(curItem))
        item_values = item_data['values']
        id_from_selection = str(item_values[4])


        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute('SELECT Ready from bikes WHERE oid=?', (id_from_selection,))
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
                        'oid':id_from_selection,}
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
                                'oid':id_from_selection,

                        }
                    )

            conn.commit()
            conn.close()
            my_tree.delete(*my_tree.get_children())
            query_database()
    except:
        pass

def change_appearance_mode_event(new_appearance_mode: str):

    set_appearance_mode(new_appearance_mode)

    if new_appearance_mode == "Light":
        s.configure('Treeview.Heading', background="#ffffff", foreground='#555555', )
        s.configure('Treeview', fieldbackground="white")
        s.map('Treeview', background=[('selected', '#55bd7f')], foreground=[('selected', 'white')])
        my_tree.tag_configure('oddrow', background= '#cccccc', foreground='#121212')
        my_tree.tag_configure('evenrow',background='#dddddd', foreground='#121212')

    if new_appearance_mode == "Dark":
        s.configure('Treeview.Heading', background="#181818", foreground='white', )
        s.configure('Treeview', rowheight=int(button_width*3.5), fieldbackground="#363636")
        s.map('Treeview', background=[('selected', '#319f6d')])
        my_tree.tag_configure('oddrow', background= '#363636', foreground='white')
        my_tree.tag_configure('evenrow',background='#303030', foreground='white')

def fixed_bike():

    MsgBox = messagebox.askquestion ('Delete bike','Are you sure?')
    if MsgBox == 'yes':
        curItem = my_tree.focus()
        item_data = (my_tree.item(curItem))
        item_values = item_data['values']
        id_from_selection = str(item_values[4])

        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute('SELECT * FROM bikes WHERE rowid=' +id_from_selection )
        records = c.fetchall()
        records_list = records[0]
        conn.commit()
        conn.close()

        x = my_tree.selection()[0]
        my_tree.delete(x)

        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute("INSERT INTO history VALUES (:name, :phone, :bike, :id, :date, :work, :total)",
                {
                    'name':records_list[0],
                    'phone':records_list[1],
                    'bike':records_list[2],
                    'id':id_from_selection,
                    'date':records_list[4],
                    'work':records_list[5],
                    'total':records_list[6]

                })
        c.execute("DELETE from bikes WHERE oid=" + id_from_selection)
        conn.commit()
        conn.close()

        messagebox.showinfo("Done!", "Service Record Saved !")

menu_width = (screen_width/9)
button_width = int(menu_width/14)

main_frame = CTkFrame(root)
main_frame.pack(fill=BOTH, expand=1)

menu_frame = CTkFrame(main_frame, width=menu_width*1.2)
menu_frame.pack(side=LEFT,fill=Y)
menu_frame.propagate(0)

butt_padx = int(button_width)
butt_pady = int(button_width)

title_label = CTkLabel(menu_frame, text="Workshop Manager", font=('roboto', button_width*1.5))
title_label.pack(pady=(int(button_width*3),int(button_width*1.5)),  padx=button_width*2 ,fill='x')

butt1 = CTkButton(menu_frame, text='+ Add', command=add_bike, font=('roboto', int(button_width*1.1)))
butt1.pack(ipady=int(button_width/2), pady=(int(button_width*2), 0), padx=button_width*2 ,fill='x')

butt2 = CTkButton(menu_frame, text='Update', command=update_bike, font=('roboto',  int(button_width*1.1)))
butt2.pack(pady=button_width, ipady=int(button_width/2), padx=button_width*2 ,fill='x')

butt3 = CTkButton(menu_frame, text='Ready', command=fixed, font=('roboto',  int(button_width*1.1)))
butt3.pack(ipady=int(button_width/2), padx=button_width*2 ,fill='x')

butt4 = CTkButton(menu_frame, text='Collected', command=fixed_bike, font=('roboto',  int(button_width*1.1)))
butt4.pack(pady=button_width, ipady=int(button_width/2), padx=button_width*2 ,fill='x')

butt5 = CTkButton(menu_frame, text='Delete', command=delete_bike, font=('roboto',  int(button_width*1.1)))
butt5.pack( ipady=int(button_width/2), padx=button_width*2 ,fill='x')

appearance_mode_optionemenu = CTkOptionMenu(menu_frame, values=["Dark", "Light"], command=change_appearance_mode_event)
appearance_mode_optionemenu.pack(side=BOTTOM, pady=(0,40))

appearance_mode_label = CTkLabel(menu_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.pack(side=BOTTOM)

content_frame = CTkFrame(main_frame)
content_frame.pack(side=RIGHT, fill=BOTH, expand=1, pady=button_width*3, padx=button_width*3)

tree_and_bar_frame = CTkFrame(content_frame)
tree_and_bar_frame.pack( expand=True, fill='both')

my_tree_frame = CTkFrame(tree_and_bar_frame)
my_tree_frame.pack( expand=True, fill='both')

my_tree = ttk.Treeview(my_tree_frame, selectmode='extended')
my_tree.pack(fill='both', expand=True)

bar_and_label_frame = CTkFrame(tree_and_bar_frame)
bar_and_label_frame.pack( fill='x', anchor=N, pady=(button_width*1.5, 0))

bar_label = CTkLabel(bar_and_label_frame, text='Service capacity : ', font=('roboto', button_width, 'bold'))
bar_label.pack(side=LEFT, pady=(button_width), padx=(button_width,0 ), anchor=N)

progressbar = CTkProgressBar(master=bar_and_label_frame)
progressbar.pack(fill='x', expand=1, side=LEFT,  pady=(button_width*1.7, 0), padx=(button_width), anchor=N )

my_tree['columns'] = ('Ready', 'Name', 'Phone', 'Bike', 'ID', 'Date','Total')

my_tree.column('#0', width=0, stretch=NO)
my_tree.column("Ready", anchor=CENTER, width=button_width*8)
my_tree.column("Name", anchor=CENTER, width=button_width*15)
my_tree.column("Phone", anchor=CENTER, width=button_width*15)
my_tree.column("Bike", anchor=CENTER, width=button_width*25)
my_tree.column("ID", anchor=CENTER)
my_tree.column("Date", anchor=CENTER)
my_tree.column("Total", anchor=CENTER)

my_tree.heading("#0", text="", anchor=CENTER)
my_tree.heading("Ready", text="Ready", anchor=CENTER)
my_tree.heading("Name", text="Name", anchor=CENTER)
my_tree.heading("Phone", text="Phone", anchor=CENTER)
my_tree.heading("Bike", text="Bike", anchor=CENTER)
my_tree.heading("ID", text="ID", anchor=CENTER)
my_tree.heading("Date", text="Date", anchor=CENTER)
my_tree.heading("Total", text="Total", anchor=CENTER)

my_tree.tag_configure('oddrow', background= '#363636', foreground='white')
my_tree.tag_configure('evenrow',background='#303030', foreground='white')

s = ttk.Style()
s.theme_use('classic')

s.configure('Treeview.Heading', background="#181818", foreground='white', font=('roboto', int(button_width*1.3), 'bold' ), height=14, borderwidth=0 )
s.configure('Treeview', rowheight=int(button_width*3.5), font=('roboto' ,button_width ), fieldbackground="#363636", bordercolor='#262626')
s.map('Treeview', background=[('selected', '#319f6d')])

more_butt_frame = CTkFrame(content_frame)
more_butt_frame.pack(fill='x',  side=BOTTOM)

details_and_label_frame = CTkFrame(more_butt_frame)
details_and_label_frame.pack(anchor=W,side=LEFT, fill='x', expand=1, pady=(button_width*1.5), padx=(0, button_width*1.5))

service_details_label = CTkLabel(details_and_label_frame, height=button_width*6.3, wraplength=button_width*50, justify=LEFT, text='Commue, Front e PFront Geear Wire', font=('roboto', button_width))
service_details_label.pack(anchor=W, pady=button_width, padx= button_width*1.5)

stat_frame = CTkFrame(more_butt_frame)
stat_frame.pack(side=RIGHT, pady=button_width*1.5, anchor=N)

checkbuttons_frame = CTkFrame(stat_frame)
checkbuttons_frame.pack(pady=button_width, padx=(button_width*1.5))

checkbox_1 = CTkCheckBox(master=checkbuttons_frame, text='Basic Service')
checkbox_1.pack(pady=button_width, padx=(button_width*2, 0), side=LEFT)

checkbox_2 = CTkCheckBox(master=checkbuttons_frame, text='Commuter Service')
checkbox_2.pack(pady=button_width, padx=(button_width, 0), side=LEFT)

checkbox_3 = CTkCheckBox(master=checkbuttons_frame, text='Full Service', )
checkbox_3.pack(pady=button_width, padx=(button_width), side=LEFT)

graph_butt = CTkButton(stat_frame, text='Statistics', font=('roboto',  int(button_width*1.1)))
graph_butt.pack(pady=(0, button_width), padx=( button_width*1.5), side=LEFT, fill='x', expand=1)

hist_butt = CTkButton(stat_frame, text='History', font=('roboto',  int(button_width*1.1)))
hist_butt.pack(pady=(0, button_width,), padx=(0, button_width*1.5), side=RIGHT, fill='x', expand=1)

query_database()

root.mainloop()
