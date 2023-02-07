from tkinter import *
from tkinter import ttk
import tkcalendar as cal
import sqlite3
from tkinter import font
from tkinter import messagebox 
from itertools import count
from tkinter.scrolledtext import ScrolledText
from customtkinter import *


darkpurple = '#3B3355'
mediumpurple = '#5D5D81'   
lightpurple = '#909CC2'
lightgreen = '#CEEC97'
lightgreen2= '#DBE4CB'
darkgreen = '#909CC2'

root = CTk()
root.title("Bikeztube")
root.state("zoomed")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

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
    total text,
    ready text
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

def add_bike():

    try:
        last = my_tree.get_children()[-1]
    except:
        last=0



    def add_bike_to_database():
        
        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute("INSERT INTO bikes VALUES (:name, :phone, :bike, :id, :date , :work, :total, :ready)",
                {
                    'name':name_entry.get(),
                    'phone':phone_entry.get(),
                    'bike':bike_entry.get(),
                    'id': int(last)+1,
                    'date':date_entry.get(),
                    'work':work_entry.get('1.0', END),
                    'total':'£'+total_price_entry.get(),
                    'ready' : ''
                })

        conn.commit()
        conn.close()


        add_level.destroy()
        my_tree.delete(*my_tree.get_children())
        query_database()

    add_level = CTkToplevel(root)
    add_level.title("Add Customer")

    work_width = int(screen_width/3)
    add_level.wm_transient(root)    

    entries_buttons_and_work = CTkFrame(add_level)
    entries_buttons_and_work.pack(fill='both', expand=True)

    entries_frame = CTkFrame(entries_buttons_and_work)
    entries_frame.pack(padx=20, pady=20, ipadx=50)

    date_label = CTkLabel(entries_frame, text="Date : ", font=('Verdana', 14))
    date_label.grid(row=0, column=0)

    s.configure('DateEntry', fieldbackground='white')
    date_entry = cal.DateEntry(entries_frame, date_pattern='dd/MM/yyyy', font=('Verdana', 11))
    date_entry.grid(row=0, column=1, sticky=W)

    name_label = CTkLabel(entries_frame, text="Name : ", font=('Verdana', 14))
    name_label.grid(row=1, column=0, sticky=W)

    name_entry = CTkEntry(entries_frame, font=('Verdana',14))
    name_entry.grid(row=1, column=1, sticky=W)

    phone_label = CTkLabel(entries_frame, text="Phone : ", font=('Verdana', 14))
    phone_label.grid(row=1, column=2,)

    phone_entry = CTkEntry(entries_frame, font=('Verdana',14))
    phone_entry.grid(row=1, column=3, sticky=W)

    bike_label = CTkLabel(entries_frame, text="Bike : ", font=('Verdana', 14))
    bike_label.grid(row=2, column=0, sticky=W)

    bike_entry = CTkEntry(entries_frame, font=('Verdana',14 ))
    bike_entry.grid(row=2, column=1, sticky=W)

    total_price_label = CTkLabel(entries_frame, text="Total : ", font=('Verdana', 14))
    total_price_label.grid(row=2, column=2,)

    total_price_entry = CTkEntry(entries_frame, font=('Verdana',14))
    total_price_entry.grid(row=2, column=3, sticky=W)

    work_label = CTkLabel(entries_frame, text="Work : ", font=('Verdana', 14))
    work_label.grid(row=3, column=0, sticky=W)

    work_entry = CTkTextbox(entries_frame, font=('Verdana',14), width=work_width, height=int(work_width/3))
    work_entry.grid(row=3, column=1, columnspan=3, sticky=W)

    add_but = CTkButton(entries_frame, text="Add", command=add_bike_to_database, font=('Verdana', button_width, 'bold'))
    add_but.grid(row=4, column=0, columnspan=5, sticky=W, ipadx=int(button_width*1.4), ipady=int(button_width/2), pady=20)



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
                            'name':name_entry.get(),
                            'phone':phone_entry.get(),
                            'bike':bike_entry.get(),
                            'oid':id_from_selection,
                            'date':date_entry.get(),
                            'work':work_entry.get('1.0', END),
                            'total':total_price_entry.get()

                    }
                )

                conn.commit()
                conn.close()

                my_tree.delete(*my_tree.get_children())
                query_database()
            else:
                pass


        update_level = Toplevel(root)
        update_level.title("Update")

        entries_buttons_and_work = Frame(update_level, background=darkpurple)
        entries_buttons_and_work.pack(fill='both', expand=True)

        entries_and_buttons = LabelFrame(entries_buttons_and_work, text='Customer Information', background=darkpurple, foreground='white', font=('Verdana', 11))
        entries_and_buttons.pack(fill='both', expand=True, padx=20, pady=20)

        entries_frame = Frame(entries_and_buttons, background=darkpurple)
        entries_frame.pack(side=LEFT, padx=20, pady=20, anchor=W)

        entries_frame_top = Frame(entries_frame, background=darkpurple)
        entries_frame_top.pack(fill='x', expand=True)

        date_label = Label(entries_frame_top, text="Date : ", font=('Verdana', 14), background=darkpurple, foreground='white')
        date_label.grid(row=0, column=0)

        s.configure('DateEntry', fieldbackground='white')
        date_entry = cal.DateEntry(entries_frame_top, width=23, date_pattern='dd/MM/yyyy', font=('Verdana', 11), background='white')
        date_entry.grid(row=0, column=1, padx=(6,36), ipady=3)

        id_label = Label(entries_frame_top, text="ID : ", font=('Verdana', 14), background=darkpurple, foreground='white')
        id_label.grid(row=0, column=2)

        id_entry = Entry(entries_frame_top, font=('Verdana', 14), width=20, background='white')
        id_entry.grid(row=0, column=3, padx=(44,0), ipady=3)

        entries_frame_middle = Frame(entries_frame, background=darkpurple)
        entries_frame_middle.pack(fill='x', expand=True)

        name_label = Label(entries_frame_middle, text="Name : ", font=('Verdana', 14), background=darkpurple, foreground='white')
        name_label.grid(row=0, column=0)

        name_entry = Entry(entries_frame_middle, font=('Verdana',14), width=20, background='white')
        name_entry.grid(row=0, column=1, pady=20, ipady=3)

        phone_label = Label(entries_frame_middle, text="Phone : ", font=('Verdana', 14), background=darkpurple, foreground='white')
        phone_label.grid(row=0, column=2, padx=(30,10))

        phone_entry = Entry(entries_frame_middle, font=('Verdana',14), width=20, background='white')
        phone_entry.grid(row=0, column=3, ipady=3, padx=(5,0))

        entries_frame_bottom = Frame(entries_frame, background=darkpurple)
        entries_frame_bottom.pack(fill='x', expand=True)

        bike_label = Label(entries_frame_bottom, text="Bike : ", font=('Verdana', 14), background=darkpurple, foreground='white')
        bike_label.grid(row=0, column=0)

        bike_entry = Entry(entries_frame_bottom, font=('Verdana',14 ), width=20, background='white')
        bike_entry.grid(row=0, column=1, padx=(13,0), ipady=3)

        total_price_label = Label(entries_frame_bottom, text="Total : ", font=('Verdana', 14), background=darkpurple, foreground='white')
        total_price_label.grid(row=0, column=2, padx=(30,10))

        total_price_entry = Entry(entries_frame_bottom, font=('Verdana',14), width=20, background='white')
        total_price_entry.grid(row=0, column=3, padx=(14,0), ipady=3)

        entries_frame_bottom_work = Frame(entries_frame, background=darkpurple)
        entries_frame_bottom_work.pack(fill='x', expand=True, pady=20)

        work_label = Label(entries_frame_bottom_work, text="Work : ", font=('Verdana', 14), background=darkpurple, foreground='white')
        work_label.pack(side=LEFT)

        work_entry = Text(entries_frame_bottom_work, font=('Verdana', 14), height=3, width=51, background='white')
        work_entry.pack(padx=(5, 50), side=LEFT)

        entries_frame_bottom_clear = Frame(entries_frame, background=darkpurple)
        entries_frame_bottom_clear.pack(side=LEFT,anchor=W, pady=20)

        update_but = Button(entries_frame_bottom_clear, text="Update", command=update_bike_in_database, background='purple', foreground='white', font=('Verdana', 12, 'bold'), width=13)
        update_but.pack(side=LEFT,anchor=W)

        clear_but = Button(entries_frame_bottom_clear, text="Clear", background='purple', foreground='white', font=('Verdana', 12, 'bold'), width=13)
        clear_but.pack(side=LEFT, anchor=W, padx=20)


        name_entry.insert(0, item_values[1]),
        phone_entry.insert(0, item_values[2]),
        bike_entry.insert(0, item_values[3]),
        id_entry.insert(0, item_values[4]),
        date_entry.insert(item_values[5]),
        work_entry.insert('1.0',  work),
        total_price_entry.insert(0, item_values[6])

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


