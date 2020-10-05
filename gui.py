import tkinter as tk
import tweepy
import threading
from functools import partial
from mybot import continuousRun, setStatus

#intialize window as tk
window = tk.Tk()


#GUI class
class Gui:
    def __init__(self, master):
        #sets master to private
        self.__master = master
        #calls main window func
        self.__create_window(master)

    #creates main func
    def __create_window(self, master):
        #call set size of the main window func
        self.__setSize()
        #creates the intial window
        self.__create_label("Tweet:")
        #sets status to the input
        status = self.__create_TextBox()
        #calls the send button func
        self.__send_button(status)
        #calls the close button func
        self.__close_button(master)
    
    #creates the confirm window
    def __confirmWindow(self, status):
        #makes it on top of the main window
        self.__newWindow = tk.Toplevel()
        #size of the window
        self.__newWindow.minsize(290,150)
        #title of the window
        self.__newWindow.title("Confirm")
        #calls the confirm msg func
        self.__createConfirmMsg(self.__newWindow, status)
        #calls the confirm button func
        self.__sendConfirm(self.__newWindow, status)

    #confirm msg
    def __createConfirmMsg(self, window, status):
        #creates confirm msg
        self.__msg = tk.Message(self.__newWindow, anchor = "center", width = 200, pady = 20,
         text = "Are you sure you would like to tweet: \n\n" + status + ".")
        #puts it on the window
        self.__msg.pack()

    #confirm button for confiorm window
    def __sendConfirm(self, window, status):
        #creates button
        self.send_button = tk.Button(window, text="Confirm", command = partial(self.__close, window, status))
        #puts on screen
        self.send_button.pack()

    #sets size of the window    
    def __setSize(self):
        #size measurements
        self.__master.minsize(350,350)

    #close button
    def __close_button(self, window):
        #gets rid of status so it doesn't post status over close func
        status = ""
        #creates close button
        self.close_button = tk.Button(window, text="Close Button", command = partial(self.__close, window, status))
        #puts it on the window
        self.close_button.pack(pady = 0)
    
    #send button
    def __send_button(self, status):
        #creation
        self.send_button = tk.Button(window, text="Send Tweet", command = partial(self.__sendClick, status)) 
        #adds it to the window and padding
        self.send_button.pack(pady = 20)

    #click func for main
    def __sendClick(self, status):
        #takes input
        status = status.get(1.0, "end-1c")
        #puts input into the confirm msg
        self.__confirmWindow(status)

    #create label func
    def __create_label(self, text):
        #creation
        self.label = tk.Label(window, text=text)
        #puts on screen
        self.label.pack(pady = 10)

    #input box
    def __create_TextBox(self):
        #creation and size
        self.e = tk.Text(height = 10, width = 40)
        #puts on screen
        self.e.pack()
        #return the input
        return self.e

    #close func
    def __close(self, window, status):
        #distroy main window
        window.destroy()
        #if its the confirm window it sets the status as well
        if str(window) == ".!toplevel":
            setStatus(status)
               

def main():
    #pushes window into the class
    Gui(window)
    #starts the bot thread
    continuousRun()
    #starts the window
    window.mainloop() 
 #starts main func   
main()