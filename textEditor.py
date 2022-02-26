import os
from tkinter import (
    END,
    BooleanVar,
    Button,
    Checkbutton,
    Entry,
    Label,
    Tk,
    Menu,
    PhotoImage,
    Frame,
    Text,
    Scrollbar,
    IntVar,
    StringVar,
    Toplevel,
    filedialog,
    messagebox,
)
import tkinter
from xmlrpc.client import Boolean


root = Tk()
PROGRAM_NAME = "The Text Editor"
root.title(PROGRAM_NAME)
root.geometry("400x400")

content_text = Text(root, wrap="word", undo=1)
# creatng events
def cut():
    content_text.event_generate("<<Cut>>")
    on_content_changed()
    return "break"


def copy():
    content_text.event_generate("<<Copy>>")
    on_content_changed()
    return "break"


def paste():
    content_text.event_generate("<<Paste>>")
    on_content_changed()
    return "break"


def undo():
    content_text.event_generate("<<Undo>>")
    return "break"


def redo(event=None):
    content_text.event_generate("<<Redo>>")
    return "break"


def select_all(event=None):
    content_text.tag_add("sel", "1.0", "end")
    return "break"


def find_text(event=None):
    search_toplevel = Toplevel(root)
    search_toplevel.title("Find Text")
    search_toplevel.transient(root)
    search_toplevel.resizable(False, False)
    Label(search_toplevel, text="Find All : ").grid(column=0, row=0, sticky="e")
    search_entry = Entry(search_toplevel, width=25)
    search_entry.grid(column=1, row=0, padx=2, pady=2, sticky="we")
    search_entry.focus_set()
    ignore_case_value = IntVar()
    ignore_case_value.set(1)
    Checkbutton(
        search_toplevel,
        text="ignore case",
        variable=ignore_case_value,
        background="white",
        foreground="black",
    ).grid(column=3, row=1, sticky="e")
    Button(
        search_toplevel,
        text="Find All",
        underline=0,
        command=lambda: search_output(
            search_entry.get(),
            ignore_case_value.get(),
            content_text,
            search_toplevel,
            search_entry,
        ),
    ).grid(row=0, column=7, padx=2, pady=2, sticky="e" + "w")

    def close_search_window():
        content_text.tag_remove("match", "1.0", END)
        search_toplevel.destroy()

    search_toplevel.protocol("WM_DELETE_WINDOW", close_search_window)
    return "break"


def search_output(needle, if_ignore_case, content_text, search_toplevel, search_box):
    content_text.tag_remove("match", "1.0", END)
    matches_found = 0
    if needle:
        start_pos = "1.0"
        while True:
            start_pos = content_text.search(
                needle, start_pos, nocase=if_ignore_case, stopindex=END
            )
            if not start_pos:
                break
            end_pos = "{}+{}c".format(start_pos, len(needle))
            content_text.tag_add("match", start_pos, end_pos)
            matches_found += 1
            start_pos = end_pos
        content_text.tag_config("match", foreground="red", background="yellow")
    search_box.focus_set()
    search_toplevel.title("{} matches found".format(matches_found))


file_name = None


def new_file(event=None):
    global file_name
    root.title("Untitled")
    file_name = None
    content_text.delete(1.0, END)


def open_file(event=None):
    input_file_name = filedialog.askopenfilename(
        defaultextension=".txt",
        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")],
    )
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title("{} - {}".format(os.path.basename(file_name), PROGRAM_NAME))
        content_text.delete("1.0", END)

        with open(file_name) as _file:
            content_text.insert(1.0, _file.read())


def save(event=None):
    global file_name
    if not file_name:
        save_as()
    else:
        filedialog.write_to_file(file_name)
    return "break"


def save_as(event=None):
    input_file_name = tkinter.filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("All Files", "*.*"), ("Text Documents", "*.txt")],
    )
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title("{} - {}".format(os.path.basename(file_name), PROGRAM_NAME))
    return "break"


def write_to_file(file_name):
    try:
        content = content_text.get(1.0, END)
        with open(file_name, "w") as the_file:
            the_file.write(content)
    except IOError:
        pass


