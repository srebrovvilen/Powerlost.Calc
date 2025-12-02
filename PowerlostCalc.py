import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import ImageTk, Image


def calculate():
    R_mat = selected_option.get()
    L = txt_l.get()
    S = txt_s.get()
    I = txt_i.get()
    U = txt_U.get()
    N = input_number.get()
    R = input_resistor.get()
    all_variables = [R_mat, L, S, U, N, R]

    if not all(all_variables):
        CTkMessagebox(
            title="Ошибка!",
            message="Все поля должны быть заполнены!",
            icon="cancel",
            width=70,
            height=50,
        )
        return

    if not all(
        v.isdigit() if v != S else v.replace(".", "", 1).isdigit()
        for v in all_variables
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
    L = int(L)
    S = float(S)
    I = int(I)
    U = int(U)
    N = int(N)
    R = int(R)

    if R_mat == 1:
        R_mat = 0.0175
    elif R_mat == 2:
        R_mat = 0.0295

    U_lost = ((R_mat * (L * 2)) / S) * (((I * 10 ** (-3)) + (U / R)) * N)
    U_min = U - U_lost
    lost_percent = (U_lost / U) * 100

    if U_min <= 0:
        U_min = 0
        lost_percent = 100

    if lost_percent >= 10:
        lbl_res_2.configure(text_color="red")
    else:
        lbl_res_2.configure(text_color="green")

    lbl_res_2.configure(
        text="⬤ Потери на расстоянии "
        + str(L)
        + " м составят: "
        + str(round(lost_percent, 2))
        + " процентов (%)"
        + "\n"
        + "⬤ Итоговое напряжение в сети: "
        + str(round(U_min, 2))
        + " В"
    )


def clear():
    cleared = [txt_l, txt_s, txt_i, txt_U, input_number, input_resistor]
    for inputs in cleared:
        inputs.delete(0, ctk.END)

    lbl_res_2.configure(text="")
    selected_option.set(1)


def switch_theme():
    new_appearance_mode = switch_var.get()
    ctk.set_appearance_mode(new_appearance_mode)


ctk.set_appearance_mode("light")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
try:
    root.wm_iconbitmap()
    icon = ImageTk.PhotoImage(Image.open("img/ee_.png"))
    root.iconphoto(False, icon)
except FileNotFoundError:
    print("Icon file not found. Used the default.")
root.title("Powerlost.Calc")
root.geometry("420x460")
root.resizable(False, False)

frame = ctk.CTkFrame(master=root, fg_color="transparent")
frame.pack()

hello = ctk.CTkLabel(
    frame,
    text="""Добро пожаловать в программу расчета падения напряжения
от длинны и сечения кабеля 🔥🧯🚒""",
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
rad_r_mat.grid(row=2, column=1)
rad_r_mat2.grid(row=3, column=1)

lbl_s = ctk.CTkLabel(frame, text="Сечение кабеля (мм2):")
lbl_s.grid(row=4, column=0, sticky="w")
txt_s = ctk.CTkEntry(frame, width=100)
txt_s.grid(row=4, column=1)

lbl_i = ctk.CTkLabel(frame, text="Ток нагрузки одного устройства (мА):")
lbl_i.grid(row=5, column=0, sticky="w")
txt_i = ctk.CTkEntry(frame, width=100)
txt_i.grid(row=5, column=1)

label_number = ctk.CTkLabel(frame, text="Количество устройств в цепи (шт):")
label_number.grid(row=6, column=0, sticky="w")
input_number = ctk.CTkEntry(frame, width=100)
input_number.grid(row=6, column=1)

label_resistor = ctk.CTkLabel(frame, text="Сопротивление оконечного резистора (Ом):")
label_resistor.grid(row=7, column=0, sticky="w")
input_resistor = ctk.CTkEntry(frame, width=100)
input_resistor.grid(row=7, column=1)

lbl_l = ctk.CTkLabel(frame, text="Длина линии (м):")
lbl_l.grid(row=8, column=0, sticky="w")
txt_l = ctk.CTkEntry(frame, width=100)
txt_l.grid(row=8, column=1, pady=(0, 10))

btn_res = ctk.CTkButton(frame, text="Сброс", command=clear)
btn_res.grid(row=9, column=0, sticky="e")

btn_res = ctk.CTkButton(frame, text="Вычислить", command=calculate)
btn_res.grid(row=9, column=1)

lbl_res = ctk.CTkLabel(frame, anchor="w", text="Результат ↓")
lbl_res.grid(row=10, column=0, columnspan=2, sticky="w")

lbl_res_2 = ctk.CTkLabel(
    frame,
    justify="left",
    anchor="w",
    corner_radius=8,
    fg_color=("white", "grey20"),
    width=400,
    height=60,
    text="",
)
lbl_res_2.grid(row=11, column=0, columnspan=2, sticky="w", pady=(0, 10))

switch_var = ctk.StringVar()
switch_1 = ctk.CTkSwitch(
    frame,
    text="🌙",
    onvalue="dark",
    offvalue="light",
    variable=switch_var,
    command=switch_theme,
)
switch_1.grid(row=12, column=1, sticky="e")

root.mainloop()
