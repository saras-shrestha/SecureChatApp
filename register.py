from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter.messagebox import *
import mysql.connector
import re
from mysql.connector import Error

def goToLogin():
    root.destroy()
    import Client_Chat

def clear():
    entryemail.delete(0, END)
    entrycontact.delete(0, END)
    entrypassword.delete(0, END)
    entryconfirmpassword.delete(0, END)
    entryname.delete(0, END)
    entryusername.delete(0, END)
    check.set(0)

def register():
    name=username=email=phone=password=compassword=gender=check==None
    if entryname.get() == '' or entryusername.get() == '' or entryemail.get() == '' or entrycontact.get() == '' or\
            entrypassword.get() == '' or entryconfirmpassword.get() == '':
        showerror('Error', "All Fields Are Required", parent=root)
    else:
        if entryname.get():
            # searching regex
            errName.set("")
            if re.search("^[A-Za-z]+(?: [A-Za-z]+){0,3}$", entryname.get()):# ^[A-Z][a-z]+(?: [A-Z][a-z]+){0,3}$
                name = entryname.get()
            else:
                errName.set("*Only Letters are allowed")
        if entryusername.get():
            errUsername.set("")
            if re.search("^[A-Za-z]+[A-Za-z0-9]*$", entryusername.get()):
                username = entryusername.get()
            else:
                errUsername.set("*Only Letters and Numbers are allowed")
                # Label(frame1, text="*Only Letters and Numbers are allowed", fg="red").place(x=290, y=140)

        if entrycontact.get():
            errContact.set("")
            if re.search("^[0-9]\d{9}$", entrycontact.get()):
                phone = entrycontact.get()
            else:
                errContact.set("*Please enter a valid 10 digit mobile number")
                # Label(frame1, text="*Please enter a valid 10 digit mobile number", fg="red").place(x=20, y=225)
        if entryemail.get():
            errEmail.set("")
            if re.search("[A-Za-z0-9_]+[@][a-z]+[\.][a-z]+", entryemail.get()):
                email = entryemail.get()
            else:
                errEmail.set("*Please enter a valid email address")
                # Label(frame1, text="*Please enter a valid email address", fg="red").place(x=290, y=225)

        if entrypassword.get():
            errPass.set("")
            if len(entrypassword.get())<6 or len(entrypassword.get())>16:
                errPass.set("Password length must be greater than 7 and less than 16")
                # Label(frame1, text="Password length must be greater than 7 and less than 16", fg="red").place(
                #     x=20, y=310)
            else:
                if re.search("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])[A-Za-z0-9_#@%\*\$\-]{6,16}$", entrypassword.get()):
                    password = entrypassword.get()
                else:
                    errPass.set("*atleast one uppercase, one lowercase, & one digit -(may include special character _ # @ % * $ -)")
                    # Label(frame1, text="*atleast one uppercase, one lowercase, & one digit (may include special character _ # @ % * $ -)", fg="red").place(x=20, y=310)

        if entryconfirmpassword.get():
            errConPass.set("")
            if entrypassword.get() != entryconfirmpassword.get():
                errConPass.set("*Password didn't match")
                # Label(frame1, text="*Password didn't match", fg="red").place(x=290, y=310)
        if var.get():
            errGender.set("")
            if var.get()==0:
                errGender.set("*Please select your gender")
                # Label(frame1, text="*Please select your gender", fg="red").place(x=20, y=395)
            else:
                genValue=var.get()
                if genValue==1:
                    gender="Female"
                elif genValue==2:
                    gender="Male"
                else:
                    gender="Others"
        if check.get() == 0:
            showerror('Error', "Please Agree To Our Terms & Conditions", parent=root)
    if (username and email and phone and password and gender):
        # database
        try:
            connection = mysql.connector.connect(host='localhost',
                                                     database='chat',
                                                     user='root',
                                                     password='')

            mySql_insert_query = 'INSERT INTO users (name, username, email, password, phone, gender) VALUES (%s,%s,%s,%s,%s,%s)'

            cursor = connection.cursor()

            cursor.execute("select * from users where email=%s", (email,))

            row = cursor.fetchone()

            if row!=None:
                showerror("Error","User already Exist, Please try with another email", parent=root)
            else:
                cursor.execute(mySql_insert_query, (name, username, email, password, phone, gender))
                connection.commit()
                print(cursor.rowcount, "Record inserted successfully into Users table")
                cursor.close()
                import Client_Chat
                print ('HEllo')
        except mysql.connector.Error as error:
            print("Failed to insert record into users table {}".format(error))
        connection.close()

        # except Exception as e:
        #     showerror('Error', f"Error due to: {e}", parent=root)

root = Tk()
root.geometry('1350x710+0+0')
root.title('Registration Form')

