import tkinter as tk
from tkinter import ttk 
from tkinter import messagebox
from Crawl.compare import compare
from Crawl.crawl import crawl_data

OPTION_LIST = [
    "Invoice Details vs Promotion",
    "TXN_NOTEHDR_CP vs INVOICE_HDR",
    "Promotion vs OPI",
    "CRM vs Promotion",
    "CL02 vs Promotion"
]

def process_button(status_login, option: str) -> None:
    """
    Crawl vs process data
    
    Args:
        option: int
            option in theme where 2 source to compare

    Returns:
        None
    """ 

    try:
        crawl_data(status_login=status_login.get(), option = option)
        status_login.set(True)
        messagebox.showinfo("showinfo", "Done")
    except:
        messagebox.showerror("showerror", "Error") 

def compare_button(option: int) -> None:
    """
    Compare 2 source export to file
    
    Args:
        option: int
            option in theme where 2 source to compare

    Returns:
        None
    """  
    try:
        compare(option=option)
        messagebox.showinfo("showinfo", "Done")
    except Exception as e:
        messagebox.showerror(e, "Error") 

def process_theme() -> None:
    """
    process click button take value from combo box

    Returns:
        None
    """  

    win = tk.Tk()
    
    status_login = tk.BooleanVar()
    status_login.set(False)
    # win.geometry(f'{width}x{height}') 
    process=tk.Button(
        win, 
        text = "Process", 
        bg = "yellow",
        font = "25", 
        command = lambda:process_button(
            status_login=status_login,
            option = choosen.get()
        )
    )
    process.grid(row=1, column=1, padx = 20,pady=10)

    start=tk.Button(
        win, 
        text = "Run",
        bg = "green",
        font = "25",
        width = 5, 
        command = lambda:compare_button(
            option = OPTION_LIST.index(
                choosen.get()
            ) + 1
        ) 
    )
    start.grid(row=2, column=1, padx = 20,pady=10)

    ttk.Label(win, text = "Select Report :", 
            font = ("Times New Roman", 20)).grid(column = 2, 
            row = 1, padx = 10, pady = 10) 

    choosen = ttk.Combobox(win, width = 25,font=25, textvariable = tk.Listbox()) 
    
    # Adding combobox drop down list 
    choosen['values'] = OPTION_LIST

    choosen.grid(column = 2, row = 2, padx = 20,pady=10) 
    choosen.current(0)

    win.eval('tk::PlaceWindow . center')
    win.mainloop()