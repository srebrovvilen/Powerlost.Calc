from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


def calculate():
    R_mat = selected_option.get()
    l = txt_l.get()
    S = txt_s.get()
    I = txt_i.get()
    U = txt_U.get()
    s = S.replace(".", "")

    if not R_mat or not l or not S or not I or not U:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return

    if (
        not R_mat.isdigit()
        or not l.isdigit()
        or not s.isdigit()
        or not I.isdigit()
        or not U.isdigit()
    ):
        messagebox.showerror("Ошибка", "Введены недопустимые символы!")
        return

    R_mat = int(R_mat)
    l = int(l)
    S = float(S)
    I = int(I)
    U = int(U)

    if R_mat == 1:
        R_mat = 0.0175
    elif R_mat == 2:
        R_mat = 0.0295

    U_lost = ((R_mat * (l * 2)) / S) * I
    U_min = U - U_lost
    lost_percent = (U_lost / U) * 100

    if U_min <= 0:
        U_min = 0
        lost_percent = 100

    if lost_percent >= 10:
        lbl_res.configure(fg="red")
        lbl_res_2.configure(fg="red")
    else:
        lbl_res.configure(fg="green")
        lbl_res_2.configure(fg="green")

    lbl_res.configure(
        text="⬤ Потери на расстоянии "
        + str(l)
        + " м составят: "
        + str(round(lost_percent, 2))
        + " процентов (%)"
    )
    lbl_res_2.configure(
        text="⬤ Итоговое напряжение в сети: " + str(round(U_min, 2)) + " В"
    )


def clear():
    txt_l.delete(0, END)
    txt_s.delete(0, END)
    txt_i.delete(0, END)
    txt_U.delete(0, END)
    lbl_res.configure(text="")
    lbl_res_2.configure(text="")
    selected_option.set(1)


root = Tk()
root.title("Powerlost.Calc")
root.resizable(False, False)
try:
    icon = ImageTk.PhotoImage(Image.open("ee_.png"))
    root.iconphoto(False, icon)
except FileNotFoundError:
    print("Icon file not found. Used the default.")

frame = Frame(root, border=10)
frame.pack()

hello = Label(
    frame,
    text="""Добро пожаловать в программу расчета падения напряжения
от длинны и сечения кабеля 💀💀💀""",
)
hello.grid(row=0, column=0, columnspan=2, sticky="n", pady=(10, 10))

lbl_U = Label(frame, text="Введите общий вольтаж линии (В): ")
lbl_U.grid(row=1, column=0, sticky="w")
txt_U = Entry(frame, width=10)
txt_U.grid(row=1, column=1)

selected_option = StringVar()
selected_option.set(1)
lbl_r_mat = Label(frame, text="Из какого материала изготовлен кабель:")
lbl_r_mat.grid(row=2, column=0, sticky="w")
rad_r_mat = Radiobutton(frame, text="Медь", variable=selected_option, value="1")
rad_r_mat2 = Radiobutton(frame, text="Аллюминий", variable=selected_option, value="2")
rad_r_mat.grid(row=2, column=1, sticky="w")
rad_r_mat2.grid(row=3, column=1, sticky="w")

lbl_s = Label(frame, text="Введите сечение кабеля (мм2):")
lbl_s.grid(row=4, column=0, sticky="w")
txt_s = Entry(frame, width=10)
txt_s.grid(row=4, column=1)

lbl_i = Label(frame, text="Введите предпологаемый ток нагрузки (А):")
lbl_i.grid(row=5, column=0, sticky="w")
txt_i = Entry(frame, width=10)
txt_i.grid(row=5, column=1)

lbl_l = Label(frame, text="Введите длину линии (м):")
lbl_l.grid(row=6, column=0, sticky="w")
txt_l = Entry(frame, width=10)
txt_l.grid(row=6, column=1, pady=(0, 10))

btn_res = Button(frame, text="Сброс", command=clear)
btn_res.grid(row=7, column=0, sticky="e")

btn_res = Button(frame, text="Вычислить", command=calculate)
btn_res.grid(row=7, column=1)

lbl_res = Label(frame, text="")
lbl_res.grid(row=8, column=0, columnspan=2, sticky="w")

lbl_res_2 = Label(frame, text="")
lbl_res_2.grid(row=9, column=0, columnspan=2, sticky="w")

root.mainloop()
