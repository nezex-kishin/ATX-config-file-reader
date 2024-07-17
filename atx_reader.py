from tkinter import *
import psycopg2
import os

path = r'C:\Users\Denis\Documents\AutoGraphGSMConf 5.0\CONF'
passz = r'C:\Users\Denis\Documents\AutoGraphGSMConf 5.0\PASS'
bb = 1
with open('config.txt', 'r', encoding = 'UTF-8') as config:
    host = f'{config.readline().split(sep='=')[1][:-1]}'
    user = f'{config.readline().split(sep='=')[1][:-1]}'
    password = f'{config.readline().split(sep='=')[1][:-1]}'
    database = f'{config.readline().split(sep='=')[1]}'

try:
    root = Tk()
    root.geometry('500x300')
    root.resizable(width=FALSE,height=FALSE)
    root.title('Считыватель ATX файлов')
    root['bg'] = 'black'
    root.iconbitmap(default='3592841-cog-gear-general-machine-office-setting-settings_107765.ico')

    connection = psycopg2.connect(
        host=f'{host}',
        user=f'{user}',
        password=f'{password}',
        database=f'{database}'
    )
    connection.autocommit = True

#BACKEND
    def createtable():
        with connection.cursor() as cursor:
            cursor.execute(
            """CREATE TABLE atx(
            id serial,
            proshivka varchar(50),
            kod varchar(50),
            password varchar(50),
            masterpassword varchar(50),
            imei varchar(50),
            server varchar(50));        
            """)
        with connection.cursor() as cursor:
            cursor.execute(
            """CREATE TABLE shadow(
            id serial,
            proshivka varchar(50),
            kod varchar(50),
            password varchar(50),
            masterpassword varchar(50),
            imei varchar(50),
            server varchar(50));        
            """)
    def droptable():
        with connection.cursor() as cursor:
            cursor.execute(
                """
                DROP TABLE atx,shadow;
                """
            )

