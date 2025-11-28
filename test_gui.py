import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import ImageTk, Image


def calculate():
    R_mat = selected_option.get()
    l = txt_l.get()
    S = txt_s.get()
    I = txt_i.get()
    U = txt_U.get()
    s = S.replace(".", "")

    if not R_mat or not l or not S or not I or not U:
        CTkMessagebox(
            title="Ошибка!",
            message="Все поля должны быть заполнены!",
            icon="cancel",
            width=70,
            height=50,
        )
        return

    if (
        not R_mat.isdigit()
        or not l.isdigit()
        or not s.isdigit()
        or not I.isdigit()
        or not U.isdigit()
    ):
        CTkMessagebox(
            title="Ошибка!",
            message="Введены недопустимые символы!",
            icon="cancel",
            width=70,
            height=50,
        )
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
        lbl_res.configure(text_color="red")
        lbl_res_2.configure(text_color="red")
    else:
        lbl_res.configure(text_color="green")
        lbl_res_2.configure(text_color="green")

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
    txt_l.delete(0, ctk.END)
    txt_s.delete(0, ctk.END)
    txt_i.delete(0, ctk.END)
    txt_U.delete(0, ctk.END)
    lbl_res.configure(text="")
    lbl_res_2.configure(text="")
    selected_option.set(1)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
try:
    root.wm_iconbitmap()
    icon = ImageTk.PhotoImage(Image.open("ee_.png"))
    root.iconphoto(False, icon)
except FileNotFoundError:
    print("Icon file not found. Used the default.")
root.title("Powerlost.Calc")
root.geometry("420x350")
root.resizable(False, False)

frame = ctk.CTkFrame(master=root, fg_color="transparent")
frame.pack()

hello = ctk.CTkLabel(
    frame,
    text="""Добро пожаловать в программу расчета падения напряжения
от длинны и сечения кабеля 💀💀💀""",
)
hello.grid(row=0, column=0, columnspan=2, sticky="n", pady=(20, 20))

lbl_U = ctk.CTkLabel(frame, text="Общий вольтаж линии (В): ")
lbl_U.grid(row=1, column=0, sticky="w")
txt_U = ctk.CTkEntry(frame, width=100)
txt_U.grid(row=1, column=1)

selected_option = ctk.StringVar()
selected_option.set(1)
lbl_r_mat = ctk.CTkLabel(frame, text="Из какого материала изготовлен кабель:")
lbl_r_mat.grid(row=2, column=0, sticky="w")
rad_r_mat = ctk.CTkRadioButton(
    frame,
    radiobutton_width=15,
    radiobutton_height=15,
    border_width_unchecked=2,
    border_width_checked=4,
    text="Медь",
    variable=selected_option,
    value="1",
)
rad_r_mat2 = ctk.CTkRadioButton(
    frame,
    radiobutton_width=15,
    radiobutton_height=15,
    border_width_unchecked=2,
    border_width_checked=4,
    text="Аллюминий",
    variable=selected_option,
    value="2",
)
rad_r_mat.grid(row=2, column=1, sticky="w")
rad_r_mat2.grid(row=3, column=1, sticky="w")

lbl_s = ctk.CTkLabel(frame, text="Сечение кабеля (мм2):")
lbl_s.grid(row=4, column=0, sticky="w")
txt_s = ctk.CTkEntry(frame, width=100)
txt_s.grid(row=4, column=1)

lbl_i = ctk.CTkLabel(frame, text="Предпологаемый ток нагрузки (А):")
lbl_i.grid(row=5, column=0, sticky="w")
txt_i = ctk.CTkEntry(frame, width=100)
txt_i.grid(row=5, column=1)

lbl_l = ctk.CTkLabel(frame, text="Длина линии (м):")
lbl_l.grid(row=6, column=0, sticky="w")
txt_l = ctk.CTkEntry(frame, width=100)
txt_l.grid(row=6, column=1, pady=(0, 10))

btn_res = ctk.CTkButton(frame, text="Сброс", command=clear)
btn_res.grid(row=7, column=0, sticky="e")

btn_res = ctk.CTkButton(frame, text="Вычислить", command=calculate)
btn_res.grid(row=7, column=1)

lbl_res = ctk.CTkLabel(frame, text="")
lbl_res.grid(row=8, column=0, columnspan=2, sticky="w", pady=(10, 0))

lbl_res_2 = ctk.CTkLabel(frame, text="")
lbl_res_2.grid(row=9, column=0, columnspan=2, sticky="w", pady=(0, 10))

root.mainloop()
