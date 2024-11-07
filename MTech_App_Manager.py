import customtkinter as ctk
import json
from tkinter import messagebox
from tkinter import filedialog
import os
import sys

class AppManager:
    def __init__(self):
        # Set dark theme with orange accent
        ctk.set_appearance_mode("dark")
        
        # Initialize apps dictionary before loading
        self.apps = {}
        
        # Initialize main window
        self.window = ctk.CTk()
        self.window.title("MTech App Manager")
        self.window.geometry("600x500")
        
        # Load saved apps
        self.load_apps()
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        # Title label
        title_label = ctk.CTkLabel(
            self.window,
            text="App Manager",
            font=("Arial", 24, "bold"),
            text_color="#f79505"  # Bright orange
        )
        title_label.pack(pady=10)
        
        # Input frame
        input_frame = ctk.CTkFrame(
            self.window
        )
        input_frame.pack(pady=10, padx=10, fill="x")
        
        # Path entry and browse button frame
        path_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        path_frame.pack(fill="x", pady=5)
        
        self.path_entry = ctk.CTkEntry(
            path_frame,
            width=400,
            placeholder_text="App path (or click Browse)"
        )
        self.path_entry.pack(side="left", padx=5, expand=True, fill="x")
        
        browse_button = ctk.CTkButton(
            path_frame,
            text="Browse",
            command=self.browse_app,
            width=100,
            fg_color="#FF6B00",  # Normal orange
            hover_color="#FF8C44"  # Bright orange
        )
        browse_button.pack(side="right", padx=5)
        
        self.name_entry = ctk.CTkEntry(
            input_frame,
            width=200,
            placeholder_text="Enter app name"
        )
        self.name_entry.pack(side="left", padx=5, expand=True, fill="x")

        # Add button
        add_button = ctk.CTkButton(
            input_frame,
            text="Add App",
            command=self.add_app,
            fg_color="#FF6B00",  # Normal orange
            hover_color="#FF8C44"  # Bright orange
        )
        add_button.pack(pady=10, side="right")
        
        # List frame
        list_frame = ctk.CTkFrame(self.window)
        list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Scrollable frame for app list
        list_label = ctk.CTkLabel(
            list_frame,
            text="Your Apps",
            font=("Arial", 16, "bold"),
            text_color="#f79505"  # Bright orange
        )
        list_label.pack(pady=5)
        
        self.app_list_frame = ctk.CTkScrollableFrame(
            list_frame
        )
        self.app_list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Update the app list display
        self.update_app_list()
        
    def browse_app(self):
        if sys.platform == "win32":
            initial_dir = "C:\\Program Files"
            file_types = [("Executable files", "*.exe")]
        elif sys.platform == "darwin":
            initial_dir = "/Applications"
            file_types = [("Applications", "*.app")]
        else:
            initial_dir = "/usr/bin"
            file_types = [("All files", "*")]
            
        filepath = filedialog.askopenfilename(
            title="Select Application",
            initialdir=initial_dir,
            filetypes=file_types
        )
        
        if filepath:
            self.path_entry.delete(0, 'end')
            self.path_entry.insert(0, filepath)
            
            # Auto-fill name if empty
            if not self.name_entry.get().strip():
                suggested_name = os.path.splitext(os.path.basename(filepath))[0]
                self.name_entry.delete(0, 'end')
                self.name_entry.insert(0, suggested_name)
            
    def add_app(self):
        app_name = self.name_entry.get().strip()
        app_path = self.path_entry.get().strip()
        
        if not app_name:
            messagebox.showwarning("Warning", "Please enter an app name!")
            return
            
        if not app_path:
            messagebox.showwarning("Warning", "Please select an app file!")
            return
            
        if not os.path.exists(app_path):
            messagebox.showwarning("Warning", "The specified file does not exist!")
            return
            
        if app_name in self.apps:
            confirm = messagebox.askyesno("Warning", 
                "An app with this name already exists. Do you want to update its path?")
            if not confirm:
                return
                
        self.apps[app_name] = app_path
        self.save_apps()
        self.update_app_list()
        self.name_entry.delete(0, 'end')
        self.path_entry.delete(0, 'end')
            
    def remove_app(self, app_name):
        if app_name in self.apps:
            del self.apps[app_name]
            self.save_apps()
            self.update_app_list()
        
    def update_app_list(self):
        # Clear all widgets in the scrollable frame
        for widget in self.app_list_frame.winfo_children():
            widget.destroy()
            
        # Add app items with buttons
        for app_name, app_path in self.apps.items():
            app_frame = ctk.CTkFrame(
                self.app_list_frame
            )
            app_frame.pack(fill="x", pady=2, padx=5)
            
            # Name and path labels
            name_label = ctk.CTkLabel(
                app_frame,
                text=app_name,
                font=("Arial", 12, "bold"),
                text_color="#FF8C44",  # Bright orange
                anchor="w"
            )
            name_label.pack(side="left", padx=5)
            
            # Buttons frame
            buttons_frame = ctk.CTkFrame(app_frame, fg_color="transparent")
            buttons_frame.pack(side="right", padx=5)
            
            launch_button = ctk.CTkButton(
                buttons_frame,
                text="Launch",
                command=lambda p=app_path: self.launch_app(p),
                width=80,
                height=25,
                fg_color="#FF6B00",  # Normal orange
                hover_color="#FF8C44"  # Bright orange
            )
            launch_button.pack(side="left", padx=2)
            
            remove_button = ctk.CTkButton(
                buttons_frame,
                text="Remove",
                command=lambda n=app_name: self.remove_app(n),
                width=80,
                height=25,
                fg_color="#FF6B00",  # Normal orange
                hover_color="#FF8C44"  # Bright orange
            )
            remove_button.pack(side="left", padx=2)
            
    def launch_app(self, app_path):
        try:
            if sys.platform == "win32":
                os.startfile(app_path)
            elif sys.platform == "darwin":
                os.system(f"open '{app_path}'")
            else:
                os.system(f"xdg-open '{app_path}'")
        except Exception as e:
            messagebox.showerror("Error", f"Could not launch app: {str(e)}")
            
    def save_apps(self):
        try:
            with open("apps.json", "w") as f:
                json.dump(self.apps, f)
        except Exception as e:
            messagebox.showerror("Error", f"Could not save apps: {str(e)}")
            
    def load_apps(self):
        try:
            with open("apps.json", "r") as f:
                loaded_apps = json.load(f)
                if isinstance(loaded_apps, dict):
                    self.apps = loaded_apps
                else:
                    self.apps = {}
        except FileNotFoundError:
            self.apps = {}
        except Exception as e:
            messagebox.showerror("Error", f"Could not load apps: {str(e)}")
            self.apps = {}
            
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = AppManager()
    app.run()