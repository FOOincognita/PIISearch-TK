"""
    @File: PIISearch.py
    @Author: Archer Simmons, UGTA
    @Contact: Archer.Simmons@tamu.edu 
        > Mobile: 832 <dash> 433 <dash> 2245  
"""

try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
except:
    pass


from tkinter import filedialog, ttk, messagebox
from tkinter.font import Font
import tkinter as tk
import pandas as pd
import threading


## ____________________ GUI Classes ____________________ ##
class Application(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #* Global Settings
        self.title("PII-Search")
        self.geometry('1060x640')
        
        self.configure(bg = 'grey14')
        self.style = ttk.Style()
        self.style.theme_use('alt')
        
        #* Button Style
        self.style.configure(
            "TButton",
            background  = 'grey10',
            foreground  = 'white',
            bordercolor = 'grey16',
            relief      = 'flat',
            font        = ('Helvetica', 11)
        )
        self.style.map(
            'TButton', 
            background = [('active', 'grey14')]
        )

        #* Label Style
        self.style.configure(
            "TLabel",
            background  = 'grey14',
            foreground  = 'white',
            relief      = 'flat',
            font        = ('Helvetica', 11)
        )
        
        #* Frame Style
        self.style.configure(
            "TFrame",
            background = 'grey14',
            relief     = 'flat'
        )
        
        #* Tree-View Style
        self.style.configure(
            "Treeview.Heading",
            background     = 'grey10',
            foreground     = 'white',
            bordercolor    = 'grey10',
            highlightcolor = 'grey16',
            relief         = 'flat',
            font           = ('Helvetica', 11),
            justify        = 'left'
        )
        self.style.configure(
            "Treeview", 
            background      = "grey16", 
            fieldbackground = "grey16", 
            foreground      = "white",
            relief          = "flat",
            font            = ('Helvetica', 11)
        )
        
        #* Button Style
        self.style.configure(
            "TEntry",
            background      = 'blue',
            fieldbackground = "grey16",
            foreground      = 'white',
            relief          = 'flat',
            font            = ('Helvetica', 11)
        )
        
        #* Button Style
        self.style.configure(
            "TScrollbar",
            background       = 'grey10',
            fieldbackground  = "purple",
            foreground       = 'yellow',
            relief           = 'flat',
            arrowcolor       = 'white',
            activerelief     = 'flat',
            troughcolor      = 'grey16',
            troughrelief     = 'flat',
            activebackground = 'red'
            
        )

        #* Labels Vars
        self.csvPath = tk.StringVar()
        
        #* Pandas DataFrame
        self.df = pd.DataFrame()
        
        #* Init all widgets
        self.create_widgets()


    def create_widgets(self):
        """ Init all widgets in GUI """
        main_frame = ttk.Frame(self)
        main_frame.pack(side="top", padx=10, pady=10, anchor="nw")

        #* Frame for name entry
        name_frame = ttk.Frame(main_frame)
        name_frame.pack(side="left", padx=10)

        ttk.Label(name_frame, text="Name").pack(side="left", anchor="w", padx=10)
        self.name_entry = ttk.Entry(name_frame, validate="key", width=25)
        self.name_entry.pack()
        self.name_entry.bind("<KeyRelease>", self.update_results)

        #* Frame for SID entry
        sid_frame = ttk.Frame(main_frame)
        sid_frame.pack(side="left", padx=10)

        ttk.Label(sid_frame, text="UIN").pack(side="left", anchor="w", padx=10)
        self.sid_entry = ttk.Entry(sid_frame, validate="key", width=25)
        self.sid_entry.pack()
        self.sid_entry.bind("<KeyRelease>", self.update_results)
        
        #* Frame for Submission ID entry
        subID_frame = ttk.Frame(main_frame)
        subID_frame.pack(side="left", padx=10)

        ttk.Label(subID_frame, text="Submission ID").pack(side="left", anchor="w", padx=10)
        self.subID_entry = ttk.Entry(subID_frame, validate="key", width=25)
        self.subID_entry.pack()
        self.subID_entry.bind("<KeyRelease>", self.update_results)        
        

        #* Frame for load button
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(side="left", padx=10)

        load_button = ttk.Button(button_frame, text="Load CSV", command=self.load_csv)
        load_button.pack(side="left", anchor="w", padx=10)


        #* Frame for Treeview and Scrollbar
        tree_frame = ttk.Frame(self)
        tree_frame.pack(padx=10, pady=10, expand=True, fill="both")
    
        #* Treeview for results
        self.result_tree = ttk.Treeview(
            tree_frame, 
            columns = ("1", "2", "3", "4", "5", "6"), 
            show    = 'headings',
            #selectmode='browse'
        )
        self.result_tree.heading("1", text="First Name", anchor='w')
        self.result_tree.column( "1", minwidth=100, width=150)
        self.result_tree.heading("2", text="Last Name", anchor='w')
        self.result_tree.column( "2", minwidth=100, width=150)
        self.result_tree.heading("3", text="Submission ID", anchor='w')
        self.result_tree.column( "3", minwidth=100, width=125)
        self.result_tree.heading("4", text="UIN", anchor='w')
        self.result_tree.column( "4", minwidth=100, width=125)
        self.result_tree.heading("5", text="Email", anchor='w')
        self.result_tree.column( "5", minwidth=225, width=250)
        self.result_tree.heading("6", text="Sections", anchor='w')
        self.result_tree.column( "6", minwidth=200, width=200)
        
        
        #* Scrollbar for Treeview
        self.scrollbar = ttk.Scrollbar(tree_frame, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=self.scrollbar.set)

        self.result_tree.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y", padx=(0, 10))


    #> -------------------- PIISearch Main -------------------- <#
    def update_results(self, event=None):
        """ Start a new thread to perform the search """
        threading.Thread(target=self.search).start()

    def search(self):
        """ Search entries for match """
        name_search = self.name_entry.get()
        sid_search = self.sid_entry.get()
        subID_search = self.subID_entry.get()

        # Filter dataframe by input
        df_filtered = self.df[
            (self.df["First Name"].str.contains(name_search, case=0, na=0) | 
            (self.df["Last Name"].str.contains(name_search, case=0, na=0))) & 
            (self.df["SID"].str.contains(sid_search, na=0) if sid_search else 1) &
            (self.df["Submission ID"].str.contains(subID_search, na=0) if subID_search else 1)
        ]

        # Update the results in the main GUI thread
        self.after(0, self.display_results, df_filtered)


    def display_results(self, results):
        # Delete previous results
        for row in self.result_tree.get_children():
            self.result_tree.delete(row)

        # Insert new results
        for _, row in results.iterrows():
            self.result_tree.insert('', 'end', 
                values=(row['First Name'], row['Last Name'], row['Submission ID'], row['SID'], row['Email'], row['Sections']))


    def load_csv(self):
        csv_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if csv_path:
            try:
                self.df = pd.read_csv(csv_path)
                self.df = self.df[self.df['Status'] != 'Missing'] # exclude rows with 'Missing' status

                self.df["SID"] = self.df["SID"].fillna(-1).astype(int).astype(str)
                self.df.loc[self.df["SID"] == "-1", "SID"] = ""  # replace the placeholder with empty string
                
                self.df["Submission ID"] = self.df["Submission ID"].fillna(-1).astype(int).astype(str)
                self.df.loc[self.df["Submission ID"] == "-1", "Submission ID"] = ""  # replace the placeholder with empty string
                
                self.df["Sections"] = self.df["Sections"].fillna("None")

                self.update_results()
                
            except Exception as e:
                messagebox.showerror("Error", "Could not load file: " + str(e))


if __name__ == "__main__":
    app = Application()
    app.mainloop()