def fixed_ready():

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
                        'oid':id_from_selection,

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
                                'oid':id_from_selection,

                        }
                    )

            conn.commit()
            conn.close()
            my_tree.delete(*my_tree.get_children())
            query_database()
    except:
        pass

















menu_width = (screen_width/9)
button_width = int(menu_width/14)

main_frame = CTkFrame(root)
main_frame.pack(fill=BOTH, expand=1)

menu_frame = CTkFrame(main_frame, width=menu_width)
menu_frame.pack(side=BOTTOM,fill=X, padx=button_width*3, pady=button_width*3)

print(button_width)

butt_padx = int(button_width)
butt_pady = int(button_width)

butt1 = CTkButton(menu_frame, text='+ Add', command=add_bike, font=('arial', int(button_width*3), 'bold'))
butt1.grid(row=0, column=0, ipady=button_width, ipadx=int(button_width*3), pady=button_width, padx=button_width)

butt2 = CTkButton(menu_frame, text='Update', command=update_bike, font=('arial',  int(button_width*2)))
butt2.grid(row=0, column=1, ipady=(button_width/2), ipadx=button_width*2, sticky=S, pady=button_width)

butt3 = CTkButton(menu_frame, text='Ready', command=fixed_ready, font=('arial',  int(button_width*2)))
butt3.grid(row=0, column=2, ipady=(button_width/2), ipadx=button_width*2, sticky=S, pady=button_width)

