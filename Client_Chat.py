import io
import random
from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import mysql.connector
from tkinter.messagebox import *
import pickle
import rsa
from LSB_Stego import ImageSteg
import threading
import binascii
import socket
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


HOST='127.0.0.1'
PORT=12345
running=True

# generating public key
public, private = rsa.generateKeys(1024)
msg = pickle.dumps(public)

def set_ip():
    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    # distroy input root
    root.destroy()
    # end of input root:
    root.quit()


def login_window():
    root.destroy()
    import Client_Chat
def goToRegister():
    root.destroy()
    import register


def clear():
    entryuser.delete(0, END)
    entrypassword.delete(0, END)

def login():
    global name,connection
    if entryuser.get() == '' or entrypassword.get() == '':
        showerror('Error', "All Fields Are Required", parent=root)

    else:
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database='chat',
                                                 user='root',
                                                 password='')

            cursor = connection.cursor()
            cursor.execute("select * from users where username=%s and password=%s", (entryuser.get(),entrypassword.get()))
            row = cursor.fetchone()
            if row == None:
                showerror('Error', "Invalid User or Password", parent=root)
            else:
                name=entryuser.get()
                set_ip()
                print("connected")


        except Exception as e:
            showerror('Error', f"Error due to: {e}", parent=root)

root = Tk()
root.geometry('1350x710+0+0')
root.title('Login Form')

root.configure(bg="purple")

registerFrame = Frame(root, bg='white')
registerFrame.pack(fill=BOTH, expand=True, padx=120,pady=80)

frame1 = Frame(registerFrame)
frame1.pack(fill=BOTH,side=LEFT, expand=True)

frame2 = Frame(registerFrame)
frame2.pack(fill=BOTH, side=RIGHT, expand=True)

# ===Right img===
image = Image.open("images/login.jpg")
image = image.resize((550, 550), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)
imgLabel=Label(frame2,image=img).place(x=0, y=0)

titleLabel = Label(frame1, text='Login', font=('arial', 22, 'bold '), fg='purple')
titleLabel.place(x=220, y=80)

userLabel = Label(frame1, text='Username', font=('times new roman', 18, 'bold'), bg='white', fg='gray20')
userLabel.place(x=120, y=165)
entryuser = Entry(frame1, font=('times new roman', 18), bg='lightgray')
entryuser.place(x=120, y=200, width=250)

passwordLabel = Label(frame1, text='Password', font=('times new roman', 18, 'bold'), bg='white',fg='gray20')
passwordLabel.place(x=120, y=250)
entrypassword = Entry(frame1, show="*", font=('times new roman', 18), bg='lightgray')
entrypassword.place(x=120, y=285, width=250)

loginbutton = Button(frame1, text='Login', bd=0, font=('times new roman', 18), cursor='hand2', bg='purple', fg='white', command=login)
loginbutton.place(x=220, y=350)

alregister = Button(frame1, text='Not Yet a User?Register', font=('arial', 12, 'bold'), bd=0, fg='blue', cursor='hand2', command=goToRegister)
alregister.place(x=165, y=400)

root.mainloop()

# #sending details
sock.send(msg)
namemsg = sock.recv(1024).decode('utf-8')
if namemsg == 'NICK':
    sock.send(name.encode('utf-8'))

# methods for second GUI
BUFFER_SIZE=4096

def on_click(event=None):
    # decrypting text from image
    imgDecrypt = ImageSteg()
    decryptmsg = imgDecrypt.decrypt_text_in_image(to_dec_path)
    intDecryptMsg = int(decryptmsg)
    decrypted_msg = rsa.decrypt(intDecryptMsg , private)
    final_msg = str(decrypted_msg)
    text.set(final_msg)
    # disMsgLabel['text']=final_msg
    # Label(msgDisFrame, text=f"{final_msg}", bg="pink", width="20", anchor="e").pack()


def receive():
    while running:
        try:
            uname=sock.recv(1024).decode('utf-8')

            user_text.set(f">  {uname}")
            # print(f'umane->{uname}')
            Label(scrollable_frame, text=f'{uname}:',font=('arial', 8, 'bold '), bg="#E9EBEE", fg="#7E7E7E", width=100,anchor="w").pack()
            file_stream=io.BytesIO()
            recv_data=sock.recv(BUFFER_SIZE)
            while recv_data:
                file_stream.write(recv_data)
                recv_data=sock.recv(BUFFER_SIZE)

                if(recv_data[-4:]==b'%IC%'):
                    break
            image=Image.open(file_stream)

            to_dec_num = random.random()
            global to_dec_path
            to_dec_path="decrypt_assets/trans_im"+str(to_dec_num)+".png"

            image.save(to_dec_path)
            # image.save('assets/transferimage.png')

            image = Image.open(to_dec_path)
            pic = ImageTk.PhotoImage(image)

            i_label = Label(scrollable_frame, bg="#595656", image=pic , anchor="w", width=100, height=100)
            i_label.image = pic
            i_label.pack(pady=5, anchor='w')
            i_label.bind('<Button-1>', on_click)

        except ConnectionAbortedError:
            break
        except:
            sock.close()
            break

