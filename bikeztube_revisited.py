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
# screen_resolution = str(screen_width)+'x'+str(screen_height)
# print(screen_resolution)

# root.geometry(screen_resolution+'+-10+-1')

root.attributes('-fullscreen')

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


def get_history():
    
    his = CTkToplevel(root) 
    his.state('zoomed') 
    his.wm_transient(root)  
    


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
        clear_hist_entries()


    def clear_hist_entries():
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
        clear_hist_entries()

        messagebox.showinfo("Deleted!", "Your Bike Service Has Been Deleted!")

    def select_record_hist(e):
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


    hist_frame = CTkFrame(his)
    hist_frame.pack(fill='both', expand=True, pady=button_width*2, padx=button_width*2)

    my_hist_tree_frame = CTkFrame(hist_frame)
    my_hist_tree_frame.pack(pady=(button_width*2, button_width*4), padx=button_width*2, side=LEFT, expand=True, fill='both')

    buttons_hist_frame = CTkFrame(hist_frame)
    buttons_hist_frame.pack(side=RIGHT, fill='y', expand=1, pady=(0, button_width))

    my_hist_tree = ttk.Treeview(my_hist_tree_frame, selectmode='extended')
    my_hist_tree.pack(fill='both', expand=True, pady=(button_width*2), padx=button_width*2)

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

    my_hist_tree.tag_configure('oddrow', background= '#319f6d', foreground='#ffffff')
    my_hist_tree.tag_configure('evenrow',background='#288058', foreground='#ffffff')

    entries_frame = CTkFrame(buttons_hist_frame)
    entries_frame.pack(fill='y', expand=1)

    search_frame = CTkFrame(entries_frame)
    search_frame.pack(fill='x', expand=1, padx=button_width*2, pady=button_width)

    searchbox_label = CTkLabel(search_frame, text='Search :  ', justify=CENTER)
    searchbox_label.pack(side=LEFT, padx=(button_width*2,0), pady=(button_width*2))

    searchbox_entry = CTkEntry(search_frame)
    searchbox_entry.pack(side=RIGHT, padx=(0, button_width*2) , pady=button_width*2, fill='x', expand=1)

    search_frame_buttons= CTkFrame(entries_frame)
    search_frame_buttons.pack(fill='x', padx=(button_width*2), pady=(0, button_width)) 

    reset_button = CTkButton(search_frame_buttons, text='Reset', command=reset)
    reset_button.pack(side=LEFT, pady=button_width, padx=(button_width, int(button_width/2)), fill='x', expand=1)

    search_button = CTkButton(search_frame_buttons, text='Go', command=searcht)
    search_button.pack(side=RIGHT, pady=button_width, padx=(int(button_width/2), button_width), fill='x', expand=1)

    entries_frame2 = CTkFrame(entries_frame)
    entries_frame2.pack(fill='both', expand=1, padx=button_width*2)

    date_entry2 = cal.DateEntry(entries_frame2, width=button_width*3, date_pattern='dd/MM/yyyy', font=('roboto', int(button_width*1.5)))
    date_entry2.pack(fill='x', expand=1, padx=button_width*2)

    id_label2 = CTkLabel(entries_frame2, text="ID (Always Leave Empty!)")
    id_label2.pack()

    id_entry2 = CTkEntry(entries_frame2)
    id_entry2.pack()

    name_label2 = CTkLabel(entries_frame2, text="Name")
    name_label2.pack()

    name_entry2 = CTkEntry(entries_frame2)
    name_entry2.pack()

    phone_label2 = CTkLabel(entries_frame2, text="Phone")
    phone_label2.pack()

    phone_entry2 = CTkEntry(entries_frame2)
    phone_entry2.pack()

    bike_label2 = CTkLabel(entries_frame2, text="Bike")
    bike_label2.pack()

    bike_entry2 = CTkEntry(entries_frame2)
    bike_entry2.pack()

    work_label2 = CTkLabel(entries_frame2, text="Work")
    work_label2.pack()

    work_entry2 = CTkTextbox(entries_frame2, height=3)
    work_entry2.pack()

    total_price_label2 = CTkLabel(entries_frame2, text="Total")
    total_price_label2.pack()

    total_price_entry2 = CTkEntry(entries_frame2)
    total_price_entry2.pack()

    buttons_hist = CTkFrame(entries_frame)
    buttons_hist.pack(fill='x', expand=1, padx=button_width*2, pady=button_width*2)

    del_button2 = CTkButton(buttons_hist, text="Update" , command=update_bike)
    del_button2.pack(side=LEFT, pady=button_width, padx=(button_width, int(button_width/2)), fill='x', expand=1)

    update_bike_button2 = CTkButton(buttons_hist, text="Delete", command=delete_bike)
    update_bike_button2.pack(side=RIGHT, pady=button_width, padx=(int(button_width/2), button_width), fill='x', expand=1)

    my_hist_tree.bind("<ButtonRelease-1>", select_record_hist)
    query_history()


    his.mainloop()



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
        s.configure('Treeview',  fieldbackground="#363636")
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


def select_record(e):

    global service_text


    try:

        curItem = my_tree.focus()
        item_data = (my_tree.item(curItem))
        item_values = item_data['values']
        id_from_selection = str(item_values[4])

        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute('SELECT work FROM bikes WHERE rowid=' +id_from_selection )
        records = c.fetchall()
        records_list = records[0]
        service_text.set('Service Details :  '+records_list[0])
        conn.commit()
        conn.close()

       

    except:
        pass  

