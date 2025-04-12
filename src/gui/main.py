import os
import json
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path


class HashtagGenerator:
    def __init__(self):
        # Initialize settings with defaults
        self.settings = {
            "remove_special_chars": False,
            "capitalization_mode": "first",
            "history_max_items": 10,
            "theme": "light",
            "character_limit": 0
        }
        self.history = []
        self.load_settings()
        
    def _get_config_dir(self):
        """Get the appropriate configuration directory based on OS"""
        home = Path.home()
        
        if sys.platform == "win32":
            config_dir = home / "AppData" / "Local" / "HashtagGenerator"
        elif sys.platform == "darwin":
            config_dir = home / "Library" / "Application Support" / "HashtagGenerator"
        else:  # Linux and other Unix-like
            config_dir = home / ".config" / "hashtag-generator"
            
        # Create config directory if it doesn't exist
        config_dir.mkdir(parents=True, exist_ok=True)
        return config_dir
    
    def generate_hashtag(self, text):
        """Transform input text into a hashtag format based on settings"""
        if not text:
            return ""
            
        # Remove special characters if enabled
        if self.settings["remove_special_chars"]:
            text = ''.join(c for c in text if c.isalnum() or c.isspace())
        
        # Apply capitalization mode based on setting
        mode = self.settings.get("capitalization_mode", "first")
        if mode == "first":
            text = text.title()
        elif mode == "all_caps":
            text = text.upper()
        elif mode == "lowercase":
            text = text.lower()
        # If mode is "none", leave text unchanged
        
        # Remove spaces and prepend hashtag symbol
        hashtag = "#" + text.replace(" ", "")
        
        # Add to history if not already present
        if hashtag not in self.history:
            self.history.insert(0, hashtag)
            # Maintain max history size based on settings (if needed, could use history_max_items)
            self.history = self.history[:self.settings["history_max_items"]]
            self.save_settings()  # Save history to file
        
        return hashtag
    
    def load_settings(self):
        """Load settings from config file if exists, otherwise create one with defaults"""
        config_dir = self._get_config_dir()
        config_path = config_dir / "config.json"
        history_path = config_dir / "history.json"
        
        if not config_path.exists():
            # Create config file with default settings
            with open(config_path, "w") as f:
                json.dump(self.settings, f)
        else:
            try:
                with open(config_path, "r") as f:
                    self.settings.update(json.load(f))
            except:
                pass
                
        # Load history if exists, otherwise create an empty one
        if not history_path.exists():
            with open(history_path, "w") as f:
                json.dump(self.history, f)
        else:
            try:
                with open(history_path, "r") as f:
                    self.history = json.load(f)
            except:
                self.history = []

    def save_settings(self):
        """Save settings and history to their respective files"""
        config_dir = self._get_config_dir()
        config_path = config_dir / "config.json"
        history_path = config_dir / "history.json"
        
        # Save settings
        with open(config_path, "w") as f:
            json.dump(self.settings, f)
        
        # Save history
        with open(history_path, "w") as f:
            json.dump(self.history, f)
    
    def import_from_file(self, filename="input.txt"):
        """Import text from file"""
        if not os.path.exists(filename):
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
        self.root.geometry("600x800")
        self.root.resizable(True, True)
        icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'icon.ico'))
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        else:
            print('Using icon in assets folder')
            self.root.iconbitmap(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'icons', 'app_icon.ico')))
        
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
        self.text_input = tk.Text(input_frame, height=4, width=40, wrap=tk.WORD, font=("Times New Roman", 12))
        self.text_input.pack(fill=tk.X, pady=5)
        self.text_input.bind("<KeyRelease>", self.on_text_change)
        
        # Buttons frame
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        generate_btn = ttk.Button(button_frame, text="Generate Hashtag", command=self.generate_hashtag)
        generate_btn.pack(side=tk.LEFT, padx=5)
        
        copy_btn = ttk.Button(button_frame, text="Copy Hashtag", command=self.copy_hashtag)
        copy_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_input)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        import_btn = ttk.Button(button_frame, text="Import", command=self.import_text)
        import_btn.pack(side=tk.RIGHT, padx=5)
        
        export_btn = ttk.Button(button_frame, text="Export", command=self.export_hashtag)
        export_btn.pack(side=tk.RIGHT, padx=5)
        
        # Output frame
        output_frame = ttk.LabelFrame(self.main_frame, text="Generated Hashtag", padding="10")
        output_frame.pack(fill=tk.X, pady=10)
        
        self.hashtag_output = ttk.Label(output_frame, text="#YourHashtagHere", font=("Times New Roman", 12))
        self.hashtag_output.pack(fill=tk.X, pady=5)
        
        # Settings frame
        settings_frame = ttk.LabelFrame(self.main_frame, text="Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # Remove special characters option
        self.remove_special_var = tk.BooleanVar(value=self.generator.settings["remove_special_chars"])
        remove_special_cb = ttk.Checkbutton(settings_frame, text="Remove Special Characters", 
                                            variable=self.remove_special_var, command=self.update_settings)
        remove_special_cb.grid(row=0, column=0, sticky="w", padx=5, pady=2)
        
        # Capitalization control
        ttk.Label(settings_frame, text="Capitalization:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.capitalization_var = tk.StringVar(value=self.generator.settings.get("capitalization_mode", "first"))
        capitalization_combo = ttk.Combobox(settings_frame, textvariable=self.capitalization_var, 
                                            values=["none", "first", "all_caps", "lowercase"], state="readonly", width=15)
        capitalization_combo.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        capitalization_combo.bind("<<ComboboxSelected>>", self.update_settings)
        
        # Character Limit control
        ttk.Label(settings_frame, text="Character Limit:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.character_limit_var = tk.IntVar(value=self.generator.settings.get("character_limit", 0))
        character_limit_spinbox = tk.Spinbox(settings_frame, from_=0, to=100000, textvariable=self.character_limit_var, width=5, command=self.update_settings)
        character_limit_spinbox.grid(row=2, column=1, sticky="w", padx=5, pady=2)

        
        # Theme selection moved to next row
        theme_frame = ttk.Frame(settings_frame)
        theme_frame.grid(row=3, column=0, columnspan=2, sticky="w", padx=5, pady=2)
        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=(0, 5))
        self.theme_var = tk.StringVar(value=self.generator.settings["theme"])
        theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, 
                                   values=["light", "dark"], state="readonly", width=10)
        theme_combo.pack(side=tk.LEFT)
        theme_combo.bind("<<ComboboxSelected>>", self.update_settings)
        
        # History frame
        history_frame = ttk.LabelFrame(self.main_frame, text="History", padding="10")
        history_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.history_listbox = tk.Listbox(history_frame, height=5)
        self.history_listbox.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_select)
        self.update_history_display()
        
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def on_text_change(self, event=None):
        """Real-time hashtag generation with character limit enforcement."""
        limit = self.generator.settings.get("character_limit", 0)
        current_text = self.text_input.get("1.0", "end-1c")
        if limit > 0 and len(current_text) > limit:
            # Truncate the text to the limit
            truncated_text = current_text[:limit]
            # Replace text in widget (avoiding recursive events)
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert("1.0", truncated_text)
            self.status_var.set("Character limit reached!")
        else:
            # Continue to generate hashtag if text remains within the limit
            self.generate_hashtag()

    
    def generate_hashtag(self):
        """Generate hashtag from input text with delayed update for history handling"""
        def delayed_update():
            text = self.text_input.get("1.0", "end-1c").strip()
            if text:
                hashtag = self.generator.generate_hashtag(text)
                self.hashtag_output.config(text=hashtag)
                self.update_history_display()
                # Check for character limit warning
                if len(hashtag) > self.generator.settings["character_limit"]:
                    self.status_var.set("Warning: Hashtag exceeds character limit!")
                else:
                    self.status_var.set("Hashtag generated")
            else:
                self.status_var.set("Please enter some text")
        
        if hasattr(self, "_update_timer"):
            self.root.after_cancel(self._update_timer)
        self._update_timer = self.root.after(800, delayed_update)
    
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
        self.generator.settings["capitalization_mode"] = self.capitalization_var.get()
        try:
            self.generator.settings["character_limit"] = int(self.character_limit_var.get())
        except ValueError:
            self.generator.settings["character_limit"] = 30  # default fallback
        self.generator.settings["theme"] = self.theme_var.get()
        
        self.generator.save_settings()
        self.apply_theme()
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
    root = tk.Tk()
    app = HashtagGeneratorApp(root)
    root.mainloop()
