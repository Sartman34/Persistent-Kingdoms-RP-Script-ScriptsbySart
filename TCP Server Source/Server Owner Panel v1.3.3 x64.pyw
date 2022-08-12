# -*- coding: utf8 -*-

import tkinter
import datetime
import socket
import os
import sys

ip_adress = "127.0.0.1"
start_year = 2021
start_month = 10
start_day = 10
server_name = "Public User"
is_so = True
is_32Bit = False

##settable_files = [
##    "admin_permissions.txt",
##    "banned_ips.txt",
##    "basic_settings.txt",
##    "door_keys.txt",
##    "inventories.txt",
##    "mails.txt",
##    "permissions.txt",
##    "whitelist.txt"
##]
##only_gettable_files = [
##    "admin_permissions_readme.txt",
##    "banned_players.txt",
##    "database.txt",
##    "logs.txt",
##    "names.txt"
##]
settable_files = []
only_gettable_files = []

x32 = " x32" if is_32Bit else " x64"
version = "1.3.3" + x32
app_width = 500
app_height = 400
port = 80

app_description = "Bu panel {} adınadır.".format(server_name)
panel_name = "Server Owner" if is_so else "Admin"
app_title = "{} {} Panel".format(server_name, panel_name)
admin_pass = ""
years = []
time = datetime.datetime.now()
day_of_months = {1 : 31,
                 2 : 30,
                 3 : 31,
                 4 : 30,
                 5 : 31,
                 6 : 30,
                 7 : 31,
                 8 : 31,
                 9 : 30,
                 10 : 31,
                 11 : 30,
                 12 : 31}

for x in range(start_year, time.year + 1):
    years.append(x)

this_years_months = []
if time.year == start_year:
    y = start_month
else:
    y = 1
for x in range(y, time.month + 1):
    this_years_months.append(x)

this_months_days = []
if time.year == start_year and time.month == start_month:
    y = start_day
else:
    y = 1
for x in range(1, time.day + 1):
    this_months_days.append(x)

start_years_months = []
if start_year == time.year:
    y = time.month
else:
    y = 12
for x in range(start_month, y + 1):
    start_years_months.append(x)

start_months_days = []
if start_year == time.year and start_month == time.month:
    y = time.day
else:
    y = day_of_months[time.month]
for x in range(start_day, y + 1):
    start_months_days.append(x)

class MainApp(tkinter.Frame):
    presentations = {"main_menu" : lambda x: MainApp.MainMenu(x),
                 "server_owner_panel_menu" : lambda x: ServerOwnerPanel(x),
                 "get_log_file_menu" : lambda x: LogFileGetter(x)}
    def __init__(self, parent):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        self.presentation = MainApp.presentations["main_menu"](self)
        self.presentation.pack()

    def changePresentation(self, prsnt):
        self.presentation.destroy()
        self.presentation = MainApp.presentations[prsnt](self)
        self.presentation.pack()

    class MainMenu(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)
            self.main_content_holder = tkinter.Frame(self)
            tkinter.Label(self.main_content_holder, text = app_description).pack(fill = "x")
            tkinter.Label(self.main_content_holder).pack()
            button_holder = tkinter.Frame(self.main_content_holder)
            if is_so:
                tkinter.Button(button_holder, text = "Server Owner Panel", command = lambda: self.parent.changePresentation("server_owner_panel_menu")).pack(fill = "x")
            tkinter.Button(button_holder, text = "Get log file", command = lambda: self.parent.changePresentation("get_log_file_menu")).pack(fill = "x")
            button_holder.pack()
            self.main_content_holder.grid(row = 0)
            tkinter.Label(self).grid(row = 1)
            tkinter.Label(self).grid(row = 2)
            tkinter.Label(self, text = "Version {}\nScripts by Sart".format(version), justify = "center").grid(row = 3, sticky = "S" + "E")

class ServerOwnerPanel(tkinter.Frame):
    presentations = {"main_menu" : lambda x: ServerOwnerPanel.MainMenu(x),
                     "script_files_menu" : lambda x: ScriptFileEditor(x),
                     "player_operations_menu" : lambda x: PlayerOperations(x)}
    
    def __init__(self, parent):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        self.presentation = ServerOwnerPanel.presentations["main_menu"](self)
        self.presentation.pack()

    def changePresentation(self, prsnt):
        self.presentation.destroy()
        self.presentation = ServerOwnerPanel.presentations[prsnt](self)
        self.presentation.pack()

    class MainMenu(tkinter.Frame):
        def __init__(self, parent):
            self.parent = parent
            tkinter.Frame.__init__(self, self.parent)
            
            button_holder = tkinter.Frame(self)
            tkinter.Button(button_holder, text = "Script Files Panel", command = lambda: self.parent.changePresentation("script_files_menu")).pack(fill = "x")
            tkinter.Button(button_holder, text = "Player Operations", command = lambda: self.parent.changePresentation("player_operations_menu")).pack(fill = "x")
            button_holder.pack()

            tkinter.Label(self).pack()
            
            button_holder = tkinter.Frame(self)
            tkinter.Button(button_holder, command = self.return_to_menu, text = "Return").pack(side = "left")
            button_holder.pack()

        def return_to_menu(self):
            self.parent.parent.changePresentation("main_menu")

