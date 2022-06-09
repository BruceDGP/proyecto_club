import psycopg2
import tkinter as tk
import tkinter.font as font
from tkinter import messagebox
from tkcalendar import DateEntry
import datetime
import re

class app(tk.Tk):
    def __init__(self):
        super().__init__()

        #Configuracion de la ventana
        self.config(bg="#070A2F")
        alto = self.winfo_screenheight() #Para determinar el alto del monitor
        ancho = self.winfo_screenwidth() #Para determinar el ancho del monitor
        self.geometry(f'600x375+{int(ancho/2)-300}+{int(alto/2)-300}')
        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.end_fullscreen)
        #contenedor de los framse que se van a mostrar
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.user_save = None
        #Diccionario con los framse a mostrar
        self.frames = {}
        for f in (main_menu, inicio, registro, iniciado, registrado):
            name = f.__name__
            frame = f(self.container,self)
            self.frames[name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show("main_menu")

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.attributes("-fullscreen", False)
        return "break"

    def show(self, name): #Para cambiar de ventanas
        frame = self.frames[name]
        self.title(frame.titulo)
        frame.tkraise()

    #Envio de registro
    def reg(self, nombre, apellido, date, cedula, user, correo, contraseña, nombre_box, apellido_box, cedula_box, user_box, correo_box, contraseña_box):
        conexion = psycopg2.connect(host="192.168.100.19", database="authenticator", user="postgres", password="admin")
        cur = conexion.cursor()

        validacion_datos = {
            "nombre": False,
            "apellido": False,
            "date": False,
            "cedula": False,
            "user": False,
            "correo": False,
            "contraseña": False
        }
        #validar nombre
        regex = r'^[a-zA-Z]+$'
        if len(nombre) > 0 and re.fullmatch(regex, nombre):
            nombre_box.config(highlightbackground = "#0CFF00", highlightcolor= "#0CFF00", bg="#D6FFD4")
            validacion_datos["nombre"] = True
        else:
            nombre_box.config(highlightbackground = "#BE0000", highlightcolor= "#BE0000", bg="#FF8F8F")
            return tk.messagebox.showinfo(title="Datos incorrectos", message="Ingresa un nombre válido")
        #validar apellido
        if len(apellido) > 0 and re.fullmatch(regex, apellido):
            apellido_box.config(highlightbackground = "#0CFF00", highlightcolor= "#0CFF00", bg="#D6FFD4")
            validacion_datos["apellido"] = True
        else:
            apellido_box.config(highlightbackground = "#BE0000", highlightcolor= "#BE0000", bg="#FF8F8F")
            return tk.messagebox.showinfo(title="Datos incorrectos", message="Ingresa un apellido válido")
        #validar fecha
        today = datetime.datetime.now()
        if date > datetime.date(year=today.year, month=today.month, day=today.day):
            return tk.messagebox.showinfo(title="Datos incorrectos", message="Ingresa una fecha valida")
        else:
            validacion_datos["date"] = True
        #validar cedula
        cur.execute("SELECT code FROM usuarios")
        code_list = []
        for code in cur.fetchall():
            code_list.append(code[0])
        try:
            if cedula in code_list:
                cedula_box.config(highlightbackground = "#BE0000", highlightcolor= "#BE0000", bg="#FF8F8F")
                return tk.messagebox.showinfo(title="Datos incorrectos", message="Número de cédula ya registrado")
            if len(cedula) <= 0:
                cedula_box.config(highlightbackground = "#BE0000", highlightcolor= "#BE0000", bg="#FF8F8F")
                return tk.messagebox.showinfo(title="Datos incorrectos", message="Ingresa un número de cédula válido")
            sumatoria_cedula = 0
            for i in range(0,9):
                valor = int(cedula[i])
                if i%2 == 0:
                    valor *= 2
                    if valor >= 10:
                        valor -= 9
                sumatoria_cedula += valor
            while sumatoria_cedula >= 0:
                sumatoria_cedula -= 10
            sumatoria_cedula *= -1
            if sumatoria_cedula == 10:
                sumatoria_cedula = 0
            if sumatoria_cedula == int(cedula[-1]) and int(cedula[0]) <= 2 and int(cedula[0]) >= 0 and int(cedula[2]) < 6 and len(cedula) == 10:
                cedula_box.config(highlightbackground = "#0CFF00", highlightcolor= "#0CFF00", bg="#D6FFD4")
                validacion_datos["cedula"] = True
            else:
                cedula_box.config(highlightbackground = "#BE0000", highlightcolor= "#BE0000", bg="#FF8F8F")
                return tk.messagebox.showinfo(title="Datos incorrectos", message="Ingresa un número de cédula válido")
        except:
            cedula_box.config(highlightbackground = "#BE0000", highlightcolor= "#BE0000", bg="#FF8F8F")
            return tk.messagebox.showinfo(title="Datos incorrectos", message="Ingresa un número de cédula válido")
        #validar correo
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b' #Expresion regular para validar email
        if(re.fullmatch(regex, correo)):
            correo_box.config(highlightbackground = "#0CFF00", highlightcolor= "#0CFF00", bg="#D6FFD4")
            validacion_datos["correo"] = True
        else:
            correo_box.config(highlightbackground = "#BE0000", highlightcolor= "#BE0000", bg="#FF8F8F")
            return tk.messagebox.showinfo(title="Datos incorrectos", message="Ingresa un correo válido")
        #validar usuarios
        cur.execute("SELECT username FROM usuarios")
        users_list = []
        for usuario in cur.fetchall():
            users_list.append(usuario[0])
        if user in users_list:
            user_box.config(highlightbackground = "#BE0000", highlightcolor= "#BE0000", bg="#FF8F8F")
            return tk.messagebox.showinfo(title="Datos incorrectos", message="El usuario escogido no está disponible")
        elif len(user) == 0:
            user_box.config(highlightbackground = "#BE0000", highlightcolor= "#BE0000", bg="#FF8F8F")
            return tk.messagebox.showinfo(title="Datos incorrectos", message="Ingresa un usuario válido")
        else:
            user_box.config(highlightbackground = "#0CFF00", highlightcolor= "#0CFF00", bg="#D6FFD4")
            validacion_datos["user"] = True
        #validar contraseña
        validacion_contraseña = {
            "largo": 0,
            "minusculas": 0,
            "mayusculas": 0,
            "numeros": 0,
            "car_esp": 0
        }
        if len(contraseña) >= 8:
            validacion_contraseña["largo"] = len(contraseña)
        for char in contraseña:
            if char.isupper():
                validacion_contraseña["mayusculas"] += 1
            elif char.islower():
                validacion_contraseña["minusculas"] += 1
            elif char.isnumeric():
                validacion_contraseña["numeros"] += 1
            else:
                validacion_contraseña["car_esp"] += 1
        if 0 in validacion_contraseña.values():
            mensaje = """
                \n\nLa contraseña debe cumplir con las siguientes condiciones:
                • Debe tener al menos un largo de 8 caracteres
                • Debe tener al menos una letra MAYUSCULA
                • Debe tener al menos una letra MINUSCULA
                • Debe tener al menos un caracter numérico
                • Debe tener al menos un caracter especial
            """
            contraseña_box.config(highlightbackground = "#BE0000", highlightcolor= "#BE0000", bg="#FF8F8F")
            return tk.messagebox.showinfo(title="Datos incorrectos", message=mensaje)
        else:
            contraseña_box.config(highlightbackground = "#0CFF00", highlightcolor= "#0CFF00", bg="#D6FFD4")
            validacion_datos["contraseña"] = True
        #Si pasa todos los campos
        if False not in validacion_datos.values():
            birthday = f'{date.year}-{date.month}-{date.day}'
            sentencia = f'INSERT INTO usuarios (surename, lastname, email, code, username, password, birthday) VALUES (\'{nombre}\', \'{apellido}\', \'{correo}\', \'{cedula}\', \'{user}\', PGP_SYM_ENCRYPT(\'{contraseña}\', \'AES_KEY\'), \'{birthday}\')'
            cur.execute(sentencia)
            conexion.commit()
            date = str(datetime.datetime.now())
            cur.execute(f'INSERT INTO logs (id, surename, lastname, date, reason) VALUES (\'{id}\', \'{nombre}\', \'{apellido}\', \'{date}\', \'se registro\')')
            conexion.commit()
            conexion.close()

            self.show("registrado")
    #verificacion de inicio de sesion
    def login(self, user, contraseña):
        conexion = psycopg2.connect(host="192.168.100.19", database="authenticator", user="postgres", password="admin")
        cur = conexion.cursor()

        cur.execute("SELECT username, PGP_SYM_DECRYPT(password::bytea, 'AES_KEY') FROM usuarios")
        users = {}
        for username, password in cur.fetchall():
            users[username] = password
        
        if username in users.keys() and contraseña == users[user]:
            cur.execute(f'SELECT id, surename, lastname FROM usuarios WHERE username = \'{user}\'')
            for id, surename, lastname in cur.fetchall():
                lista = [id, surename, lastname]
            today = datetime.datetime.now()

            cur.execute(f'INSERT INTO logs (id, surename, lastname, date, reason) VALUES (\'{id}\', \'{surename}\', \'{lastname}\', \'{str(today)}\', \'inicio sesion\')')
            conexion.commit()
            conexion.close()
            self.user_save = user
            self.show("iniciado")
        else:
            return tk.messagebox.showinfo(title="Datos incorrectos", message="Usuario y/o contraseña inválidos")
    #Frame que se muestra con los datos de los usuarios
    def show_users(self):
        self.attributes("-fullscreen", True)
        users_frame = tk.Frame(self.container)
        users_frame.grid(row=0, column=0, sticky="nsew")
        users_frame.grid_rowconfigure(0, weight=1)
        users_frame.grid_columnconfigure(0, weight=1)
        users_frame.tkraise()

        users_frame.config(bg="#070A2F")
        users_frame.grid_propagate(False)

        canvas = tk.Canvas(users_frame,  bg="#070A2F")
        canvas.grid(row=0, column=0, sticky="news")

        vsb = tk.Scrollbar(users_frame,  orient="vertical", command=canvas.yview)
        vsb.grid(row=0, column=1, sticky='ns')
        canvas.configure(yscrollcommand=vsb.set)

        hsb = tk.Scrollbar(users_frame,  orient="horizontal", command=canvas.xview)
        hsb.grid(row=1, column=0, sticky='ew')
        canvas.configure(xscrollcommand=hsb.set)

        frame_table = tk.Frame(canvas, bg="#070A2F")
        canvas.create_window((0, 0), window=frame_table, anchor='nw')

        conexion = psycopg2.connect(host="192.168.100.19", database="authenticator", user="postgres", password="admin")
        cur = conexion.cursor()
        
        cur.execute("SELECT surename, lastname, username, email, code, password FROM usuarios")

        fuente = font.Font(family="Arial", size=16, weight="bold", slant="italic")
        tk.Label(frame_table, text="LISTA DE USUARIOS REGISTRADOS", bg="#070A2F", fg="white", font=fuente).grid(row=0, column=0, pady=8, columnspan=5, sticky="ew")
        fuente = font.Font(family="Arial", size=10, weight="bold", slant="italic")
        tk.Label(frame_table, text="NOMBRE", bg="#FF8071", font=fuente, borderwidth=2, relief="solid", highlightcolor="black").grid(row=1, column=0, pady=8, sticky="ew")
        tk.Label(frame_table, text="APELLIDO", bg="#FF8071", font=fuente, borderwidth=2, relief="solid", highlightcolor="black").grid(row=1, column=1, pady=8, sticky="ew")
        tk.Label(frame_table, text="CORREO", bg="#FF8071", font=fuente, borderwidth=2, relief="solid", highlightcolor="black").grid(row=1, column=2, pady=8, sticky="ew")
        tk.Label(frame_table, text="CEDULA", bg="#FF8071", font=fuente, borderwidth=2, relief="solid", highlightcolor="black").grid(row=1, column=3, pady=8, sticky="ew")
        tk.Label(frame_table, text="CONTRASEÑA", bg="#FF8071", font=fuente, borderwidth=2, relief="solid", highlightcolor="black").grid(row=1, column=4, pady=8, sticky="ew")

        fuente = font.Font(family="Arial", size=10)
        row_number = 1
        for surename, lastname, username, email, code, password in cur.fetchall():
            row_number += 1
            tk.Label(frame_table, text=surename, bg="#EBB0FF" if self.user_save != username else "#F6FF6B", font=fuente, borderwidth=2, relief="solid", highlightcolor="black").grid(row=row_number, column=0, sticky="ew")
            tk.Label(frame_table, text=lastname, bg="#EBB0FF" if self.user_save != username else "#F6FF6B", font=fuente, borderwidth=2, relief="solid", highlightcolor="black").grid(row=row_number, column=1, sticky="ew")
            tk.Label(frame_table, text=email, bg="#EBB0FF" if self.user_save != username else "#F6FF6B", font=fuente, borderwidth=2, relief="solid", highlightcolor="black").grid(row=row_number, column=2, sticky="ew")
            tk.Label(frame_table, text=code, bg="#EBB0FF" if self.user_save != username else "#F6FF6B", font=fuente, borderwidth=2, relief="solid", highlightcolor="black").grid(row=row_number, column=3, sticky="ew")
            tk.Label(frame_table, text=password, bg="#EBB0FF" if self.user_save != username else "#F6FF6B", font=fuente, borderwidth=2, relief="solid", highlightcolor="black").grid(row=row_number, column=4, sticky="ew")

        frame_table.update_idletasks()

        canvas.config(scrollregion=canvas.bbox("all"))

        tk.Button(users_frame, text="Cerrar sesión", bg="#43FF3A", fg="black" ,height=2, width=15, command=lambda: self.show("main_menu")).grid(row=2, column=0, pady=8, padx=8, sticky="ns")

    #automaticamente fullscreen
    def fs(self):
        self.show("usuarios")

    #crea un txt con los logs
    def log_file(self):
        conexion = psycopg2.connect(host="192.168.100.19", database="authenticator", user="postgres", password="admin")
        cur = conexion.cursor()

        file = open("logs.txt", "w")
        
        cur.execute("SELECT surename, lastname, id, reason, date FROM logs")
        
        for nombre, apellido, id_value, razon, fecha in cur.fetchall():
            lista = [nombre, apellido, id_value, razon, fecha]
            if razon == "inicio sesion":
                texto = f'{nombre} {apellido} con id: {id_value}, {razon}. {fecha}\n'
            else:
                texto = f'{nombre} {apellido}, {razon}. {fecha}\n'
            file.write(texto)
        
        file.close()

        conexion.close()

class main_menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.titulo = "Menú principal"
        self = tk.Frame(self)
        self.pack(side="top",expand=True, fill="both")
        self.config(bg="#070A2F") 
        #Muestra el menu principal
        fuente = font.Font(family="Arial", size=16, weight="bold", slant="italic")
        login = tk.Button(self,text="Iniciar sesión", bg="#43FF3A", fg="black" ,height=2, width=15, command=lambda: controller.show("inicio"))
        login["font"] = fuente
        login.pack(pady=50)
        register = tk.Button(self,text="Registrarse", bg="#20DAFF", fg="black" ,height=1, width=10, command=lambda: controller.show("registro"))
        register["font"] = fuente
        register.pack()
        logs = tk.Button(self, text="Descargar logs", bg="#070A2F", fg="#11FFFB", activebackground="#070A2F", command=lambda: controller.log_file())
        logs.pack(pady=20)

class inicio(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.titulo = "Iniciar sesión"
        self = tk.Frame(self)
        self.pack(side="top", expand=True, fill="both")
        self.config(bg="#070A2F")
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        #Muestra el menu de inisio de sesion
        fuente = font.Font(family="Arial", size=16, weight="bold", slant="italic")
        tk.Label(self, text="Llene sus datos para iniciar", bg="#070A2F", fg="white", font= fuente).grid(row=0, column=0, columnspan=5, pady=5, sticky="nsew")
        fuente = font.Font(family="Arial", size=10, weight="bold", slant="italic")
        tk.Label(self, text="Usuario", bg="#070A2F", fg="white", font= fuente).grid(row=1, column=0, padx=8, pady=8)
        user = tk.StringVar()
        tk.Entry(self, textvariable=user).grid(row=1, column=1, padx=8, pady=8, sticky="ew", columnspan=4)
        tk.Label(self, text="Contraseña", bg="#070A2F", fg="white", font= fuente).grid(row=2, column=0, padx=8, pady=8)
        contraseña = tk.StringVar()
        tk.Entry(self, show="*", textvariable=contraseña).grid(row=2, column=1, padx=8, pady=8, sticky="ew", columnspan=4)

        back = tk.Button(self, text="Volver", bg="#FF9338",height=1, width=10, command= lambda: controller.show("main_menu"))
        back.grid(row=6, column=3, padx=8, pady=8)
        submit = tk.Button(self, text="Enviar", bg="#19B61E",height=1, width=10, command= lambda: controller.login(user.get(), contraseña.get()))
        submit.grid(row=6, column=4, padx=8, pady=8)

class registro(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.titulo = "Registro"
        self = tk.Frame(self)
        self.pack(side="top", expand=True, fill="both")
        self.config(bg="#070A2F")
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        #Muestra el menu de registro de usuarios
        fuente = font.Font(family="Arial", size=16, weight="bold", slant="italic")
        tk.Label(self, text="Llene los datos siguientes", bg="#070A2F", fg="white", font= fuente).grid(row=0, column=0, columnspan=5, pady=5, sticky="nsew")
        fuente = font.Font(family="Arial", size=10, weight="bold", slant="italic")
        tk.Label(self, text="Nombre", bg="#070A2F", fg="white", font= fuente).grid(row=1, column=0, padx=8, pady=8)
        nombre = tk.StringVar()
        nombre_box = tk.Entry(self, textvariable=nombre, highlightthickness=2)
        nombre_box.grid(row=1, column=1, padx=8, pady=8, sticky="ew", columnspan=4)

        tk.Label(self, text="Apellido", bg="#070A2F", fg="white", font= fuente).grid(row=2, column=0, padx=8, pady=8)
        apellido = tk.StringVar()
        apellido_box = tk.Entry(self, textvariable=apellido, highlightthickness=2)
        apellido_box.grid(row=2, column=1, padx=8, pady=8, sticky="ew", columnspan=4)

        tk.Label(self, text="Fecha de nacimiento", bg="#070A2F", fg="white", font= fuente).grid(row=3, column=0, padx=8, pady=8)
        cal = DateEntry(self, year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day, highlightthickness=2,
                 selectbackground='gray80',
                 selectforeground='black',
                 normalbackground='gray80',
                 normalforeground='black',
                 background='#FF7261',
                 foreground='black',
                 bordercolor='gray90',
                 othermonthforeground='gray50',
                 othermonthbackground='white',
                 othermonthweforeground='gray50',
                 othermonthwebackground='white',
                 weekendbackground='gray80',
                 weekendforeground='black',
                 headersbackground='white',
                 headersforeground='gray70')
        cal.grid(row=3, column=1, pady=8, padx=8, columnspan=3, sticky="ew")

        tk.Label(self, text="Cédula", bg="#070A2F", fg="white", font= fuente).grid(row=4, column=0, padx=8, pady=8)
        cedula = tk.StringVar()
        cedula_box = tk.Entry(self, textvariable=cedula, highlightthickness=2)
        cedula_box.grid(row=4, column=1, padx=8, pady=8, sticky="ew", columnspan=4)

        tk.Label(self, text="Correo", bg="#070A2F", fg="white", font= fuente).grid(row=5, column=0, padx=8, pady=8)
        correo = tk.StringVar()
        correo_box = tk.Entry(self, textvariable=correo, highlightthickness=2)
        correo_box.grid(row=5, column=1, padx=8, pady=8, sticky="ew", columnspan=4)

        tk.Label(self, text="Usuario", bg="#070A2F", fg="white", font= fuente).grid(row=6, column=0, padx=8, pady=8)
        user = tk.StringVar()
        user_box = tk.Entry(self, textvariable=user, highlightthickness=2)
        user_box.grid(row=6, column=1, padx=8, pady=8, sticky="ew", columnspan=4)

        tk.Label(self, text="Contraseña", bg="#070A2F", fg="white", font= fuente).grid(row=7, column=0, padx=8, pady=8)
        contraseña = tk.StringVar()
        contraseña_box = tk.Entry(self, show="*", textvariable=contraseña, highlightthickness=2)
        contraseña_box.grid(row=7, column=1, padx=8, pady=8, sticky="ew", columnspan=4)

        back = tk.Button(self, text="Volver", bg="#FF9338",height=1, width=10, command=lambda: controller.show("main_menu"))
        back.grid(row=8, column=3, padx=8, pady=8)
        submit = tk.Button(self, text="Enviar", bg="#FF9338",height=1, width=10, command=lambda: controller.reg(nombre.get(), apellido.get(), cal.get_date(), cedula.get(), user.get(), correo.get(), contraseña.get(), nombre_box, apellido_box, cedula_box, user_box, correo_box, contraseña_box))
        submit.grid(row=8, column=4, padx=8, pady=8)

class registrado(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.titulo = "Registrado"
        self = tk.Frame(self)
        self.pack(side="top", expand=True, fill="both")
        self.config(bg="#070A2F")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        fuente = font.Font(family="Arial", size=16, weight="bold", slant="italic")
        tk.Label(self, text="Su registro fue enviado con éxito !!", bg="#070A2F", fg="white", font= fuente).grid(row=0, column=0, pady=5, sticky="ew")
        tk.Button(self,text="Iniciar sesión", bg="#43FF3A", fg="black" ,height=2, width=15, command=lambda: controller.show("inicio")).grid(row=1, column=0, pady=8, padx=8, sticky="ns")

class iniciado(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.titulo = "Inicio exitoso"
        self = tk.Frame(self)
        self.pack(side="top", expand=True, fill="both")
        self.config(bg="#070A2F")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_propagate(False)

        fuente = font.Font(family="Arial", size=24, weight="bold", slant="italic")
        tk.Label(self, text="Inicio exitoso !!", font=fuente, bg="#070A2F", fg="white").grid(row=0, column=0, sticky="nsew")
        
        continuar = tk.Button(self, text="Continuar", bg="#FF9338", command=lambda: controller.show_users()).grid(row=1, column=0, pady=25)

autenticador = app()
autenticador.mainloop()