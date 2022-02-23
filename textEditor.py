
from tkinter import Tk, Menu, PhotoImage, Frame, Text, Scrollbar, IntVar, StringVar


root = Tk()
PROGRAM_NAME = "The Text Editor"
root.title(PROGRAM_NAME)
root.geometry('400x400')

new_file_icon = PhotoImage(file="icons/new_file.gif")
open_file_icon = PhotoImage(file="icons/open_file.gif")
cut_file_icon = PhotoImage(file="icons/cut.gif")
copy_file_icon = PhotoImage(file="icons/copy.gif")
paste_file_icon = PhotoImage(file="icons/paste.gif")
undo_file_icon = PhotoImage(file="icons/undo.gif")
redo_file_icon = PhotoImage(file="icons/redo.gif")
save_file_icon = PhotoImage(file="icons/save.gif")


menu_bar = Menu(root)

#file menu

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", accelerator="Ctrl+N", compound="left", image=new_file_icon , underline=0)
file_menu.add_command(label="Open", accelerator="Ctrl+O", compound="left", image=open_file_icon , underline=0)
file_menu.add_command(label="Save", accelerator="Ctrl+S", compound="left", image=save_file_icon , underline=0)
file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", underline=0)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator="Alt+F4",underline=0)
menu_bar.add_cascade(label='File', menu=file_menu) #adding menu-tems to the menu_bar

#edit menu
edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", compound="left", image=undo_file_icon , underline=0)
edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", compound="left", image=redo_file_icon , underline=0)
edit_menu.add_separator()
edit_menu.add_command(label="Cut", accelerator="Ctrl+X", compound="left", image=cut_file_icon , underline=0)
edit_menu.add_command(label="Copy", accelerator="Ctrl+C", compound="left", image=copy_file_icon , underline=0)
edit_menu.add_command(label="Paste", accelerator="Ctrl+V", compound="left", image=paste_file_icon , underline=0)
edit_menu.add_separator()
edit_menu.add_command(label="Find", accelerator="Ctrl+F", underline=0)
edit_menu.add_separator()
edit_menu.add_command(label="Select All", accelerator="Ctrl+A",underline=0)
menu_bar.add_cascade(label='Edit', menu=edit_menu)

#view menu
view_menu = Menu(menu_bar, tearoff=0)
show_line_number = IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(label="Show Line Number", variable=show_line_number, foreground='white')
show_cursor_info = IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(label="Show Cursor Location At Bottom", variable=show_cursor_info, foreground='white')
highlight_line = IntVar()
view_menu.add_checkbutton(label="Highlight Current Line", onvalue=1, offvalue=0, variable=highlight_line, foreground='white')
themes_menu = Menu(menu_bar, tearoff=0)
view_menu.add_cascade(label="Themes", menu=themes_menu)

#adding the color scehems
color_schemes = {
    'Default': '#000000.#FFFFFF',
    'Greygarious': '#83406A.#D1D4D1',
    'Aquamarine': '#5B8340.#D1E7E0',
    'Bold Beige': '#4B4620.#FFF0E1',
    'Cobalt Blue': '#ffffBB.#3333aa',
    'Olive Green': '#D1E7E0.#5B8340',
    'Night Mode': '#FFFFFF.#000000',
}
color_choice = StringVar()
color_choice.set('Default')
for k in sorted(color_schemes):
    themes_menu.add_radiobutton(label=k, variable=color_choice)

menu_bar.add_cascade(label='View', menu=view_menu)

#about menu
about_menu = Menu(menu_bar, tearoff=0)
about_menu.add_command(label="About", underline=0)
about_menu.add_command(label="Help", underline=0)
menu_bar.add_cascade(label='About', menu=about_menu)

#shortcut bar
shortcut_bar = Frame(root, background='#9F68B4', height=25)
shortcut_bar.pack(fill='x', expand='no')

#number line
number_line = Text(root, background='#7A8942', width=4, padx=4,takefocus=0, state='disabled', wrap='none', border=0)
number_line.pack(fill='y', side='left')

#main text widget
content_text = Text(root, wrap='word')
content_text.pack(fill='both', expand='yes')
#create scrollbar
scroll_bar = Scrollbar(content_text)
content_text.configure(yscrollcommand=scroll_bar.set) # scrollbar configured to yview of text
scroll_bar.configure(command=content_text.yview) # text connected to scrollbar
scroll_bar.pack(side='right', fill='y')
root.config(menu=menu_bar)

root.mainloop()