class PlayerOperations(tkinter.Frame):
    def __init__(self, parent):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        
        essentials = tkinter.Frame(self)
        tkinter.Label(essentials, text = "Server Owner Pass:").grid(row = 0, column = 0)
        self.admin_pass_entry = tkinter.Entry(essentials)
        self.admin_pass_entry.insert(0, admin_pass)
        self.admin_pass_entry.grid(row = 0, column = 1)
        
        tkinter.Label(essentials, text = "Unique ID (GUID): ").grid(row = 1, column = 0)
        self.guid_entry = tkinter.Entry(essentials)
        self.guid_entry.grid(row = 1, column = 1)
        essentials.pack(anchor = "w")

        tkinter.Label(self).pack()

        operations_holder = tkinter.Frame(self)

        ban_holder = tkinter.Frame(operations_holder)
        
        tkinter.Label(ban_holder, text = "Ban:").grid(row = 0, column = 0, sticky = "w")

        tkinter.Button(ban_holder, text = "Perma Ban", command = self.perma_ban).grid(row = 1, column = 0, sticky = "w" + "e")
        
        tkinter.Button(ban_holder, text = "Temp Ban", command = self.temp_ban).grid(row = 2, column = 0, sticky = "w" + "e")
        tkinter.Label(ban_holder, width = 1).grid(row = 2, column = 1, sticky = "w" + "e")
        self.temp_ban_sure = tkinter.Entry(ban_holder, width = 4)
        self.temp_ban_sure.insert(0, "1")
        self.temp_ban_sure.grid(row = 2, column = 2)
        tkinter.Label(ban_holder, text = "saat").grid(row = 2, column = 3)

        tkinter.Button(ban_holder, text = "Ban Kaldır", command = self.remove_ban).grid(row = 3, column = 0, sticky = "w" + "e")

        ban_holder.pack(side = "left", anchor = "n")

        tkinter.Label(operations_holder, width = 2).pack(side = "left")

        refund_holder = tkinter.Frame(operations_holder)

        tkinter.Label(refund_holder, text = "Refund: -Kullanılabilir Değildir!-").pack(anchor = "w")
        tkinter.Label(refund_holder, text = "Uyarı: Kişi refund için oyunda olmamalıdır.").pack(anchor = "w")

        show_money_holder = tkinter.Frame(refund_holder)

        tkinter.Button(show_money_holder, text = "Show", command = self.show_money).pack(side = "left")
        tkinter.Label(show_money_holder, text = "Gold: ").pack(side = "left")
        self.player_gold = tkinter.Label(show_money_holder, width = 6).pack(side = "left")
        tkinter.Label(show_money_holder, text = " Banka: ").pack(side = "left")
        self.player_bank = tkinter.Label(show_money_holder, width = 6).pack(side = "left")

        show_money_holder.pack(anchor = "w")

        take_give_holder = tkinter.Frame(refund_holder)

        tkinter.Button(take_give_holder, text = "Ver", command = self.give_money, width = 3).pack(side = "left")
        tkinter.Button(take_give_holder, text = "Al", command = self.take_money, width = 3).pack(side = "left")
        tkinter.Label(take_give_holder, width = 1).pack(side = "left")
        take_give_amount = tkinter.Entry(take_give_holder)
        take_give_amount.pack(side = "left")

        take_give_holder.pack(anchor = "w")

