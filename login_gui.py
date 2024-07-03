from dataclasses import dataclass

from tkinter import Tk, StringVar, Label, Entry, Button

@dataclass
class LoginApp:
    root: Tk

    def __post_init__(self):
        self.root.title("Database Configuration")
        self.drivername = StringVar()
        self.host = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.database = StringVar()
        self.create_widgets()
        self.load_existing_config()
    
    def create_widgets(self) -> None:
        Label(self.root, text="Driver Name:").grid(row=0, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.drivername).grid(row=0, column=1, padx=10, pady=5)

        Label(self.root, text="Host:").grid(row=1, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.host).grid(row=1, column=1, padx=10, pady=5)

        Label(self.root, text="Username:").grid(row=2, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.username).grid(row=2, column=1, padx=10, pady=5)

        Label(self.root, text="Password:").grid(row=3, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.password, show='*').grid(row=3, column=1, padx=10, pady=5)

        Label(self.root, text="Database:").grid(row=4, column=0, padx=10, pady=5)
        Entry(self.root, textvariable=self.database).grid(row=4, column=1, padx=10, pady=5)

        Button(self.root, text="Save", command=self.save_config).grid(row=5, column=0, columnspan=2, pady=10)
