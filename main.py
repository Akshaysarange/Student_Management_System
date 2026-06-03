import tkinter as tk # GUI
from tkinter import messagebox # for pop up message
from tkinter.ttk import Combobox,Treeview # for Drop down list option, Data ko GUI table me convert
from tkinter.filedialog import askopenfilename, askdirectory # tkinter se filedialog module se import karo askopenfilename -> file ko open karna | askdirectory -> folder ko open kara
from PIL import Image, ImageTk,ImageDraw,ImageFont # Python Image Library(PIL) module se Image -> image ko open,create,resize,save | ImageTk -> tkinter mee image show | ImageDraw -> image me changes | ImageFont -> image me text 
import re # conditions
import random # randomly std id 
import mysql.connector # database se connect

# database script
def db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='root',
        database='studentdb'
    )

# GUL root
root = tk.Tk()
root.geometry('500x600')
root.title('Student Registration & Management System')

bg_color = '#273b7a'

# Image ka path save
register_icon = tk.PhotoImage(file='images/register.png')
login_icon = tk.PhotoImage(file='images/login.png')
admin_icon = tk.PhotoImage(file='images/admin.png')
locked_icon=tk.PhotoImage(file='images/locked.png')
unlocked_icon=tk.PhotoImage(file='images/unlocked.png')
add_std_pic_icon = tk.PhotoImage(file='images/add_image.png')

# database create 
def init_database():
    conn = db()
    cur = conn.cursor()

    cur.execute("create table if not exists data(id_number int primary key,password varchar(100),name varchar(255),age int,gender enum('Male','Female'),phone_number varchar(10),student_class varchar(100),email varchar(255),image varchar(255))")
    conn.commit()
    conn.close()

# add user data in database
def add_data(id_number,password,name,age,gender,phone_number,student_class,email,image):
    conn = db()
    cur = conn.cursor()

    cur.execute("insert into data values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(id_number,password,name,age,gender,phone_number,student_class,email,image))

    conn.commit()
    conn.close()

def check_id_exists(id_number):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT id_number FROM data WHERE id_number=%s",(id_number,))
    result = cur.fetchone()
    conn.close()
    return result

# user ne jo id, password banaya hee usses vo login kare 
def check_valid_user(id_number,password=None):
    conn = db()
    cur=conn.cursor()

    cur.execute("select id_number,password from data where id_number =%s and password=%s",(id_number,password))
    response = cur.fetchone()

    conn.close()
    return response

#Create std card
def draw_std_card(std_pic_path,std_data):
    labels = """
Id Number:
Name:
Gender:
Age:
Class:
Contact:
Email:
    """
    std_card = Image.open('images/student_card_frame.png')
    pic = Image.open(std_pic_path)
    pic = pic.resize((100,100),Image.LANCZOS)

    std_card.paste(pic,(15,15))

    draw = ImageDraw.Draw(std_card)

    heading_font = ImageFont.truetype('bahnschrift',18)
    labels_font = ImageFont.truetype('arial',15)
    data_font = ImageFont.truetype('bahnschrift',13)

    draw.text(xy=(150,60),text='Student Card',fill=(0,0,0),font=heading_font)
    draw.multiline_text(xy=(15,110),text=labels,fill=(0,0,0),font=labels_font,spacing=6)
    draw.multiline_text(xy=(95,110),text=std_data,fill=(0,0,0),font=data_font,spacing=10)

    return std_card

def fetch_std_data(query, params=None):
    conn = db()
    cur = conn.cursor()

    cur.execute(query, params)
    response = cur.fetchall()

    conn.close()
    return response

# login page function
def login_page_func():
    def login_acc():
        verify_user = check_valid_user(id_number=id_en.get(),password=pass_en.get())

        if verify_user:
            entry_pass = id_en.get()
            login_page.destroy()
            root.update()
            std_dashboard(entry_pass)
        else:
            messagebox.showerror('Error','Please Enter Valid Student ID & Password')

    login_page = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)
    login_page.pack(pady=30)
    login_page.configure(width=400, height=450)

    tk.Label(login_page,text='Student Login Page',bg=bg_color,fg='white',font=('bold',18)).place(x=0, y=0, width=420)

    def forward_to_welcome_page():
        login_page.destroy()
        root.update()
        welcome_page_func()

    back_btn = tk.Button(login_page,text='←',font=('bold',20),fg=bg_color,bd=0,command=forward_to_welcome_page)
    back_btn.place(x=5,y=40)

    tk.Label(login_page, image=login_icon).place(x=150,y=40)

    tk.Label(login_page,text='Enter Student ID Number',font=('bold', 15),fg=bg_color).place(x=80,y=140)

    id_en = tk.Entry(login_page,font=('bold',15),justify=tk.CENTER,highlightthickness=2)
    id_en.place(x=80,y=190)

    def show_hide_func():
        if pass_en['show'] == '*':
            pass_en.config(show='')
            show_hide_btn.config(image=unlocked_icon)
        else:
            pass_en.config(show='*')
            show_hide_btn.config(image=locked_icon)

    tk.Label(login_page,text='Enter Student Password',font=('bold', 15),fg=bg_color).place(x=80,y=240)

    pass_en = tk.Entry(login_page,font=('bold',15),justify=tk.CENTER,highlightcolor=bg_color,highlightthickness=2,show='*')
    pass_en.place(x=80,y=290)

    show_hide_btn=tk.Button(login_page,image=locked_icon,bd=0,command=show_hide_func)
    show_hide_btn.place(x=310,y=280)

    tk.Button(login_page,text='Login',font=('bold',15),bg=bg_color,fg='white',command=login_acc).place(x=95,y=340,width=200,height=40)

    def forget_password_page():
        def recover_password():
            if check_id_exists(forget_en.get()):
                conn = db()
                cur = conn.cursor()
                cur.execute("select password from data where id_number = %s",(forget_en.get(),))
                recover_password = cur.fetchone()
                messagebox.showinfo(message=f'Your Password is:- {recover_password}')
            else:
                messagebox.showwarning(message='Invalid Student ID')

        forget_page_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)
        forget_page_fm.place(x=75,y=120,width=350,height=250)

        tk.Label(forget_page_fm, text='⚠ Forgetting Password',font=('bold',15),bg=bg_color,fg='white').place(x=0,y=0,width=350)

        tk.Button(forget_page_fm,text='X',font=('bold',13),bg=bg_color,fg='white',command=lambda:forget_page_fm.destroy()).place(x=320,y=0)

        tk.Label(forget_page_fm, text='Enter Student ID Number',font=('bold',13)).place(x=70,y=40)

        forget_en = tk.Entry(forget_page_fm,font=('bold',13),justify=tk.CENTER)
        forget_en.place(x=70,y=70,width=180)

        tk.Label(forget_page_fm, text="""Use Your Student ID 
Number To Recover Password
! If You Forget Your Password.""",justify=tk.LEFT,font=('bold',13)).place(x=75,y=110)

        tk.Button(forget_page_fm,text='Next',font=('bold',13),bg=bg_color,fg='white',command=recover_password).place(x=130,y=190,width=80)

    tk.Button(login_page,text='⚠\nForget Password',fg=bg_color,bd=0,command=forget_password_page).place(x=150,y=390)