##        refund_holder.pack(side = "left", anchor = "n")

        operations_holder.pack(anchor = "w")

        tkinter.Label(self).pack()
        
        button_holder = tkinter.Frame(self)
        tkinter.Button(button_holder, command = self.return_to_menu, text = "Return").pack(side = "left")
        button_holder.pack()
        
        self.server_message_menu = tkinter.Label(self, text = "")
        self.server_message_menu.pack()

    def remove_ban(self):
        server = socket.socket()
        server.connect((ip_adress, port))
        server.send("GET /remove_ban%3C{}%3C{}".format(self.admin_pass_entry.get(), self.guid_entry.get()).encode())
        message = server.recv(1024).decode().split("%")
        action = message.pop(0)
        if action == "message":
            server_message = message[0]
            self.server_message_menu.config(text = server_message)

    def perma_ban(self):
        server = socket.socket()
        server.connect((ip_adress, port))
        server.send("GET /player_ban%3C{}%3C{}%3C{}%3C{}".format(self.admin_pass_entry.get(), self.guid_entry.get(), 1, 5).encode())
        message = server.recv(1024).decode().split("%")
        action = message.pop(0)
        if action == "message":
            server_message = message[0]
            self.server_message_menu.config(text = server_message)

    def temp_ban(self):
        ban_suresi = self.temp_ban_sure.get()
        if ban_suresi.isnumeric():
            server = socket.socket()
            server.connect((ip_adress, port))
            server.send("GET /player_ban%3C{}%3C{}%3C{}%3C{}".format(self.admin_pass_entry.get(), self.guid_entry.get(), 0, ban_suresi).encode())
            message = server.recv(1024).decode().split("%")
            action = message.pop(0)
            if action == "message":
                server_message = message[0]
                self.server_message_menu.config(text = server_message)
        else:
            self.server_message_menu.config(text = "Hatalı süre tanımı")
            
    def show_money(self):
        pass

    def give_money(self):
        pass

    def take_money(self):
        pass

    def return_to_menu(self):
        global admin_pass
        admin_pass = self.admin_pass_entry.get()
        self.parent.changePresentation("main_menu")

class ScriptFileEditor(tkinter.Frame):
    def __init__(self, parent):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        
        admin_pass_holder = tkinter.Frame(self)
        tkinter.Label(admin_pass_holder, text = "Server Owner Pass:").pack(side = "left")
        self.admin_pass_entry = tkinter.Entry(admin_pass_holder)
        self.admin_pass_entry.insert(0, admin_pass)
        self.admin_pass_entry.pack(side = "left")
        admin_pass_holder.pack(fill = "x")

        file_holder = tkinter.Frame(self)
        row_counter = 0
        row_counter_limit = len(settable_files) - 1
        for file in range(len(settable_files)):
            tkinter.Button(file_holder, text = "Get", command = lambda file = settable_files[file]: self.get_file(file), padx = 5).grid(column = 0, row = row_counter)
            tkinter.Button(file_holder, text = "Set", command = lambda file = settable_files[file]: self.set_file(file), padx = 5).grid(column = 1, row = row_counter)
            tkinter.Label(file_holder, text = settable_files[file], padx = 10).grid(column = 2, row = row_counter, sticky = "w")
            row_counter += 1
        row_counter_limit += len(only_gettable_files) - 1
        for file in range(len(only_gettable_files)):
            tkinter.Button(file_holder, text = "Get", command = lambda file = only_gettable_files[file]: self.get_file(file), padx = 5).grid(column = 0, row = row_counter, columnspan = 2, sticky = "w" + "e")
            tkinter.Label(file_holder, text = only_gettable_files[file], padx = 10).grid(column = 2, row = row_counter, sticky = "w")
            row_counter += 1
        #tkinter.Button(file_holder, text = "Get", command = lambda: self.get_file("database.txt"), padx = 21).grid(column = 0, row = len(files), columnspan = 2, sticky = "w" + "e")
        #tkinter.Label(file_holder, text = "database.txt", padx = 10).grid(column = 2, row = len(files), sticky = "w")
        file_holder.pack(anchor = "w")
        
        button_holder = tkinter.Frame(self)
        tkinter.Button(button_holder, command = self.reimport_files, text = "Reimport Files").pack(side = "left")
        tkinter.Button(button_holder, command = self.return_to_menu, text = "Return").pack(side = "left")
        button_holder.pack()
        
        self.server_message_menu = tkinter.Label(self, text = "")
        self.server_message_menu.pack()

    def get_file(self, file_name):
        server = socket.socket()
        server.connect((ip_adress, port))
        server.send("GET /get_file%3C{}%3C{}".format(self.admin_pass_entry.get(), file_name).encode())
        message = server.recv(1024).decode().split("%")
        action = message.pop(0)
        if action == "recv_file":
            with open(file_name, 'wb') as file:
                while True:
                    data = server.recv(1024)
                    if not data:
                        break
                    file.write(data)
            self.server_message_menu.config(text = "Succesfully downloaded {}.".format(file_name))
        elif action == "message":
            server_message = message[0]
            self.server_message_menu.config(text = server_message)
        server.close()

    def set_file(self, file_name):
        try:
            file = open(file_name, 'rb')
        except IOError:
            self.server_message_menu.config(text = "File not found on computer.")
            return
        server = socket.socket()
        server.connect((ip_adress, port))
        server.send("GET /set_file%3C{}%3C{}".format(self.admin_pass_entry.get(), file_name).encode())
        message = server.recv(1024).decode().split("%")
        action = message.pop(0)
        if action == "send_file":
            l = file.read(1024)
            while (l):
               server.send(l)
               l = file.read(1024)
            file.close()
            self.server_message_menu.config(text = "Succesfully sent {}.".format(file_name))
        elif action == "message":
            server_message = message[0]
            self.server_message_menu.config(text = server_message)
        server.close()
    
    def reimport_files(self):
        server = socket.socket()
        server.connect((ip_adress, port))
        server.send("GET /reimport%3C{}".format(self.admin_pass_entry.get()).encode())
        message = server.recv(1024).decode().split("%")
        action = message.pop(0)
        if action == "message":
            server_message = message[0]
            self.server_message_menu.config(text = server_message)

    def return_to_menu(self):
        global admin_pass
        admin_pass = self.admin_pass_entry.get()
        self.parent.changePresentation("main_menu")
        
