from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import mm
import tkinter as tk
from tkinter import messagebox
import os
from distutils.core import setup


def generate_pdf():
    #External Settigns
    ID = entry_3.get()
    doctor = entry_1.get()
    paciente = entry_2.get()
    n_alineadores_sup = int(entry_4.get())
    n_alineadores_inf = int(entry_5.get())
    if(n_alineadores_sup<n_alineadores_inf):
        n_Steps = n_alineadores_inf
    else:
        n_Steps = n_alineadores_sup

    sexo = int(variable.get())
    IPR = text_box.get(1.0, tk.END)
    IPRS = IPR.splitlines()
    # jorge = IPRS.split(',')
    steps_with_ipr = []
    IPR_list = []
    for x in IPRS:
        step_with_ipr = x.split(', ')
        IPR_list.append(step_with_ipr)
    for y in IPR_list:
        print(y)
        steps_with_ipr.append(y[0])

    print(IPR_list)
    #Internal Settings
    w, h = A4
    x_in = 4*mm #x inicial
    y_in = 4*mm #y inicial
    lin_jump = 14.4 #Salto de linea
    RGB_cuadro = [98, 86, 160]
    RGB_texto = [0,0,0]
    RGB_Step = [98, 86, 160]
    ancho_linea_cuadro = 0.7*mm
    y_in_text = 70*mm -7.5*mm
    x = 0
    y = 0
    offset_vertical = 73*mm
    offset_horizontal = 68*mm
    c = canvas.Canvas("Alineo_stickers.pdf", pagesize=A4)
    c.setLineWidth(ancho_linea_cuadro)

    #loop for stickers
    for n in range(0,n_Steps+1):
        c.setFillColorRGB(RGB_texto[0], RGB_texto[1], RGB_texto[2]) #black
        #c.setFont('Courier', 14)
        c.drawString((x_in+5*mm) + offset_horizontal*x, (y_in_text) + offset_vertical*y, "ID: " + ID)
        if(sexo):
            c.drawString((x_in+5*mm) + offset_horizontal*x, (y_in_text - lin_jump*1) + offset_vertical*y , "Doctora:  " + doctor)
        else:
            c.drawString((x_in+5*mm) + offset_horizontal*x, (y_in_text - lin_jump*1) + offset_vertical*y , "Doctor:     " + doctor)
        c.drawString((x_in+5*mm) + offset_horizontal*x, (y_in_text - lin_jump*2) + offset_vertical*y , "Paciente: " + paciente)
        if(n==0):
            c.drawString((x_in+5*mm) + offset_horizontal*x, (y_in_text - lin_jump*4) + offset_vertical*y , "Alineador superior: MATRIZ")
            c.drawString((x_in+5*mm) + offset_horizontal*x, (y_in_text - lin_jump*5) + offset_vertical*y , "Alineador inferior:   MATRIZ")
        else:
            if(n<=n_alineadores_inf+1):
                texto_alineador_inf = "Alineador inferior:   {} de {} ".format(n-1, n_alineadores_inf)
            else:
                texto_alineador_inf = "Alineador inferior:   --"
            if(n<=n_alineadores_sup+1):
                texto_alineador_sup = "Alineador superior: {} de {}".format(n-1, n_alineadores_sup)
            else:
                texto_alineador_sup = "Alineador superior: --"
            c.drawString((x_in+5*mm) + offset_horizontal*x, (y_in_text - lin_jump*4) + offset_vertical*y , texto_alineador_sup)
            c.drawString((x_in+5*mm) + offset_horizontal*x, (y_in_text - lin_jump*5) + offset_vertical*y , texto_alineador_inf)
        c.setFillColorRGB(RGB_Step[0]/256, RGB_Step[1]/256, RGB_Step[2]/256)
        #c.setFont('Courier', 14)
        c.drawString((x_in + 40*mm) + offset_horizontal*x, (y_in_text+3*mm) + offset_vertical*y, "STEP {}".format(n))

        if(str(n) in steps_with_ipr):
            try:
                indice = steps_with_ipr.index(str(n))
            except:
                messagebox.showinfo(message="Bad IPR format!", title="Alineo")

            c.setStrokeColorRGB(RGB_cuadro[0]/256, RGB_cuadro[1]/256, RGB_cuadro[2]/256)
            c.drawString((x_in+3*mm) + offset_horizontal*x, (y_in_text - lin_jump*7) + offset_vertical*y , "IPR requerido " + IPRS[indice][3:])
            # 10, 14][15 - 0.2 mm
        # Dibujamos una imagen (IMAGEN, X,Y, WIDTH, HEIGH)
        c.drawImage('Alineo_logo.png', (x_in+7.5*mm) + offset_horizontal*x, (y_in+3*mm)+offset_vertical*y , 50*mm, 10.3*mm)

        # Dibujamos el cuadrado
        c.setStrokeColorRGB(RGB_cuadro[0]/256, RGB_cuadro[1]/256, RGB_cuadro[2]/256)  # Color Alineo
        c.rect(x_in + offset_horizontal*x, y_in + offset_vertical*y , 65*mm, 70*mm, stroke = 1, fill = 0) #canvas.rect(x, y, width, height, stroke=1, fill=0)

        if((n+1)%4==0):
            x = x + 1
            y = 0
        else:
            y = y + 1

        if((n+1)%12 == 0):
            c.showPage()
            c.setLineWidth(ancho_linea_cuadro)
            x = 0

    c.save()
    messagebox.showinfo(message="Stickers generated!", title="Alineo")


