import socket
from tkinter import *
from tkinter import filedialog
import sys
import sqlite3
import numpy
import sklearn
import pandas as pd
import pickle



def get_symptoms():
    f = open("/root/Desktop/symptomsboolean.txt", "wb")
    while True:
        data = conn.recv(1024)
        f.write(data)
        if not data:
             return
        else:
            break
    f.close()


def upload(event):
    root1.filename = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=(("all files", "*.*"), ("all files", "*.*")))
    realfilename = root1.filename
    with open(realfilename, 'rb') as f:
        print('Sending...')
        data = f.read()
        conn.sendall(data)
    f.close()
    conn.close()
    sys.exit(0)


def find_using_ML():

    filename= "final_model.sav"
    dtc = pickle.load(open(filename, 'rb'))
    f = open('/root/Desktop/symptomsboolean.txt', "r")
    lines = f.readlines()
    sym = lines[0].split(',')                                       # Disease prediction by ML Algorithm
    sym = list(map(lambda x : int(x), sym))
    f.close()
    symdf = pd.DataFrame([sym])
    pred = dtc.predict(symdf)
    predicted=pred[0]
    print(predicted)

    dbconn = sqlite3.connect('prescription')

    result = dbconn.execute("SELECT * FROM TAB WHERE disease=(?)", (predicted,))      #Database Access for prescription
    F = open("/root/Desktop/Results_from_ML.txt", "a")
    for row in result:
        n = len(row)
        F.write("Disease : ")
        F.write(row[0])
        F.write("\n\nPrescriptions are as follows: \n\n")
        for i in range(1, n):
            if row[i] is not None:
                #F.write("• ")
                F.write(row[i])
                F.write("\n\n")
    F.close()
    dbconn.close()

def send_results_to_patient():
    find_using_ML()
    bt = Button(root1, text="Upload", bg="red", fg="white")
    bt.pack()
    bt.bind('<Button-1>', upload)



global root
root = Tk()
root.title("Doctor")
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth() / 2 - windowWidth / 2 - 210)
positionDown = int(root.winfo_screenheight() / 2 - windowHeight / 2 - 200)
root.geometry("+{}+{}".format(positionRight, positionDown))
root.configure(bg='black')
root.geometry("600x600")
root.configure(bg='black')
label = Label(root, text="Client is now connected. ML algorithm will be now applied.",bg="black", fg="white", anchor="center", font=("Arial", 14),pady="100")
label.pack()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host =""
port = 12341
s.bind((host, port))
s.listen(1)
global conn
conn, addr = s.accept()
get_symptoms()
root.mainloop()



global root1
root1 = Tk()
root1.title("Doctor")
windowWidth = root1.winfo_reqwidth()
windowHeight = root1.winfo_reqheight()
positionRight = int(root1.winfo_screenwidth() / 2 - windowWidth / 2 - 210)
positionDown = int(root1.winfo_screenheight() / 2 - windowHeight / 2 - 200)
root1.geometry("+{}+{}".format(positionRight, positionDown))
root1.configure(bg='black')
root1.geometry("600x600")
root1.configure(bg='black')
root1.configure(bg='black')
label = Label(root1, text="Send the results to the client by choosing the file.",bg="black", fg="white", anchor="center", font=("Arial", 14),pady="100")
label.pack()

send_results_to_patient()

root1.mainloop()