class LogFileGetter(tkinter.Frame):
    def __init__(self, parent):
        self.parent = parent
        tkinter.Frame.__init__(self, self.parent)
        self.main = tkinter.Frame(self)
        self.years_list = years
        self.months_list = start_years_months
        self.days_list = start_months_days
        self.set_year = start_year
        self.set_month = start_month
        self.set_day = start_day
        self.day_variable = tkinter.IntVar(self)
        self.month_variable = tkinter.IntVar(self)
        self.month_variable.trace("w", self.update_month)
        self.year_variable = tkinter.IntVar(self)
        self.no_trace = False
        self.refresh()
        
    def refresh(self):
        self.main.destroy()
        self.main = tkinter.Frame(self)
        
        self.date_holder = tkinter.Frame(self.main)
        self.no_trace = True
        self.day_variable.set(self.set_day)
        tkinter.OptionMenu(self.date_holder, self.day_variable, *self.days_list).pack(side = "left")
        self.month_variable.set(self.set_month)
        tkinter.OptionMenu(self.date_holder, self.month_variable, *self.months_list).pack(side = "left")
        self.year_variable.set(self.set_year)
        tkinter.OptionMenu(self.date_holder, self.year_variable, *self.years_list).pack(side = "left")
        self.no_trace = False
        self.date_holder.pack()
        
        self.option_holder = tkinter.Frame(self.main)
        tkinter.Button(self.option_holder, command = self.request_log, text = "Get Log").pack(side = "left")
        tkinter.Button(self.option_holder, command = self.return_to_menu, text = "Return").pack(side = "left")
        self.option_holder.pack()

        self.server_message_menu = tkinter.Label(self.main, text = "")
        self.server_message_menu.pack()

        self.main.pack()
        
    def request_log(self):
        self.no_trace = True
        year = self.year_variable.get()
        month = self.month_variable.get()
        day = self.day_variable.get()
        self.no_trace = False
        server = socket.socket()
        server.connect((ip_adress, port))
        file_name = "server_log_{0:{2}>2}_{1:{2}>2}_{3}.txt".format(month, day, "0", year - 2000)
        server.send("GET /get_log%3C{}".format(file_name).encode())
        message = server.recv(1024).decode().split("%")
        action = message.pop(0)
        if action == "recv_file":
            with open(file_name, 'wb') as file:
                while True:
                    data = server.recv(1024)
                    if not data:
                        break
                    file.write(data)
            self.server_message_menu.config(text = "Succesfully downloaded {}.".format(file_name))
        elif action == "message":
            server_message = message[0]
            self.server_message_menu.config(text = server_message)
        server.close()
        
    def return_to_menu(self):
        self.parent.changePresentation("main_menu")

    def update_month(self, *args):
        if self.no_trace:
            return
        self.no_trace = True
        year = self.year_variable.get()
        month = self.month_variable.get()
        day = self.day_variable.get()
        self.no_trace = False
        self.set_month = month
        self.set_day = day
        if start_month == month and start_year == year:
            if not start_day <= day:
                self.set_day = start_day
            if (not day <= time.day) and time.month == month and time.year == year:
                self.set_day = time.day
            self.days_list = start_months_days
            
        elif time.month == month and time.year == year:
            if not day <= time.day:
                self.set_day = time.day
            self.days_list = this_months_days
        else:
            if not day <= day_of_months[month]:
                self.set_day = day_of_months[month]
            self.days_list = [x for x in range(1, day_of_months[month] + 1)]
        self.refresh()
#self renaming :)
##extension = os.path.splitext(sys.argv[0])[1]
##os.rename(sys.argv[0], "_{} {} Panel v{}{}".format(server_name, panel_name, version, extension))

main = tkinter.Tk()
main.title(app_title)
x = (main.winfo_screenwidth() // 2) - (app_width // 2)
y = (main.winfo_screenheight() // 2) - (app_height // 2) - 50
main.geometry('{}x{}+{}+{}'.format(app_width, app_height, x, y))
MainApp(main).pack(expand = True)
#main.wm_attributes("-topmost", 1)
main.mainloop()
