import socket
import os
from tkinter import *
from tkinter import messagebox

symptoms = ['Do you have skin rash?','Do you have continuous sneezing?','Do you experience stills?',
'Do you have joint pain?','Did you vomit?','Did you experience fatigue?','Do you have a cough?',
'Do you have a high fever?','Did you experience breathlessness?','Did you sweat?','Do you have a headache?',
'Do you have nausea?','Did you experience loss of appetite?','Do you have pain behind your eyes?',
'Do you have back pain?','Did you constipate?','Do you have abdominal pain?',
 'Do you have diarrhoea?','Do you have swelled lymph nodes?','Do you have malaise?','Do you have phlegm?',
 'Do you have a throat irritation?','Are your eyes red?','Do you feel sinus pressure?',
'Do you have a runny nose?','Do you have congestion?','Do you have chest pain?','Is your heart beating fast?',
'Are you experiencing loss of smell?','Do you have a toxic look which may indicate typhos?',
'Do you have muscle pain?','Do you have red spots on your body?',
'Do you have belly pain?','Do you have rusty sputum?','Do you have small dents in nails?']

n = len(symptoms)


def select_symptoms(event):
    F = open("/root/Desktop/symptomsboolean.txt", "a")
    for i in range(n):
        result = messagebox.askyesno("Symptoms", symptoms[i], icon='question')
        if result == 1:
            F.write("1")
        else:
            F.write("0")
        if i != n - 1:
            F.write(",")
    F.close()
    filename = "/root/Desktop/symptomsboolean.txt"
    with open(filename, 'rb') as f:
        print('Sending...')
        data = f.read()
        s.sendall(data)
        print("Now receiving the results...")


def send_symptoms():
        bt = Button(root, text="CHECK", bg="red", fg="white")
        bt.pack()
        bt.bind('<Button-1>',select_symptoms)


def get_final_results():
    with open('/root/Desktop/predicted_disease.txt', 'wb') as f:
        while True:
            data = s.recv(1024)
            print(data)
            if not data:
                break
            f.write(data)
    f.close()
    s.close()


global root
root = Tk()
root.title("Patient")
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2 - 210)
positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2 - 200)
root.geometry("+{}+{}".format(positionRight, positionDown))
root.configure(bg='black')
root.geometry("600x600")
root.configure(bg='black')




s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
#host = "192.168.43.37"
port = 12341
s.connect((host, port))

label = Label(root, text="You are now connected to the server.",bg="black", fg="white", anchor="center", font=("Arial", 14),pady="100")
label.pack()
label = Label(root, text="Please select the Symptoms: ",bg="black", fg="white", anchor="center", font=("Aria", 14))
label.pack()
label = Label(root, text=" ",bg="black", fg="white", anchor="center", font=("Lato", 14),pady="20")
label.pack()

send_symptoms()

root.mainloop()


global root1
root1 = Tk()
root1.title("Patient")
windowWidth = root1.winfo_reqwidth()
windowHeight = root1.winfo_reqheight()
positionRight = int(root1.winfo_screenwidth() / 2 - windowWidth / 2 - 210)
positionDown = int(root1.winfo_screenheight() / 2 - windowHeight / 2 - 200)
root1.geometry("+{}+{}".format(positionRight, positionDown))
root1.configure(bg='black')
root1.geometry("600x600")
root1.configure(bg='black')

get_final_results()
label = Label(root1, text="You got the results: ",fg="white",bg="black",anchor="center", font=("Arial", 11))
label.pack()
configfile = Text(root1, wrap=WORD,bg='black',fg="white")
filename='/root/Desktop/predicted_disease.txt'
statinfo = os.stat(filename)
if statinfo.st_size is 0:
    label = Label(root1, text="\n\nDisease not predicted because of unsatisfactory probability value.",bg="black", fg="red", anchor="center", font=("Arial", 14))
    label.pack()
    label = Label(root1, text="\n\nKindly visit the doctor",bg="black", fg="red", anchor="center", font=("Arial", 14))
    label.pack()



else:
    with open(filename, 'r') as f:
        configfile.insert(INSERT, f.read())
        configfile.pack(fill="none", expand=TRUE)

root1.mainloop()