def display_about_messagebox(event=None):
    messagebox.showinfo("About", f"{PROGRAM_NAME} My Tkinter Project")


def display_help_messagebox(event=None):
    messagebox.showinfo("Help", "There is no Help!", icon="question")

def exit_program(event=None):
    if messagebox.askokcancel("Quit", "Really Quit?"):
        root.destroy()

## function for line numbering
def on_content_changed(event=None):
    update_line_numbers()
    select_theme()

def get_line_numbers(event=None):
    output = ""
    if show_line_number:
        row, col  = content_text.index("end").split(".")
        for i in range(1, int(row)):
            output += str(i) + "\n"
    return output

def update_line_numbers(event=None):
    line_numbers = get_line_numbers()
    number_line.config(state="normal")
    number_line.delete("1.0", "end")
    number_line.insert('1.0', line_numbers)
    number_line.config(state="disabled")

def highlight_line(interval=100):
    content_text.tag_remove("active_line", 1.0, "end")
    content_text.tag_add("active_line", "insert linestart", "insert lineend+1c")
    content_text.after(interval, toggle_highlight)

def undo_highlight():
    content_text.tag_remove("active_line", 1.0, "end")

def toggle_highlight():
    if to_highlight_line.get():
        highlight_line
    else:
        undo_highlight

def select_theme(event=None):
    selected_theme = color_choice.get()
    fg_bg_colors = color_schemes.get(selected_theme)
    background, foreground = fg_bg_colors.split(".")
    content_text.config(background=background, foreground=foreground)

new_file_icon = PhotoImage(file="icons/new_file.gif")
open_file_icon = PhotoImage(file="icons/open_file.gif")
cut_file_icon = PhotoImage(file="icons/cut.gif")
copy_file_icon = PhotoImage(file="icons/copy.gif")
paste_file_icon = PhotoImage(file="icons/paste.gif")
undo_file_icon = PhotoImage(file="icons/undo.gif")
redo_file_icon = PhotoImage(file="icons/redo.gif")
save_file_icon = PhotoImage(file="icons/save.gif")


menu_bar = Menu(root)

# file menu

file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(
    label="New",
    accelerator="Ctrl+N",
    compound="left",
    image=new_file_icon,
    underline=0,
    command=new_file,
)
file_menu.add_command(
    label="Open",
    accelerator="Ctrl+O",
    compound="left",
    image=open_file_icon,
    underline=0,
    command=open_file,
)
file_menu.add_command(
    label="Save",
    accelerator="Ctrl+S",
    compound="left",
    image=save_file_icon,
    underline=0,
    command=save,
)
file_menu.add_command(
    label="Save As", accelerator="Ctrl+Shift+S", underline=0, command=save_as
)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator="Alt+F4", underline=0, command=exit_program)
menu_bar.add_cascade(label="File", menu=file_menu)  # adding menu-tems to the menu_bar

# edit menu
edit_menu = Menu(menu_bar, tearoff=0)
edit_menu.add_command(
    label="Undo",
    accelerator="Ctrl+Z",
    compound="left",
    image=undo_file_icon,
    underline=0,
    command=undo,
)
edit_menu.add_command(
    label="Redo",
    accelerator="Ctrl+Y",
    compound="left",
    image=redo_file_icon,
    underline=0,
    command=redo,
)
edit_menu.add_separator()
edit_menu.add_command(
    label="Cut",
    accelerator="Ctrl+X",
    compound="left",
    image=cut_file_icon,
    underline=0,
    command=cut,
)
edit_menu.add_command(
    label="Copy",
    accelerator="Ctrl+C",
    compound="left",
    image=copy_file_icon,
    underline=0,
    command=copy,
)
edit_menu.add_command(
    label="Paste",
    accelerator="Ctrl+V",
    compound="left",
    image=paste_file_icon,
    underline=0,
    command=paste,
)
edit_menu.add_separator()
edit_menu.add_command(
    label="Find", accelerator="Ctrl+F", underline=0, command=find_text
)
edit_menu.add_separator()
edit_menu.add_command(
    label="Select All", accelerator="Ctrl+A", underline=0, command=select_all
)
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# view menu
view_menu = Menu(menu_bar, tearoff=0)
show_line_number = IntVar()
show_line_number.set(1)
view_menu.add_checkbutton(
    label="Show Line Number", variable=show_line_number, foreground="white"
)
show_cursor_info = IntVar()
show_cursor_info.set(1)
view_menu.add_checkbutton(
    label="Show Cursor Location At Bottom",
    variable=show_cursor_info,
    foreground="white",
)
to_highlight_line = BooleanVar()
view_menu.add_checkbutton(
    label="Highlight Current Line",
    onvalue=1,
    offvalue=0,
    variable=to_highlight_line,
    foreground="white",
)
themes_menu = Menu(menu_bar, tearoff=0)
color_choice = StringVar()
view_menu.add_cascade(label="Themes", menu=themes_menu, command=color_choice)

