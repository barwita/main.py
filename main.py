from tkinter import *
from tkinter import ttk, messagebox
import sqlite3

f = Tk()
f.geometry('480x420')

def inserer():
    montrer()
    if (not e0.get()) or (not e1.get()) or (not e2.get()) or (not e3.get()):
        messagebox.showwarning("showwarning", "veuiller remplir tous les champs")
        return
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO eleve VALUES (:e0,:e1,:e2,:e3)", {'e0': e0.get(), 'e1': e1.get(), 'e2': e2.get(), 'e3': e3.get()})
    connection.commit()
    connection.close()
    e0.delete(0, END)
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    montrer()

def suprimer():
    if not e4.get():
        return
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("DELETE FROM eleve WHERE oid = " + e4.get())
    connection.commit()
    connection.close()
    e4.delete(0, END)
    montrer()

def montrer():
    for row in tree.get_children():
        tree.delete(row)
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * ,oid FROM eleve")
    records = cursor.fetchall()
    for record in records:
        tree.insert(parent='', index='end', values=(record[4], record[1], record[2], record[3]))
    connection.commit()
    connection.close()

def editer():
    global e0
    global e1
    global e2
    global e3
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM eleve WHERE oid =" + e4.get())
    record = cursor.fetchone()
    e0.insert(0, record[0])
    e1.insert(0, record[1])
    e2.insert(0, record[2])
    e3.insert(0, record[3])
    connection.commit()
    connection.close()

def save():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute("""UPDATE eleve SET
    id = :champ0,
    nom = :champ1,
    note1 = :champ2,
    note2 = :champ3
    WHERE oid= :oid""",
    {
    'champ0' : e0.get(),
    'champ1' : e1.get(),
    'champ2' : e2.get(),
    'champ3' : e3.get(),
    'oid' : e4.get()
    })
    connection.commit()
    connection.close()
    e0.delete(0, END)
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)



frame1 = Frame(f)
frame1.pack()
frame2 = Frame(f)
frame2.pack()
frame3 = Frame(f)
frame3.pack()
e0 = Entry(frame1)
e0.pack()
e1 = Entry(frame1)
e1.pack()
e2 = Entry(frame1)
e2.pack()
e3 = Entry(frame1)
e3.pack()
e4 = Entry(frame1)
e4.pack()

bouton1 = Button(frame2, text="inserer un nouvel eleve", command=inserer)
bouton1.pack()
bouton2 = Button(frame2, text="supprimer cette entree", command=suprimer)
bouton2.pack()
bouton3 = Button(frame2, text="montrer la liste", command=montrer)
bouton3.pack()
bouton4 = Button(frame2, text="editer", command=editer)
bouton4.pack()
bouton5 = Button(frame2, text="save", command=save)
bouton5.pack()

scroll = Scrollbar(frame3)
scroll.pack(side=RIGHT, fill=Y)
tree = ttk.Treeview(frame3, yscrollcommand=scroll.set, columns=('0', '1', '2', '3'), show="headings")
tree.heading(0, text="id")
tree.heading(1, text="nom")
tree.heading(2, text="note1")
tree.heading(3, text="note2")

tree.column(0, width=50)
tree.column(1, width=50)
tree.column(2, width=50)
tree.column(3, width=50)

scroll.config(command=tree.yview)

connection = sqlite3.connect('database.db')
cursor = connection.cursor()
cursor.execute("SELECT * FROM eleve")
records = cursor.fetchall()
connection.commit()
connection.close()
#for record in records:
    #tree.insert(parent='', index='end', values=(record[0], record[1], record[2]))
tree.pack()
f.mainloop()
