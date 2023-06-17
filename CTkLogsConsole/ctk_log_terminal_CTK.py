import customtkinter
from PIL import Image
import datetime
import os
import time
import sys
from tkinter import Toplevel, Frame

customtkinter.set_appearance_mode("dark")

PATH = os.path.dirname(os.path.realpath(__file__))

class CTkConsole(customtkinter.CTkFrame):
    def __init__(self,
                 master=None,
                 log_file: str='logs.txt',
                 width: int = 500,
                 height: int = 300,
                 ):
        super().__init__(master)

        self.configure(width=width, height=height, corner_radius=0)
        self.pack_propagate(False)
        self.pack()
        self.logs = []
        self.log_file = log_file

        self.log_frame = customtkinter.CTkScrollableFrame(self, width=width, height=height-20, corner_radius=0)
        self.log_frame.pack(fill='both', expand=True)

        #self.frame_color = self.get_frame_color()
        self.counter_frame = customtkinter.CTkFrame(self, width=width, height=20, corner_radius=0)
        self.counter_frame.pack(fill='x', pady=(0, 1))
        self.counter_frame.pack_propagate(False)

        self.error_count = 0
        self.warning_count = 0
        self.info_count = 0
        self.debug_count = 0

        self.error_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH, 'error.png')), dark_image=Image.open(os.path.join(PATH, 'error.png')), size=(14, 14))
        self.warning_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH, 'warning.png')), dark_image=Image.open(os.path.join(PATH, 'warning.png')), size=(14, 14))
        self.info_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH, 'info.png')), dark_image=Image.open(os.path.join(PATH, 'info.png')), size=(14, 14))
        self.debug_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH, 'debug.png')), dark_image=Image.open(os.path.join(PATH, 'debug.png')), size=(14, 14))
        self.tooltip_icon = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH, 'tooltip-light.png')), dark_image=Image.open(os.path.join(PATH, 'tooltip-dark.png')), size=(16, 16))
        self.red_status = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH, 'red_status.png')), dark_image=Image.open(os.path.join(PATH, 'red_status.png')), size=(13, 13))
        self.orange_status = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH, 'orange_status.png')), dark_image=Image.open(os.path.join(PATH, 'orange_status.png')), size=(13, 13))
        self.green_status = customtkinter.CTkImage(light_image=Image.open(os.path.join(PATH, 'green_status.png')), dark_image=Image.open(os.path.join(PATH, 'green_status.png')), size=(13, 13))

        #self.change_appearance_mode(appearance_mode=appearance_mode)
        self.display_counters()
        self.update_counters()

    def log(self, type, text):
        log_entry = {
            'type': type,
            'text': text,
            'timestamp': datetime.datetime.now(),
        }
        self.logs.append(log_entry)
        self.update_counters()
        self.display_logs()
        self.save_log_to_file(log_entry)
        self.print_log_in_console(log_entry)

    def update_counters(self):
        global error_count
        self.error_count = 0
        global warning_count
        self.warning_count = 0
        global info_count
        self.info_count = 0
        global debug_count
        self.debug_count = 0

        for log in self.logs:
            if log['type'] == 'ERROR':
                self.error_count = self.error_count + 1
            elif log['type'] == 'WARNING':
                self.warning_count = self.warning_count + 1
            elif log['type'] == 'INFO':
                self.info_count = self.info_count + 1
            elif log['type'] == 'DEBUG':
                self.debug_count = self.debug_count + 1

        self.display_counters()

    def get_status_icon(self):
        if self.error_count > 0:
            return self.red_status
        elif self.warning_count > 0:
            return self.orange_status
        elif self.warning_count > 0 and self.error_count > 0:
            return self.red_status
        else:
            return self.green_status

    def display_counters(self):
        for widget in self.counter_frame.winfo_children():
            widget.destroy()

        errors_counter_image = customtkinter.CTkLabel(self.counter_frame, image=self.error_icon, text='')
        errors_counter_label = customtkinter.CTkLabel(self.counter_frame, text=self.error_count)
        errors_counter_image.pack(side='left', padx=(5, 2), pady=2)
        errors_counter_label.pack(side='left')

        info_counter_image = customtkinter.CTkLabel(self.counter_frame, image=self.info_icon, text='')
        info_counter_label = customtkinter.CTkLabel(self.counter_frame, text=self.info_count)
        info_counter_image.pack(side='left', padx=(5, 2), pady=2)
        info_counter_label.pack(side='left')

        warning_counter_image = customtkinter.CTkLabel(self.counter_frame, image=self.warning_icon, text='')
        warning_counter_label = customtkinter.CTkLabel(self.counter_frame, text=self.warning_count)
        warning_counter_image.pack(side='left', padx=(5, 2), pady=2)
        warning_counter_label.pack(side='left')

        debug_counter_image = customtkinter.CTkLabel(self.counter_frame, image=self.debug_icon, text='')
        debug_counter_label = customtkinter.CTkLabel(self.counter_frame, text=self.debug_count)
        debug_counter_image.pack(side='left', padx=(5, 2), pady=2)
        debug_counter_label.pack(side='left')

        tooltip_icon = customtkinter.CTkLabel(self.counter_frame, image=self.tooltip_icon, text='')
        tooltip_icon.pack(side='right', padx=(0, 3), pady=2)
        CTkToolTip(tooltip_icon, message='Real-time Log Monitoring:\nThe console provides real-time log monitoring,\nenabling efficient error tracking, warning management,\nand information analysis for effective troubleshooting and debugging.')

        self.status_icon = self.get_status_icon()
        status_image = customtkinter.CTkLabel(self.counter_frame, image=self.status_icon, text='')
        status_image.pack(side='right', padx=(0, 3), pady=2)
        CTkToolTip(status_image, message='Console Status:\n1.  Green - Good\n2. Orange - Moderate\n3. Red - Critical')

        self.counter_frame.configure(fg_color=self.get_frame_color())

    def display_logs(self):
        for widget in self.log_frame.winfo_children():
            widget.destroy()

        for log in self.logs:
            self.frame_color = self.get_frame_color()
            self.log_container = customtkinter.CTkFrame(self.log_frame, corner_radius=5, fg_color=self.frame_color)
            self.log_container.pack(fill='x', pady=(2, 0), padx=5)

            icon_path = str(self.get_icon_path(log['type']))
            icon = customtkinter.CTkImage(light_image=Image.open(icon_path), dark_image=Image.open(icon_path), size=(16, 16))
            icon_label = customtkinter.CTkLabel(self.log_container, image=icon, text='')
            icon_label.pack(side='left', padx=(4, 1))
            CTkToolTip(icon_label, message=f'{log["type"]}')

            log_text = f' {log["timestamp"].strftime("%H:%M:%S")} - {log["text"]}'
            text_label = customtkinter.CTkLabel(self.log_container, text=log_text)
            text_label.pack(side='left')

    def save_log_to_file(self, log_entry):
        if self.log_file is None:
            return

        log_text = f'{log_entry["type"]} - {log_entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S")} - {log_entry["text"]}'
        with open(self.log_file, 'a') as file:
            file.write(log_text + '\n')

    def print_log_in_console(self, log_entry):
        log_text = f'{log_entry["type"]} - {log_entry["timestamp"].strftime("%Y-%m-%d %H:%M:%S")} - {log_entry["text"]}'
        print(log_text)

    def get_frame_color(self):
        appearance_mode = self._get_appearance_mode()
        if appearance_mode.lower() == 'dark':
            return '#2b2b2b'
        if appearance_mode.lower() == 'light':
            return '#dbdbdb'

    def get_icon_path(self, log_type):
        if log_type.lower() == 'info':
            return PATH + '\\info.png'
        elif log_type.lower() == 'warning':
            return PATH + '\\warning.png'
        elif log_type.lower() == 'error':
            return PATH + '\\error.png'
        elif log_type.lower() == 'debug':
            return PATH + '\\debug.png'
        else:
            return PATH + '\\default.png'

    def clear_file_saved_logs(self):
        if self.log_file is None:
            return

        with open(self.log_file, 'w') as file:
            file.truncate()

    def clear(self):
        for widget in self.log_frame.winfo_children():
            widget.destroy()

        self.logs = []
        self.update_counters()


