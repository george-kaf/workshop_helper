import contextlib
from tkinter import *
from tkinter import ttk
from tkcalendar import * 
import sqlite3
from tkinter import messagebox
from itertools import count
from customtkinter import *
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


darkpurple = '#3B3355'
mediumpurple = '#5D5D81'
lightpurple = '#909CC2'
lightgreen = '#CEEC97'
lightgreen2= '#DBE4CB'
darkgreen = '#909CC2'

root = CTk()
root.title("Bikeztube")
root.state('zoomed') 

screen_width = root.winfo_screenwidth()
screen_height = int(root.winfo_screenheight()/1.05)

set_appearance_mode("light")  # Modes: "System" (standard), "Dark", "Light"
set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

conn = sqlite3.connect('bikes.db')
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS bikes (
    name text,
    phone text,
    bike text,
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
    date text,
    work text,
    total text
)
""")

c.execute("""CREATE TABLE IF NOT EXISTS quotes (
    quote text,
    name text,
    bike text,
    phone text
)
""")

c.execute("""CREATE TABLE IF NOT EXISTS cre (
    usr text,
    pss text,
    recip text,
    sub text
)
""")

c.execute(
    "INSERT INTO cre VALUES (:usr, :pss, :recip, :sub )",
    {
        'usr': "Sample",
        'pss':"Sample",
        'recip': "Sample",
        'sub': "Sample"
    },
)
conn.commit()
conn.close()

def add_bike():
    def add_bike_to_database():
        # delete the last letter of work entry so it is not nothing after a comma
        work_entry_limit = (work_entry.get('0.0', END))
        phone_number_limit = (phone_entry.get())
        if len(phone_number_limit) < 11:
            messagebox.showinfo("Invalid Number", "Phone number has 10 or less digits. Please put a number with 11 or more")
        else:
            if len(work_entry_limit) > 200:
                messagebox.showinfo("Too Long", "Please keep work entry under 200 character!")
            else:
                conn = sqlite3.connect('bikes.db')
                c = conn.cursor()
                c.execute(
                    "INSERT INTO bikes VALUES (:name, :phone, :bike, :date , :work, :total, :Ready)",
                    {
                        'name': name_entry.get().strip(),
                        'phone': phone_entry.get().strip(),
                        'bike': bike_entry.get().strip(),
                        'date': date_entry.get(),
                        'work': work_entry.get('0.0', END).strip(),
                        'total': f'£{total_price_entry.get().strip()}',
                        'Ready': '',
                    },
                )
                conn.commit()
                conn.close()

                if quote_var.get() == 'yes':
                    conn = sqlite3.connect('bikes.db')
                    c = conn.cursor()
                    c.execute("INSERT INTO quotes VALUES (:quote, :name, :bike, :phone)",
                        {
                            'quote':quote_var.get().strip(),
                            'name':name_entry.get().strip(),
                            'bike':bike_entry.get().strip(),
                            'phone':phone_entry.get().strip(),      
                        })
                    conn.commit()
                    conn.close()

                refresh_quotes()
                add_level.destroy()
                my_tree.delete(*my_tree.get_children())
                query_database()
                capacity()

                            # the bike's id after add bike is the length of the treeview +1 where as in the history it is handled by a for loop with count for iid


    add_level = CTkToplevel(root)
    add_level.title("Add Customer")

    add_level.wm_transient(root)    

    entries_buttons_and_work = CTkFrame(add_level)
    entries_buttons_and_work.pack(fill='both', expand=True, side=LEFT)

    entries_frame = CTkFrame(entries_buttons_and_work)
    entries_frame.pack(padx=20, pady=20, ipadx=50)

    date_label = CTkLabel(entries_frame, text="Date : ", font=('roboto', 14, 'bold'))
    date_label.grid(row=0, column=0, sticky=W, padx=(button_width, 0))

    date_entry = DateEntry(entries_frame, date_pattern='dd/MM/yyyy', font=('roboto', 11))
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

    quote_var = StringVar(entries_frame, "no")
    checkbox_q = CTkCheckBox(entries_frame, text='Needs Quote', variable=quote_var, onvalue='yes', offvalue='no', font=('roboto', 14))
    checkbox_q.grid(row=3, column=3, sticky=E, pady=(0, 20))
    quote_var.set("yes")

    work_label = CTkLabel(entries_frame, text="Work : ", font=('roboto', 14, 'bold'))
    work_label.grid(row=4, column=0, sticky=NW, padx=(button_width, 0))

    work_entry = CTkTextbox(entries_frame, font=('roboto',14), width=button_width*35, height=button_width*10)
    work_entry.grid(row=4, column=1, columnspan=5, sticky=W)

    add_but = CTkButton(entries_frame, text="Add", command=add_bike_to_database, font=('roboto', button_width), width=button_width*7)
    add_but.grid(row=5, column=3, sticky=E, pady=20)

    service_parts = CTkFrame(add_level)
    service_parts.pack(fill='both', expand=True, side=RIGHT)

    service_options_list_frame = CTkFrame(service_parts)
    service_options_list_frame.pack(side=LEFT, padx= button_width*2, pady=button_width*2, anchor=N)

    service_options_list_frame2 = CTkFrame(service_parts)
    service_options_list_frame2.pack(side=LEFT, padx= (0,button_width*2), pady=button_width*2, anchor=N)

    service_options_list_frame3 = CTkFrame(service_parts)
    service_options_list_frame3.pack(side=LEFT, padx= (0,button_width*2), pady=button_width*2, anchor=N)

    service_choice = CTkFrame(service_options_list_frame, fg_color="transparent")
    service_choice.pack(pady=button_width, padx=button_width)

    basic_butt = CTkButton(service_choice, text="Basic Service", command=lambda: work_entry.insert(END, 'Basic Service '))
    basic_butt.pack()

    commuter_butt = CTkButton(service_choice, text="Commuter Service", command=lambda: work_entry.insert(END, 'Commuter Service '))
    commuter_butt.pack()

    full_butt = CTkButton(service_choice, text="Full Service", command=lambda: work_entry.insert(END, 'Full Service '))
    full_butt.pack()

    brakes_choice = CTkFrame(service_options_list_frame, fg_color="transparent")
    brakes_choice.pack( padx=button_width)

    BrakePadsF_butt = CTkButton(brakes_choice, text="Brake Pads Front", command=lambda: work_entry.insert(END, 'Brake Pads Front '))
    BrakePadsF_butt.pack()

    BrakePadsR_butt = CTkButton(brakes_choice, text="Brake Pads Rear", command=lambda: work_entry.insert(END, 'Brake Pads Rear '))
    BrakePadsR_butt.pack()

    BrakeWireF_butt = CTkButton(brakes_choice, text="Brake Wire Front", command=lambda: work_entry.insert(END, 'Brake Wire Front '))
    BrakeWireF_butt.pack()

    BrakeWireR_butt = CTkButton(brakes_choice, text="Brake Wire Rear", command=lambda: work_entry.insert(END, 'Brake Wire Rear '))
    BrakeWireR_butt.pack()

    wheels_choice = CTkFrame(service_options_list_frame, fg_color="transparent")
    wheels_choice.pack(pady=button_width, padx=button_width)

    TyreFront_butt = CTkButton(wheels_choice, text="Tyre Front", command=lambda: work_entry.insert(END, 'Tyre Front '))
    TyreFront_butt.pack()

    Tyre_Rear_butt = CTkButton(wheels_choice, text="Tyre Rear", command=lambda: work_entry.insert(END, 'Tyre Rear '))
    Tyre_Rear_butt.pack()

    innerTubeFront_butt = CTkButton(wheels_choice, text="Inner Tube Front", command=lambda: work_entry.insert(END, 'Inner Tube Front '))
    innerTubeFront_butt.pack()

    innerTubeREAR_butt = CTkButton(wheels_choice, text="Inner Tube Rear", command=lambda: work_entry.insert(END, 'Inner Tube Rear '))
    innerTubeREAR_butt.pack()

    wheelF_butt = CTkButton(wheels_choice, text="Wheel Front", command=lambda: work_entry.insert(END, 'Wheel Front '))
    wheelF_butt.pack()

    wheelR_butt = CTkButton(wheels_choice, text="Wheel Rear", command=lambda: work_entry.insert(END, 'Wheel Rear '))
    wheelR_butt.pack()

    gears_choice = CTkFrame(service_options_list_frame2, fg_color="transparent")
    gears_choice.pack(pady=button_width, padx=button_width)

    GearWireF_butt = CTkButton(gears_choice, text="Gear Wire Front", command=lambda: work_entry.insert(END, 'Gear Wire Front '))
    GearWireF_butt.pack()

    GearWireR_butt = CTkButton(gears_choice, text="Gear Wire Rear", command=lambda: work_entry.insert(END, 'Gear Wire Rear '))
    GearWireR_butt.pack()

    Chain_butt = CTkButton(gears_choice, text="Chain", command=lambda: work_entry.insert(END, 'Chain '))
    Chain_butt.pack()

    Cassette_butt = CTkButton(gears_choice, text="Cassette", command=lambda: work_entry.insert(END, 'Cassette '))
    Cassette_butt.pack()

    Crankset_butt = CTkButton(gears_choice, text="Crankset", command=lambda: work_entry.insert(END, 'Crankset '))
    Crankset_butt.pack()

    Chainring_butt = CTkButton(gears_choice, text="Chainring", command=lambda: work_entry.insert(END, 'Chainring '))
    Chainring_butt.pack()

    DerailleurF_butt = CTkButton(gears_choice, text="Derailleur Front", command=lambda: work_entry.insert(END, 'Derailleur Front '))
    DerailleurF_butt.pack()

    DerailleurR_butt = CTkButton(gears_choice, text="Derailleur Rear", command=lambda: work_entry.insert(END, 'Derailleur Rear '))
    DerailleurR_butt.pack()

    frame_choice = CTkFrame(service_options_list_frame2, fg_color="transparent")
    frame_choice.pack(pady=(0, button_width), padx=button_width)

    headset_butt = CTkButton(frame_choice, text="Headset", command=lambda: work_entry.insert(END, 'Headset '))
    headset_butt.pack()

    BottomB_butt = CTkButton(frame_choice, text="Bottom Bracket", command=lambda: work_entry.insert(END, 'Bottom Bracket '))
    BottomB_butt.pack()

    hanger_butt = CTkButton(frame_choice, text="Hanger", command=lambda: work_entry.insert(END, 'Hanger '))
    hanger_butt.pack()

    Pedals_butt = CTkButton(frame_choice, text="Pedals", command=lambda: work_entry.insert(END, 'Pedals '))
    Pedals_butt.pack()

    Bartape_butt = CTkButton(frame_choice, text="Bartape", command=lambda: work_entry.insert(END, 'Bartape '))
    Bartape_butt.pack()

    grips_butt = CTkButton(frame_choice, text="Grips", command=lambda: work_entry.insert(END, 'Grips '))
    grips_butt.pack()

    adj_choice = CTkFrame(service_options_list_frame3, fg_color="transparent")
    adj_choice.pack(pady=button_width, padx=button_width)

    GearAdjF_butt = CTkButton(adj_choice, text="Gear Adjust. Front", command=lambda: work_entry.insert(END, 'Gear Adjustment Front '))
    GearAdjF_butt.pack()

    GearAdjR_butt = CTkButton(adj_choice, text="Gear Adjust. Rear", command=lambda: work_entry.insert(END, 'Gear Adjustment Rear '))
    GearAdjR_butt.pack()

    BrakeAdjF_butt = CTkButton(adj_choice, text="Brake Adjust. Front", command=lambda: work_entry.insert(END, 'Brake Adjustment Front '))
    BrakeAdjF_butt.pack()

    BrakeAdjR_butt = CTkButton(adj_choice, text="Brake Adjust. Rear", command=lambda: work_entry.insert(END, 'Brake Adjustment Rear '))
    BrakeAdjR_butt.pack()

    HeadAdj_butt = CTkButton(adj_choice, text="Headset Adjust.", command=lambda: work_entry.insert(END, 'Headset Adjustment '))
    HeadAdj_butt.pack()

    BottombAdj_butt = CTkButton(adj_choice, text="B. Bracket Adjust.", command=lambda: work_entry.insert(END, 'Bottom Bracket Adjustment '))
    BottombAdj_butt.pack()

    add_level.mainloop()

def update_bike():
    with contextlib.suppress(Exception):
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
            global quotes
            MsgBox = messagebox.askquestion ('Update bike','Are you sure?')
            if MsgBox == 'yes':
                limit2 = (work_entry1.get('0.0', END))
                if len(limit2) > 200:
                    messagebox.showinfo("Too Long", "Please keep work entry under 200 character!")
                else: 
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
                                'name':name_entry1.get().strip(),
                                'phone':phone_entry1.get().strip(),
                                'bike':bike_entry1.get().strip(),
                                'oid':id_from_selection,
                                'date':date_entry1.get(),
                                'work':work_entry1.get('0.0', END).strip(),
                                'total':total_price_entry1.get().strip()

                        }
                    )

                    conn.commit()
                    conn.close()

                    if quote_var3.get() == 'yes':
                        conn = sqlite3.connect('bikes.db')
                        c = conn.cursor()
                        c.execute("DELETE from quotes WHERE name=? AND bike=?", (name_entry1.get(), bike_entry1.get()))
                        conn.commit()
                        conn.close()

                    refresh_quotes()
                    my_tree.delete(*my_tree.get_children())
                    query_database()
                    update_level.destroy()

        def insert_entries():
            date_entry1.set_date(item_values[5]),
            name_entry1.insert(0, item_values[1]),
            phone_entry1.insert(0, item_values[2]),
            bike_entry1.insert(0, item_values[3]),
            total_price_entry1.insert(0, item_values[6]),
            work_entry1.insert('1.0',  work)

        update_level = CTkToplevel(root)
        update_level.title("Update")

        update_level.wm_transient(root)    

        entries_buttons_and_work1 = CTkFrame(update_level)
        entries_buttons_and_work1.pack(fill='both', expand=True, side=LEFT)

        entries_frame1 = CTkFrame(entries_buttons_and_work1)
        entries_frame1.pack(padx=20, pady=20, ipadx=50)

        date_label1 = CTkLabel(entries_frame1, text="Date : ", font=('roboto', 14, 'bold'))
        date_label1.grid(row=0, column=0, sticky=W, padx=(button_width, 0))

        date_entry1 = DateEntry(entries_frame1, date_pattern='dd/MM/yyyy', font=('roboto', 11))
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

        quote_var3 = StringVar(entries_frame1)
        checkbox_q3 = CTkCheckBox(entries_frame1, text='Quote Confirmed !', variable=quote_var3, onvalue='yes', offvalue='no', font=('roboto', 14))
        checkbox_q3.grid(row=4, column=3, sticky=E, pady=(0, 20))

        work_label1 = CTkLabel(entries_frame1, text="Work : ", font=('roboto', 14, 'bold'))
        work_label1.grid(row=5, column=0, sticky=NW, padx=(button_width, 0))

        work_entry1 = CTkTextbox(entries_frame1, font=('roboto',14), width=button_width*35)
        work_entry1.grid(row=5, column=1, columnspan=3, sticky=W)

        update_but1 = CTkButton(entries_frame1, text="Update", command=update_bike_in_database, font=('roboto', button_width), width=button_width*7)
        update_but1.grid(row=6, column=3, sticky=E, pady=20)

        service_parts1 = CTkFrame(update_level)
        service_parts1.pack(fill='both', expand=True, side=LEFT)

        service_options_list_frame = CTkFrame(service_parts1)
        service_options_list_frame.pack(side=LEFT, padx= button_width*2, pady=button_width*2)

        service_options_list_frame2 = CTkFrame(service_parts1)
        service_options_list_frame2.pack(side=LEFT, padx= (0,button_width*2), pady=button_width*2)

        service_options_list_frame3 = CTkFrame(service_parts1)
        service_options_list_frame3.pack(side=LEFT, padx= (0,button_width*2), pady=button_width*2)

        service_choice = CTkFrame(service_options_list_frame, fg_color="transparent")
        service_choice.pack(pady=button_width, padx=button_width)

        basic_butt = CTkButton(service_choice, text="Basic Service", command=lambda: work_entry1.insert(END, 'Basic Service '))
        basic_butt.pack()

        commuter_butt = CTkButton(service_choice, text="Commuter Service", command=lambda: work_entry1.insert(END, 'Commuter Service '))
        commuter_butt.pack()

        full_butt = CTkButton(service_choice, text="Full Service", command=lambda: work_entry1.insert(END, 'Full Service '))
        full_butt.pack()

        brakes_choice = CTkFrame(service_options_list_frame, fg_color="transparent")
        brakes_choice.pack( padx=button_width)

        BrakePadsF_butt = CTkButton(brakes_choice, text="Brake Pads Front", command=lambda: work_entry1.insert(END, 'Brake Pads Front '))
        BrakePadsF_butt.pack()

        BrakePadsR_butt = CTkButton(brakes_choice, text="Brake Pads Rear", command=lambda: work_entry1.insert(END, 'Brake Pads Rear '))
        BrakePadsR_butt.pack()

        BrakeWireF_butt = CTkButton(brakes_choice, text="Brake Wire Front", command=lambda: work_entry1.insert(END, 'Brake Wire Front '))
        BrakeWireF_butt.pack()

        BrakeWireR_butt = CTkButton(brakes_choice, text="Brake Wire Rear", command=lambda: work_entry1.insert(END, 'Brake Wire Rear '))
        BrakeWireR_butt.pack()

        wheels_choice = CTkFrame(service_options_list_frame, fg_color="transparent")
        wheels_choice.pack(pady=button_width, padx=button_width)

        TyreFront_butt = CTkButton(wheels_choice, text="Tyre Front", command=lambda: work_entry1.insert(END, 'Tyre Front '))
        TyreFront_butt.pack()

        Tyre_Rear_butt = CTkButton(wheels_choice, text="Tyre Rear", command=lambda: work_entry1.insert(END, 'Tyre Rear '))
        Tyre_Rear_butt.pack()

        innerTubeFront_butt = CTkButton(wheels_choice, text="Inner Tube Front", command=lambda: work_entry1.insert(END, 'Inner Tube Front '))
        innerTubeFront_butt.pack()

        innerTubeREAR_butt = CTkButton(wheels_choice, text="Inner Tube Rear", command=lambda: work_entry1.insert(END, 'Inner Tube Rear '))
        innerTubeREAR_butt.pack()

        wheelF_butt = CTkButton(wheels_choice, text="Wheel Front", command=lambda: work_entry1.insert(END, 'Wheel Front '))
        wheelF_butt.pack()

        wheelR_butt = CTkButton(wheels_choice, text="Wheel Rear", command=lambda: work_entry1.insert(END, 'Wheel Rear '))
        wheelR_butt.pack()

        gears_choice = CTkFrame(service_options_list_frame2, fg_color="transparent")
        gears_choice.pack(pady=button_width, padx=button_width)

        GearWireF_butt = CTkButton(gears_choice, text="Gear Wire Front", command=lambda: work_entry1.insert(END, 'Gear Wire Front '))
        GearWireF_butt.pack()

        GearWireR_butt = CTkButton(gears_choice, text="Gear Wire Rear", command=lambda: work_entry1.insert(END, 'Gear Wire Rear '))
        GearWireR_butt.pack()

        Chain_butt = CTkButton(gears_choice, text="Chain", command=lambda: work_entry1.insert(END, 'Chain '))
        Chain_butt.pack()

        Cassette_butt = CTkButton(gears_choice, text="Cassette", command=lambda: work_entry1.insert(END, 'Cassette '))
        Cassette_butt.pack()

        Crankset_butt = CTkButton(gears_choice, text="Crankset", command=lambda: work_entry1.insert(END, 'Crankset '))
        Crankset_butt.pack()

        Chainring_butt = CTkButton(gears_choice, text="Chainring", command=lambda: work_entry1.insert(END, 'Chainring '))
        Chainring_butt.pack()

        DerailleurF_butt = CTkButton(gears_choice, text="Derailleur Front", command=lambda: work_entry1.insert(END, 'Derailleur Front '))
        DerailleurF_butt.pack()

        DerailleurR_butt = CTkButton(gears_choice, text="Derailleur Rear", command=lambda: work_entry1.insert(END, 'Derailleur Rear '))
        DerailleurR_butt.pack()

        frame_choice = CTkFrame(service_options_list_frame2, fg_color="transparent")
        frame_choice.pack(pady=(0, button_width), padx=button_width)

        headset_butt = CTkButton(frame_choice, text="Headset", command=lambda: work_entry1.insert(END, 'Headset '))
        headset_butt.pack()

        BottomB_butt = CTkButton(frame_choice, text="Bottom Bracket", command=lambda: work_entry1.insert(END, 'Bottom Bracket '))
        BottomB_butt.pack()

        hanger_butt = CTkButton(frame_choice, text="Hanger", command=lambda: work_entry1.insert(END, 'Hanger '))
        hanger_butt.pack()

        Pedals_butt = CTkButton(frame_choice, text="Pedals", command=lambda: work_entry1.insert(END, 'Pedals '))
        Pedals_butt.pack()

        Bartape_butt = CTkButton(frame_choice, text="Bartape", command=lambda: work_entry1.insert(END, 'Bartape '))
        Bartape_butt.pack()

        grips_butt = CTkButton(frame_choice, text="Grips", command=lambda: work_entry1.insert(END, 'Grips '))
        grips_butt.pack()

        adj_choice = CTkFrame(service_options_list_frame3, fg_color="transparent")
        adj_choice.pack(pady=button_width, padx=button_width)

        GearAdjF_butt = CTkButton(adj_choice, text="Gear Adjust. Front", command=lambda: work_entry1.insert(END, 'Gear Adjustment Front '))
        GearAdjF_butt.pack()

        GearAdjR_butt = CTkButton(adj_choice, text="Gear Adjust. Rear", command=lambda: work_entry1.insert(END, 'Gear Adjustment Rear '))
        GearAdjR_butt.pack()

        BrakeAdjF_butt = CTkButton(adj_choice, text="Brake Adjust. Front", command=lambda: work_entry1.insert(END, 'Brake Adjustment Front '))
        BrakeAdjF_butt.pack()

        BrakeAdjR_butt = CTkButton(adj_choice, text="Brake Adjust. Rear", command=lambda: work_entry1.insert(END, 'Brake Adjustment Rear '))
        BrakeAdjR_butt.pack()

        HeadAdj_butt = CTkButton(adj_choice, text="Headset Adjust.", command=lambda: work_entry1.insert(END, 'Headset Adjustment '))
        HeadAdj_butt.pack()

        BottombAdj_butt = CTkButton(adj_choice, text="B. Bracket Adjust.", command=lambda: work_entry1.insert(END, 'Bottom Bracket Adjustment '))
        BottombAdj_butt.pack()

        insert_entries()

        update_level.mainloop()

def get_history():
    his = CTkToplevel(root)
    his.state('zoomed')
    his.wm_transient(root)  


    def update_bike_in_db():
        curItem2 = my_hist_tree.focus()
        item_data2 = (my_hist_tree.item(curItem2))
        item_values2 = item_data2['values']
        id_from_selection2 = str(item_values2[3]) 

        selected = my_hist_tree.focus()
        my_hist_tree.item(selected, text='', values=(name_entry2.get(),phone_entry2.get(), bike_entry2.get(), id_from_selection2, date_entry2.get(), work_entry2.get('1.0', END), total_price_entry2.get()))

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
                    'oid':id_from_selection2,
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
        work_entry2.delete('1.0', END)
        total_price_entry2.delete(0, END)

    def delete_bike_hist():
        curItem3 = my_hist_tree.focus()
        item_data3 = (my_hist_tree.item(curItem3))
        item_values3 = item_data3['values']
        id_from_selection3 = str(item_values3[3])

        x = my_hist_tree.selection()[0]
        my_hist_tree.delete(x)

        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute(f"DELETE from history WHERE rowid={id_from_selection3}")
        conn.commit()
        conn.close()
        clear_hist_entries()

        my_hist_tree.delete(*my_hist_tree.get_children())
        query_history()

        messagebox.showinfo("Deleted!", "Your Bike Service Has Been Deleted!")

    def select_record_hist(e):
        with contextlib.suppress(Exception):
            name_entry2.delete(0, END)
            phone_entry2.delete(0, END)
            bike_entry2.delete(0, END)
            date_entry2.delete(0, END)
            work_entry2.delete('1.0', END)
            total_price_entry2.delete(0, END)

            selected = my_hist_tree.focus()
            values = my_hist_tree.item(selected, "values")

            name_entry2.insert(0, values[0])
            phone_entry2.insert(0, values[1])
            bike_entry2.insert(0, values[2])
            date_entry2.insert(0, values[4])
            work_entry2.insert('1.0', values[5])
            total_price_entry2.insert(0, values[6])

    def reset():
        my_hist_tree.delete(*my_hist_tree.get_children())

        name_entry2.delete(0, END)
        phone_entry2.delete(0, END)
        bike_entry2.delete(0, END)
        date_entry2.delete(0, END)
        work_entry2.delete('1.0', END)
        total_price_entry2.delete(0, END)
        query_history()

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
            if count % 2 == 0:
                my_hist_tree.insert(parent='', index='end', iid=count, text='', values=(l[0], str(l[1]), l[2], l[3], l[4], l[5], l[6]), tags=('evenrow',))
            else:
                my_hist_tree.insert(parent='', index='end', iid=count, text='', values=(l[0], str(l[1]), l[2], l[3], l[4], l[5], l[6]), tags=('oddrow',))
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
                my_hist_tree.insert(parent='', index='end',  text='', values=(str(record[1]), str(record[2]), str(record[3]), record[0], str(record[4]), str(record[5]), str(record[6])), tags=('evenrow',))
            else:
                my_hist_tree.insert(parent='', index='end',  text='', values=(str(record[1]), str(record[2]), str(record[3]), record[0], str(record[4]), str(record[5]), str(record[6])), tags=('oddrow',))
            count +=1
        conn.commit()
        conn.close() 

    hist_frame = CTkFrame(his)
    hist_frame.pack(fill='both', expand=True)

    my_hist_tree_frame = CTkFrame(hist_frame, width=screen_width/1.3)
    my_hist_tree_frame.pack(fill='both', expand=True,side=LEFT, pady=int(screen_height/8), padx=(button_width, 0))
    my_hist_tree_frame.propagate(0)

    buttons_hist_frame = CTkFrame(hist_frame)
    buttons_hist_frame.pack(side=RIGHT, fill='x', expand=1)

    my_hist_tree = ttk.Treeview(my_hist_tree_frame, selectmode='extended')
    my_hist_tree.pack(fill='both', expand=True)
   

    my_hist_tree['columns'] = ('Name', 'Phone', 'Bike', 'ID', 'Date', 'Work', 'Total')

    my_hist_tree.column('#0', width=0, stretch=NO)
    my_hist_tree.column("Name", anchor=CENTER)
    my_hist_tree.column("Phone", anchor=CENTER)
    my_hist_tree.column("Bike", anchor=CENTER)
    my_hist_tree.column("ID", anchor=CENTER, width=button_width*4)
    my_hist_tree.column("Date", anchor=CENTER)
    my_hist_tree.column("Work", anchor=CENTER)
    my_hist_tree.column("Total", anchor=CENTER)

    my_hist_tree.heading("#0", text="", anchor=CENTER)
    my_hist_tree.heading("Name", text="Name", anchor=CENTER)
    my_hist_tree.heading("Phone", text="Phone", anchor=CENTER)
    my_hist_tree.heading("Bike", text="Bike", anchor=CENTER)
    my_hist_tree.heading("ID", text="ID", anchor=CENTER)
    my_hist_tree.heading("Date", text="Date", anchor=CENTER)
    my_hist_tree.heading("Work", text="Work", anchor=CENTER)
    my_hist_tree.heading("Total", text="Total", anchor=CENTER)

    my_hist_tree.tag_configure('oddrow', background= '#236C4B', foreground='#ffffff')
    my_hist_tree.tag_configure('evenrow',background='#1D5F41', foreground='#ffffff')

    # entries_frame = CTkFrame(buttons_hist_frame, width=int(screen_width/4), height=int(screen_height/1.2))
    # entries_frame.pack(fill='y', expand=1)
    # entries_frame.propagate(0)

    search_frame = CTkFrame(buttons_hist_frame)
    search_frame.pack(fill='x',  padx=button_width*2, pady=(button_width))

    searchbox_label = CTkLabel(search_frame, text='Search :  ', justify=CENTER, font=("roboto", button_width*1.8))
    searchbox_label.pack(side=LEFT, padx=(button_width*2,0), pady=(button_width*2))

    searchbox_entry = CTkEntry(search_frame)
    searchbox_entry.pack(side=RIGHT, padx=(0, button_width*2) , pady=button_width*2, fill='x', expand=1)

    search_frame_buttons= CTkFrame(buttons_hist_frame)
    search_frame_buttons.pack(fill='x', padx=(button_width*2), pady=(0, button_width)) 

    reset_button = CTkButton(search_frame_buttons, text='Reset', command=reset, font=("roboto", button_width*1.8))
    reset_button.pack(side=LEFT, pady=button_width, padx=(button_width, int(button_width/2)), fill='x', expand=1)

    search_button = CTkButton(search_frame_buttons, text='Go', command=searcht, font=("roboto", button_width*1.8))
    search_button.pack(side=RIGHT, pady=button_width, padx=(int(button_width/2), button_width), fill='x', expand=1)

    entries_frame2 = CTkFrame(buttons_hist_frame)
    entries_frame2.pack(fill='both', expand=1, padx=button_width*2)

    date_entry2 = DateEntry(entries_frame2, date_pattern='dd/MM/yyyy', font=('roboto', int(button_width*1.8)))
    date_entry2.pack(fill='x',  padx=button_width*2, pady=(button_width*2))

    entries_and_labels_frame = CTkFrame(entries_frame2, corner_radius=0)
    entries_and_labels_frame.pack(fill='both', expand=1)

    name_frame = CTkFrame(entries_and_labels_frame, corner_radius=0, fg_color="transparent")
    name_frame.pack(fill='both', expand=1, pady=(button_width,0))

    name_label2 = CTkLabel(name_frame, text="Name :  ", width=button_width, font=('roboto', button_width*1.8, 'bold'), text_color='#585858')
    name_label2.pack(side=LEFT, anchor=E, fill='x', padx=button_width)

    name_entry2 = CTkEntry(name_frame, font=('roboto', button_width*1.8))
    name_entry2.pack(side=RIGHT, fill='x', expand=1)

    phone_frame = CTkFrame(entries_and_labels_frame, corner_radius=0, fg_color="transparent")
    phone_frame.pack(fill='both', expand=1, pady=(button_width,0))

    phone_label2 = CTkLabel(phone_frame, text="Phone :  ", width=button_width, font=('roboto', button_width*1.8, 'bold'), text_color='#585858')
    phone_label2.pack(side=LEFT, anchor=E, fill='x', padx=button_width)

    phone_entry2 = CTkEntry(phone_frame, font=('roboto', button_width*1.8))
    phone_entry2.pack(side=RIGHT, fill='x', expand=1)

    bike_frame = CTkFrame(entries_and_labels_frame, corner_radius=0, fg_color="transparent")
    bike_frame.pack(fill='both', expand=1, pady=(button_width,0))

    bike_label2 = CTkLabel(bike_frame, text="Bike :  ", width=button_width, font=('roboto', button_width*1.8, 'bold'), text_color='#585858')
    bike_label2.pack(side=LEFT, anchor=E, fill='x', padx=button_width*1.4)

    bike_entry2 = CTkEntry(bike_frame, font=('roboto', button_width*1.8))
    bike_entry2.pack(side=RIGHT, fill='x', expand=1)

    total_frame = CTkFrame(entries_and_labels_frame, corner_radius=0, fg_color="transparent")
    total_frame.pack(fill='both', expand=1, pady=(button_width,0))

    total_price_label2 = CTkLabel(total_frame, text="Total :  ", width=button_width, font=('roboto', button_width*1.8, 'bold'), text_color='#585858')
    total_price_label2.pack(side=LEFT, anchor=E, fill='x', padx=button_width*1.3)

    total_price_entry2 = CTkEntry(total_frame, font=('roboto', button_width*1.8))
    total_price_entry2.pack(side=RIGHT, fill='x', expand=1)

    work_frame = CTkFrame(entries_and_labels_frame, corner_radius=0, fg_color="transparent")
    work_frame.pack(fill='both', expand=1, pady=button_width)

    work_label2 = CTkLabel(work_frame, text="Work :  ", width=button_width, font=('roboto', button_width*1.8, 'bold'), text_color='#585858')
    work_label2.pack(side=LEFT, anchor=E, fill='x', padx=button_width*1.3)

    work_entry2 =CTkTextbox(work_frame, height=int(screen_height/9), font=('roboto', button_width*1.8))
    work_entry2.pack(side=RIGHT, fill='x', expand=1)

    buttons_hist = CTkFrame(buttons_hist_frame, fg_color="transparent")
    buttons_hist.pack(fill='x', padx=button_width*2, pady=button_width)

    del_button2 = CTkButton(buttons_hist, text="Update" , command=update_bike_in_db, font=("roboto", button_width*1.8))
    del_button2.pack(side=LEFT, pady=button_width, padx=(0, int(button_width/2)), fill='x', expand=1)

    update_bike_button2 = CTkButton(buttons_hist, text="Delete", command=delete_bike_hist, font=("roboto", button_width*1.8))
    update_bike_button2.pack(side=RIGHT, pady=button_width, padx=(int(button_width/2), 0), fill='x', expand=1)

    my_hist_tree.bind("<ButtonRelease-1>", select_record_hist)
    query_history()

    his.mainloop()

def query_database():
    global count
    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute('SELECT rowid, * FROM bikes')
    records = c.fetchall()
    for count, record in enumerate(records):
        if count % 2 ==0:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[7], record[1], record[2], record[3], record[0], record[4], record[6]), tags=('evenrow',))
        else:
            my_tree.insert(parent='', index='end', iid=count, text='', values=(record[7], record[1], record[2], record[3], record[0], record[4], record[6]), tags=('oddrow',))
    conn.commit()
    conn.close()

def delete_bike():
    with contextlib.suppress(Exception):
        curItem = my_tree.focus()
        item_data = (my_tree.item(curItem))
        item_values = item_data['values']
        if item_values:
            MsgBox = messagebox.askquestion ('Delete bike','Are you sure?')
            if MsgBox == 'yes':
                remove_item_from_database()
        else:
            messagebox.showinfo("No items selected", "Please select an item to delete")

def remove_item_from_database():
    curItem = my_tree.focus()
    item_data = (my_tree.item(curItem))
    item_values = item_data['values']
    id_from_selection = str(item_values[4])

    x = my_tree.selection()[0]
    my_tree.delete(x)

    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute(f"DELETE from bikes WHERE oid={id_from_selection}")
    c.execute("DELETE from quotes WHERE name=? AND bike=?", (str(item_values[1]), str(item_values[3])) )
    conn.commit()
    conn.close()

    messagebox.showinfo("Deleted!", "Your Bike Has Been Deleted!")

    capacity()
    refresh_quotes()

def fixed():

    with contextlib.suppress(Exception):
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
            insert_ready_inDb(
                """UPDATE bikes SET
                Ready = :ready
                WHERE oid = :oid""",
                '✓',
                id_from_selection,
            )
        if res_str[0] == '✓':
            insert_ready_inDb(
                """UPDATE bikes SET
                        Ready = :ready
                        WHERE oid = :oid""",
                '',
                id_from_selection,
            )

def insert_ready_inDb(arg0, arg1, id_from_selection):
    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute(arg0, {'ready': arg1, 'oid': id_from_selection})
    conn.commit()
    conn.close()
    my_tree.delete(*my_tree.get_children())
    query_database()

def change_appearance_mode_event(new_appearance_mode: str):
    set_appearance_mode(new_appearance_mode)
    if new_appearance_mode == "Dark":
        set_dark()
    elif new_appearance_mode == "Light":
        s.configure('Treeview.Heading', background="#ffffff", foreground='#555555', )
        s.configure('Treeview', fieldbackground="#cecece")
        s.map('Treeview', background=[('selected', '#55bd7f')], foreground=[('selected', 'white')])
        my_tree.tag_configure('oddrow', background= '#cccccc', foreground='#121212')
        my_tree.tag_configure('evenrow',background='#dddddd', foreground='#121212')

def set_dark():
    s.configure('Treeview.Heading', background="#181818", foreground='white', )
    s.configure('Treeview',  fieldbackground="#363636")
    s.map('Treeview', background=[('selected', '#319f6d')])
    my_tree.tag_configure('oddrow', background= '#363636', foreground='white')
    my_tree.tag_configure('evenrow',background='#303030', foreground='white')
    notif.configure(background="#343434", fg="#ffffff")

def fixed_bike():
    global progressbar
    MsgBox = messagebox.askquestion ('Delete bike','Are you sure?')
    if MsgBox == 'yes':
        curItem = my_tree.focus()
        item_data = (my_tree.item(curItem))
        item_values = item_data['values']
        id_from_selection = str(item_values[4])

        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute(f'SELECT * FROM bikes WHERE rowid={id_from_selection}')
        records = c.fetchall()
        records_list = records[0]
        print(records_list)
        conn.commit()
        conn.close()

        x = my_tree.selection()[0]
        my_tree.delete(x)

        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute("INSERT INTO history VALUES (:name, :phone, :bike, :date, :work, :total)",
                {
                    'name':records_list[0],
                    'phone':records_list[1],
                    'bike':records_list[2],
                    'date':records_list[3],
                    'work':records_list[4],
                    'total':records_list[5]

                })
        c.execute(f"DELETE from bikes WHERE oid={id_from_selection}")
        c.execute("DELETE from quotes WHERE name=? AND bike=?", (str(item_values[1]), str(item_values[3])) )
        conn.commit()
        conn.close()

        messagebox.showinfo("Done!", "Service Record Saved !")
        refresh_quotes()
        capacity()

def select_record(e):
    global service_text
    with contextlib.suppress(Exception):
        curItem = my_tree.focus()
        item_data = (my_tree.item(curItem))
        item_values = item_data['values']
        id_from_selection = str(item_values[4])

        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute(f'SELECT work FROM bikes WHERE rowid={id_from_selection}')
        records = c.fetchall()
        records_list = records[0]
        service_text.set(records_list[0])
        conn.commit()
        conn.close()  

def change_scaling_event(new_scaling: str):
    
    global button_width
    if new_scaling == "Large":
        button_width3 = button_width
        set_widget_scaling(1.0)
        s=ttk.Style()
        s.configure('Treeview.Heading', font=('roboto', int(button_width3*2), 'bold' ), borderwidth=0 )
        s.configure('Treeview', rowheight= int(button_width3*4) , font=('roboto' , int(button_width3*2)))

    elif new_scaling == "Small":
        button_width2 = int(button_width/1.1)
        set_widget_scaling(0.8)
        s=ttk.Style()
        s.configure('Treeview.Heading', font=('roboto', int(button_width2*1.1), 'bold' ), borderwidth=0 )
        s.configure('Treeview', rowheight= int(button_width2*4) , font=('roboto' , int(button_width2*1.5)))

    elif new_scaling == "Standard":
        button_width4 = button_width*1.7
        set_widget_scaling(0.9)
        s=ttk.Style()
        s.configure('Treeview.Heading',  font=('roboto', int(button_width4), 'bold' ), borderwidth=0 )
        s.configure('Treeview', rowheight=int(button_width4*2.5), font=('roboto' , int(button_width4) ))

def capacity():
    progressbar.set(0)
    cap = 0

    for _ in my_tree.get_children():
        cap += 1 / 25
        progressbar.set(cap) 

def refresh_quotes():
    global quote

    if starting_quotes := _extracted_from_refresh_quotes_13(quote):
        starting_quotes = _extracted_from_refresh_quotes_13(quote)
        quote_list_of_top_4 = starting_quotes[:4]

        quotes_for_display = list(quote_list_of_top_4)
        for q2 in quotes_for_display:
            quote.set(quote.get() + str(q2[1])+"-"+ str(q2[2])+"-"+ str(q2[3])+"\n")

    else:
        quote.set("")
        quote.set("No awaiting bicycles for quotation")


def _extracted_from_refresh_quotes_13(quote):
    quote.set("")
    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM quotes")
    result = c.fetchall()
    conn.commit()
    conn.close()

    return result
        
def reset_quotes():

    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute("DELETE FROM quotes")
    conn.commit()
    conn.close() 
    quote.set("No awaiting bicycles for quotation")

def set_cred():
    global temp_username
    global temp_password
    global temp_receiver
    global temp_subject
    global temp_body
    with contextlib.suppress(Exception):
        from_set_cred_(
            temp_username, temp_password, temp_receiver, temp_subject
        )


def from_set_cred_(temp_username, temp_password, temp_receiver, temp_subject):
    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    c.execute("SELECT * FROM cre")
    reslt = c.fetchall()
    cred_list = reslt[0]
    temp_username.set(cred_list[0])
    temp_password.set(cred_list[1])
    temp_receiver.set(cred_list[2])
    temp_subject.set(cred_list[3])
    conn.commit()
    conn.close()

def save():
    global temp_username
    global temp_password
    global temp_receiver
    global temp_subject
    global temp_body
    global notif

    try:
        username = temp_username.get()
        password = temp_password.get()
        to = temp_receiver.get()
        subject = temp_subject.get()

        conn = sqlite3.connect('bikes.db')
        c = conn.cursor()
        c.execute("DELETE FROM cre")
        c.execute("INSERT INTO cre VALUES (:usr, :pss, :recip, :sub)",
            {
                'usr':username,
                'pss':password,
                'recip':to,
                'sub':subject
                })
        c.execute("SELECT * FROM cre")
        cred = c.fetchall()
        cred_list2 = cred[0]
        temp_username.set(cred_list2[0])
        temp_password.set(cred_list2[1])
        temp_receiver.set(cred_list2[2])
        temp_subject.set(cred_list2[3])

        conn.commit()
        conn.close()
        notif.configure(text="Settings saved!", background='lightgreen', height=2)
    except Exception:
        notif.configure(text="Error while making changes", background='red', height=2)

def email_settings():
    def reset_mail():
        email_entry.delete(0, 'end')
        pass_entry.delete(0, 'end')
        to_entry.delete(0, 'end')
        subject_entry.delete(0, 'end')
        body_entry.delete(0, 'end')

    email_level = CTkToplevel(root)

    email_level.wm_transient(root)    

    entries_buttons_and_work_email = CTkFrame(email_level)
    entries_buttons_and_work_email.pack(fill='both', expand=True, side=LEFT)

    entries_frame_email = CTkFrame(entries_buttons_and_work_email)
    entries_frame_email.pack(padx=20, pady=20, ipadx=50)

    email_label = CTkLabel(entries_frame_email, text="Email : ", font=('roboto', 14, 'bold'))
    email_label.grid(row=1, column=0, sticky=W, padx=(button_width, 0), pady=(button_width,0))
    pass_label = CTkLabel(entries_frame_email, text="Password : ", font=('roboto', 14, 'bold'))
    pass_label.grid(row=1, column=2, padx=(button_width*1.3, 0), pady=(button_width,0))
    to_label = CTkLabel(entries_frame_email, text="To : ", font=('roboto', 14, 'bold'))
    to_label.grid(row=2, column=0, sticky=W, padx=(button_width, 0))
    subject_label = CTkLabel(entries_frame_email, text="Subject : ", font=('roboto', 14, 'bold'))
    subject_label.grid(row=2, column=2, padx=(button_width*1.3, 0))
    body_label = CTkLabel(entries_frame_email, text="Body : ", font=('roboto', 14, 'bold'))
    body_label.grid(row=4, column=0, sticky=NW, padx=(button_width, 0))

    email_entry = CTkEntry(entries_frame_email, textvariable=temp_username, font=('roboto',14))
    email_entry.grid(row=1, column=1, sticky=W, pady=(button_width,0))
    pass_entry = CTkEntry(entries_frame_email, textvariable=temp_password, show="*", font=('roboto',14))
    pass_entry.grid(row=1, column=3, sticky=W, pady=(button_width,0))
    to_entry = CTkEntry(entries_frame_email, textvariable=temp_receiver, font=('roboto',14 ))
    to_entry.grid(row=2, column=1, sticky=W, pady=20)
    subject_entry = CTkEntry(entries_frame_email, textvariable=temp_subject, font=('roboto',14))
    subject_entry.grid(row=2, column=3, sticky=W)
    body_entry = CTkEntry(entries_frame_email, textvariable=temp_body, font=('roboto',14), width=button_width*25)
    body_entry.grid(row=4, column=1, columnspan=3, sticky=W)

    notif2 = CTkLabel(entries_frame_email, text="", font=('roboto',14))
    notif2.grid(row=5, column=3, sticky=E, pady=20)

    save_but = CTkButton(entries_frame_email, text="Save", command=save,  font=('roboto', button_width*1.5, 'bold'), width=button_width*7)
    save_but.grid(row=6, column=3, sticky=E, pady=20)
    reset_but = CTkButton(entries_frame_email, text="Reset", command=reset_mail,  font=('roboto', button_width*1.5, 'bold'), width=button_width*7)
    reset_but.grid(row=6, column=2, sticky=E, pady=20)

    email_level.mainloop()

def send():
    try:
        username = temp_username.get()
        password = temp_password.get()
        to = temp_receiver.get()
        subject = temp_subject.get()
        body = temp_body.get()

        if username == "" or password == "" or to == "" or subject == "" or body == "":
            notif.configure(text='All fields are required!', background='red', padx=button_width, height=2)
            return
        else:
            server = smtplib.SMTP(host='smtp-mail.outlook.com', port=587)
            server.starttls()
            server.login(username, password)

            msg = MIMEMultipart()   

            msg['From']= username
            msg['To']= to
            msg['Subject']=subject

            msg.attach(MIMEText(body, 'plain'))

            server.send_message(msg)

            server.quit()
            del msg

            notif.configure(text='Email has been sent', background='green', foreground='#ffffff', height=2)

    except Exception:
        notif.configure(text="Error sending email", background='red', height=2)

temp_username = StringVar()
temp_password = StringVar()
temp_receiver = StringVar()
temp_subject = StringVar()
temp_body = StringVar()

@staticmethod
def select_for_email(e):
    global temp_body
    global my_tree

    list_for_email = []
    curItems = my_tree.selection()
    [list_for_email.append(my_tree.item(i)['values']) for i in curItems]
    selected_items_forEmail = []

    conn = sqlite3.connect('bikes.db')
    c = conn.cursor()
    for i in list_for_email:
        c.execute(f'SELECT * FROM bikes WHERE rowid={str(i[4])}')
        records = c.fetchall()
        selected_items_forEmail.append(records[0])
    conn.commit()
    conn.close()

    for s in selected_items_forEmail:
        temp_body.set(temp_body.get() + str(s[0])+" - " + str(s[2])+" - " + str(s[4])+"\n")

    notif.configure(text='Items Copied!', background='orange', height=2)

menu_width = (screen_width/8)
button_width = int(menu_width/18)

main_frame = CTkFrame(root)
main_frame.pack(fill=BOTH, expand=1)

menu_frame = CTkFrame(main_frame, width=menu_width*1.6)
menu_frame.pack(side=LEFT,fill=Y)
menu_frame.propagate(0)

butt_padx = button_width
butt_pady = button_width

title_label = CTkLabel(menu_frame, text="Workshop Helper", font=('roboto', button_width*2))
title_label.pack(pady=(int(button_width*3),int(button_width*1.5)),  padx=button_width*2 ,fill='x')

butt1 = CTkButton(menu_frame, text='+ Add', command=add_bike, font=('roboto', int(button_width*1.7), 'bold'))
butt1.pack(
    ipady=button_width // 2,
    pady=(int(button_width * 2), 0),
    padx=button_width * 2,
    fill='x',
)

butt2 = CTkButton(menu_frame, text='Update', command=update_bike, font=('roboto',  int(button_width*1.7), 'bold'))
butt2.pack(
    pady=button_width, ipady=button_width // 2, padx=button_width * 2, fill='x'
)

butt3 = CTkButton(menu_frame, text='Ready', command=fixed, font=('roboto',  int(button_width*1.7), 'bold'))
butt3.pack(ipady=button_width // 2, padx=button_width*2, fill='x')

butt4 = CTkButton(menu_frame, text='Collected', command=fixed_bike, font=('roboto',  int(button_width*1.7), 'bold'))
butt4.pack(
    pady=button_width, ipady=button_width // 2, padx=button_width * 2, fill='x'
)

send_butt = CTkButton(menu_frame, text='Email Quotes', command=send, font=('roboto',  int(button_width*1.7), 'bold'))
send_butt.pack(
    pady=(button_width*3, button_width),
    ipady=button_width // 2,
    padx=button_width * 2,
    fill='x',
)

notif = Label(menu_frame, text="", font=('roboto',int(button_width*1.5)), wraplength=int(menu_width*1.2), background="#cecece")
notif.pack(
    pady=(0, button_width),
    padx=button_width * 2,
   fill='x'
)
notif.configure(text="Hold Ctrl and select items by left-clicking them. Press Enter to copy and press Email Quotes to send.", height=5)

optionmenu_1 = CTkOptionMenu(menu_frame, values=["Small", "Standard", "Large"],  command=change_scaling_event, font=("roboto", button_width*1.4, 'bold'))
optionmenu_1.pack(side=BOTTOM, pady=(button_width, button_width*2), padx=button_width*2 ,fill='x')
optionmenu_1.set("Standard")

appearance_mode_optionemenu = CTkOptionMenu(menu_frame, values=["Light", "Dark"], command=change_appearance_mode_event, font=("roboto", button_width*1.4, 'bold'))
appearance_mode_optionemenu.pack(side=BOTTOM, padx=button_width*2 ,fill='x')

appearance_mode_label = CTkLabel(menu_frame, text="Appearance Mode:", anchor="w")
appearance_mode_label.pack(side=BOTTOM)

butt5 = CTkButton(menu_frame, text='Delete', command=delete_bike, font=('roboto',  int(button_width*1.7), 'bold'))
butt5.pack(
    side=BOTTOM,
    ipady=button_width // 2,
    pady=(0, button_width * 2),
    padx=button_width * 2,
    fill='x',
)

content_frame = CTkFrame(main_frame, fg_color="transparent")
content_frame.pack(side=RIGHT, fill=BOTH, expand=1)

my_tree_frame = CTkFrame(content_frame, border_width=2)
my_tree_frame.pack( expand=True, fill='both', padx=button_width, pady=button_width)

my_tree = ttk.Treeview(my_tree_frame, selectmode='extended')
my_tree.pack(fill='both', expand=True, padx=button_width, pady=button_width)

my_tree['columns'] = ('Ready', 'Name', 'Phone', 'Bike', 'ID', 'Date','Total')

my_tree.column('#0', width=0, stretch=NO)
my_tree.column("Ready", anchor=CENTER, width=button_width*8)
my_tree.column("Name", anchor=CENTER)
my_tree.column("Phone", anchor=CENTER)
my_tree.column("Bike", anchor=CENTER)
my_tree.column("ID", anchor=CENTER, width=button_width*4)
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
tree_font_size = int(button_width*1.7)

s.configure('Treeview.Heading', background="#ffffff", foreground='#464646', font=('roboto', tree_font_size, 'bold' ), borderwidth=0 )
s.configure(
    'Treeview',
    rowheight=int(tree_font_size * 2.5),
    font=('roboto', tree_font_size),
    fieldbackground="#cecece"
)
s.map('Treeview', background=[('selected', '#55bd7f')],foreground=[('selected', '#ffffff')])
my_tree.tag_configure('oddrow', background= '#cccccc', foreground='#121212')
my_tree.tag_configure('evenrow',background='#dddddd', foreground='#121212')

bar_label = CTkLabel(my_tree_frame, text='Shop capacity ( Max: 25 ) : ', font=('roboto', int(button_width*1.5), 'bold'))
bar_label.pack(side=LEFT, padx=(button_width,0 ), pady=(0, button_width // 2))

progressbar = CTkProgressBar(master=my_tree_frame)
progressbar.pack(
    side=LEFT,
    pady=(0, button_width // 2),
    padx=(button_width),
    fill='x',
    expand=1,
)

more_butt_frame = CTkFrame(content_frame)
more_butt_frame.pack(fill='x',   pady=(0, button_width), padx=button_width)

bottom_frame_height = screen_height/7
details_and_label_width = screen_width/4

details_and_label_pre_frame = CTkFrame(more_butt_frame, border_width=2)
details_and_label_pre_frame.pack(side=LEFT, fill='both', expand=1, pady=button_width, padx=button_width/2)

details_and_label_frame = CTkFrame(details_and_label_pre_frame)
details_and_label_frame.pack(padx=button_width, pady=button_width, side=LEFT, fill='both', expand=1)

service_details_title = CTkLabel(details_and_label_frame,text='Service Details' , font=('roboto', button_width*1.9, 'bold'))
service_details_title.pack(padx=button_width, pady=(button_width, button_width))

separator = Frame(details_and_label_frame, background="#727272", height=2)
separator.pack(padx=button_width*3, fill='x', anchor=N)

service_text = StringVar()
service_text.set('Click On A Customer For More Information')
service_details_label = CTkLabel(details_and_label_frame, justify=CENTER, wraplength=details_and_label_width, textvariable=service_text , font=('roboto', button_width*1.9))
service_details_label.pack(pady=button_width/3)

service_details_frame = CTkFrame(details_and_label_pre_frame)
service_details_frame.pack(padx=(0, button_width), pady=(butt_pady), side=RIGHT, fill='y')

need_quote_title = CTkLabel(service_details_frame , text='Need Quote', font=('roboto', button_width*1.9, 'bold'), width=screen_width/5)
need_quote_title.pack(padx=button_width*2, pady=(butt_pady))

separator3 = Frame(service_details_frame, background="#727272", height=2)
separator3.pack(padx=button_width*3, fill='x', anchor=N, pady=(0, button_width))

quote = StringVar()
need_quote_label = CTkLabel(service_details_frame, justify=CENTER, wraplength=details_and_label_width, textvariable=quote , font=('roboto', button_width*1.9))
need_quote_label.pack(pady=(0), fill='y', padx=button_width*2)

lower_pre_frame = CTkFrame(more_butt_frame, border_width=2)
lower_pre_frame.pack(side=LEFT, pady=button_width, padx=(button_width*2, button_width/2), anchor=N, fill='x')

lower_butt_frame = CTkFrame(lower_pre_frame)
lower_butt_frame.pack(padx=button_width, pady=button_width, fill='x')

due_butt = CTkButton(lower_butt_frame, text='Reset Quotes', font=('roboto',  int(button_width*1.5), 'bold'), command=reset_quotes)
due_butt.pack(pady=( button_width, 0), padx=( button_width*2), fill='both', expand=1, ipadx=button_width*1.2, ipady=button_width/3)

hist_butt = CTkButton(lower_butt_frame, text='History', command=get_history, font=('roboto',  int(button_width*1.5), 'bold'))
hist_butt.pack(pady=(button_width), padx=(button_width*2), fill='both', expand=1, ipadx=button_width*1.2, ipady=button_width/3)

email_settings_butt = CTkButton(lower_butt_frame, text='Email Settings', command=email_settings, font=('roboto',  int(button_width*1.5), 'bold'))
email_settings_butt.pack(pady=(0, button_width), padx=(button_width*2), fill='both', expand=1, ipadx=button_width*1.2, ipady=button_width/3)

set_cred()
refresh_quotes()
set_widget_scaling(0.9)
query_database()
change_scaling_event(0.0)
my_tree.bind("<ButtonRelease-1>", select_record)
my_tree.bind("<Return>", select_for_email)
capacity()

root.mainloop()
