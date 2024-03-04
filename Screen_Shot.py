import tkinter as tk
from PIL import ImageGrab
import numpy as np
import cv2

class ScreenShotApp:
    def __init__(self, master, screen_width, screen_height):
        self.master = master
        self.master.geometry(f"{screen_width}x{screen_height}+0+0")  # Cover entire screen
        self.canvas = None
        self.x1, self.y1, self.x2, self.y2 = 0, 0, 0, 0
        self.screen_width = screen_width
        self.screen_height = screen_height


    def start_screenshot(self):
        self.master.bind('<Button-1>', self.start_selection)
        self.master.bind('<B1-Motion>', self.draw_selection)
        self.master.bind('<ButtonRelease-1>', self.capture_screenshot)
        
    def start_selection(self, event):
        self.x1, self.y1 = event.x, event.y

    def draw_selection(self, event):
        self.x2, self.y2 = event.x, event.y
        if self.canvas:
            self.canvas.delete('selection')
        else:
            self.canvas = tk.Canvas(self.master, highlightbackground="purple", bg='#ab23ff', highlightthickness=3, relief="ridge", width=self.screen_width, height=self.screen_height)
            self.canvas.grid(sticky='nsew')
        # Ensure that the rectangle coordinates are within the bounds of the canvas
        x1_canvas, y1_canvas = max(self.x1, 0), max(self.y1, 0)
        x2_canvas, y2_canvas = min(self.x2, self.master.winfo_width()), min(self.y2, self.master.winfo_height())
        self.canvas.create_rectangle(x1_canvas, y1_canvas, x2_canvas, y2_canvas, fill='lime', outline='red', dash=(40, 30), width=7, tags='selection')
        cursor_option = 'C:/Users/Dr/HBI-Systems/icons8-launchpad-material-filled/icons8-plus-math-32.cur'
        cursor_width = 10
        cursor_height = 10

        border_width = 0
        delta_y = self.y2 - self.y1
        delta_x = self.x2 - self.x1
        new_height = delta_y - 20
        new_width = delta_x + 10
                                    
            # Check if the mouse is within the border region
        if (self.x2 > border_width or self.x2 < new_width - border_width or
            self.y2 > border_width or self.y2 < new_height - border_width):
            # Change the cursor to the resize cursor
            self.master.configure(cursor= '@'+ cursor_option)
        else:
            # Change the cursor to the default cursor
            self.master.configure(cursor='tcross')


    def capture_screenshot(self, event):
        bbox = (min(self.x1, self.x2), min(self.y1, self.y2), max(self.x1, self.x2), max(self.y1, self.y2))
        screenshot = ImageGrab.grab(bbox=bbox)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        cv2.imshow('Screenshot', frame)
        self.canvas.delete('selection')
        
        
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('HBIS Screen Recorder')
        self.attributes("-alpha", 0.5)
        self.attributes('-transparentcolor', 'lime')
        self.overrideredirect(True)
        self.bind("<Escape>", lambda event: self.quit())

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.screenshot_app = ScreenShotApp(self, screen_width, screen_height)
        self.screenshot_app.start_screenshot()

        self.configure(bg='#ab23ff')
        self.mainloop()

App()
