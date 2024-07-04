from dataclasses import dataclass
import os
import json

from tkinter import Tk, StringVar, Label, Entry, Button, messagebox

CONFIG_FILE = 'config.json'

def save_config(config) -> None:
    with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
        json.dump(config, file, indent=4)
    
def load_config() -> (dict | None):
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return None


@dataclass
class ConfigApp:
    root: Tk

    def __post_init__(self):
        self.root.resizable(False, False)
        self.root.title("Configuration")
        self.drivername = StringVar()
        self.host = StringVar()
        self.username = StringVar()
        self.password = StringVar()
        self.database = StringVar()
        self.create_widgets()
        self.load_existing_config()
    
    def create_widgets(self) -> None:
        Label(self.root, text="Driver Name:").grid(row=0, column=0, padx=10, pady=5)
        self.drivername_entry = Entry(self.root, textvariable=self.drivername)
        self.drivername_entry.grid(row=0, column=1, padx=10, pady=5)

        Label(self.root, text="Host:").grid(row=1, column=0, padx=10, pady=5)
        self.host_entry = Entry(self.root, textvariable=self.host)
        self.host_entry.grid(row=1, column=1, padx=10, pady=5)

        Label(self.root, text="Username:").grid(row=2, column=0, padx=10, pady=5)
        self.username_entry = Entry(self.root, textvariable=self.username)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5)

        Label(self.root, text="Password:").grid(row=3, column=0, padx=10, pady=5)
        self.password_entry = Entry(self.root, textvariable=self.password, show='*')
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)

        Label(self.root, text="Database:").grid(row=4, column=0, padx=10, pady=5)
        self.database_entry = Entry(self.root, textvariable=self.database)
        self.database_entry.grid(row=4, column=1, padx=10, pady=5)

        self.clear_button = Button(self.root, text="Clear", command=self.clear_fields)
        self.clear_button.grid(row=5, column=0, pady=10, padx=10)

        self.save_button = Button(self.root, text="Save", command=self.save_config)
        self.save_button.grid(row=5, column=1, pady=10, padx=10)

    def clear_fields(self) -> None:
        self.drivername_entry.delete(0, 'end')
        self.host_entry.delete(0, 'end')
        self.username_entry.delete(0, 'end')
        self.password_entry.delete(0, 'end')
        self.database_entry.delete(0, 'end')

    def load_existing_config(self) -> None:
        config = load_config()
        if config:
            self.drivername.set(config.get('drivername', ''))
            self.host.set(config.get('host', ''))
            self.username.set(config.get('username', ''))
            self.password.set(config.get('password', ''))
            self.database.set(config.get('database', ''))

    def save_config(self) -> None:
        config = {
            'drivername': self.drivername.get(),
            'host': self.host.get(),
            'username': self.username.get(),
            'password': self.password.get(),
            'database': self.database.get()
        }
        save_config(config)
        messagebox.showinfo("Info", "Configuration saved successfully!")
        self.root.destroy()

def run_config_app() -> None:
    root = Tk()
    ConfigApp(root)
    root.mainloop()
