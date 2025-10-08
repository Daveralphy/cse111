import tkinter as tk
from tkinter import Frame, Label, Button
from number_entry import IntEntry

def main():
    root = tk.Tk()
    frm_main = Frame(root)
    frm_main.master.title("Heart Rate Calculator")
    frm_main.pack(padx=4, pady=3, fill=tk.BOTH, expand=1)
    populate_main_window(frm_main)
    root.mainloop()

def populate_main_window(frm_main):
    lbl_age = Label(frm_main, text="Age (12 - 90):")
    ent_age = IntEntry(frm_main, width=4, lower_bound=12, upper_bound=90)
    lbl_age_units = Label(frm_main, text="years")
    lbl_rates = Label(frm_main, text="Rates:")
    lbl_slow = Label(frm_main, width=3)
    lbl_fast = Label(frm_main, width=3)
    lbl_units = Label(frm_main, text="beats/minute")
    btn_clear = Button(frm_main, text="Clear")

    lbl_age.grid(row=0, column=0, padx=3, pady=3)
    ent_age.grid(row=0, column=1, padx=3, pady=3)
    lbl_age_units.grid(row=0, column=2, padx=0, pady=3)
    lbl_rates.grid(row=1, column=0, padx=(30,3), pady=3)
    lbl_slow.grid(row=1, column=1, padx=3, pady=3)
    lbl_fast.grid(row=1, column=2, padx=3, pady=3)
    lbl_units.grid(row=1, column=3, padx=0, pady=3)
    btn_clear.grid(row=2, column=0, padx=3, pady=3, columnspan=4, sticky="w")

    def calculate(event):
        try:
            age = ent_age.get()
            max_rate = 220 - age
            slow = max_rate * 0.65
            fast = max_rate * 0.85
            lbl_slow.config(text=f"{slow:.0f}")
            lbl_fast.config(text=f"{fast:.0f}")
        except ValueError:
            lbl_slow.config(text="")
            lbl_fast.config(text="")

    def clear():
        btn_clear.focus()
        ent_age.clear()
        lbl_slow.config(text="")
        lbl_fast.config(text="")
        ent_age.focus()

    ent_age.bind("<KeyRelease>", calculate)
    btn_clear.config(command=clear)
    ent_age.focus()

if __name__ == "__main__":
    main()