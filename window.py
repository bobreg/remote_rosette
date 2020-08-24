import tkinter
import udp_socket
import time


class Win:
    def __init__(self, my_ip='127.0.0.5', ip_rosette='2.2.3.3'):

        self.sock = udp_socket.udp()
        self.my_ip = my_ip
        self.ip_rosette = ip_rosette
        self.win_main = tkinter.Tk()
        self.win_main.title('Умная розетка!')
        self.win_main.geometry('240x480')
        self.win_main.resizable(False, False)

        self.win_main.protocol('WM_DELETE_WINDOW', self.stop_program)

        self.label1 = tkinter.Label(self.win_main, text='Кнопку выбери, что хочешь нажать.\n')
        self.label1.grid(row=0, column=0, columnspan=3, padx=3, pady=3)
        self.label2 = tkinter.Label(self.win_main, text='service messages...\n', width=30, height=3,
                                    anchor='w', relief='groove', bg='OliveDrab2')
        self.label2.grid(row=11, column=0, columnspan=3, sticky='w', padx=3, pady=3)
        self.label3 = tkinter.Label(self.win_main, text='Введите имя сети:')
        self.label3.grid(row=6, column=0, columnspan=3, sticky='w', padx=3, pady=3)
        self.label4 = tkinter.Label(self.win_main, text='Введите пароль сети:')
        self.label4.grid(row=7, column=0, columnspan=3, sticky='w', padx=3, pady=3)
        self.label5 = tkinter.Label(self.win_main, text='Вве-те IP устройства:')
        self.label5.grid(row=8, column=0, columnspan=3, sticky='w', padx=3, pady=3)

        self.button1 = tkinter.Button(self.win_main, text='Отправить', command=self.send_command, width=12, height=7,
                                      bg='forest green')
        self.button1.grid(row=1, column=0, rowspan=4, sticky='w', padx=3, pady=3)
        self.button2 = tkinter.Button(self.win_main, text='Выйти', command=self.stop_program, width=12, height=5,
                                      bg='coral1')
        self.button2.grid(row=9, column=0, sticky='w', padx=3, pady=3)
        self.button3 = tkinter.Button(self.win_main, text='Поиск розетки', command=self.find_rosette, width=12,
                                      height=5, bg='MistyRose2')
        self.button3.grid(row=9, column=1, sticky='w', padx=3, pady=3)
        self.button4 = tkinter.Button(self.win_main, text='справка', command=self.help_window, bg='snow2')
        self.button4.grid(row=12, column=0, sticky='w', padx=3, pady=30)

        self.var = tkinter.StringVar()
        self.r_button1 = tkinter.Radiobutton(self.win_main, text='Пинг', variable=self.var, value='ping')
        self.r_button2 = tkinter.Radiobutton(self.win_main, text='Включить', variable=self.var, value='on')
        self.r_button3 = tkinter.Radiobutton(self.win_main, text='Выключить', variable=self.var, value='off')
        self.r_button4 = tkinter.Radiobutton(self.win_main, text='Подключится', variable=self.var, value='new')

        self.r_button1.grid(row=1, column=1, sticky='w', padx=3, pady=3)
        self.r_button2.grid(row=2, column=1, sticky='w', padx=3, pady=3)
        self.r_button3.grid(row=3, column=1, sticky='w', padx=3, pady=3)
        self.r_button4.grid(row=4, column=1, sticky='w', padx=3, pady=3)

        self.text1 = tkinter.Entry(self.win_main, width=15)
        self.text1.insert(0, 'ssid')
        self.text1.grid(row=6, column=1, sticky='w', padx=10, pady=3)
        self.text2 = tkinter.Entry(self.win_main, width=15)
        self.text2.insert(0, 'password')
        self.text2.grid(row=7, column=1, sticky='w', padx=30, pady=3)
        self.text3 = tkinter.Entry(self.win_main, width=15)
        # self.text3.insert(0, '192.168.0.1')  # эта строка для запуска приложения из android
        self.text3.insert(0, self.my_ip)  # эта строка для запуска приложения из android
        # self.text3.insert(0, self.sock.my_ip)  # эта строка для запуска приложения из windows
        if self.ip_rosette == '2.2.3.3':
            self.label2['text'] = 'Произведите поиск розетки'
        else:
            self.label2['text'] = 'Розетка была найдена по адресу:\n' + self.ip_rosette
            self.sock.ip = self.ip_rosette
        self.text3.grid(row=8, column=1, sticky='w', padx=30, pady=3)

        self.win_main.mainloop()

    def send_command(self):
        if self.var.get() == 'new':
            ssid = 'ssid:' + self.text1.get()
            self.sock.send_comm(ssid)
            time.sleep(0.3)
            password = 'pass:' + self.text2.get()
            self.sock.send_comm(password)
        else:
            self.sock.send_comm(self.var.get())
            time.sleep(0.3)
            # print(self.sock.data)
            if self.sock.data == b'Relay ON!':
                self.label2['text'] = 'Розетка включена'
            elif self.sock.data == b'Relay OFF!':
                self.label2['text'] = 'Розетка выключена'
            elif self.sock.data == b'ping!':
                self.label2['text'] = 'Есть соединение с розеткой'
            elif self.sock.data == b'':
                self.label2['text'] = 'Нет соединения с розеткой.\n' \
                                      'Проверьте сетевые соединения.\n' \
                                      'Выполните поиск розетки повторно.'
            self.sock.data = b''

    def find_rosette(self):
        flag = False
        flag = self.sock.find_rosette(self.text3.get())
        if flag is True:
            self.label2['text'] = 'Розетка найдена по адресу\n' + self.sock.ip
            with open('adress.txt', 'a') as ip_file:
                ip_file.write(self.sock.ip)
        else:
            self.label2['text'] = 'Розетка не найдена\nпопробуйте поискать ещё'
            with open('adress.txt', 'a') as ip_file:
                ip_file.write('2.2.3.3')

    def stop_program(self):
        self.sock.flag_thread = False
        self.sock.udp_s.close()
        self.win_main.destroy()
        exit()

    def help_window(self):
        text = '''
        Управление wifi - розеткой через локальную
        сеть осуществляется следующим способом
        
        1. Если розетка никогда не использовалась
        в местной сети, то розетка создаст свою 
        wifi сеть "setup_rosette".
        1.1. Необходимо с телефона или 
             компьютера подключится к этой 
             сети.
        1.2. В данной программе нажать кнопку 
             "Поиск розетки"
        1.3. Через несколько секунд в окошке 
             "service messages" должна 
             появится надпись "Розетка найдена 
             по адресу плюс IP розетки".
        1.4. После этого нужно: ввести в поле 
             "ssid" имя местной wifi сети,
             в поле "password" пароль от 
             местной wifi сети, выбрать пункт 
             "Подключиться" и нажать кнопку 
             "Отправить".
        1.5  После этого wifi сеть 
             "setup_rosette" исчезнет и розетка 
             подключится к местной wifi сети.
        2. При запуске программы неоходимо каждый 
        раз нажимать кнопку "Поиск розетки".
        3. В дальнейшем при отключении питания 
        розетки не требуется проводить процедуру 
        описанную в п. 1.
        4. При отсутствии местной wifi сети, можно 
        управлять розеткой из сети  
        "setup_rosette".
        5. управление розеткой осуществляется при 
        помощи пунктов "Включить" и "Выключить" 
        и нажатием кнопки "Отправить". 
        '''
        self.help = tkinter.Tk()
        self.help.title('Help me, help you!')
        label = tkinter.Label(self.help, text=text, justify='left')
        label.pack()
        button = tkinter.Button(self.help, text='Закрыть', command=self.close_help_window)
        button.pack()
        self.help.mainloop()

    def close_help_window(self):
        self.help.destroy()