class CTkToolTip(Toplevel):
    """
    Creates a ToolTip (pop-up) widget for customtkinter.
    By Akascape
    """

    def __init__(
        self,
        widget: any = None,
        message: str = None,
        delay: float = 0.2,
        follow: bool = True,
        x_offset: int = +20,
        y_offset: int = +10,
        bg_color: str = None,
        corner_radius: int = 10,
        border_width: int = 0,
        border_color: str = None,
        alpha: float = 0.8,
        padding: tuple = (10,2),
        **message_kwargs):
        
        super().__init__()

        self.widget = widget
        
        self.withdraw()
        # Disable ToolTip's title bar
        self.overrideredirect(True)
                
        if sys.platform.startswith("win"):
            self.transparent_color = self.widget._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkToplevel"]["fg_color"])
            self.attributes("-transparentcolor", self.transparent_color)
            self.transient()
        elif sys.platform.startswith("darwin"):
            self.transparent_color = 'systemTransparent'
            self.attributes("-transparent", True)
            self.transient(self.master)
        else:
            self.transparent_color = '#000001'
            corner_radius = 0
            self.transient()
            
        self.resizable(width=True, height=True)
        self.transient()
        
        # Make the background transparent
        self.config(background=self.transparent_color)
        
        # StringVar instance for msg string
        self.messageVar = customtkinter.StringVar()
        self.message = message
        self.messageVar.set(self.message)
      
        self.delay = delay
        self.follow = follow
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.corner_radius = corner_radius
        self.alpha = alpha
        self.border_width = border_width
        self.padding = padding
        self.bg_color = bg_color
        self.border_color = border_color
        self.disable = False
        
        # visibility status of the ToolTip inside|outside|visible
        self.status = "outside"
        self.last_moved = 0
        self.attributes('-alpha', self.alpha)
        
        # Add the message widget inside the tooltip
        self.transparent_frame = Frame(self, bg=self.transparent_color)
        self.transparent_frame.pack(padx=0, pady=0, fill="both", expand=True)
        
        self.frame = customtkinter.CTkFrame(self.transparent_frame, bg_color=self.transparent_color, corner_radius=self.corner_radius,
                                            border_width=self.border_width, fg_color=self.bg_color, border_color=self.border_color)
        self.frame.pack(padx=0, pady=0, fill="both", expand=True)
        
        self.message_label = customtkinter.CTkLabel(self.frame, textvariable=self.messageVar, **message_kwargs)
        self.message_label.pack(fill="both", padx=self.padding[0]+self.border_width,
                                pady=self.padding[1]+self.border_width, expand=True)

        if self.widget.winfo_name()!="tk":
            if self.frame.cget("fg_color")==self.widget.cget("bg_color"):
                if not bg_color:             
                    self._top_fg_color = self.frame._apply_appearance_mode(customtkinter.ThemeManager.theme["CTkFrame"]["top_fg_color"])
                    self.frame.configure(fg_color=self._top_fg_color)
  
        # Add bindings to the widget without overriding the existing ones
        self.widget.bind("<Enter>", self.on_enter, add="+")
        self.widget.bind("<Leave>", self.on_leave, add="+")
        self.widget.bind("<Motion>", self.on_enter, add="+")
        self.widget.bind("<B1-Motion>", self.on_enter, add="+")
        self.widget.bind("<Destroy>", lambda _: self.hide(), add="+")
 
    def show(self) -> None:
        """
        Enable the widget.
        """
        self.disable = False
        
    def on_enter(self, event) -> None:
        """
        Processes motion within the widget including entering and moving.
        """

        if self.disable: return
        self.last_moved = time.time()

        # Set the status as inside for the very first time
        if self.status == "outside":
            self.status = "inside"

        # If the follow flag is not set, motion within the widget will make the ToolTip dissapear
        if not self.follow:
            self.status = "inside"
            self.withdraw()

        # Offsets the ToolTip using the coordinates od an event as an origin
        self.geometry(f"+{event.x_root + self.x_offset}+{event.y_root + self.y_offset}")

        # Time is in integer: milliseconds
        self.after(int(self.delay * 1000), self._show)

    def on_leave(self, event=None) -> None:
        """
        Hides the ToolTip temporarily.
        """

        if self.disable: return
        self.status = "outside"
        self.withdraw()

    def _show(self) -> None:
        """
        Displays the ToolTip.
        """

        if not self.widget.winfo_exists():
            self.hide()
            self.destroy()
            
        if self.status == "inside" and time.time() - self.last_moved >= self.delay:
            self.status = "visible"
            self.deiconify()
        
    def hide(self) -> None:
        """
        Disable the widget from appearing.
        """
        if not self.winfo_exists():
            return
        self.withdraw()
        self.disable = True

    def is_disabled(self) -> None:
        """
        Return the window state
        """
        return self.disable
    
    def get(self) -> None:
        """
        Returns the text on the tooltip.
        """  
        return self.messageVar.get()
    
    def configure(self, message: str = None, delay: float = None, bg_color: str = None, **kwargs):
        """
        Set new message or configure the label parameters.
        """
        if delay: self.delay = delay
        if bg_color: self.frame.configure(fg_color=bg_color)
        
        self.messageVar.set(message)
        self.message_label.configure(**kwargs)
