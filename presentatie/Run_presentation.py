import tkinter as tk
from tkinter import ttk
import threading
import subprocess
import sys
from pathlib import Path

class IPadSplitViewer:
    def __init__(self):
        """
        iPad-achtige split screen GUI die de bestaande viewers gebruikt
        """
        self.root = tk.Tk()
        self.root.title("Calculator - Presentatie & Website")
        self.root.geometry("1400x800")
        
        # iPad-achtige donkere styling
        self.root.configure(bg='#1c1c1e')
        
        # Style configuratie
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Dark.TFrame', background='#1c1c1e')
        style.configure('Dark.TLabel', background='#1c1c1e', foreground='white', font=('SF Pro Display', 16))
        style.configure('Dark.TButton', font=('SF Pro Display', 14))
        
        # Hoofdframe
        main_frame = ttk.Frame(self.root, style='Dark.TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Titel
        title_label = ttk.Label(main_frame, text="Split Screen", 
                               style='Dark.TLabel', font=('SF Pro Display', 24, 'bold'))
        title_label.pack(pady=20)
        
        # Container voor de split view
        split_container = ttk.Frame(main_frame, style='Dark.TFrame')
        split_container.pack(fill=tk.BOTH, expand=True)
        
        # Linker panel - Presentatie
        left_panel = ttk.Frame(split_container, relief=tk.RIDGE, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        left_title = ttk.Label(left_panel, text="📄 Presentatie", 
                              font=('SF Pro Display', 18, 'bold'), background='#2c2c2e', foreground='white')
        left_title.pack(fill=tk.X, pady=10)
        
        left_content = ttk.Frame(left_panel)
        left_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(left_content, text="PDF Presentatie Viewer\n\nKlik om de presentatie te openen",
                 justify=tk.CENTER).pack(pady=50)
        
        self.open_presentation_btn = ttk.Button(left_content, 
                                               text="Open Presentatie", 
                                               command=self.open_presentation,
                                               style='Dark.TButton')
        self.open_presentation_btn.pack(pady=10)
        
        # Rechter panel - Website
        right_panel = ttk.Frame(split_container, relief=tk.RIDGE, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))
        
        right_title = ttk.Label(right_panel, text="🌐 Website", 
                               font=('SF Pro Display', 18, 'bold'), background='#2c2c2e', foreground='white')
        right_title.pack(fill=tk.X, pady=10)
        
        right_content = ttk.Frame(right_panel)
        right_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        ttk.Label(right_content, text="Website Viewer\n\nKlik om de website te openen",
                 justify=tk.CENTER).pack(pady=50)
        
        self.open_website_btn = ttk.Button(right_content, 
                                          text="Open Website", 
                                          command=self.open_website,
                                          style='Dark.TButton')
        self.open_website_btn.pack(pady=10)
        
        # Onderste controls
        controls_frame = ttk.Frame(main_frame, style='Dark.TFrame')
        controls_frame.pack(fill=tk.X, pady=20)
        
        # Open beide button
        self.open_both_btn = ttk.Button(controls_frame, 
                                       text="🚀 Open Beide (Split Screen)", 
                                       command=self.open_both,
                                       style='Dark.TButton')
        self.open_both_btn.pack()
        
        # Info label
        info_label = ttk.Label(controls_frame, 
                              text="Tip: Klik 'Open Beide' voor de volledige iPad split screen ervaring!",
                              style='Dark.TLabel', font=('SF Pro Display', 12))
        info_label.pack(pady=10)
        
    def open_presentation(self):
        """Start presentation_viewer.py in een aparte thread"""
        def run_presentation():
            script_path = Path(__file__).parent / "presentation_viewer.py"
            subprocess.Popen([sys.executable, str(script_path)])
        
        thread = threading.Thread(target=run_presentation)
        thread.daemon = True
        thread.start()
        
    def open_website(self):
        """Start website_viewer.py in een aparte thread"""
        def run_website():
            script_path = Path(__file__).parent / "website_viewer.py"
            subprocess.Popen([sys.executable, str(script_path)])
        
        thread = threading.Thread(target=run_website)
        thread.daemon = True
        thread.start()
        
    def open_both(self):
        """Open beide viewers tegelijk voor split screen ervaring"""
        self.open_presentation()
        # Kleine delay zodat de vensters niet overlappen
        self.root.after(500, self.open_website)
        
    def run(self):
        """Start de GUI"""
        self.root.mainloop()

def main():
    """Hoofdfunctie"""
    app = IPadSplitViewer()
    app.run()

if __name__ == "__main__":
    main() 