butt4 = CTkButton(menu_frame, text='Picked Up', font=('arial',  int(button_width*2)))
butt4.grid(row=0, column=3, ipady=(button_width/2), ipadx=button_width*2, sticky=S, pady=button_width)

butt5 = CTkButton(menu_frame, text='History', font=('arial',  int(button_width*2)))
butt5.grid(row=0, column=4, ipady=(button_width/2), ipadx=button_width*2, sticky=S, pady=button_width)

butt6 = CTkButton(menu_frame, text='Delete', command=delete_bike, font=('arial',  int(button_width*2)))
butt6.grid(row=0, column=5, ipady=(button_width/2), ipadx=button_width*2, sticky=S, pady=button_width)

Grid.rowconfigure(menu_frame, index=0, weight=1)


button_list = [ butt1, butt2, butt3, butt4, butt5, butt6,]

column_number = 0

for button in button_list:
    Grid.columnconfigure(menu_frame, column_number, weight=1)
    column_number += 1


# appearance_frame = CTkFrame(main_frame)
# appearance_frame.pack(side=TOP)

def change_appearance_mode_event(new_appearance_mode: str):
    set_appearance_mode(new_appearance_mode)


appearance_mode_label = CTkLabel(main_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.pack(side=TOP, anchor=NE, padx=button_width*2)

appearance_mode_optionemenu = CTkOptionMenu(main_frame, values=["Dark", "Light"], command=change_appearance_mode_event)
appearance_mode_optionemenu.pack(side=TOP, anchor=NE, padx=button_width*2)




content_frame = CTkFrame(main_frame)
content_frame.pack(side=TOP, fill=BOTH, expand=1, pady=button_width*3, padx=button_width*3)




my_tree_frame = CTkFrame(content_frame)
my_tree_frame.pack( side=LEFT, expand=True, fill='both')

my_tree = ttk.Treeview(my_tree_frame, selectmode='extended')
my_tree.pack(fill='both', expand=True)

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

my_tree.tag_configure('oddrow', background= '#262626', foreground='white')
my_tree.tag_configure('evenrow',background='#222222', foreground='white')

s = ttk.Style()
s.theme_use('clam')
s.configure('Treeview.Heading', background="#003f6b", foreground='white', font=('arial', int(button_width*1.3), 'bold' ), height=14, bordercolor='#303030', darkcolor="#303030" )
s.configure('Treeview', rowheight=int(button_width*3.5), font=('Verdana' ,13), fieldbackground="#262626", bordercolor='#262626', border=0)
s.map('Treeview', background=[('selected', '#363636')])
# entries_buttons_and_work = Frame(my_tree_frame, background=darkpurple, width=screen_width/2, height=screen_height/2)
# entries_buttons_and_work.pack(fill='both', expand=True)
# entries_buttons_and_work.propagate(0)

# entries_and_buttons = LabelFrame(entries_buttons_and_work, text='Service Details', background=darkpurple, foreground='white', font=('Verdana', 11))
# entries_and_buttons.pack(fill='both', expand=True, padx=20, pady=20)


# work_entry = Label(entries_and_buttons, font=('Verdana', 14), background='white')
# work_entry.pack(padx=(button_width*2), pady=button_width*2, side=BOTTOM, fill='both', expand=True)


query_database()












root.mainloop()