# adding the color scehems
color_schemes = {
    "Default": "#000000.#FFFFFF",
    "Greygarious": "#83406A.#D1D4D1",
    "Aquamarine": "#5B8340.#D1E7E0",
    "Bold Beige": "#4B4620.#FFF0E1",
    "Cobalt Blue": "#ffffBB.#3333aa",
    "Olive Green": "#D1E7E0.#5B8340",
    "Night Mode": "#FFFFFF.#000000",
}
color_choice = StringVar()
color_choice.set("Default")
for k in sorted(color_schemes):
    themes_menu.add_radiobutton(label=k, variable=color_choice)

menu_bar.add_cascade(label="View", menu=view_menu)

# about menu
about_menu = Menu(menu_bar, tearoff=0)
about_menu.add_command(label="About", underline=0, command=display_about_messagebox)
about_menu.add_command(label="Help" ,underline=0, command=display_help_messagebox)
menu_bar.add_cascade(label="About", menu=about_menu)

# shortcut bar
shortcut_bar = Frame(root, background="#9F68B4", height=25)

#adding icons to the shortcut bar
icons = ("save", "paste", "copy", "undo", "redo", "cut", "open_file", "new_file","find_text")
for i, icon in enumerate(icons):
    tool_bar_icon = PhotoImage(file=f"icons/{icon}.gif")
    cmd = eval(icon)
    tool_bar = Button(shortcut_bar, image=tool_bar_icon, command=cmd)
    tool_bar.image = tool_bar_icon
    tool_bar.pack(side="left")
shortcut_bar.pack(fill="x", expand="no")
# number line
number_line = Text(
    root,
    background="#7A8942",
    width=4,
    padx=4,
    takefocus=0,
    state="disabled",
    wrap="none",
    border=0,
)
number_line.pack(fill="y", side="left")

# main text widget
content_text = Text(root, wrap="word", undo=1)
content_text.focus_set()
content_text.pack(fill="both", expand="yes")
# create scrollbar
scroll_bar = Scrollbar(content_text)
content_text.configure(
    yscrollcommand=scroll_bar.set
)  # scrollbar configured to yview of text
scroll_bar.configure(command=content_text.yview)  # text connected to scrollbar
scroll_bar.pack(side="right", fill="y")
root.config(menu=menu_bar)

# handling the redo issue
content_text.bind("<Control-y>", redo)
content_text.bind("<Control-Y>", redo)

# binding the Ctrl + A shortcut to the text
content_text.bind("<Control-a>", select_all)
content_text.bind("<Control-A>", select_all)
content_text.tag_config("sel", background="#B2B22E")  # adding the highlight color

# binding Ctrl+F
content_text.bind("<Control-f>", find_text)
content_text.bind("<Control-F>", find_text)
content_text.bind("<Control-o>", open_file)
content_text.bind("<Control-O>", open_file)
content_text.bind("<Control-s>", save)
content_text.bind("<Control-S>", save)
content_text.bind("<Control-Shift-s>", save_as)
content_text.bind("<Control-Shift-S>", save_as)
content_text.bind("<Control-n>", new_file)
content_text.bind("<Control-N>", new_file)
content_text.bind("<KeyPress-F1>", display_help_messagebox)
content_text.bind("<Any-KeyPress>", on_content_changed)
root.mainloop()
