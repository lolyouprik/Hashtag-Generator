import os
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class HashtagGenerator:
    def __init__(self):
        # Initialize settings with defaults
        self.settings = {
            "remove_special_chars": True,
            "capitalize_first_letter": True,
            "history_max_items": 10,
            "theme": "light"
        }
        self.history = []
        self.load_settings()
    
    def generate_hashtag(self, text):
        """Transform input text into a hashtag format"""
        if not text:
            return ""
            
        # Remove special characters if enabled
        if self.settings["remove_special_chars"]:
            # Keep alphanumeric and spaces only
            text = ''.join(c for c in text if c.isalnum() or c.isspace())
        
        # Capitalize first letter of each word if enabled
        if self.settings["capitalize_first_letter"]:
            text = text.title()
        
        # Remove spaces
        hashtag = text.replace(" ", "")
        
        # Add hashtag symbol
        hashtag = f"#{hashtag}"
        
        # Add to history
        if hashtag not in self.history:
            self.history.insert(0, hashtag)
            # Maintain max history size
            self.history = self.history[:self.settings["history_max_items"]]
            
        return hashtag
    
    def load_settings(self):
        """Load settings from config file if exists"""
        if os.path.exists("config.json"):
            try:
                with open("config.json", "r") as f:
                    self.settings.update(json.load(f))
            except:
                # If error reading, use defaults
                pass
                
        # Load history if exists
        if os.path.exists("history.json"):
            try:
                with open("history.json", "r") as f:
                    self.history = json.load(f)
            except:
                # If error reading, use empty history
                self.history = []
    
    def save_settings(self):
        """Save settings to config file"""
        with open("config.json", "w") as f:
            json.dump(self.settings, f)
            
        # Save history
        with open("history.json", "w") as f:
            json.dump(self.history, f)
    
    def import_from_file(self, filename="input.txt"):
        """Import text from file"""
        if not os.path.exists(filename):
            # Create file if it doesn't exist
            with open(filename, "w") as f:
                f.write("Enter text here")
            return "Enter text here"
        
        try:
            with open(filename, "r") as f:
                return f.read().strip()
        except Exception as e:
            return f"Error reading file: {str(e)}"
    
    def export_to_file(self, hashtag, filename="output.txt"):
        """Export hashtag to file"""
        try:
            with open(filename, "w") as f:
                f.write(hashtag)
            return True
        except Exception as e:
            return False


class HashtagGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hashtag Generator")
        self.root.geometry("500x600")
        self.root.resizable(True, True)
        
        self.generator = HashtagGenerator()
        
        self.setup_ui()
        self.apply_theme()
    
    def setup_ui(self):
        """Set up the user interface"""
        # Create main frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # App title
        title_label = ttk.Label(self.main_frame, text="Hashtag Generator", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 20))
        
        # Input frame
        input_frame = ttk.LabelFrame(self.main_frame, text="Enter Text", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Text input
        self.text_input = tk.Text(input_frame, height=4, width=40, wrap=tk.WORD)
        self.text_input.pack(fill=tk.X, pady=5)
        self.text_input.bind("<KeyRelease>", self.on_text_change)
        
        # Buttons frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        # Generate button
        generate_btn = ttk.Button(button_frame, text="Generate Hashtag", command=self.generate_hashtag)
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        # Copy button
        copy_btn = ttk.Button(button_frame, text="Copy Hashtag", command=self.copy_hashtag)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear button
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_input)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Import/Export buttons
        import_btn = ttk.Button(button_frame, text="Import", command=self.import_text)
        import_btn.pack(side=tk.RIGHT, padx=5)
        
        export_btn = ttk.Button(button_frame, text="Export", command=self.export_hashtag)
        export_btn.pack(side=tk.RIGHT, padx=5)
        
        # Output frame
        output_frame = ttk.LabelFrame(self.main_frame, text="Generated Hashtag", padding="10")
        output_frame.pack(fill=tk.X, pady=10)
        
        # Hashtag output
        self.hashtag_output = ttk.Label(output_frame, text="#YourHashtagHere", font=("Helvetica", 12))
        self.hashtag_output.pack(fill=tk.X, pady=5)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(self.main_frame, text="Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Settings options
        self.remove_special_var = tk.BooleanVar(value=self.generator.settings["remove_special_chars"])
        remove_special_cb = ttk.Checkbutton(settings_frame, text="Remove Special Characters", 
                                         variable=self.remove_special_var, command=self.update_settings)
        remove_special_cb.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        self.capitalize_var = tk.BooleanVar(value=self.generator.settings["capitalize_first_letter"])
        capitalize_cb = ttk.Checkbutton(settings_frame, text="Capitalize First Letter of Each Word", 
                                     variable=self.capitalize_var, command=self.update_settings)
        capitalize_cb.grid(row=1, column=0, sticky="w", padx=5, pady=2)
        
        # Theme selection
        theme_frame = ttk.Frame(settings_frame)
        theme_frame.grid(row=2, column=0, sticky="w", padx=5, pady=2)
        
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=(0, 5))
        
        self.theme_var = tk.StringVar(value=self.generator.settings["theme"])
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, 
                                values=["light", "dark"], state="readonly", width=10)
        theme_combo.pack(side=tk.LEFT)
        theme_combo.bind("<<ComboboxSelected>>", self.update_settings)
        
        # History frame
        history_frame = ttk.LabelFrame(self.main_frame, text="History", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # History listbox
        self.history_listbox = tk.Listbox(history_frame, height=5)
        self.history_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        # Scrollbar for history
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        
        # Configure history listbox
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_select)
        self.update_history_display()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def on_text_change(self, event=None):
        """Real-time hashtag generation"""
        if self.text_input.get("1.0", "end-1c").strip():
            self.generate_hashtag()
    
    def generate_hashtag(self):
        """Generate hashtag from input text"""
        text = self.text_input.get("1.0", "end-1c").strip()
        if text:
            hashtag = self.generator.generate_hashtag(text)
            self.hashtag_output.config(text=hashtag)
            self.update_history_display()
            self.status_var.set("Hashtag generated")
        else:
            self.status_var.set("Please enter some text")
    
    def copy_hashtag(self):
        """Copy hashtag to clipboard"""
        hashtag = self.hashtag_output.cget("text")
        if hashtag != "#YourHashtagHere":
            self.root.clipboard_clear()
            self.root.clipboard_append(hashtag)
            self.status_var.set("Hashtag copied to clipboard")
        else:
            self.status_var.set("Nothing to copy")
    
    def clear_input(self):
        """Clear the input field"""
        self.text_input.delete("1.0", tk.END)
        self.hashtag_output.config(text="#YourHashtagHere")
        self.status_var.set("Input cleared")
    
    def import_text(self):
        """Import text from file"""
        filename = filedialog.askopenfilename(
            title="Select Input File",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, "r") as f:
                    text = f.read().strip()
                    self.text_input.delete("1.0", tk.END)
                    self.text_input.insert("1.0", text)
                    self.generate_hashtag()
                    self.status_var.set(f"Imported from {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Import Error", f"Error reading file: {str(e)}")
        else:
            # Try default input.txt if no file selected
            text = self.generator.import_from_file()
            if text and text != "Error reading file":
                self.text_input.delete("1.0", tk.END)
                self.text_input.insert("1.0", text)
                self.status_var.set("Imported from input.txt")
    
    def export_hashtag(self):
        """Export hashtag to file"""
        hashtag = self.hashtag_output.cget("text")
        
        if hashtag == "#YourHashtagHere":
            messagebox.showinfo("Export", "Generate a hashtag first")
            return
            
        filename = filedialog.asksaveasfilename(
            title="Save Hashtag",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            initialfile="output.txt"
        )
        
        if filename:
            try:
                with open(filename, "w") as f:
                    f.write(hashtag)
                self.status_var.set(f"Exported to {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Error writing file: {str(e)}")
    
    def update_settings(self, event=None):
        """Update settings based on UI controls"""
        self.generator.settings["remove_special_chars"] = self.remove_special_var.get()
        self.generator.settings["capitalize_first_letter"] = self.capitalize_var.get()
        self.generator.settings["theme"] = self.theme_var.get()
        
        self.generator.save_settings()
        self.apply_theme()
        
        # Regenerate hashtag with new settings
        self.generate_hashtag()
        self.status_var.set("Settings updated")
    
    def update_history_display(self):
        """Update the history listbox"""
        self.history_listbox.delete(0, tk.END)
        for item in self.generator.history:
            self.history_listbox.insert(tk.END, item)
    
    def on_history_select(self, event=None):
        """Handle history item selection"""
        if self.history_listbox.curselection():
            index = self.history_listbox.curselection()[0]
            selected_hashtag = self.history_listbox.get(index)
            self.hashtag_output.config(text=selected_hashtag)
            self.status_var.set("Selected from history")
    
    def apply_theme(self):
        """Apply the selected theme"""
        theme = self.generator.settings["theme"]
        
        if theme == "light":
            self.root.configure(bg="#f0f0f0")
            self.hashtag_output.configure(foreground="#000")
            ttk.Style().configure("TLabel", background="#f0f0f0", foreground="#000")
            ttk.Style().configure("TFrame", background="#f0f0f0")
            ttk.Style().configure("TLabelframe", background="#f0f0f0")
            ttk.Style().configure("TLabelframe.Label", background="#f0f0f0", foreground="#000")
            self.text_input.configure(bg="white", fg="black")
            self.history_listbox.configure(bg="white", fg="black")
        else:  # dark theme
            self.root.configure(bg="#2e2e2e")
            self.hashtag_output.configure(foreground="#fff")
            ttk.Style().configure("TLabel", background="#2e2e2e", foreground="#fff")
            ttk.Style().configure("TFrame", background="#2e2e2e")
            ttk.Style().configure("TLabelframe", background="#2e2e2e")
            ttk.Style().configure("TLabelframe.Label", background="#2e2e2e", foreground="#fff")
            self.text_input.configure(bg="#3e3e3e", fg="white")
            self.history_listbox.configure(bg="#3e3e3e", fg="white")

if __name__ == "__main__":
    # Create and initialize application
    root = tk.Tk()
    app = HashtagGeneratorApp(root)
    root.mainloop()
