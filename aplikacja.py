# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import filedialog, messagebox
from math import sqrt, tan, cos, sin, pi, log, asin, acos

def GK_projection(fi_p, lam_p, lam_0, m0=1):
    t = tan(fi_p)
    ni = cos(fi_p)*sqrt(e_2_prim)
    delta_lambda = lam_p - lam_0
    N = a/((1-e_2*(sin(fi_p)**2))**(1/2))
    M = (a*(1-e_2))/((1-e_2*(sin(fi_p)**2))**(3/2))
    R = sqrt(M*N)
    y_GK = delta_lambda*N*cos(fi_p) + ((delta_lambda**3)/6)*N*(cos(fi_p)**3)*(1-(t**2)+(ni**2)) + ((delta_lambda**5)/120)*N*(cos(fi_p)**5)*(5-(18*(t**2))+(t**4)+(14*(ni**2))-(58*(ni**2)*(t**2)))

    m = round(m0 * (1+((y_GK**2)/(2*(R**2)))+((y_GK**4)/(24*(R**4)))), 6)

    return m

def LAEA_projection(fi_p, lam_p):
    fi_0 = 52 * pi/180
    lam_0 = 10 * pi/180
    qp = (1 - e_2) * ((1 / (1 - e_2)) - (log((1-e)/(1+e)) / (2 * e)))
    Rq = a * sqrt(qp / 2)
    q = (1 - e_2) * ((sin(fi_p) / (1 - e_2*(sin(fi_p)**2))) - (log((1 - e*sin(fi_p)) / (1 + e*sin(fi_p))) / (2 * e)))
    q0 = (1 - e_2) * ((sin(fi_0) / (1 - e_2 * (sin(fi_0) ** 2))) - (log((1 - e * sin(fi_0)) / (1 + e * sin(fi_0))) / (2 * e)))
    fi_p_authalic = asin(q/qp)
    fi_0_authalic = asin(q0/qp)
    delta = acos(sin(fi_0_authalic)*sin(fi_p_authalic)+cos(fi_0_authalic)*cos(fi_p_authalic)*cos(lam_p-lam_0))

    h = round(cos(delta/2), 6)
    k = round(1/cos(delta/2), 6)

    return h, k

def LCC_projection(fi_p):
    row1 = 35 * pi / 180
    row2 = 65 * pi / 180
    m1 = cos(row1) / (sqrt(1 - e_2 * (sin(row1) ** 2)))
    m2 = cos(row2) / (sqrt(1 - e_2 * (sin(row2) ** 2)))
    t1 = (tan((45 * pi / 180) - (row1) / 2)) / (((1 - e * sin(row1)) / (1 + e * sin(row1))) ** (e / 2))
    t2 = (tan((45 * pi / 180) - (row2) / 2)) / (((1 - e * sin(row2)) / (1 + e * sin(row2))) ** (e / 2))
    t_p = (tan((45 * pi / 180) - (fi_p) / 2)) / (((1 - e * sin(fi_p)) / (1 + e * sin(fi_p))) ** (e / 2))
    n = log(m1 / m2) / log(t1 / t2)
    F = m1 / (n * (t1 ** n))
    p = a * F * (t_p ** n)
    m = cos(fi_p) / (sqrt(1 - e_2 * (sin(fi_p) ** 2)))

    k = round(p * (n / (a * m)), 6)

    return k

