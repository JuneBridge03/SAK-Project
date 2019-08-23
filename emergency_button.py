from tkinter import Tk, Label
import bpm
import cprhelper
import emergency
import sak_gpio
import threading


def readloops():
    def readloop():
        while True:
            data = sak_gpio.get_button()
            if data:
                start_emergency()

    threading.Thread(readloop).start()


def start_emergency():
    window = Tk()
    window.geometry("100x100+0+0")
    window.resizable(False, False)
    window.title("Emergency!!")

    Label(window, text="Emergency!!",
                          width=10, height=5, relief="solid").pack()

    window.mainloop()

    bpm.start_gui()
    cprhelper.start_gui()
    emergency.start_gui()
