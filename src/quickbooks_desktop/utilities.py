from datetime import datetime
import json
import tkinter as tk
from PIL import Image, ImageTk
import easygui
import threading
import time
import logging

logger = logging.getLogger(__name__)

def to_lower_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0].lower() + ''.join(x.title() for x in components[1:])

def snake_to_camel(snake_str):
    components = snake_str.split('_')
    # Capitalize the first letter of each component
    return ''.join(x.title() for x in components)

def convert_datetime(date_str):
    if isinstance(date_str, str):
        if date_str == '':
            return None
        else:
            try:
                logger.debug(date_str)
                return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
            except ValueError as e:
                logger.debug(f"Error parsing date: {e}")
                raise
    elif isinstance(date_str, datetime):
        return date_str  # Already a datetime object, no conversion needed
    else:
        return None  # None or other inappropriate data types

def convert_float(float_str):
    if float_str == "":
        return None  # Return None immediately if the input is an empty string
    try:
        return float(float_str)
    except (TypeError, ValueError) as e:
        logger.debug(f"Error parsing float: {e}")
        raise


def convert_to_json_string(data):
    if isinstance(data, (dict, list)):
        return json.dumps(data)
    return data

def convert_all_dicts_and_lists(obj):
    """
    Go through all attributes of an object, converting any that are dictionaries to JSON strings.
    """
    for key, value in vars(obj).items():
        setattr(obj, key, convert_to_json_string(value))



class SearchableComboBox():
    def __init__(self, root, options, geometry) -> None:
        self.dropdown_id = None
        self.options = options
        self.geometry = geometry

        # Create a Text widget for the entry field
        wrapper = tk.Frame(root)
        wrapper.pack()

        self.entry = tk.Entry(wrapper, width=24)
        self.entry.bind("<KeyRelease>", self.on_entry_key)
        self.entry.bind("<FocusIn>", self.show_dropdown)
        self.entry.pack(side=tk.LEFT)

        # Dropdown icon/button
        self.icon = ImageTk.PhotoImage(Image.open("dropdown_arrow.png").resize((16,16)))
        tk.Button(wrapper, image=self.icon, command=self.show_dropdown).pack(side=tk.LEFT)

        # Create a Listbox widget for the dropdown menu
        self.listbox = tk.Listbox(root, height=5, width=30)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        for option in self.options:
            self.listbox.insert(tk.END, option)

    def on_entry_key(self, event):
        typed_value = event.widget.get().strip().lower()
        if not typed_value:
            # If the entry is empty, display all options
            self.listbox.delete(0, tk.END)
            for option in self.options:
                self.listbox.insert(tk.END, option)
        else:
            # Filter options based on the typed value
            self.listbox.delete(0, tk.END)
            filtered_options = [option for option in self.options if option.lower().startswith(typed_value)]
            for option in filtered_options:
                self.listbox.insert(tk.END, option)
        self.show_dropdown()

    def on_select(self, event):
        selected_index = self.listbox.curselection()
        if selected_index:
            selected_option = self.listbox.get(selected_index)
            self.entry.delete(0, tk.END)
            self.entry.insert(0, selected_option)

    def show_dropdown(self, event=None):
        self.listbox.place(in_=self.entry, x=0, rely=1, relwidth=1.0, anchor="nw")
        self.listbox.lift()

        # Show dropdown for 2 seconds
        if self.dropdown_id: # Cancel any old events
            self.listbox.after_cancel(self.dropdown_id)
        self.dropdown_id = self.listbox.after(2000, self.hide_dropdown)

    def hide_dropdown(self):
        self.listbox.place_forget()

def convert_integer(value):
    if isinstance(value, int):
        if value == 1:
            return 'True'
        elif value == 0:
            return 'False'
        else:
            return str(value)
    return value

class EasyGuiPopup:
    def __init__(self, message, title="Message"):
        self.message = message
        self.title = title
        self.stop_thread = False
        self.thread = threading.Thread(target=self.show)

    def show(self):
        while not self.stop_thread:
            easygui.msgbox(self.message, self.title)
            time.sleep(0.1)

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_thread = True
        # Give some time for the thread to stop
        time.sleep(0.2)