#FRONTEND
    def opennewwindow():
        newwindow = Toplevel(root)
        newwindow.title('Конфигурации')
        newwindow.geometry('500x500')
        newwindow.resizable(width=FALSE,height=FALSE)
        Label(newwindow,
              text = 'Все доступные конфигурации',
              font = 'Arial 15'
              ).pack()
        devices_listbox = Listbox(newwindow, font = 'Arial 13', selectmode=MULTIPLE)
        for i in range(len(os.listdir(path))):
            devices_listbox.insert(i, os.listdir(path)[i])
        devices_listbox.pack()
        #Вывод выбранных приборов
        def add_selected(event):
            selected_device = devices_listbox.curselection()
            list_devices = ",".join([devices_listbox.get(i) for i in selected_device])
            msg = f'Вы выбрали: {list_devices}'
            selection_label['text'] = msg
        def inputinfo():
            selected_device = devices_listbox.curselection()
            for i in selected_device:
                pribor = os.listdir(path)[i]
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""
                            INSERT INTO atx(kod)
                            SELECT '{pribor}'
                            WHERE NOT EXISTS(
                            SELECT kod FROM atx WHERE kod = '{pribor}'
                            );
                            """)
                pathh = rf'C:\Users\Denis\Documents\AutoGraphGSMConf 5.0\CONF\{pribor}'
                files = os.listdir(pathh)
                if files:
                    files = [os.path.join(pathh, file) for file in files]
                    files = [file for file in files if os.path.isfile(file)]
                q = max(files, key=os.path.getctime)
                file = open(f'{q}')
                a = file.readlines()
                i = 0
                while i != len(a):
                    b = a[i]
                    if b.startswith('AT') == True:
                        inf = b[:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                    UPDATE atx
                                        SET proshivka = '{inf}'
                                        WHERE kod = '{pribor}';
                                    """
                            )
                        i += 1
                    elif b.startswith('PASSWORD') == True:
                        b = b.split(sep='=')
                        inf = b[1][:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                    UPDATE atx
                                        SET password = '{inf}'
                                        WHERE kod = '{pribor}';
                                    """
                            )
                        i += 1
                    elif b.startswith('MODEM1IMEI') == True:
                        b = b.split(sep='=')
                        inf = b[1][:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                    UPDATE atx
                                        SET imei = '{inf}'
                                        WHERE kod = '{pribor}';
                                    """
                            )
                        i += 1
                    elif b.startswith('SRV1MAINDOMAIN') == True:
                        b = b.split(sep='=')
                        inf = b[1][:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                    UPDATE atx
                                        SET server = '{inf}'
                                        WHERE kod = '{pribor}';
                                    """
                            )
                        i += 1
                    else:
                        i += 1
                passsz = rf'C:\Users\Denis\Documents\AutoGraphGSMConf 5.0\PASS\{pribor}'
                if os.path.exists(passsz):
                    filess = os.listdir(passsz)
                    if filess:
                        filess = [os.path.join(passsz, file) for file in filess]
                        filess = [file for file in filess if os.path.isfile(file)]
                    q = max(filess, key=os.path.getctime)
                    file = open(f'{q}')
                    a = file.readline()
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"""
                            UPDATE atx
                                SET masterpassword = '{a}'
                                WHERE kod = '{pribor}';
                            """
                        )
                else:
                    continue
        def updateinfo():
            selected_device = devices_listbox.curselection()
            for i in selected_device:
                pribor = os.listdir(path)[i]
                pathh = rf'C:\Users\Denis\Documents\AutoGraphGSMConf 5.0\CONF\{pribor}'
                files = os.listdir(pathh)
                if files:
                    files = [os.path.join(pathh, file) for file in files]
                    files = [file for file in files if os.path.isfile(file)]
                q = max(files, key=os.path.getctime)
                file = open(f'{q}')
                a = file.readlines()
                i = 0
                while i != len(a):
                    b = a[i]
                    if b.startswith('AT') == True:
                        inf = b[:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                INSERT INTO shadow SELECT * FROM atx WHERE kod = '{pribor}' AND proshivka <> '{inf}';
                                """
                            )
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                UPDATE atx SET proshivka = '{inf}' WHERE NOT EXISTS (SELECT kod FROM atx WHERE kod = '{pribor}' AND proshivka = '{inf}') AND kod = '{pribor}';
                                """
                            )
                        i += 1
                    elif b.startswith('PASSWORD') == True:
                        b = b.split(sep='=')
                        inf = b[1][:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                INSERT INTO shadow SELECT * FROM atx WHERE kod = '{pribor}' AND password <> '{inf}';
                                """
                            )
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                UPDATE atx SET password = '{inf}' WHERE NOT EXISTS (SELECT kod FROM atx WHERE kod = '{pribor}' AND password = '{inf}') AND kod = '{pribor}';
                                """
                            )
                        i += 1
                    elif b.startswith('MODEM1IMEI') == True:
                        b = b.split(sep='=')
                        inf = b[1][:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                INSERT INTO shadow SELECT * FROM atx WHERE kod = '{pribor}' AND imei <> '{inf}';
                                """
                            )
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                UPDATE atx SET imei = '{inf}' WHERE NOT EXISTS (SELECT kod FROM atx WHERE kod = '{pribor}' AND imei = '{inf}') AND kod = '{pribor}';
                                """
                            )
                        i += 1
                    elif b.startswith('SRV1MAINDOMAIN') == True:
                        b = b.split(sep='=')
                        inf = b[1][:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                INSERT INTO shadow SELECT * FROM atx WHERE kod = '{pribor}' AND server <> '{inf}';
                                """
                                )
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                UPDATE atx SET server = '{inf}' WHERE NOT EXISTS (SELECT kod FROM atx WHERE kod = '{pribor}' AND server = '{inf}') AND kod = '{pribor}';
                                """
                                )
                        i += 1
                    else:
                        i += 1
                passsz = rf'C:\Users\Denis\Documents\AutoGraphGSMConf 5.0\PASS\{pribor}'
                if os.path.exists(passsz):
                    filess = os.listdir(passsz)
                    if filess:
                        filess = [os.path.join(passsz, file) for file in filess]
                        filess = [file for file in filess if os.path.isfile(file)]
                    q = max(filess, key=os.path.getctime)
                    file = open(f'{q}')
                    a = file.readline()
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"""
                            INSERT INTO shadow SELECT * FROM atx WHERE kod = '{pribor}' AND (masterpassword <> '{a}' OR masterpassword IS NULL);
                            """
                        )
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"""
                            UPDATE atx SET masterpassword = '{a}' WHERE NOT EXISTS (SELECT kod FROM atx WHERE kod = '{pribor}' AND masterpassword = '{a}') AND kod = '{pribor}';
                            """
                        )
                else:
                    continue
        #Добавление ВСЕХ доступных приборов
        def inputALLinfo():
            for i in range(len(os.listdir(path))):
                pribor = os.listdir(path)[i]
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""
                            INSERT INTO atx(kod)
                            SELECT '{pribor}'
                            WHERE NOT EXISTS(
                            SELECT kod FROM atx WHERE kod = '{pribor}'
                            );
                            """)
                pathh = rf'C:\Users\Denis\Documents\AutoGraphGSMConf 5.0\CONF\{pribor}'
                files = os.listdir(pathh)
                if files:
                    files = [os.path.join(pathh, file) for file in files]
                    files = [file for file in files if os.path.isfile(file)]
                q = max(files, key=os.path.getctime)
                file = open(f'{q}')
                a = file.readlines()
                i = 0
                while i != len(a):
                    b = a[i]
                    if b.startswith('AT') == True:
                        inf = b[:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                    UPDATE atx
                                        SET proshivka = '{inf}'
                                        WHERE kod = '{pribor}';
                                    """
                            )
                        i += 1
                    elif b.startswith('PASSWORD') == True:
                        b = b.split(sep='=')
                        inf = b[1][:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                    UPDATE atx
                                        SET password = '{inf}'
                                        WHERE kod = '{pribor}';
                                    """
                            )
                        i += 1
                    elif b.startswith('MODEM1IMEI') == True:
                        b = b.split(sep='=')
                        inf = b[1][:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                    UPDATE atx
                                        SET imei = '{inf}'
                                        WHERE kod = '{pribor}';
                                    """
                            )
                        i += 1
                    elif b.startswith('SRV1MAINDOMAIN') == True:
                        b = b.split(sep='=')
                        inf = b[1][:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                    UPDATE atx
                                        SET server = '{inf}'
                                        WHERE kod = '{pribor}';
                                    """
                            )
                        i += 1
                    else:
                        i += 1
                passsz = rf'C:\Users\Denis\Documents\AutoGraphGSMConf 5.0\PASS\{pribor}'
                if os.path.exists(passsz):
                    filess = os.listdir(passsz)
                    if filess:
                        filess = [os.path.join(passsz, file) for file in filess]
                        filess = [file for file in filess if os.path.isfile(file)]
                    q = max(filess, key=os.path.getctime)
                    file = open(f'{q}')
                    a = file.readline()
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"""
                            UPDATE atx
                                SET masterpassword = '{a}'
                                WHERE kod = '{pribor}';
                            """
                        )
                else:
                    continue
        #Обновление ВСЕХ доступных приборов
        def updateALLinfo():
            for i in range(len(os.listdir(path))):
                pribor = os.listdir(path)[i]
                pathh = rf'C:\Users\Denis\Documents\AutoGraphGSMConf 5.0\CONF\{pribor}'
                files = os.listdir(pathh)
                if files:
                    files = [os.path.join(pathh, file) for file in files]
                    files = [file for file in files if os.path.isfile(file)]
                q = max(files, key=os.path.getctime)
                file = open(f'{q}')
                a = file.readlines()
                i = 0
                while i != len(a):
                    b = a[i]
                    if b.startswith('AT') == True:
                        inf = b[:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                INSERT INTO shadow SELECT * FROM atx WHERE kod = '{pribor}' AND proshivka <> '{inf}';
                                """
                            )
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                UPDATE atx SET proshivka = '{inf}' WHERE NOT EXISTS (SELECT kod FROM atx WHERE kod = '{pribor}' AND proshivka = '{inf}') AND kod = '{pribor}';
                                """
                            )
                        i += 1
                    elif b.startswith('PASSWORD') == True:
                        b = b.split(sep='=')
                        inf = b[1][:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                INSERT INTO shadow SELECT * FROM atx WHERE kod = '{pribor}' AND password <> '{inf}';
                                """
                            )
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                UPDATE atx SET password = '{inf}' WHERE NOT EXISTS (SELECT kod FROM atx WHERE kod = '{pribor}' AND password = '{inf}') AND kod = '{pribor}';
                                """
                            )
                        i += 1
                    elif b.startswith('MODEM1IMEI') == True:
                        b = b.split(sep='=')
                        inf = b[1][:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                INSERT INTO shadow SELECT * FROM atx WHERE kod = '{pribor}' AND imei <> '{inf}';
                                """
                            )
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                UPDATE atx SET imei = '{inf}' WHERE NOT EXISTS (SELECT kod FROM atx WHERE kod = '{pribor}' AND imei = '{inf}') AND kod = '{pribor}';
                                """
                            )
                        i += 1
                    elif b.startswith('SRV1MAINDOMAIN') == True:
                        b = b.split(sep='=')
                        inf = b[1][:-2]
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                INSERT INTO shadow SELECT * FROM atx WHERE kod = '{pribor}' AND server <> '{inf}';
                                """
                            )
                        with connection.cursor() as cursor:
                            cursor.execute(
                                f"""
                                UPDATE atx SET server = '{inf}' WHERE NOT EXISTS (SELECT kod FROM atx WHERE kod = '{pribor}' AND server = '{inf}') AND kod = '{pribor}';
                                """
                            )
                        i += 1
                    else:
                        i += 1
                passsz = rf'C:\Users\Denis\Documents\AutoGraphGSMConf 5.0\PASS\{pribor}'
                if os.path.exists(passsz):
                    filess = os.listdir(passsz)
                    if filess:
                        filess = [os.path.join(passsz, file) for file in filess]
                        filess = [file for file in filess if os.path.isfile(file)]
                    q = max(filess, key=os.path.getctime)
                    file = open(f'{q}')
                    a = file.readline()
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"""
                            INSERT INTO shadow SELECT * FROM atx WHERE kod = '{pribor}' AND (masterpassword <> '{a}' OR masterpassword IS NULL);
                            """
                        )
                    with connection.cursor() as cursor:
                        cursor.execute(
                            f"""
                            UPDATE atx SET masterpassword = '{a}' WHERE NOT EXISTS (SELECT kod FROM atx WHERE kod = '{pribor}' AND masterpassword = '{a}') AND kod = '{pribor}';
                            """
                        )
                else:
                    continue


        selection_label = Label(newwindow,
                                text = 'Вы выбрали: ',
                                font='Arial 13')
        selection_label.pack(anchor=S)
        devices_listbox.bind("<<ListboxSelect>>", add_selected)
        #Добавление выбранных приборов в таблицу
        add_devices = Button(newwindow,
                             text = 'Добавить в таблицу',
                             font = 'Arial 15',
                             command=inputinfo)
        add_devices.pack(anchor = S)
        #Обновление выбранных приборов в таблице
        update_devices = Button(newwindow,
                                text='Обновить в таблице',
                                font='Arial 15',
                                command=updateinfo)
        update_devices.pack(anchor=S)

        add_ALL_devices = Button(newwindow,
                                 text = 'Добавить все приборы в таблицу',
                                 font = 'Arial 15',
                                 command=inputALLinfo)
        update_All_devices = Button(newwindow,
                                    text = 'Обновить все приборы в таблице',
                                    font = 'Arial 15',
                                    command=updateALLinfo)
        add_ALL_devices.pack(anchor=S)
        update_All_devices.pack(anchor=S)



#MAIN WINDOW
    createt = Button(root,
                 text = 'Создание таблицы',
                 command = createtable,
                 font = 'Arial 15'
                 )
    dropt = Button(root,
                   text = 'Удаление таблицы',
                   command = droptable,
                   font = 'Arial 15'
                   )
    insertinfo = Button(root,
                        text = 'Найти конфигурации',
                        command=opennewwindow,
                        font = 'Arial 15'
                        )

    createt.place(x=150, y=50)
    dropt.place(x=150, y=100)
    insertinfo.place(x=144, y=150)
    root.mainloop()


except Exception as _ex:
    print("[INFO] Error while working with PostgreSQL", _ex)