def calculations():
    if openPath.get() == 'brak':
        open_button.config(bg='red')
        messagebox.showwarning('Uwaga!', 'Nie wskazano lokalizacji pliku z danymi')
    elif savePath.get() == 'brak':
        save_button.config(bg='red')
        messagebox.showwarning('Uwaga!', 'Nie wybrano lokalizacji zapisu pliku wynikowego')
    elif not dataList:
        messagebox.showwarning('Uwaga!', 'Żaden z wprowadzonych punktów nie jest poprawny. Obliczenia nie zostały wykonane')
    else:
        status_label.config(anchor=tk.E,text='Autor: Mółka Maciej  ')
        global a, e_2, e, e_2_prim
        a = 6378137;
        e_2 = 0.00669438002290
        e = sqrt(e_2)
        e_2_prim = 0.00673949677548

        if savePath.get()[-4:] == '.txt':
            finalPath = savePath.get()
        else:
            finalPath = savePath.get()+'.txt'

        open(finalPath,'w').close()
        if variable_CS.get() == 'PL-LAEA':
            with open(finalPath, 'w') as file:
                file.write('Punkt Szerokość_geodezyjna Długość_geodezyjna a b')
                file.write('\n')
                for i in dataList:
                    a, b = LAEA_projection(i[1] * pi / 180, i[2] * pi / 180)
                    file.write(i[0]+' '+str(i[1])+' '+str(i[2])+' '+str(a)+' '+str(b))
                    file.write('\n')

        if variable_CS.get() == 'PL-LCC':
            with open(finalPath, 'w') as file:
                file.write('Punkt Szerokość_geodezyjna Długość_geodezyjna a=b')
                file.write('\n')
                for i in dataList:
                    a = LCC_projection(i[1]*pi/180)
                    file.write(i[0]+' '+str(i[1])+' '+str(i[2])+' '+str(a))
                    file.write('\n')

        if variable_CS.get() == 'PL-UTM':
            with open(finalPath, 'w') as file:
                file.write('Punkt Szerokość_geodezyjna Długość_geodezyjna a=b')
                file.write('\n')
                for i in dataList:
                    if variable_UTM_zones.get() == '33N':
                        a = GK_projection(i[1]*pi/180, i[2]*pi/180, 15* pi / 180, 0.9996)
                    elif variable_UTM_zones.get() == '34N':
                        a = GK_projection(i[1] * pi / 180, i[2] * pi / 180, 21* pi / 180, 0.9996)
                    elif variable_UTM_zones.get() == '35N':
                        a = GK_projection(i[1] * pi / 180, i[2] * pi / 180, 27* pi / 180, 0.9996)
                    file.write(i[0] + ' ' + str(i[1]) + ' ' + str(i[2]) + ' ' + str(a))
                    file.write('\n')

        if variable_CS.get() == 'PL-1992':
            with open(finalPath, 'w') as file:
                file.write('Punkt Szerokość_geodezyjna Długość_geodezyjna a=b')
                file.write('\n')
                for i in dataList:
                    a = GK_projection(i[1]*pi/180, i[2]*pi/180, 19* pi / 180, 0.9993)
                    file.write(i[0] + ' ' + str(i[1]) + ' ' + str(i[2]) + ' ' + str(a))
                    file.write('\n')

        if variable_CS.get() == 'PL-2000':
            with open(finalPath, 'w') as file:
                file.write('Punkt Szerokość_geodezyjna Długość_geodezyjna a=b')
                file.write('\n')
                for i in dataList:
                    if variable_2000_zones.get() == '5':
                        a = GK_projection(i[1]*pi/180, i[2]*pi/180, 15* pi / 180, 0.999923)
                    elif variable_2000_zones.get() == '6':
                        a = GK_projection(i[1] * pi / 180, i[2] * pi / 180, 18* pi / 180, 0.999923)
                    elif variable_2000_zones.get() == '7':
                        a = GK_projection(i[1] * pi / 180, i[2] * pi / 180, 21* pi / 180, 0.999923)
                    elif variable_2000_zones.get() == '8':
                        a = GK_projection(i[1] * pi / 180, i[2] * pi / 180, 24 * pi / 180, 0.999923)
                    file.write(i[0] + ' ' + str(i[1]) + ' ' + str(i[2]) + ' ' + str(a))
                    file.write('\n')

        messagebox.showinfo('Brawo!', 'Obliczenia zakończono!')

def openFile():
    tf = filedialog.askopenfilename(filetypes=(("Plik tekstowy", "*.txt"),))
    if tf:
        open_button.config(bg='green')
        openPath.set(tf)
        with open(tf, 'r') as file:
            for line in file:
                if not line.isspace() and len(line.split()) == 3:
                    try:
                        data = line.split()
                        if float(data[1]) > 57 or float(data[1]) < 47 or float(data[2]) > 26 or float(data[2]) < 12:
                            pass
                        else:
                            dataList.append([data[0], float(data[1]), float(data[2])])
                    except ValueError:
                        pass

def saveFile():
    tf = filedialog.asksaveasfilename(filetypes=(("Plik tekstowy", "*.txt"),))
    if tf:
        save_button.config(bg='green')
        savePath.set(tf)

def zones(choise):
    if choise == 'PL-UTM':
        label5.place_forget()
        label2.config(text='Strefa')
        variable_UTM_zones.set(optionList_UTM[0])
        variable_2000_zones.set('')
        opt2.config(width=3)
        opt2.place(relx=0.64, rely=0.27, anchor = 'w')
        opt3.place_forget()
    elif choise == 'PL-2000':
        label5.place_forget()
        label2.config(text='Strefa')
        variable_2000_zones.set(optionList_2000[0])
        variable_UTM_zones.set('')
        opt2.place_forget()
        opt3.config(width=1)
        opt3.place(relx=0.64, rely=0.27, anchor = 'w')
    else:
        label5.place(relx=0.70, rely=0.05)
        label2.config(text='')
        opt2.place_forget()
        opt3.place_forget()
        variable_UTM_zones.set('')
        variable_2000_zones.set('')