menu_width = (screen_width/9)
button_width = int(menu_width/14)

main_frame = CTkFrame(root)
main_frame.pack(fill=BOTH, expand=1)

menu_frame = CTkFrame(main_frame, width=menu_width*1.2)
menu_frame.pack(side=LEFT,fill=Y)
menu_frame.propagate(0)

butt_padx = int(button_width)
butt_pady = int(button_width)

title_label = CTkLabel(menu_frame, text="Workshop Helper", font=('roboto', button_width*1.5))
title_label.pack(pady=(int(button_width*3),int(button_width*1.5)),  padx=button_width*2 ,fill='x')

butt1 = CTkButton(menu_frame, text='+ Add', command=add_bike, font=('roboto', int(button_width*1.4), 'bold'))
butt1.pack(ipady=int(button_width/2), pady=(int(button_width*2), 0), padx=button_width*2 ,fill='x')

butt2 = CTkButton(menu_frame, text='Update', command=update_bike, font=('roboto',  int(button_width*1.4), 'bold'))
butt2.pack(pady=button_width, ipady=int(button_width/2), padx=button_width*2 ,fill='x')

butt3 = CTkButton(menu_frame, text='Ready', command=fixed, font=('roboto',  int(button_width*1.4), 'bold'))
butt3.pack(ipady=int(button_width/2), padx=button_width*2 ,fill='x')

butt4 = CTkButton(menu_frame, text='Collected', command=fixed_bike, font=('roboto',  int(button_width*1.4), 'bold'))
butt4.pack(pady=button_width, ipady=int(button_width/2), padx=button_width*2 ,fill='x')

appearance_mode_optionemenu = CTkOptionMenu(menu_frame, values=["Dark", "Light"], command=change_appearance_mode_event)
appearance_mode_optionemenu.pack(side=BOTTOM, pady=(0,40))

appearance_mode_label = CTkLabel(menu_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.pack(side=BOTTOM)

butt5 = CTkButton(menu_frame, text='Delete', command=delete_bike, font=('roboto',  int(button_width*1.4), 'bold'))
butt5.pack(side=BOTTOM, ipady=int(button_width/2), pady=(0,button_width*2), padx=button_width*2 ,fill='x')

content_frame = CTkFrame(main_frame)
content_frame.pack(side=RIGHT, fill=BOTH, expand=1, pady=(button_width*3, 0), padx=button_width*3)

tree_and_bar_frame = CTkFrame(content_frame)
tree_and_bar_frame.pack( expand=True, fill='both')

my_tree_frame = CTkFrame(tree_and_bar_frame)
my_tree_frame.pack( expand=True, fill='both')

my_tree = ttk.Treeview(my_tree_frame, selectmode='extended')
my_tree.pack(fill='both', expand=True)

bar_and_label_frame = CTkFrame(tree_and_bar_frame)
bar_and_label_frame.pack( fill='x', anchor=N, pady=(button_width*1.5, 0))

bar_label = CTkLabel(bar_and_label_frame, text='Shop capacity : ', font=('roboto', button_width, 'bold'))
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
s.configure('Treeview', rowheight=int(button_width*6), font=('roboto' ,button_width*2 ), fieldbackground="#363636", bordercolor='#262626')
s.map('Treeview', background=[('selected', '#319f6d')])

more_butt_frame = CTkFrame(content_frame)
more_butt_frame.pack(fill='x',  side=BOTTOM)

details_and_label_frame = CTkFrame(more_butt_frame)
details_and_label_frame.pack(anchor=W,side=LEFT, fill='x', expand=1, pady=(button_width*1.5), padx=(0, button_width*1.5))

service_text = StringVar()
service_text.set('Click A Customer To Show Its Details')
service_details_label = CTkLabel(details_and_label_frame, height=button_width*6.3, wraplength=button_width*50, justify=LEFT, textvariable=service_text , font=('roboto', button_width*1.5))
service_details_label.pack(anchor=NW, pady=button_width, padx= button_width*1.5)

stat_frame = CTkFrame(more_butt_frame)
stat_frame.pack(side=RIGHT, pady=button_width*1.5, anchor=N)

checkbuttons_frame = CTkFrame(stat_frame)
checkbuttons_frame.pack(pady=button_width, padx=(button_width*1.5))

checkbox_1 = CTkCheckBox(master=checkbuttons_frame, text='Basic Service', font=('roboto', button_width))
checkbox_1.pack(pady=button_width, padx=(button_width*2, 0), side=LEFT)

checkbox_2 = CTkCheckBox(master=checkbuttons_frame, text='Commuter Service', font=('roboto', button_width))
checkbox_2.pack(pady=button_width, padx=(button_width, 0), side=LEFT)

checkbox_3 = CTkCheckBox(master=checkbuttons_frame, text='Full Service', font=('roboto', button_width))
checkbox_3.pack(pady=button_width, padx=(button_width), side=LEFT)

graph_butt = CTkButton(stat_frame, text='Statistics', font=('roboto',  int(button_width*1.1), 'bold'))
graph_butt.pack(pady=(0, button_width), padx=( button_width*1.5), side=LEFT, fill='x', expand=1)

hist_butt = CTkButton(stat_frame, text='History', command=get_history, font=('roboto',  int(button_width*1.1), 'bold'))
hist_butt.pack(pady=(0, button_width,), padx=(0, button_width*1.5), side=RIGHT, fill='x', expand=1)

query_database()

my_tree.bind("<ButtonRelease-1>", select_record)

root.mainloop()
