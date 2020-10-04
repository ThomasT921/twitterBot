import tkinter as tk
import tweepy
import threading
from functools import partial
from mybot import continuousRun, setStatus

window = tk.Tk()
#label = tk.Label(window, text="hello")


class Gui:
    def __init__(self, master):
        self.__master = master
        self.__create_window(master)

    def __create_window(self, master):
        self.__setSize()
        self.__close_button(master)
        self.__create_label("Tweet:")
        status = self.__create_TextBox()
        self.__send_button(status)

    def __confirmWindow(self, status):
        self.__newWindow = tk.Toplevel()
        self.__newWindow.minsize(290,300)
        self.__newWindow.title("Confirm")
        self.__createConfirmMsg(self.__newWindow, status)
        self.__sendConfirm(self.__newWindow, status)

    def __createConfirmMsg(self, window, status):
        self.__msg = tk.Message(self.__newWindow, anchor = "center", width = 200, pady = 20,
         text = "Are you sure you would like to tweet: \n\n" + status + ".")
        self.__msg.pack()

    def __sendConfirm(self, window, status):
        self.send_button = tk.Button(window, text="Confirm", command = partial(self.__close, window, status))
        self.send_button.pack()
        
    def __setSize(self):
        self.__master.minsize(1000,500)

    def __close_button(self, window):
        status = ""
        self.close_button = tk.Button(window, text="Close Button", command = partial(self.__close, window, status))
        self.close_button.pack()
    
    def __send_button(self, status):
        self.send_button = tk.Button(window, text="Send Tweet", command = partial(self.__sendClick, status)) #command = send #function for sending a tweet
        self.send_button.pack()

    def __sendClick(self, status):
        status = status.get()
        self.__confirmWindow(status)
    
    def __create_label(self, text):
        self.label = tk.Label(window, text=text)
        self.label.pack()

    def __create_TextBox(self):
        self.e = tk.Entry()
        self.e.pack()
        return self.e

    def __close(self, window, status):
        window.destroy()
        if str(window) == ".!toplevel":
            setStatus(status)
               

def main():
    Gui(window)
    
    #continuousRun()
    window.mainloop() 
    
main()