from tkinter import *
import pyautogui
import pygetwindow as gw
from pynput import mouse

class Virtual_Keyboard:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1435x562")
        self.root.title("Virtual Keyboard")
        self.root.resizable(0, 0)
        self.root.attributes('-topmost', True)  # Always on top
        self.create_buttons()
        self.target_window = None

        self.ctrl_pressed = False
        self.shift_pressed = False

        # Identify the virtual keyboard window to ignore clicks on it
        self.virtual_keyboard_window = gw.getWindowsWithTitle("Virtual Keyboard")[0]

        # Bind focus events
        self.root.bind("<FocusIn>", self.on_focus_in)
        self.root.bind("<FocusOut>", self.on_focus_out)
        self.root.bind_all("<Button>", self.on_click_anywhere)

        # Set up listener for mouse events
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()

        # Bind events for dragging the window
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)

        self.x = 0
        self.y = 0

    def create_buttons(self):
        keys = [
            ['Esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12'],
            ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '+'],
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'Backspace', '_'],
            ['Tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']'],
            ['Caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', 'Enter'],
            ['Shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'Shift', ':'],
            ['Ctrl', 'Win', 'Alt', 'Space', 'Alt', 'Fn', 'Menu', 'Ctrl', '\\'],
            ['{', '}', '|', ':', '"', '<', '>', '?', '=', 'PrtSc', 'ScrLk', 'Pause'],
        ]

        self.buttons = {}  # To store button references

        row_offset = 0
        for row in keys:
            col_offset = 0
            for key in row:
                if key == 'Space':
                    btn = Button(self.root, text=key, width=45, height=2, bd=4, font="arial 12 bold", bg="black", fg="white",
                           relief=RAISED, overrelief=RIDGE, command=lambda k=key: self.type_key(k))
                    btn.grid(row=row_offset, column=col_offset, columnspan=5)
                    col_offset += 4
                else:
                    btn = Button(self.root, text=key, width=8, height=2, bd=4, font="arial 12 bold", bg="black", fg="white",
                           relief=RAISED, overrelief=RIDGE, command=lambda k=key: self.type_key(k))
                    btn.grid(row=row_offset, column=col_offset)

                self.buttons[key] = btn  # Save the button reference
                col_offset += 1
            row_offset += 1

    def type_key(self, key):
        # Send key press event to the active window
        if key == 'Space':
            pyautogui.press('space')
        elif key == 'Backspace':
            pyautogui.press('backspace')
        elif key == 'Enter':
            pyautogui.press('enter')
        elif key == 'Tab':
            pyautogui.press('tab')
        elif key == 'Caps':
            pyautogui.press('capslock')
        elif key == 'Shift':
            if self.shift_pressed:
                pyautogui.keyUp('shift')
                self.shift_pressed = False
                self.buttons['Shift'].config(bg="black")  # Change background color back to black
            else:
                pyautogui.keyDown('shift')
                self.shift_pressed = True
                self.buttons['Shift'].config(bg="blue")  # Change background color to blue
        elif key == 'Ctrl':
            if self.ctrl_pressed:
                pyautogui.keyUp('ctrl')
                self.ctrl_pressed = False
                self.buttons['Ctrl'].config(bg="black")  # Change background color back to black
            else:
                pyautogui.keyDown('ctrl')
                self.ctrl_pressed = True
                self.buttons['Ctrl'].config(bg="blue")  # Change background color to blue
        elif key == 'Alt':
            pyautogui.press('alt')
        elif key == 'Win':
            pyautogui.press('win')
        elif key == 'Fn':
            pass  # pyautogui does not support Fn key
        elif key == 'Menu':
            pyautogui.press('menu')
        elif key in ['F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12']:
            pyautogui.press(key.lower())
        elif key == 'PrtSc':
            pyautogui.press('printscreen')
        elif key == 'ScrLk':
            pyautogui.press('scrolllock')
        elif key == 'Pause':
            pyautogui.press('pause')
        else:
            pyautogui.press(key)

        # Reactivate the target window after pressing a key
        if self.target_window:
            try:
                self.target_window.activate()
            except gw.PyGetWindowException as e:
                # print(f"Error activating target window: {e}")
                pass

    def on_focus_in(self, event):
        # This method is called when the tkinter window gains focus
        if self.target_window:
            try:
                self.target_window.activate()
            except gw.PyGetWindowException as e:
                # print(f"Error activating target window: {e}")
                pass

    def on_focus_out(self, event):
        # This method is called when the tkinter window loses focus
        pass

    def on_click_anywhere(self, event):
        # This method is called when any mouse button is clicked
        if self.root.winfo_containing(event.x_root, event.y_root) != self.root:
            self.root.grab_release()

    def on_click(self, x, y, button, pressed):
        if pressed:
            active_window_title = self.get_active_window_title(x, y)
            if active_window_title and active_window_title != "Virtual Keyboard":
                try:
                    self.target_window = gw.getWindowsWithTitle(active_window_title)[0]
                except IndexError:
                    self.target_window = None
                except Exception as e:
                    print(f"Unexpected error while setting target window: {e}")

    def get_active_window_title(self, mouse_x, mouse_y):
        # Get all windows
        windows = gw.getAllWindows()

        # Find the window under the mouse cursor
        for window in windows:
            if window.left <= mouse_x <= window.left + window.width and \
               window.top <= mouse_y <= window.top + window.height:
                return window.title

        return None  # Return None if no window is found under the mouse cursor

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        self.root.geometry(f"+{self.root.winfo_x() + deltax}+{self.root.winfo_y() + deltay}")

root = Tk()
obj = Virtual_Keyboard(root)

root.mainloop()
