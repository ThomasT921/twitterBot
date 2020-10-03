import tkinter as tk
import tweepy
from mybot import api

window = tk.Tk()
label = tk.Label(window, text="hello")


class Gui:
    def __init__(self, master):
        self.__master = master
        self.__setSize()
        self.__close_button()
        self.__create_label("Tweet:")

    def __setSize(self):
        self.__master.minsize(1000,500)

    def __close_button(self):
        self.close_button = tk.Button(window, text="Close Button", command = self.__close)
        self.close_button.pack()
    
    def __send_button(self):
        self.send_button = tk.Button(window, text="Send") #command = send #function for sending a tweet
        self.send_button.pack()
    
    def __create_label(self, text):
        self.label = tk.Label(window, text=text)
        self.label.pack()

    def __close(self):
        self.__master.destroy()

  
           

def main():
    api.update_status("hi")
    my_window = Gui(window)
    window.mainloop()


main()