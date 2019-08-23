from tkinter import Tk, Label, Listbox
import urllib.request as urllib
import json
import os
import sqlite3
from sak_setting import RESOURCE_DIR_PATH


def start_gui():
    window = Tk()
    window.geometry("%dx%d+%d+%d" % (window.winfo_screenwidth(),
                                     window.winfo_screenheight(), 0, 0))
    window.resizable(False, False)
    window.title('Treatment SAK')
    toptext = Label(window, text="Treatments List", width=window.winfo_screenwidth(),
                    height=int(window.winfo_screenheight() / 7), anchor="n")
    treatment_list_box = Listbox(window, selectmode='extended',
                                 height=int(6 / 7 * window.winfo_screenheight()), yscrollcommand=True)
    for treatment in get_treatments():
        treatment_list_box.insert(treatment[1], treatment[2])

    treatment_list_box.bind("<<ListboxSelect>>", clicked)
    toptext.pack()
    treatment_list_box.pack()
    window.mainloop()


def clicked(event):
    index = int(event.widget.curselection()[0])
    treatment_info = get_treatment(index)

    window = Tk()
    window.geometry(str(window.winfo_screenwidth()) + "x" +
                    str(window.winfo_screenheight()) + "0+0")
    window.title('Treatment SAK - About ' + treatment_info[2])

    toptext = Label(window, text=treatment_info[2], width=window.winfo_screenwidth(),
                    height=window.winfo_screenheight() / 7)
    doctext = Label(window, text=treatment_info[4], justify="left", width=window.winfo_screenwid(),
                    height=window.winfo_screenheight() * 6 / 7)

    toptext.pack()
    doctext.pack()

    window.mainloop()


def start_db():
    conn = sqlite3.connect(RESOURCE_DIR_PATH + 'treatment.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='treatment'")  # Table Name is 'treatment'
    rows = cur.fetchall()
    is_exist = False
    for row in rows:
        if row[0] == "treatment":
            is_exist = True
            break
    if not is_exist:  # If Table is not exist, we will create table
        cur.execute("CREATE TABLE "
                    "treatment("
                    "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                    "treatment_id INTEGER NOT NULL,"
                    "name TEXT NOT NULL,"
                    "version INTEGER NOT NULL,"
                    "document TEXT)"
                    )
    conn.commit()
    conn.close()


def get_treatments():
    conn = sqlite3.connect(RESOURCE_DIR_PATH +
                           'treatment.db')
    cur = conn.cursor()
    cur.execute(
        "SELECT id, treatment_id, name, version, document FROM treatment")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_treatment(treatment_id: int):
    conn = sqlite3.connect(RESOURCE_DIR_PATH +
                           'treatment.db')
    cur = conn.cursor()
    cur.execute("SELECT id, treatment_id, name, version, document FROM treatment WHERE treatment_id = ?", [
                treatment_id])
    rows = cur.fetchall()
    conn.close()
    if len(rows) <= 0:
        return False
    return rows[0]


def register_treatment(treatment_id: int, name: str, version: int, document: str):
    conn = sqlite3.connect(RESOURCE_DIR_PATH +
                           'treatment.db')  # get treatment data
    cur = conn.cursor()
    cur.execute("INSERT INTO treatment(treatment_id, name, version, document) VALUES (?, ?, ?, ?)", [
        treatment_id, name, version, document])
    conn.commit()
    conn.close()


def delete_treatment(treatment_id: int):
    conn = sqlite3.connect(RESOURCE_DIR_PATH +
                           'treatment.db')  # get treatment data
    cur = conn.cursor()
    cur.execute("DELETE FROM treatment WHERE treatment_id = ?", [
        treatment_id])
    conn.commit()
    conn.close()


def treatment_update(treatment_id: int):
    data = urllib.urlopen("http://sak-project.ml/treatment_" +
                          str(treatment_id)+".json").read()
    delete_treatment(treatment_id)
    register_treatment(
        treatment_id, data["name"], data["version"], data["document"])


def treatments_update():  # By HTML JSON
    # id(treatment_id): version
    data = urllib.urlopen("http://sak-project.ml/treatment_list.json").read()
    data = json.loads(data)
    for (k, v) in data.items():
        treatment = get_treatment(k)
        if not treatment or treatment[3] < v:
            treatment_update(k)