#GUI Settings
window = tk.Tk()
window.geometry("550x350")
window.title("Alineo Sticker Generator")
window.iconbitmap('icono.ico')
window.columnconfigure([0, 1, 2, 3], minsize=100)
window.rowconfigure([0, 1, 2, 3, 4, 5, 6, 7,8], minsize=10)

variable = tk.StringVar()

Run = tk.Button(master=window,text="Run", width=20, command=generate_pdf)
Run.grid(row=8, column=1, sticky="n")

label_1 = tk.Label(master=window, text = "Doctor/a")
label_1.grid(row=0, column=0, sticky="n")
label_2 = tk.Label(master=window, text = "Paciente")
label_2.grid(row=1, column=0, sticky="n")
label_3 = tk.Label(master=window, text = "ID")
label_3.grid(row=2, column=0, sticky="n")
label_4 = tk.Label(master=window, text = "Nº Al sup")
label_4.grid(row=3, column=0, sticky="n")
label_5 = tk.Label(master=window, text = "Nº Al inf")
label_5.grid(row=4, column=0, sticky="n")
label_6 = tk.Label(master=window, text = "IPR requerido")
label_6.grid(row=5, column=1, sticky="n")
label_7 = tk.Label(master=window, text = "Ejemplo: 1, 14][15 - 0.2 mm")
label_7.grid(row=6, column=1, sticky="n")

text_box=tk.Text(master=window, width= 25, height=10)
text_box.grid(row=7, column=1, sticky="n")
radiobutton_1 = tk.Radiobutton(text="Mujer", variable=variable, value=1)
radiobutton_1.grid(row=0, column=2, sticky="n")
radiobutton_2 = tk.Radiobutton(text="Hombre", variable=variable, value=0)
radiobutton_2.grid(row=0, column=3, sticky="n")

entry_1 = tk.Entry(master=window, width=25)
entry_1.grid(row=0, column=1, sticky="n")
entry_2 = tk.Entry(master=window, width=25)
entry_2.grid(row=1, column=1, sticky="n")
entry_3 = tk.Entry(master=window, width=25)
entry_3.grid(row=2, column=1, sticky="n")
entry_4 = tk.Entry(master=window, width=25)
entry_4.grid(row=3, column=1, sticky="n")
entry_5 = tk.Entry(master=window, width=25)
entry_5.grid(row=4, column=1, sticky="n")

window.mainloop()