root.configure(bg="purple")

registerFrame = Frame(root, bg='white')
registerFrame.pack(fill=BOTH, expand=True, padx=120,pady=80)

frame1 = Frame(registerFrame)
frame1.pack(fill=BOTH,side=LEFT, expand=True)

frame2 = Frame(registerFrame)
frame2.pack(fill=BOTH, side=RIGHT, expand=True)

# ===Right img===
image = Image.open("images/register.jpg")
image = image.resize((550, 550), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)
imgLabel=Label(frame2,image=img).place(x=0, y=0)


titleLabel = Label(frame1, text='Registration', font=('arial', 18, 'bold '), bg='white', fg='purple')
titleLabel.place(x=200, y=5)

nameLabel = Label(frame1, text='Name', font=('times new roman', 14, 'bold'), bg='white', fg='gray20')
nameLabel.place(x=20, y=80)
entryname = Entry(frame1, font=('times new roman', 14), bg='lightgray')
entryname.place(x=20, y=115, width=250)

errName = StringVar()
errName.set("")
Label(frame1, textvariable=errName, fg="red").place(x=20, y=140)

usernameLabel = Label(frame1, text='Username', font=('times new roman', 14, 'bold'), bg='white',
                      fg='gray20', )
usernameLabel.place(x=290, y=80)
entryusername = Entry(frame1, font=('times new roman', 14), bg='lightgray')
entryusername.place(x=290, y=115, width=250)

errUsername = StringVar()
errUsername.set("")
Label(frame1, textvariable=errUsername, fg="red").place(x=290, y=140)

contactLabel = Label(frame1, text='Contact Number', font=('times new roman', 14, 'bold'), bg='white',
                     fg='gray20', )
contactLabel.place(x=20, y=165)
entrycontact = Entry(frame1, font=('times new roman', 14), bg='lightgray')
entrycontact.place(x=20, y=200, width=250)

errContact = StringVar()
errContact.set("")
Label(frame1, textvariable=errContact, fg="red").place(x=20, y=225)

emailLabel = Label(frame1, text='Email', font=('times new roman', 14, 'bold'), bg='white', fg='gray20', )
emailLabel.place(x=290, y=165)
entryemail = Entry(frame1, font=('times new roman', 14), bg='lightgray')
entryemail.place(x=290, y=200, width=250)

errEmail = StringVar()
errEmail.set("")
Label(frame1, textvariable=errEmail, fg="red").place(x=290, y=225)

passwordLabel = Label(frame1, text='Password', font=('times new roman', 14, 'bold'), bg='white',fg='gray20')
passwordLabel.place(x=20, y=250)
entrypassword = Entry(frame1, show="*", font=('times new roman', 14), bg='lightgray')
entrypassword.place(x=20, y=285, width=250)


errPass = StringVar()
errPass.set("")
Label(frame1, textvariable=errPass, fg="red").place(x=20, y=310)

confirmpasswordLabel = Label(frame1, text='Confirm Password', font=('times new roman', 14, 'bold'), bg='white', fg='gray20', )
confirmpasswordLabel.place(x=290, y=250)
entryconfirmpassword = Entry(frame1,show="*",font=('times new roman', 14), bg='lightgray')
entryconfirmpassword.place(x=290, y=285, width=250)


errConPass = StringVar()
errConPass.set("")
Label(frame1, textvariable=errConPass, fg="red").place(x=290, y=310)

radioLabel = Label(frame1, text='Gender', font=('times new roman', 14, 'bold'), bg='white', fg='gray20' )
radioLabel.place(x=20, y=335)
var = IntVar()
R1 = Radiobutton(frame1, text="Female", variable=var, value=1, font=('times new roman', 14)).place(x=20, y=370)

R2 = Radiobutton(frame1, text="Male", variable=var, value=2, font=('times new roman', 14)).place(x=120, y=370)

R3 = Radiobutton(frame1, text="Others", variable=var, value=3, font=('times new roman', 14)).place(x=220, y=370 )

errGender = StringVar()
errGender.set("")
Label(frame1, textvariable=errGender, fg="red").place(x=20, y=395)

check = IntVar()
checkButton = Checkbutton(frame1, text='I Agree All The Terms & Conditions', variable=check, onvalue=1,
                          offvalue=0, font=('times new roman', 12, 'bold'), bg='white')
checkButton.place(x=20, y=415)
registerbutton = Button(frame1, text='Register', bd=0, font=('times new roman', 14), cursor='hand2', bg='purple', fg='white', command=register)
registerbutton.place(x=220, y=450)

alregister = Button(frame1, text='Already Register?Login', font=('arial', 12, 'bold'), bd=0, fg='blue', cursor='hand2', command=goToLogin)
alregister.place(x=165, y=500)

root.mainloop()