def std_dashboard(id_number):
    get_std_details = fetch_std_data("SELECT name, age, gender, student_class, phone_number, email, image FROM data WHERE id_number=%s",(id_number,))

    if get_std_details[0][6]:
        std_pic = get_std_details[0][6]
    else:
        std_pic = "images/add_image.png"

    def switch(active_btn, page):
        home_btn.config(bg='#c3c3c3', fg=bg_color)
        std_card_btn.config(bg='#c3c3c3', fg=bg_color)
        security_btn.config(bg='#c3c3c3', fg=bg_color)
        edit_btn.config(bg='#c3c3c3', fg=bg_color)

        active_btn.config(bg='white', fg=bg_color)

        for child in std_pages_fm.winfo_children():
            child.destroy()

        root.update()
        page()

    std_dashboard_fm = tk.Frame(root, highlightbackground=bg_color,highlightthickness=3)
    std_dashboard_fm.pack(pady=5)
    std_dashboard_fm.configure(width=480,height=580)

    options_fm = tk.Frame(std_dashboard_fm,highlightbackground=bg_color,highlightthickness=2,bg='#c3c3c3')
    options_fm.place(x=0,y=0,width=120,height=575)

    std_pages_fm = tk.Frame(std_dashboard_fm, bg='white')
    std_pages_fm.place(x=120, y=0, width=355, height=575)

    def home_page():
        home_page_fm = tk.Frame(std_pages_fm)
        home_page_fm.pack(fill=tk.BOTH, expand=True)

        pic_img = Image.open(std_pic)
        pic_img = pic_img.resize((120, 120))  
        pic_img_obj = ImageTk.PhotoImage(pic_img)

        std_pic_lb = tk.Label(home_page_fm, image=pic_img_obj)
        std_pic_lb.image = pic_img_obj  
        std_pic_lb.place(x=10, y=10)

        tk.Label(home_page_fm,text=f'Welcome {get_std_details[0][0]}',font=('bold',12)).place(x=150,y=50)

        std_details = f"""
Student ID: {id_number}\n      
Name: {get_std_details[0][0]}\n     
Age: {get_std_details[0][1]}\n     
Gender: {get_std_details[0][2]}\n     
Class: {get_std_details[0][3]}\n     
Contact: {get_std_details[0][4]}\n     
Email: {get_std_details[0][5]}    
""" 
        tk.Label(home_page_fm,text=std_details,font=('bold',13),justify=tk.LEFT).place(x=20,y=130)

    home_btn = tk.Button(options_fm,text='Home',font=('bold',15),fg=bg_color,bg='#c3c3c3',bd=0,command=lambda:switch(home_btn,home_page))
    home_btn.place(x=10,y=50)

    def std_page():
        std_page_fm = tk.Frame(std_pages_fm)
        std_page_fm.pack(fill=tk.BOTH,expand=True)

        std_details = f"""
{id_number}  
{get_std_details[0][0]}    
{get_std_details[0][2]}    
{get_std_details[0][1]}    
{get_std_details[0][3]}     
{get_std_details[0][4]}     
{get_std_details[0][5]}    
"""
        std_card_img_obj = draw_std_card(std_pic_path=std_pic,std_data=std_details)
        
        std_card_img = ImageTk.PhotoImage(std_card_img_obj)

        card_lb=tk.Label(std_page_fm,image=std_card_img)
        card_lb.image=std_card_img
        card_lb.place(x=20,y=50)

        def save_std_card():
            path = askdirectory()
            if path:
                print(path)
                std_card_img_obj.save(f'{path}/student_card.png')

        tk.Button(std_page_fm,text='Save Student Card',bg=bg_color,fg='white',font=('bold',15),bd=1,command=save_std_card).place(x=60,y=400)

    std_card_btn = tk.Button(options_fm,text='Student\nCard',font=('bold',15),fg=bg_color,bg='#c3c3c3',bd=0,justify=tk.LEFT,command=lambda:switch(std_card_btn,std_page))
    std_card_btn.place(x=10,y=100)

    def security_page():
        security_page_fm = tk.Frame(std_pages_fm)
        security_page_fm.pack(fill=tk.BOTH,expand=True)

        tk.Label(security_page_fm,text='Your Current Password',font=('bold',13)).place(x=80,y=30)

        def show_hide_func():
            if current_pass_en['show'] == '*':
                current_pass_en.config(show='')
                show_hide_btn.config(image=unlocked_icon)
            else:
                current_pass_en.config(show='*')
                show_hide_btn.config(image=locked_icon)

        std_current_pass = fetch_std_data("SELECT password FROM data WHERE id_number=%s",(id_number,))

        current_pass_en = tk.Entry(security_page_fm,font=('bold',13),justify=tk.CENTER,show='*')
        current_pass_en.place(x=80,y=90)

        show_hide_btn=tk.Button(security_page_fm,image=locked_icon,bd=0,command=show_hide_func)
        show_hide_btn.place(x=270,y=70)

        current_pass_en.insert(tk.END,std_current_pass[0][0])
        current_pass_en.config(state='readonly')

        tk.Label(security_page_fm,text='Change Password',font=('bold',15),bg='red',fg='white').place(x=30,y=210,width=290)

        tk.Label(security_page_fm,text='Set New Password',font=('bold',12)).place(x=100,y=280)

        new_pass_en = tk.Entry(security_page_fm,font=('bold',15),justify=tk.CENTER)
        new_pass_en.place(x=60,y=330)

        def set_password():
            if new_pass_en.get() != '':
                confirm = messagebox.askyesno('Confirm','Do You Want To Change\nYour Password?')

                if confirm:
                    conn = db()
                    cur = conn.cursor()
                    cur.execute("update data set password=%s where id_number=%s",(new_pass_en.get(),id_number,))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo(title='Success',message='Password Changed Successfully')

                    current_pass_en.config(state=tk.NORMAL)
                    current_pass_en.delete(0,tk.END)
                    current_pass_en.insert(0,new_pass_en.get())
                    current_pass_en.config(state='readonly')

                    new_pass_en.delete(0,tk.END)
            else:
                messagebox.showwarning(message='Enter New Password Required')

        change_pass_btn = tk.Button(security_page_fm,text='Set Password',font=('bold',12),bg=bg_color,fg='white',command=set_password)
        change_pass_btn.place(x=110,y=380)

    security_btn = tk.Button(options_fm,text='Security',font=('bold',15),fg=bg_color,bg='#c3c3c3',bd=0,command=lambda:switch(security_btn,security_page))
    security_btn.place(x=10,y=170)

    def edit_page():
        def check_invalid_email(email):
            pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            match = re.match(pattern=pattern,string=email)
            return match

        def check_inputs():
            nonlocal get_std_details,std_pic
            if std_name_en.get() == '' or not std_name_en.get().replace(' ','').isalpha():
                std_name_en.focus()
                messagebox.showwarning(message='Student Full Name Invalied or Required')
            elif std_age_en.get() == '' or not std_age_en.get().isdigit() or int(std_age_en.get()) <= 0:
                std_age_en.focus()
                messagebox.showwarning(message='Student Age Invalied or Required')
            elif not std_phone_en.get().isdigit() or len(std_phone_en.get()) != 10:
                std_phone_en.focus()
                messagebox.showwarning(message='Contact Number Invalied or Required')
            elif class_btn.get() == '':
                class_btn.focus()
                messagebox.showwarning(message='Student Class is Required')
            elif std_email_en.get() == '':
                std_email_en.focus()
                messagebox.showwarning(message='Student Email is Required')
            elif not check_invalid_email(email=std_email_en.get().lower()):
                std_email_en.focus()
                messagebox.showwarning(message='Please Enter a Valid\nEmail Address')
            else:
               if pic_path.get() != '':
                new_std_pic = Image.open(pic_path.get()).resize((100,100))
                new_std_pic.save('temp_pic.png')

                image_path_to_store = pic_path.get()

                conn=db()
                cur=conn.cursor()
                cur.execute("update data set image=%s where id_number=%s",(image_path_to_store,id_number,))
                conn.commit()
                conn.close()

            name = std_name_en.get()
            age = std_age_en.get()
            selected_class = class_btn.get()
            contact_number = std_phone_en.get()
            email_address = std_email_en.get()

            conn=db()
            cur=conn.cursor()
            cur.execute("UPDATE data SET name=%s, age=%s, student_class=%s, phone_number=%s, email=%s WHERE id_number=%s", (name, age, selected_class, contact_number, email_address, id_number))
            conn.commit()
            conn.close()

            get_std_details = fetch_std_data("SELECT name, age, gender, student_class, phone_number, email, image FROM data WHERE id_number=%s",(id_number,))

            messagebox.showwarning(message='Data Successfully Updated.')

        class_list = ['5th', '6th', '7th', '8th', '9th', '10th']

        edit_page_fm = tk.Frame(std_pages_fm)
        edit_page_fm.pack(fill=tk.BOTH,expand=True)

        pic_path = tk.StringVar()
        pic_path.set('')

        def open_path():
            path = askopenfilename()
            if path:
                img = ImageTk.PhotoImage(Image.open(path).resize((100,100)))
                pic_path.set(path)

                add_pic_btn.config(image=img)
                add_pic_btn.image = img

        try:
            img = Image.open(std_pic)
        except:
            img = Image.open("default.png")

        img = img.resize((100, 100))
        std_current_pic = ImageTk.PhotoImage(img)

        add_pic_fm = tk.Frame(edit_page_fm,highlightbackground=bg_color,highlightthickness=2)
        add_pic_fm.place(x=5,y=5,width=105,height=105)

        add_pic_btn = tk.Button(add_pic_fm, image=std_current_pic, bd=0, command=open_path)
        add_pic_btn.pack()
        add_pic_btn.image = std_current_pic

        tk.Label(edit_page_fm,text='Student Full Name',font=('bold',12)).place(x=5,y=130)

        std_name_en = tk.Entry(edit_page_fm,font=('bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
        std_name_en.place(x=5,y=160,width=180)
        std_name_en.insert(tk.END,get_std_details[0][0])

        tk.Label(edit_page_fm,text='Student Age',font=('bold',12)).place(x=5,y=210)

        std_age_en = tk.Entry(edit_page_fm,font=('bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
        std_age_en.place(x=5,y=235,width=180)
        std_age_en.insert(tk.END,get_std_details[0][1])

        tk.Label(edit_page_fm,text='Contact Number',font=('bold',12)).place(x=5,y=275)

        std_phone_en = tk.Entry(edit_page_fm,font=('bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
        std_phone_en.place(x=5,y=305,width=180)
        std_phone_en.insert(tk.END,get_std_details[0][4])
        
        tk.Label(edit_page_fm,text='Student Class',font=('bold',12)).place(x=5,y=360)

        class_btn = Combobox(edit_page_fm,font=('bold',15),state='readonly',values=class_list)
        class_btn.place(x=5,y=390,width=180,height=30)
        class_btn.set(get_std_details[0][3])

        tk.Label(edit_page_fm,text='Student Email Address',font=('bold',12)).place(x=5,y=445)

        std_email_en = tk.Entry(edit_page_fm,font=('bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
        std_email_en.place(x=5,y=475,width=180)
        std_email_en.insert(tk.END,get_std_details[0][5])

        update_data_btn = tk.Button(edit_page_fm,text='Update',font=('bold',15),fg='white',bg=bg_color,bd=0,command=check_inputs)
        update_data_btn.place(x=220,y=470,width=80)

    edit_btn = tk.Button(options_fm,text='Edit Data',font=('bold',15),fg=bg_color,bg='#c3c3c3',bd=0,command=lambda:switch(edit_btn,edit_page))
    edit_btn.place(x=10,y=220)

    def logout():
        confirm = messagebox.askyesno('Confirmation','⚠ Do You Want to Logout?')
        if confirm:
            std_dashboard_fm.destroy()
            welcome_page_func()
            root.update()

    logout_btn = tk.Button(options_fm,text='Logout',font=('bold',15),fg=bg_color,bg='#c3c3c3',bd=0,command=logout)
    logout_btn.place(x=10,y=270)

    switch(home_btn, home_page)

def std_card_page(std_card_obj):
    def save_std_card():
        path = askdirectory()
        if path:
            print(path)
            std_card_obj.save(f'{path}/student_card.png')

    def close_page():
        std_card_page_fm.destroy()
        root.update()
        login_page_func()

    std_card_img = ImageTk.PhotoImage(std_card_obj)

    std_card_page_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)
    std_card_page_fm.place(x=50,y=30,width=400,height=450)

    tk.Label(std_card_page_fm,text='Student Card',bg=bg_color,fg='white',font=('bold',18)).place(x=0,y=0,width=400)

    tk.Button(std_card_page_fm,text='X',bg=bg_color,fg='white',font=('bold',13),bd=0,command=close_page).place(x=370,y=0)

    std_card_lb = tk.Label(std_card_page_fm, image=std_card_img)
    std_card_lb.place(x=50,y=50)
    std_card_lb.image = std_card_img

    tk.Button(std_card_page_fm,text='Save Student Card',bg=bg_color,fg='white',font=('bold',15),bd=1,command=save_std_card).place(x=80,y=375)

def admin_dashboard():
    adm_dashboard_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)
    adm_dashboard_fm.pack(pady=5)
    adm_dashboard_fm.configure(width=480,height=580)

    option_fm = tk.Frame(adm_dashboard_fm,highlightbackground=bg_color,highlightthickness=2,bg='#c3c3c3')
    option_fm.place(x=0,y=0,width=120,height=575)

    pages_fm = tk.Frame(adm_dashboard_fm)
    pages_fm.place(x=122,y=5,width=350,height=550)

    current_page = None

    def show_page(frame_func):
            nonlocal current_page
            if current_page is not None:
                current_page.destroy()
            current_page = frame_func()
            current_page.pack(fill=tk.BOTH, expand=True)

    def switch(indicator):
        home_btn_in.config(bg='#c3c3c3')
        find_std_btn_in.config(bg='#c3c3c3')
        delete_btn_in.config(bg='#c3c3c3')

        indicator.config(bg=bg_color)
    
    def home_page():
        home_page_fm = tk.Frame(pages_fm)

        adm_icon=tk.Label(home_page_fm,image=admin_icon)
        adm_icon.image=admin_icon
        adm_icon.place(x=10,y=10)

        tk.Label(home_page_fm,text='Welcome Admin',font=('bold',15)).place(x=120,y=40)

        tk.Label(home_page_fm,text='Number of Students By Class',font=('bold',13),bg=bg_color,fg='white').place(x=20,y=130)

        std_num_lb=tk.Label(home_page_fm,text='',font=('bold',13),justify=tk.LEFT)
        std_num_lb.place(x=20,y=170)

        class_list = ['5th', '6th', '7th', '8th', '9th', '10th']
        for i in class_list:
            res = fetch_std_data(query="SELECT COUNT(*) FROM data WHERE student_class=%s",params=(i,))

            if res:
                count = res[0][0]
            else:
                count = 0

            std_num_lb['text'] += f"{i} Class:    {count}\n\n"

        return home_page_fm

    def find_std_page():
        def find_std():
            record_table.delete(*record_table.get_children())
            found_data = ''
            if find_by.get() == 'ID':
                found_data=fetch_std_data(query = "SELECT id_number, name, student_class, gender FROM data WHERE id_number=%s", params=(search_input.get(),))
            elif find_by.get() == 'Name':
                found_data=fetch_std_data(query = "SELECT id_number, name, student_class, gender FROM data WHERE name LIKE %s", params=(f"%{search_input.get()}%",))
            elif find_by.get() == 'Class':
                found_data=fetch_std_data(query = "SELECT id_number, name, student_class, gender FROM data WHERE student_class=%s", params=(search_input.get(),))
            elif find_by.get() == 'Gender':
                found_data=fetch_std_data(query = "SELECT id_number, name, student_class, gender FROM data WHERE gender=%s", params=(search_input.get(),))

            if found_data:
                for item in record_table.get_children():
                    record_table.delete(item)

                for details in found_data:
                    record_table.insert(parent='', index='end', values=details)
            else:
                for item in record_table.get_children():
                    record_table.delete(item)

        def generate_std_card():
            selected_item = record_table.selection()

            if not selected_item:
                messagebox.showwarning("Warning", "Please select a student record first.")
                return

            selected_id = record_table.item(selected_item[0], 'values')[0]

            get_std_details = fetch_std_data(
                "SELECT name, age, gender, student_class, phone_number, email, image FROM data WHERE id_number=%s",
                (selected_id,)
            )

            if not get_std_details:
                messagebox.showerror("Error", "Student Record Not Found!")
                return

            get_std_pic = get_std_details[0][6]

            std_details = f"""
{selected_id}
{get_std_details[0][0]}
{get_std_details[0][2]}
{get_std_details[0][1]}
{get_std_details[0][3]}
{get_std_details[0][4]}
{get_std_details[0][5]}
"""

            std_card_obj = draw_std_card(std_pic_path=get_std_pic, std_data=std_details)

            std_card_page(std_card_obj=std_card_obj)

        search_filters = ['ID','Name','Class','Gender']

        find_std_page_fm = tk.Frame(pages_fm)

        tk.Label(find_std_page_fm,text='Find Student Record',font=('bold',13),fg='white',bg=bg_color).place(x=20,y=10,width=300)

        tk.Label(find_std_page_fm,text='Find By',font=('bold',12)).place(x=15,y=50)
        find_by=Combobox(find_std_page_fm,font=('bold',12),state='readonly',values=search_filters)
        find_by.place(x=80,y=50,width=80)
        find_by.set('ID')

        search_input = tk.Entry(find_std_page_fm,font=('bold',12))
        search_input.place(x=20,y=90)
        search_input.bind('<KeyRelease>', lambda e:find_std())

        tk.Label(find_std_page_fm,text='Record Table',font=('bold',13),bg=bg_color,fg='white').place(x=20,y=160,width=300)

        record_table = Treeview(find_std_page_fm, show='headings')
        record_table.place(x=0, y=200, width=350)
        record_table.bind('<<TreeviewSelect>>', lambda e:generate_std_card_btn.config(state=tk.NORMAL))

        record_table['columns'] = ('ID','Name','Class','Gender')

        record_table.heading('ID', text='ID Number', anchor=tk.W)
        record_table.column('ID', width=50, anchor=tk.W)

        record_table.heading('Name', text='Name', anchor=tk.W)
        record_table.column('Name', width=90, anchor=tk.W)

        record_table.heading('Class', text='Class', anchor=tk.W)
        record_table.column('Class', width=40, anchor=tk.W)

        record_table.heading('Gender', text='Gender', anchor=tk.W)
        record_table.column('Gender', width=40, anchor=tk.W)

        generate_std_card_btn = tk.Button(find_std_page_fm,text='Generate Student Card',font=('bold',13),bg=bg_color,fg='white',state=tk.DISABLED,command=generate_std_card)
        generate_std_card_btn.place(x=160,y=450)

        clear_btn = tk.Button(find_std_page_fm,text='Clear',font=('bold',13),bg=bg_color,fg='white',command=lambda:record_table.delete(*record_table.get_children()))
        clear_btn.place(x=10,y=450)

        return find_std_page_fm

    show_page(home_page)

    hom_btn = tk.Button(option_fm, text='Home', font=('bold',15), fg=bg_color, bg='#c3c3c3',bd=0, command=lambda: [switch(indicator=home_btn_in), show_page(home_page)])
    hom_btn.place(x=10, y=50)

    home_btn_in=tk.Label(option_fm,bg=bg_color)
    home_btn_in.place(x=5,y=48,width=3,height=40)

    find_std_btn = tk.Button(option_fm, text='Find\nStudent', font=('bold',15), fg=bg_color,bg='#c3c3c3',bd=0, justify=tk.LEFT, command=lambda: [switch(indicator=find_std_btn_in), show_page(find_std_page)])
    find_std_btn.place(x=10, y=100)

    find_std_btn_in=tk.Label(option_fm,bg='#c3c3c3')
    find_std_btn_in.place(x=5,y=108,width=3,height=40)

    def admin_del_page():
        del_page_fm = tk.Frame(pages_fm)

        tk.Label(del_page_fm,
                text='⚠ Delete Student Account',
                font=('bold', 15),
                bg='red',
                fg='white').place(x=30, y=60, width=320)

        tk.Label(del_page_fm,
                text='Enter Student ID:',
                font=('bold', 12)).place(x=60, y=140)

        student_id_entry = tk.Entry(del_page_fm, font=('bold', 12))
        student_id_entry.place(x=60, y=170, width=200)

        def confirm_delete_account():
            student_id = student_id_entry.get()

            if student_id == "":
                messagebox.showerror("Error", "Please Enter Student ID")
                return

            confirm = messagebox.askyesno("Confirm","Do You Want to Delete This Account?")

            if confirm:
                conn = db()
                cur = conn.cursor()

                cur.execute("DELETE FROM data WHERE id_number=%s", (student_id,))
                conn.commit()

                if cur.rowcount == 0:
                    messagebox.showerror("Error", "Student ID Not Found!")
                else:
                    messagebox.showinfo("Success", "Account Deleted Successfully!")

                conn.close()
                student_id_entry.delete(0, tk.END)

        tk.Button(del_page_fm,text='DELETE ACCOUNT',bg='red',fg='white',font=('bold', 13),command=confirm_delete_account).place(x=90, y=230)

        return del_page_fm

    delete_btn = tk.Button(option_fm,text='Delete\nAccount',font=('bold',15),fg=bg_color,bg='#c3c3c3',bd=0,justify=tk.LEFT,command=lambda: [switch(delete_btn_in),show_page(admin_del_page)])
    delete_btn.place(x=10, y=170)

    delete_btn_in = tk.Label(option_fm, bg='#c3c3c3')
    delete_btn_in.place(x=5,y=170,width=3,height=40)

    def logout():
        confirm = messagebox.askyesno('Confirmation','⚠ Do You Want to Logout?')
        if confirm:
            adm_dashboard_fm.destroy()
            welcome_page_func()
            root.update()

    logout_btn = tk.Button(option_fm,text='Logout',font=('bold',15),fg=bg_color,bg='#c3c3c3',bd=0,command=logout)
    logout_btn.place(x=10,y=250)

# admin page function
def admin_page_func():
    def forward_to_welcome_page():
        admin_page.destroy()
        root.update()
        welcome_page_func()

    def login_acc():
        username = user_en.get()
        password = pass_en.get()

        if username == "admin" and password == "admin":
            admin_page.destroy()
            root.update()
            admin_dashboard()
        else:
            messagebox.showwarning(message='Invalid Admin Credentials')

    admin_page = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)
    admin_page.pack(pady=30)
    admin_page.configure(width=400, height=450)

    tk.Label(admin_page,text='Admin Login Page',font=('bold', 18),bg=bg_color,fg='white').place(x=0, y=0, width=400)

    back_btn = tk.Button(admin_page,text='←',font=('bold',20),fg=bg_color,bd=0,command=forward_to_welcome_page)
    back_btn.place(x=5,y=40)

    tk.Label(admin_page, image=admin_icon).place(x=150,y=40)

    tk.Label(admin_page,text='Enter Admin User Name',font=('bold', 15),fg=bg_color).place(x=80,y=140)

    user_en = tk.Entry(admin_page,font=('bold',15),justify=tk.CENTER)
    user_en.place(x=80,y=190)

    def show_hide_func():
        if pass_en['show'] == '*':
            pass_en.config(show='')
            show_hide_btn.config(image=unlocked_icon)
        else:
            pass_en.config(show='*')
            show_hide_btn.config(image=locked_icon)

    tk.Label(admin_page,text='Enter Admin Password',font=('bold', 15),fg=bg_color).place(x=80,y=240)

    pass_en = tk.Entry(admin_page,font=('bold',15),justify=tk.CENTER,highlightcolor=bg_color,
    highlightbackground='gray',highlightthickness=2,show='*')
    pass_en.place(x=80,y=290)

    show_hide_btn=tk.Button(admin_page,image=locked_icon,bd=0,command=show_hide_func)
    show_hide_btn.place(x=310,y=280)

    tk.Button(admin_page,text='Login',font=('bold',15),bg=bg_color,fg='white',command=login_acc).place(x=95,y=340,width=200,height=40)

# account page function
def account_page_func():
    pic_path = tk.StringVar()
    pic_path.set('')

    def open_path():
        path = askopenfilename()
        if path:
            img = ImageTk.PhotoImage(Image.open(path).resize((100,100)))
            pic_path.set(path)
            add_pic_btn.config(image=img)
            add_pic_btn.image = img

    std_gen = tk.StringVar()

    class_list = ['5th', '6th', '7th', '8th', '9th', '10th']

    def forward_to_welcome_page():
        ans = messagebox.askyesno('Confirmation','Do You Want To Leave\nRegistration Form?')
        if ans:
            add_acc_fm.destroy()
            root.update()
            welcome_page_func()

    def check_invalid_email(email):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        match = re.match(pattern=pattern,string=email)
        return match

    def generate_id_number():
        for i in range(100):  # max 100 tries
            generate_id = ''.join([str(random.randint(0,9)) for i in range(6)])
            if not check_id_exists(generate_id):
                student_id.config(state=tk.NORMAL)
                student_id.delete(0, tk.END)
                student_id.insert(tk.END, generate_id)
                student_id.config(state='readonly')
                
    def check_input_validation():
        path_to_use = pic_path.get()
        if not path_to_use:
            path_to_use = 'images/add_image.png'

        if std_name_en.get() == '' or not std_name_en.get().replace(' ','').isalpha():
            std_name_en.focus()
            messagebox.showwarning(message='Student Full Name Invalied or Required')
        elif std_age_en.get() == '' or not std_age_en.get().isdigit() or int(std_age_en.get()) <= 0:
            std_age_en.focus()
            messagebox.showwarning(message='Student Age Invalied or Required')
        elif not std_phone_en.get().isdigit() or len(std_phone_en.get()) != 10:
            std_phone_en.focus()
            messagebox.showwarning(message='Contact Number Invalied or Required')
        elif class_btn.get() == '':
            class_btn.focus()
            messagebox.showwarning(message='Student Class is Required')
        elif std_email_en.get() == '':
            std_email_en.focus()
            messagebox.showwarning(message='Student Email is Required')
        elif not check_invalid_email(email=std_email_en.get().lower()):
            std_email_en.focus()
            messagebox.showwarning(message='Please Enter a Valid\nEmail Address')
        else:
            if pic_path.get() != '':
                resize_pic = Image.open(pic_path.get()).resize((100,100))
                resize_pic.save('temp_pic.png')

                read_data = open('temp_pic.png', 'rb')
                pic_data = read_data.read()
                read_data.close()
            else:
                read_data = open('images/add_image.png', 'rb')
                pic_data = read_data.read()
                read_data.close()

            add_data(id_number=student_id.get(),
                password=std_pass_en.get(),
                name=std_name_en.get(),
                age=std_age_en.get(),
                gender=std_gen.get(),
                phone_number=std_phone_en.get(),
                student_class=class_btn.get(),
                email=std_email_en.get(),
                image=path_to_use
                )

            data = f"""
{student_id.get()}
{std_name_en.get()}
{std_gen.get()}
{std_age_en.get()}
{class_btn.get()}
{std_phone_en.get()}
{std_email_en.get()}
            """
            add_acc_fm.destroy()
            root.update()

            get_std_card = draw_std_card(std_pic_path=path_to_use,std_data=data)
            std_card_page(std_card_obj=get_std_card)

    add_acc_fm = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)
    add_acc_fm.pack(pady=5)
    add_acc_fm.configure(width=480, height=580)

    add_pic_fm = tk.Frame(add_acc_fm,highlightbackground=bg_color,highlightthickness=2)
    add_pic_fm.place(x=5,y=5,width=105,height=105)
    add_pic_btn = tk.Button(add_pic_fm, image=add_std_pic_icon,bd=0,command=open_path)
    add_pic_btn.pack()

    tk.Label(add_acc_fm,text='Enter Student Full Name',font=('bold',12)).place(x=5,y=130)

    std_name_en = tk.Entry(add_acc_fm,font=('bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    std_name_en.place(x=5,y=160,width=180)

    tk.Label(add_acc_fm,text='Select Student Gender',font=('bold',12)).place(x=5,y=210)

    male_btn = tk.Radiobutton(add_acc_fm,text='Male',font=('bold',12),variable=std_gen,value='Male')
    male_btn.place(x=5,y=235)

    female_btn = tk.Radiobutton(add_acc_fm,text='Female',font=('bold',12),variable=std_gen,value='Female')
    female_btn.place(x=75,y=235)

    std_gen.set('Male')

    tk.Label(add_acc_fm,text='Enter Student Age',font=('bold',12)).place(x=5,y=275)

    std_age_en = tk.Entry(add_acc_fm,font=('bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    std_age_en.place(x=5,y=305,width=180)

    tk.Label(add_acc_fm,text='Enter Contact Number',font=('bold',12)).place(x=5,y=360)

    std_phone_en = tk.Entry(add_acc_fm,font=('bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    std_phone_en.place(x=5,y=390,width=180)

    tk.Label(add_acc_fm,text='Select Student Class',font=('bold',12)).place(x=5,y=445)

    class_btn = Combobox(add_acc_fm,font=('bold',15),state='readonly',values=class_list)
    class_btn.place(x=5,y=475,width=180,height=30)

    tk.Label(add_acc_fm,text='Student ID Number:-',font=('bold',12)).place(x=240,y=35)

    student_id = tk.Entry(add_acc_fm,font=('bold',18),bd=0)
    student_id.place(x=380,y=35,width=80)
    student_id.config(state='readonly')
    generate_id_number()

    tk.Label(add_acc_fm,text="""Automatically Generated Id Number
! Remember Using This ID Number
Student will Login Account.""",justify=tk.LEFT).place(x=240,y=65)

    tk.Label(add_acc_fm,text='Enter Student Email Address',font=('bold',12)).place(x=240,y=130)

    std_email_en = tk.Entry(add_acc_fm,font=('bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    std_email_en.place(x=240,y=160,width=180)

    tk.Label(add_acc_fm,text="""Via Email Address Student
can get Future 
Notifications.""",justify=tk.LEFT).place(x=240,y=200)

    tk.Label(add_acc_fm,text='Create Account Password',font=('bold',12)).place(x=240,y=275)

    std_pass_en = tk.Entry(add_acc_fm,font=('bold',15),highlightcolor=bg_color,highlightbackground='gray',highlightthickness=2)
    std_pass_en.place(x=240,y=307,width=180)

    tk.Label(add_acc_fm,text="""Via Student Created Password
And Provided Student ID Number
Student Can Login Account.""",justify=tk.LEFT).place(x=240,y=345)

    home_btn = tk.Button(add_acc_fm,text='Home',font=('bpld',15),bg='red',fg='white',bd=0,command=forward_to_welcome_page)
    home_btn.place(x=240,y=420)

    submit_btn = tk.Button(add_acc_fm,text='Submit',font=('bpld',15),bg=bg_color,fg='white',bd=0,command=check_input_validation)
    submit_btn.place(x=360,y=420)

# Welcome page Function
def welcome_page_func():
    def forward_to_std_login_page():
        wel_page.destroy()
        root.update()
        login_page_func()

    def forward_to_admin_page():
        wel_page.destroy()
        root.update()
        admin_page_func()

    def forward_to_regi_page():
        wel_page.destroy()
        root.update()
        account_page_func()

    wel_page = tk.Frame(root,highlightbackground=bg_color,highlightthickness=3)
    wel_page.pack(pady=30)
    wel_page.configure(width=400, height=420)

    tk.Label(wel_page, text='Welcome To Student Registration\n& Management System',bg=bg_color, 
    fg='white',font=('Bold',18)).place(x=0,y=0,width=400)

    tk.Button(wel_page,text='Login Student',bg=bg_color,fg='white',font=('bold', 15),bd=0,command=forward_to_std_login_page).place(x=120, y=125, width=200)

    tk.Button(wel_page,image=login_icon,bd=0,command=forward_to_std_login_page).place(x=60, y=100)

    tk.Button(wel_page,text='Login Admin',bg=bg_color,fg='white',font=('bold', 15),bd=0,command=forward_to_admin_page).place(x=120, y=225, width=200)

    tk.Button(wel_page,image=admin_icon,bd=0,command=forward_to_admin_page).place(x=60, y=200)

    tk.Button(wel_page,text='Create Account',bg=bg_color,fg='white',font=('bold', 15),bd=0,command=forward_to_regi_page).place(x=120, y=325, width=200)

    tk.Button(wel_page,image=register_icon,bd=0,command=forward_to_regi_page).place(x=60, y=300)

init_database()
welcome_page_func()

root.mainloop()