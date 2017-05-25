from tkinter import *
import socket
import threading
import time
import webbrowser
import requests
import subprocess
import os


class Gui:
    def __init__(self, master):

        # Variables
        self.ip_list = set()
        self.port_list = set()
        self.name = ''
        self.message = ''
        self.s_bind = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.quiting = False
        self.quiting_check = 'ok'

        self.master = master
        master.resizable(0, 0)
        master.title("Enter name")

        # -----------------------------------------------------
        # ---------- First program for entering name ----------
        # -----------------------------------------------------

        self.frame_name = Frame(master)
        self.frame_name.pack()

        self.label = Label(self.frame_name, text="Your name must be from 2 to 10 characters long.")
        self.label.pack()

        self.label_name = Label(self.frame_name, text="Enter your name: ")
        self.label_name.pack(side=LEFT)

        self.entry = Entry(self.frame_name)
        self.entry.bind("<Return>", self.check_value_name_press)
        self.entry.pack(side=LEFT)

        self.button = Button(self.frame_name, text="Enter", command=self.check_value_name_click)
        self.button.pack(side=LEFT)

        # ----------------------------------
        # ---------- Main Program ----------
        # ----------------------------------

        # ---------- Main Frame ----------
        self.frame = Frame(master)

        # ---------- Associate scrollbar with showed messages ----------
        self.scrollbar = Scrollbar(self.frame, orient=VERTICAL)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.messages = Text(self.frame, width=50, height=25)
        self.messages.configure(state=DISABLED)
        self.messages.pack()

        self.messages.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.messages.yview)

        # Welcome message
        self.welcome = "Welcome to the chat !\nSpecial commands that you can use:\n->clear() = Clears the screen\n->tips_off() = Turn all tips off\n->tips_on() = Turn all tips on\n->myip() = Shows your ip addresses\n->help() = Open documentation\n->commands() = Print all commands you can use\n"
        self.messages.configure(state=NORMAL)
        self.messages.insert(INSERT, self.welcome)
        self.messages.configure(state=DISABLED)

        # ---------- Ip addresses, ports and buttons ----------

        # Connect
        self.frame_connect = Frame(self.frame)
        self.frame_connect.pack()

        self.ip_label = Label(self.frame_connect, text="Ip address: ")
        self.ip_label.pack(side=LEFT)

        self.ip_entry = Entry(self.frame_connect, width=14)
        self.ip_entry.bind('<FocusIn>', lambda _: self.tip_ip_connect.pack())
        self.ip_entry.bind('<FocusOut>', lambda _: self.tip_ip_connect.pack_forget())
        self.ip_entry.pack(side=LEFT)

        self.port_label = Label(self.frame_connect, text="Port: ")
        self.port_label.pack(side=LEFT)

        self.port_entry = Entry(self.frame_connect, width=5)
        self.port_entry.bind('<FocusIn>', lambda _: self.tip_port_connect.pack())
        self.port_entry.bind('<FocusOut>', lambda _: self.tip_port_connect.pack_forget())
        self.port_entry.pack(side=LEFT)

        self.button_connect = Button(self.frame_connect, text="Connect", width=6, command=self.socket_connect_thread)
        self.button_connect.bind('<Enter>', lambda _: self.tip_button_connect.place(x=100, y=330))
        self.button_connect.bind('<Leave>', lambda _: self.tip_button_connect.place_forget())
        self.button_connect.pack(side=LEFT)

        # Bind
        self.frame_bind = Frame(self.frame)
        self.frame_bind.pack()

        self.ip_label2 = Label(self.frame_bind, text="Ip address: ")
        self.ip_label2.pack(side=LEFT)

        self.ip_entry2 = Entry(self.frame_bind, width=14)
        self.ip_entry2.bind('<FocusIn>', lambda _: self.tip_ip_bind.pack())
        self.ip_entry2.bind('<FocusOut>', lambda _: self.tip_ip_bind.pack_forget())
        self.ip_entry2.pack(side=LEFT)

        self.port_label2 = Label(self.frame_bind, text="Port: ")
        self.port_label2.pack(side=LEFT)

        self.port_entry2 = Entry(self.frame_bind, width=5)
        self.port_entry2.bind('<FocusIn>', lambda _: self.tip_port_bind.pack())
        self.port_entry2.bind('<FocusOut>', lambda _: self.tip_port_bind.pack_forget())
        self.port_entry2.pack(side=LEFT)

        self.button_bind = Button(self.frame_bind, text="Bind", width=6, command=self.socket_binding_thread)
        self.button_bind.bind('<Enter>', lambda _: self.tip_button_bind.place(x=160, y=330))
        self.button_bind.bind('<Leave>', lambda _: self.tip_button_bind.place_forget())
        self.button_bind.pack(side=LEFT)

        # ---------- Text field for sending messages and send button ----------

        self.frame_send = Frame(self.frame)
        self.frame_send.pack()

        self.button_send = Button(self.frame_send, text="Send", width=6, command=self.sending_messages_click)
        self.button_send.pack(side=LEFT, fill=Y)

        self.text_send = Text(self.frame_send, width=39, height=5)
        self.text_send.bind('<Return>', self.sending_messages_press)
        self.text_send.pack(side=LEFT)

        # ---------- Tips ----------

        # Connect tips
        self.tip_ip_connect = Label(self.frame, text='Ip address of your friend.')

        self.tip_port_connect = Label(self.frame, text='Open port of your friend.')

        self.tip_button_connect = Label(self.frame, text='Start trying to connecting to your friend.')

        # Bind tips
        self.tip_ip_bind = Label(self.frame, text='Your ip address.')

        self.tip_port_bind = Label(self.frame, text='Port on you want to start listening for connections.')

        self.tip_button_bind = Label(self.frame, text='Start listening for connections.')

    def check_value_name_click(self):
        name = self.entry.get().strip()
        if len(name) >= 2 and len(name) <= 10 and not name.isspace():
            self.name = ''.join(name.split())
            self.frame_name.destroy()
            self.master.title("Welcome " + str(self.name))
            self.frame.pack()

    def check_value_name_press(self, event):
        name = self.entry.get().strip()
        if len(name) >= 2 and len(name) <= 10 and not name.isspace():
            self.name = ''.join(name.split())
            self.frame_name.destroy()
            self.master.title("Welcome " + str(self.name))
            self.frame.pack()

    def sending_messages_click(self):
        message = str(self.text_send.get("1.0", "end").strip())
        if len(message) > 0 and not message.isspace():
            self.message = self.name + '-> ' + ' '.join(message.split())
            self.messages.configure(state=NORMAL)

            if "->clear()" in self.message:
                self.text_send.delete("1.0", "end")
                self.messages.delete("1.0", "end")
                self.messages.see(END)
                self.messages.configure(state=DISABLED)
                return "break"

            elif "->tips_off()" in self.message:
                self.ip_entry.unbind('<FocusIn>')
                self.ip_entry.unbind('<FocusOut>')
                self.port_entry.unbind('<FocusIn>')
                self.port_entry.unbind('<FocusOut>')
                self.button_connect.unbind('<Enter>')
                self.button_connect.unbind('<Leave>')
                self.ip_entry2.unbind('<FocusIn>')
                self.ip_entry2.unbind('<FocusOut>')
                self.port_entry2.unbind('<FocusIn>')
                self.port_entry2.unbind('<FocusOut>')
                self.button_bind.unbind('<Enter>')
                self.button_bind.unbind('<Leave>')

                self.messages.insert(INSERT, 'Tips are off.' + "\n")
                self.messages.see(END)
                self.messages.configure(state=DISABLED)
                self.text_send.delete("1.0", "end")
                return "break"

            elif "->tips_on()" in self.message:
                self.ip_entry.bind('<FocusIn>', lambda _: self.tip_ip_connect.pack())
                self.ip_entry.bind('<FocusOut>', lambda _: self.tip_ip_connect.pack_forget())
                self.port_entry.bind('<FocusIn>', lambda _: self.tip_port_connect.pack())
                self.port_entry.bind('<FocusOut>', lambda _: self.tip_port_connect.pack_forget())
                self.button_connect.bind('<Enter>', lambda _: self.tip_button_connect.place(x=100, y=330))
                self.button_connect.bind('<Leave>', lambda _: self.tip_button_connect.place_forget())
                self.ip_entry2.bind('<FocusIn>', lambda _: self.tip_ip_bind.pack())
                self.ip_entry2.bind('<FocusOut>', lambda _: self.tip_ip_bind.pack_forget())
                self.port_entry2.bind('<FocusIn>', lambda _: self.tip_port_bind.pack())
                self.port_entry2.bind('<FocusOut>', lambda _: self.tip_port_bind.pack_forget())
                self.button_bind.bind('<Enter>', lambda _: self.tip_button_bind.place(x=160, y=330))
                self.button_bind.bind('<Leave>', lambda _: self.tip_button_bind.place_forget())

                self.messages.insert(INSERT, 'Tips are on.' + "\n")
                self.messages.see(END)
                self.messages.configure(state=DISABLED)
                self.text_send.delete("1.0", "end")
                return "break"

            elif "->myip()" in self.message:
                # Ip addresses check
                cmd = subprocess.getoutput('ifconfig|grep "inet addr"')
                split = cmd.split()
                split2 = split[1]
                local_ip = split2[5:]
                if len(local_ip) >= 7 and len(local_ip) <= 15:
                    pass
                else:
                    local_ip = "<Couldn't find your local ip address>"

                source_code = requests.get('https://publicip.000webhostapp.com').text
                replace = source_code.replace('<div>', '')
                public_ip = replace.replace('</div>', '')

                if len(public_ip) >= 7 and len(public_ip) <= 16 and public_ip != 'None' and public_ip != 'NoNe':
                    pass
                else:
                    public_ip = "<Couldn't find your public ip address>"

                port_forwarding = 'https://www.howtogeek.com/66214/how-to-forward-ports-on-your-router/'

                self.messages.insert(INSERT,
                                     '\nConnection on your network:\nDefault Loopback address - 127.0.0.1\nLocal network ip address - ' + local_ip + "\n" + "\nConnection on different networks (public):\nPublic ip address -" + public_ip.replace(
                                         '\n',
                                         '') + "\nYou have to configure port forwarding - " + port_forwarding + "\n")
                self.messages.see(END)
                self.messages.configure(state=DISABLED)
                self.text_send.delete("1.0", "end")
                return "break"

            elif "->help()" in self.message:
                self.text_send.delete("1.0", "end")
                webbrowser.open('https://github.com', new=2)
                self.messages.see(END)
                self.messages.configure(state=DISABLED)
                return "break"

            elif "->exit()" in self.message:
                pass

            elif "->commands()" in self.message:
                self.text_send.delete("1.0", "end")
                self.messages.insert(INSERT,
                                     'Special commands that you can use:\n->clear() = Clears the screen\n->tips_off() = Turn all tips off\n->tips_on() = Turn all tips on\n->myip() = Shows your ip addresses\n->help() = Open documentation\n->commands() = Print all commands you can use\n')
                self.messages.see(END)
                self.messages.configure(state=DISABLED)
                return "break"

            else:
                try:
                    self.messages.insert(INSERT, self.message + "\n")
                    self.messages.see(END)
                    self.messages.configure(state=DISABLED)
                    self.text_send.delete("1.0", "end")
                    self.s_connect.send(self.message.encode('utf-8'))
                    return "break"

                except BrokenPipeError:
                    return "break"
                    pass
        else:
            return "break"

    def sending_messages_press(self, event):
        message = str(self.text_send.get("1.0", "end").strip())
        if len(message) > 0 and not message.isspace():
            self.message = self.name + '-> ' + ' '.join(message.split())
            self.messages.configure(state=NORMAL)

            if "->clear()" in self.message:
                self.text_send.delete("1.0", "end")
                self.messages.delete("1.0", "end")
                self.messages.see(END)
                self.messages.configure(state=DISABLED)
                return "break"

            elif "->tips_off()" in self.message:
                self.ip_entry.unbind('<FocusIn>')
                self.ip_entry.unbind('<FocusOut>')
                self.port_entry.unbind('<FocusIn>')
                self.port_entry.unbind('<FocusOut>')
                self.button_connect.unbind('<Enter>')
                self.button_connect.unbind('<Leave>')
                self.ip_entry2.unbind('<FocusIn>')
                self.ip_entry2.unbind('<FocusOut>')
                self.port_entry2.unbind('<FocusIn>')
                self.port_entry2.unbind('<FocusOut>')
                self.button_bind.unbind('<Enter>')
                self.button_bind.unbind('<Leave>')

                self.messages.insert(INSERT, 'Tips are off.' + "\n")
                self.messages.see(END)
                self.messages.configure(state=DISABLED)
                self.text_send.delete("1.0", "end")
                return "break"

            elif "->tips_on()" in self.message:
                self.ip_entry.bind('<FocusIn>', lambda _: self.tip_ip_connect.pack())
                self.ip_entry.bind('<FocusOut>', lambda _: self.tip_ip_connect.pack_forget())
                self.port_entry.bind('<FocusIn>', lambda _: self.tip_port_connect.pack())
                self.port_entry.bind('<FocusOut>', lambda _: self.tip_port_connect.pack_forget())
                self.button_connect.bind('<Enter>', lambda _: self.tip_button_connect.place(x=100, y=330))
                self.button_connect.bind('<Leave>', lambda _: self.tip_button_connect.place_forget())
                self.ip_entry2.bind('<FocusIn>', lambda _: self.tip_ip_bind.pack())
                self.ip_entry2.bind('<FocusOut>', lambda _: self.tip_ip_bind.pack_forget())
                self.port_entry2.bind('<FocusIn>', lambda _: self.tip_port_bind.pack())
                self.port_entry2.bind('<FocusOut>', lambda _: self.tip_port_bind.pack_forget())
                self.button_bind.bind('<Enter>', lambda _: self.tip_button_bind.place(x=160, y=330))
                self.button_bind.bind('<Leave>', lambda _: self.tip_button_bind.place_forget())

                self.messages.insert(INSERT, 'Tips are on.' + "\n")
                self.messages.see(END)
                self.messages.configure(state=DISABLED)
                self.text_send.delete("1.0", "end")
                return "break"

            elif "->myip()" in self.message:
                # Ip addresses check
                cmd = subprocess.getoutput('ifconfig|grep "inet addr"')
                split = cmd.split()
                split2 = split[1]
                local_ip = split2[5:]
                if len(local_ip) >= 7 and len(local_ip) <= 15:
                    pass
                else:
                    local_ip = "<Couldn't find your local ip address>"

                source_code = requests.get('https://publicip.000webhostapp.com').text
                replace = source_code.replace('<div>', '')
                public_ip = replace.replace('</div>', '')

                if len(public_ip) >= 7 and len(public_ip) <= 16 and public_ip != 'None' and public_ip != 'NoNe':
                    pass
                else:
                    public_ip = "<Couldn't find your public ip address>"

                port_forwarding = 'https://www.howtogeek.com/66214/how-to-forward-ports-on-your-router/'

                self.messages.insert(INSERT, '\nConnection on your network:\nDefault Loopback address - 127.0.0.1\nLocal network ip address - ' + local_ip + "\n" + "\nConnection on different networks (public):\nPublic ip address -" + public_ip.replace('\n', '') + "\nYou have to configure port forwarding - " + port_forwarding + "\n")
                self.messages.see(END)
                self.messages.configure(state=DISABLED)
                self.text_send.delete("1.0", "end")
                return "break"

            elif "->help()" in self.message:
                self.text_send.delete("1.0", "end")
                webbrowser.open('https://github.com', new=2)
                self.messages.see(END)
                self.messages.configure(state=DISABLED)
                return "break"

            elif "->commands()" in self.message:
                self.text_send.delete("1.0", "end")
                self.messages.insert(INSERT,
                                     'Special commands that you can use:\n->clear() = Clears the screen\n->tips_off() = Turn all tips off\n->tips_on() = Turn all tips on\n->myip() = Shows your ip addresses\n->help() = Open documentation\n->commands() = Print all commands you can use\n')
                self.messages.see(END)
                self.messages.configure(state=DISABLED)
                return "break"

            else:
                try:
                    self.messages.insert(INSERT, self.message + "\n")
                    self.messages.see(END)
                    self.messages.configure(state=DISABLED)
                    self.text_send.delete("1.0", "end")
                    self.s_connect.send(self.message.encode('utf-8'))
                    return "break"

                except BrokenPipeError:
                    return "break"
                    pass

        else:
            return "break"

    def socket_binding(self):
        try:

            self.quiting = False

            ip = self.ip_entry2.get()
            port = self.port_entry2.get()

            self.ip_list.clear()
            self.port_list.clear()

            if len(str(ip)) <= 15 and len(str(ip)) >= 7 and len(str(port)) <= 5 and len(str(port)) >= 4:

                ip_connect = self.ip_entry.get()
                port_connect = self.port_entry.get()

                if str(ip) == str(ip_connect) and str(port) == str(port_connect):
                    pass

                else:

                    self.ip_entry2.configure(state=DISABLED)
                    self.port_entry2.configure(state=DISABLED)
                    self.button_bind.configure(state=DISABLED)

                    self.s_bind.bind((str(ip), int(port)))
                    time.sleep(1)

                    self.messages.configure(state=NORMAL)
                    self.messages.insert(INSERT, 'Socket is bind.\n')
                    self.messages.see(END)
                    self.messages.configure(state=DISABLED)

                    self.s_bind.listen(1)
                    time.sleep(1)

                    if threading.active_count() < 4:

                        self.ip_list.add(str(ip))
                        self.port_list.add(str(port))

                        self.messages.configure(state=NORMAL)
                        self.messages.insert(INSERT, 'Starting listening for connections.\n')
                        self.messages.insert(INSERT, 'Waiting for connection on port ' + str(port) + ' on ' + str(
                            ip) + ' ip address.\n')
                        self.messages.see(END)
                        self.messages.configure(state=DISABLED)

                        self.button_bind.pack_forget()
                        self.button_bind = Button(self.frame_bind, text="Unbind", width=6, command=self.socket_binding_stop)
                        self.button_bind.pack(side=LEFT)
                        self.button_bind.configure(state=NORMAL)

                        b_data, address = self.s_bind.accept()

                        if not self.quiting:
                            self.button_bind.configure(command=self.socket_binding_stop_connected)

                            self.messages.configure(state=NORMAL)
                            self.messages.delete("1.0", "end")
                            self.messages.insert(INSERT, 'Connection established from ' + str(address) + '.\n')
                            self.messages.see(END)
                            self.messages.configure(state=DISABLED)

                        while not self.quiting:
                            data = b_data.recv(1024)
                            if data:
                                self.messages.configure(state=NORMAL)
                                self.messages.insert(INSERT, data.decode('utf-8') + '\n')
                                self.messages.see(END)
                                self.messages.configure(state=DISABLED)

                            else:
                                self.messages.configure(state=NORMAL)
                                self.messages.insert(INSERT, 'Disconnected.' + '\n')
                                self.messages.insert(INSERT, 'Connection is over.' + '\n')
                                self.messages.see(END)
                                self.messages.configure(state=DISABLED)

                                self.button_bind.pack_forget()
                                self.button_bind = Button(self.frame_bind, text="Bind", width=6,
                                                          command=self.socket_binding_thread)
                                self.button_bind.bind('<Enter>', lambda _: self.tip_button_bind.place(x=160, y=330))
                                self.button_bind.bind('<Leave>', lambda _: self.tip_button_bind.place_forget())
                                self.button_bind.pack(side=LEFT)
                                self.ip_entry2.configure(state=NORMAL)
                                self.port_entry2.configure(state=NORMAL)
                                break

                        self.s_bind.close()

                        self.messages.configure(state=NORMAL)
                        self.messages.insert(INSERT, 'Socket closed.\n')
                        self.messages.see(END)
                        self.messages.configure(state=DISABLED)

                        if '[closed]' in str(self.s_bind):
                            self.s_bind = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    else:
                        print('Threading Error. To avoid this, restart the program.')
                        pass

        except OSError:
            time.sleep(1)
            self.ip_entry2.configure(state=NORMAL)
            self.port_entry2.configure(state=NORMAL)
            self.button_bind.configure(state=NORMAL)

    def socket_binding_thread(self):
        thread = threading.Thread(target=self.socket_binding)
        thread.start()

    def socket_binding_stop(self):
        self.quiting = True
        stop_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        for x in self.ip_list:
            for y in self.port_list:
                stop_socket.connect((str(x), int(y)))

        stop_socket.close()

        self.button_bind.pack_forget()
        self.button_bind = Button(self.frame_bind, text="Bind", width=6, command=self.socket_binding_thread)
        self.button_bind.bind('<Enter>', lambda _: self.tip_button_bind.place(x=160, y=330))
        self.button_bind.bind('<Leave>', lambda _: self.tip_button_bind.place_forget())
        self.button_bind.pack(side=LEFT)
        self.ip_entry2.configure(state=NORMAL)
        self.port_entry2.configure(state=NORMAL)

        self.s_bind = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def socket_binding_stop_connected(self):
        self.quiting = True

        self.button_bind.pack_forget()
        self.button_bind = Button(self.frame_bind, text="Bind", width=6, command=self.socket_binding_thread)
        self.button_bind.bind('<Enter>', lambda _: self.tip_button_bind.place(x=160, y=330))
        self.button_bind.bind('<Leave>', lambda _: self.tip_button_bind.place_forget())
        self.button_bind.pack(side=LEFT)
        self.ip_entry2.configure(state=NORMAL)
        self.port_entry2.configure(state=NORMAL)

        self.s_bind = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def socket_connect(self):
        try:
            self.s_connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            ip = self.ip_entry.get()
            port = self.port_entry.get()

            if len(str(ip)) <= 15 and len(str(ip)) >= 7 and len(str(port)) <= 5 and len(str(port)) >= 4:

                ip_bind = self.ip_entry2.get()
                port_bind = self.port_entry2.get()

                if str(ip) == str(ip_bind) and str(port) == str(port_bind):
                    pass

                else:
                    self.s_connect.connect((str(ip), int(port)))

                    self.ip_entry.configure(state=DISABLED)
                    self.port_entry.configure(state=DISABLED)

                    self.button_connect.pack_forget()
                    self.button_connect = Button(self.frame_connect, text="Disconnect", width=6,
                                                 command=self.socket_connect_stop)
                    self.button_connect.pack(side=LEFT)

                    self.messages.configure(state=NORMAL)
                    self.messages.delete('1.0', 'end')
                    self.messages.insert(INSERT, 'Messages are now send.\n')
                    self.messages.see(END)
                    self.messages.configure(state=DISABLED)

        except ValueError:
            pass

        except ConnectionRefusedError:
            self.messages.configure(state=NORMAL)
            self.messages.insert(INSERT, 'Nobody is listening for connection on this parameters.\n')
            self.messages.see(END)
            self.messages.configure(state=DISABLED)

        except OSError:
            pass

    def socket_connect_thread(self):
        thread = threading.Thread(target=self.socket_connect)
        thread.start()

    def socket_connect_stop(self):
        self.s_connect.close()
        time.sleep(0.2)

        self.messages.configure(state=NORMAL)
        self.messages.insert(INSERT, 'Disconnected.' + '\n')
        self.messages.insert(INSERT, 'Connection is over.' + '\n')
        self.messages.see(END)
        self.messages.configure(state=DISABLED)

        self.button_connect.pack_forget()
        self.button_connect = Button(self.frame_connect, text="Connect", width=6, command=self.socket_connect_thread)
        self.button_connect.bind('<Enter>', lambda _: self.tip_button_connect.place(x=100, y=330))
        self.button_connect.bind('<Leave>', lambda _: self.tip_button_connect.place_forget())
        self.button_connect.pack(side=LEFT)

        self.ip_entry.configure(state=NORMAL)
        self.port_entry.configure(state=NORMAL)


def gui():
    root = Tk()
    Gui(root)
    root.mainloop()
    os._exit(0)


def main():
    thread_gui = threading.Thread(target=gui)
    thread_gui.start()

if __name__ == '__main__':
    try:
        main()

    except KeyboardInterrupt:
        pass

