import os
from tkinter import Toplevel, Canvas, Label
import sak_setting
import sak_gpio

import medicine
import treatment
import cprhelper as cpr
import bpm
import emergency


NUMBER_OF_MEDICINE_CONTAINER = sak_setting.NUMBER_OF_MEDICINE_CONTAINER
NUMBER_OF_IMAGE_BUTTON = 0
RESOURCE_DIR_PATH = sak_setting.RESOURCE_DIR_PATH


def start_sak_main_window():
    global NUMBER_OF_IMAGE_BUTTON

    medicine.start_db()
    print("Medicine DB ON")
    medicine.start_medicine_info_db()
    print("Medicine Info DB ON")
    medicine.check_expire_date()
    print("Medicine Checking expire date Succeed")
    medicine.start_rfid_scanning()
    print("RFID Scanning now")
    treatment.start_db()
    print("Treatment DB ON")

    NUMBER_OF_IMAGE_BUTTON = 0
    window = Toplevel()
    window.geometry(str(window.winfo_screenwidth()) +
                    "x" + str(window.winfo_screenheight()))
    window.resizable(False, False)
    window.title('SAK - Smart Aid Kit')
    canvas = Canvas(window, height=window.winfo_screenheight(),
                    width=window.winfo_screenwidth(), relief="solid", bd=2)
    for (name, func) in [
        ("treatment_logo", treatment.start_gui),
        ("medicine_logo", medicine.start_list_gui),
        ("emergency_logo", emergency.start_gui),
        ("cpr_logo", cpr.start_gui),
            ("bpm_logo", bpm.start_gui)]:
        create_rectangle_button(window, canvas, name, func)

    canvas.focus_set()
    canvas.pack()
    window.protocol("WM_DELETE_WINDOW", sak_gpio.gpio_cleanup)
    window.mainloop()


def create_rectangle_button(window: Toplevel, canvas: Canvas, name: str, func):
    side_size = int(window.winfo_screenheight() / 9)
    x, y = get_xy_pos(window)
    rec_id = canvas.create_rectangle(
        x - side_size / 2, y - side_size / 2, x + side_size / 2, y + side_size / 2, fill="lightblue")
    text_id = canvas.create_text(x, y, text=name[:-5], font=("Purisa", 10))
    canvas.tag_bind(rec_id, "<Button-1>", lambda event: func())
    canvas.tag_bind(text_id, "<Button-1>", lambda event: func())


def get_xy_pos(window: Toplevel):
    global NUMBER_OF_IMAGE_BUTTON
    NUMBER_OF_IMAGE_BUTTON += 1
    i = NUMBER_OF_IMAGE_BUTTON % 3
    if i == 0:
        i = 3
    ii = 1 if NUMBER_OF_IMAGE_BUTTON < 4 else 2
    return i * window.winfo_screenwidth() / 4, ii * window.winfo_screenheight() / 3