def open_button_hover(e):
    status_label.config(anchor=tk.CENTER,text=u'Poprawne ułożenie danych w kolumnach: Nazwa_punktu Szerokość_geodezyjna Długość_geodezyjna (np. Punkt_1 47.5 20).\nUwaga! \u03C6, \u03BB wyrażone w stopniach dziesiętnych (separator "."), kolumny rozdzielone znakiem spacji/tabulacją.')

def open_button_hover_leave(e):
    status_label.config(anchor=tk.CENTER,text = u'Program oblicza zniekształcenia dla współrzędnych geodezyjnych (elipsoida GRS80) z przedziału: 57 ≥ \u03C6 ≥ 47, 26 ≥ \u03BB ≥ 12.')

def save_button_hover(e):
    if variable_CS.get() == 'PL-LAEA':
        status_label.config(anchor=tk.CENTER,
                           text=u'W docelowym pliku zapisane zostaną kolejno: numer punktu, szerokość geodezyjna, długość geodezyjna, a, b. \n Gdzie: a to skala zniekształceń długości w kierunku wertykałów, natomiast b w kierunku almukantaratów.')
    else:
        status_label.config(anchor=tk.CENTER,text=u'W docelowym pliku zapisane zostaną kolejno: numer punktu, szerokość geodezyjna, długość geodezyjna, a=b. \n Gdzie: a=b to skala zniekształceń długości w kierunkach głównych.')

def save_button_hover_leave(e):
    status_label.config(anchor=tk.CENTER,text = u'Program oblicza zniekształcenia dla współrzędnych geodezyjnych (elipsoida GRS80) z przedziału: 57 ≥ \u03C6 ≥ 47, 26 ≥ \u03BB ≥ 12.')

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Program do wyznaczania zniekształceń odwzorowawczych")
    root.iconbitmap('icon.ico')
    root.geometry("525x250+500+250")
    root.resizable(width=False, height=False)

    global dataList
    dataList = []

    optionList_CS = ['PL-LAEA', 'PL-LCC', 'PL-UTM', 'PL-1992', 'PL-2000']
    variable_CS = tk.StringVar(root)
    variable_CS.set(optionList_CS[3])

    photo3 = tk.PhotoImage(file = 'img3.gif')
    label5 = tk.Label(image=photo3)
    label5.place(relx=0.70, rely=0.05)

    opt = tk.OptionMenu(root, variable_CS, *optionList_CS, command=zones)
    opt.config(width=8)
    opt.place(relx=0.35, rely=0.27, anchor = 'w')

    label1 = tk.Label(text='Wybierz układ współrzędnych')
    label1.place(relx=0.02, rely=0.27, anchor = 'w')
    label2 = tk.Label(text='')
    label2.place(relx=0.55, rely=0.27, anchor='w')

    optionList_UTM = ['33N', '34N', '35N']
    variable_UTM_zones = tk.StringVar(root)

    opt2 = tk.OptionMenu(root, variable_UTM_zones, *optionList_UTM)

    optionList_2000 = ['5', '6', '7', '8']
    variable_2000_zones = tk.StringVar(root)

    opt3 = tk.OptionMenu(root, variable_2000_zones, *optionList_2000)

    label3 = tk.Label(text='Wskaż lokalizację pliku tekstowego z danymi')
    label3.place(relx=0.02, rely=0.12, anchor='w')
    photo = tk.PhotoImage(file = 'img2.gif')
    open_button = tk.Button(root, image=photo, width=35, height=14, command = openFile, bg='yellow')
    open_button.place(relx=0.51, rely=0.12, anchor='w')

    openPath = tk.StringVar()
    openPath.set('brak')

    label4 = tk.Label(text='Wskaż lokalizację zapisu otrzymanych wyników')
    label4.place(relx=0.02, rely=0.42, anchor='w')
    photo2 = tk.PhotoImage(file = 'img1.gif')
    save_button = tk.Button(root, image=photo2, width=35, height=14, command = saveFile, bg='yellow')
    save_button.place(relx=0.54, rely=0.42, anchor='w')

    savePath = tk.StringVar()
    savePath.set('brak')

    action_button = tk.Button(root, text = 'Wykonaj obliczenia', command = calculations)
    action_button.place(relx=0.25, rely=0.68, height=60, width=250, anchor = 'w')

    status_label = tk.Label(root, text = u'Program oblicza zniekształcenia dla współrzędnych geodezyjnych (elipsoida GRS80) z przedziału: 57 ≥ \u03C6 ≥ 47, 26 ≥ \u03BB ≥ 12.', bd=1, relief=tk.SUNKEN, anchor=tk.CENTER, font = ("Tahoma", 7))
    status_label.pack(fill=tk.X, side=tk.BOTTOM, ipady=2)

    open_button.bind("<Enter>", open_button_hover)
    open_button.bind("<Leave>", open_button_hover_leave)

    save_button.bind("<Enter>", save_button_hover)
    save_button.bind("<Leave>", save_button_hover_leave)

    root.mainloop()