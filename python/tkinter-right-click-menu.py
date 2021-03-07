from tkinter import *

root = Tk()
root.title('Right Click Menu Popups With Tkinter')
root.geometry("500x500")

my_label = Label(root,text="", font=("Helvetica", 20))
my_label.pack(pady=20)

def hello():
    my_label.config(text="Hello World!!")


def goodbye():
    my_label.config(text="Bye!!")


def my_popup(e):
    my_menu.tk_popup(e.x_root, e.y_root)

# Create A Menu


my_menu = Menu(root, tearoff=False)
my_menu.add_command(label="Say Hello", command=hello)
my_menu.add_command(label="Say GoodBye", command=goodbye)
my_menu.add_separator()
my_menu.add_command(label="Exit", command=root.quit)

root.bind("<Button-3>", my_popup)


root.mainloop()