def write():
    if str(input_area.get('1.0', 'end')).strip() != "":
        Label(scrollable_frame, text=f'{name}:', width=100,font=('arial', 8, 'bold '), fg="#7E7E7E",bg="#E9EBEE", anchor="e").pack()
        displaymsg = f"{input_area.get('1.0', 'end')}"
        # displaying in the interface
        Label(scrollable_frame, font=('arial', 12, 'bold '), text=displaymsg, bg="#E9EBEE", anchor="e").pack(fill=X, ipadx=200)
        # sending name
        sock.send(name.encode('utf-8'))
        # sending message
        message = f"{input_area.get('1.0', 'end')}"
        bmessage= str.encode(message)
        hex_data = binascii.hexlify(bmessage)
        plain_text = int(hex_data, 16)
        ctt = rsa.encrypt(plain_text, public_key)

        # for encrypting message inside image
        img = ImageSteg()
        # list of image
        img_list = ['demo_im1.png', 'demo_im2.png', 'demo_im3.png', 'demo_im1.jpg', 'demo_im2.jpg']
        # print(f'{random.choice(img_list)}+kjgkfk')
        enc_img_path=img.encrypt_text_in_image(f'{random.choice(img_list)}',str(ctt),"encrypt_assets/")

        # for sending encrypted image
        with open(enc_img_path,'rb') as file:
            file_data = file.read(BUFFER_SIZE)

            while file_data:
                sock.send(file_data)
                file_data = file.read(BUFFER_SIZE)

        sock.send(b'%IC%')
        # print('image sent successfully')
        input_area.delete('1.0', 'end')

# 2: Main Root GUI
global u_name
u_name=" "
chat_root = Tk()
chat_root.title("Steganography-Hide a secret Text Message in an Image")
screen_width, screen_height = chat_root.winfo_screenwidth(), chat_root.winfo_screenheight()
x_co = int((screen_width / 2) - (680 / 2))
y_co = int((screen_height / 2) - (750 / 2)) - 80
chat_root.geometry(f"780x750+{x_co}+{y_co}")
# root.resizable(False, False)
chat_root.configure(bg="#875f9a")
f = ("Times bold", 14)

# label to display username at the top
labelUser=Label(chat_root, text=name,font=('arial', 22, 'bold '),width='20', fg='purple',bg='#C1C1C1').pack(side = TOP, fill="x")

# frame for chatting area
container = Frame(chat_root)
container.place(x=40, y=120, width=450, height=550)

canvas = Canvas(container, bg="#E9EBEE")
scrollable_frame = Frame(canvas, bg="#E9EBEE")

scrollable_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
def configure_scroll_region(e):
    canvas.configure(scrollregion=canvas.bbox('all'))

def resize_frame(e):
    canvas.itemconfig(scrollable_window, width=e.width)

scrollable_frame.bind("<Configure>", configure_scroll_region)

scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)
canvas.yview_moveto(1.0)

scrollbar.pack(side="right", fill="y")

canvas.bind("<Configure>", resize_frame)
canvas.pack(fill="both", expand=True)
canvas.update_idletasks()
canvas.yview_moveto(1.0)
send_button = Button(chat_root, text="Send", fg="white", font="lucida 11 bold", bg="#592984", padx=10,
                                relief="solid", bd=2, command=write)
send_button.place(x=400, y=680)

input_area = Text(chat_root, font="lucida 10 bold", width=38, height=2,
                             highlightcolor="blue", highlightthickness=1)
input_area.place(x=40, y=681)

input_area.focus_set()

# msg display frame
msgDisFrame = Frame(chat_root)
msgDisFrame.place(x=500, y=120, width=150, height=550)

Label(msgDisFrame, text="Online", font=('arial', 12, 'bold '), fg="white", bg="#592984", width=20, anchor="w").pack()
Label(msgDisFrame, text=f">  {name}",font=('arial', 12, 'bold '),bg="white", width=20, anchor="w").pack()
user_text=StringVar()
user_text.set(" ")
Label(msgDisFrame, textvariable=user_text,font=('arial', 12, 'bold '),bg="white", width=20, anchor="w").pack()
# Label(msgDisFrame, text="Online", bg="pink", width="20", anchor="e").pack()

# frame to display final msg
msgFrame = Frame(msgDisFrame, width=150, height=400)
msgFrame.place(x=0, y=100)
text = StringVar()
text.set(" ")
disMsgLabel=Label(msgFrame,text="Message:",font=('arial', 12, 'bold '), fg="green", bg="white").pack(fill='x', anchor='w')
disMsgLabel=Label(msgFrame,textvariable=text,font=('arial', 10, 'bold '), anchor="w").pack()


# Socket receiving pkey message
rmsg = sock.recv(1024)
#
# x = r_msg.find(b'##$$##')
# uname=r_msg[:x]
# rmsg=r_msg[x+6:]
# print(x)

global public_key
public_key = pickle.loads(rmsg)
print("converted")

# # Socket receiving pkey message
# uname = sock.recv(1024).decode('utf-8')
# print(uname)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

chat_root.mainloop()
connection.close()