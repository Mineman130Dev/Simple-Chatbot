import random
import os
from tkinter import ttk
import tkinter as tk
import datetime

def load_name():
    if os.path.exists("name.txt"):
        with open("name.txt", "r") as file:
            return file.read().strip()
    return None

def save_name(name):
    with open("name.txt", "w") as file:
        file.write(name)

name = load_name()

window = tk.Tk()
window.title("Chatbot")

def bring_to_front_non_topmost():
    window.attributes('-topmost', True)
    window.lift()
    window.attributes('-topmost', False)

window.resizable(False, False)
style = ttk.Style()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_width = 600
window_height = 450

x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)

window.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

notebook = ttk.Notebook(window)
notebook.pack(fill=tk.BOTH, expand=True)

chatbot_tab = ttk.Frame(notebook)
notebook.add(chatbot_tab, text="Chatbot")

settings_tab = ttk.Frame(notebook)
notebook.add(settings_tab, text="Settings")

text_area = tk.Text(chatbot_tab, state=tk.DISABLED)
text_area.pack()

entry = tk.Entry(chatbot_tab)
entry.pack()

original_text_bg = text_area.cget('bg')

# Settings variables
show_timestamp = tk.BooleanVar(value=True)
align_right = tk.BooleanVar(value=False)
stay_on_top = tk.BooleanVar(value=True)
bg_color = tk.StringVar(value="default")
chat_bg_color = tk.StringVar(value="default")
text_color = tk.StringVar(value="white")
message_delay = tk.IntVar(value=500)    # Default response delay (ms)
close_delay = tk.IntVar(value=1000)     # Default close delay (ms)

first_apply = True

def apply_settings():
    global first_apply
    bg = bg_color.get()
    chat_bg = chat_bg_color.get()

    # Apply main window background
    if bg == "default":
        window.config(bg='#f0f0f0')  # Default system color
        notebook.config(style='TNotebook')  # Reset to default style
    else:
        window.config(bg=bg)
        # Create a custom style for the notebook to match the background
        style = ttk.Style()
        style.configure('Custom.TNotebook', background=bg)
        style.configure('Custom.TNotebook.Tab', background=bg)
        notebook.config(style='Custom.TNotebook')

    # Apply chat background
    text_area.config(state=tk.NORMAL)
    if chat_bg == "default":
        text_area.configure(bg=original_text_bg)
    else:
        text_area.configure(bg=chat_bg)
    text_area.config(state=tk.DISABLED)

    # Apply text color
    text_area.config(fg=text_color.get())

    # Handle window topmost behavior
    if first_apply:
        stay_on_top.set(False)
        window.attributes("-topmost", False)
        first_apply = False
    elif stay_on_top.get():
        window.attributes("-topmost", True)
    else:
        window.attributes("-topmost", False)

# Settings UI
timestamp_check = tk.Checkbutton(settings_tab, text="Show Timestamps", variable=show_timestamp)
timestamp_check.pack()

align_frame = tk.Frame(settings_tab)
align_frame.pack()
tk.Radiobutton(align_frame, text="Left Align", variable=align_right, value=False).pack(side=tk.LEFT)
tk.Radiobutton(align_frame, text="Right Align", variable=align_right, value=True).pack(side=tk.LEFT)
top_check = tk.Checkbutton(settings_tab, text="Always on top", variable=stay_on_top)
top_check.pack()

# Color settings
#bg_label = tk.Label(settings_tab, text="Background Color:")
#bg_label.pack()
#bg_colors = ["default", "white", "pink", "blue", "green"]
#bg_dropdown = ttk.Combobox(settings_tab, textvariable=bg_color, values=bg_colors)
#bg_dropdown.pack()

chat_bg_label = tk.Label(settings_tab, text="Chat Background Color:")
chat_bg_label.pack()
chat_bg_colors = ["default", "white", "pink", "blue", "green"]
chat_bg_dropdown = ttk.Combobox(settings_tab, textvariable=chat_bg_color, values=chat_bg_colors)
chat_bg_dropdown.pack()

text_color_label = tk.Label(settings_tab, text="Text Color:")
text_color_label.pack()
text_colors = ["black", "white", "red", "blue", "green", "purple"]
text_color_dropdown = ttk.Combobox(settings_tab, textvariable=text_color, values=text_colors)
text_color_dropdown.pack()

# Delay settings
delay_frame = tk.Frame(settings_tab)
delay_frame.pack(pady=5)

response_delay_label = tk.Label(delay_frame, text="Response Delay (ms):")
response_delay_label.grid(row=0, column=0, sticky="w")
response_delay_entry = tk.Entry(delay_frame, textvariable=message_delay, width=10)
response_delay_entry.grid(row=0, column=1, padx=5)

close_delay_label = tk.Label(delay_frame, text="Close Delay (ms):")
close_delay_label.grid(row=1, column=0, sticky="w")
close_delay_entry = tk.Entry(delay_frame, textvariable=close_delay, width=10)
close_delay_entry.grid(row=1, column=1, padx=5)

apply_button = tk.Button(settings_tab, text="Apply Settings", command=apply_settings)
apply_button.pack(pady=10)

def send_bot_message(bot_message):
    """Send the bot's message to the chat"""
    if bot_message:
        text_area.config(fg=text_color.get())
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, bot_message)
        text_area.config(state=tk.DISABLED)
        text_area.see(tk.END)

def close_window():
    """Close the application window"""
    window.destroy()

def send_message(event=None):
    global name  # Add this line to access the global name variable
    message = entry.get()
    if not message.strip():
        return  # Don't send empty messages

    now = datetime.datetime.now()
    timestamp = now.strftime("%H:%M:%S")

    # Display user message immediately
    user_message = f"[{timestamp}] You: {message}\n" if show_timestamp.get() else f"You: {message}\n"
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, user_message)
    text_area.config(state=tk.DISABLED)
    entry.delete(0, tk.END)

    lower = message.lower()
    bot_message = ""

    # Special case: If we don't have a name yet, treat the first message as the name
    if lower == "reset":
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)  # Delete all content
        if name:
            text_area.insert(tk.END, f"Chatbot: Welcome back, {name}! Type 'help' to see available commands.\n")
        else:
            text_area.insert(tk.END, "Chatbot: What's your name?\n")
        text_area.config(state=tk.DISABLED)
        return
    if name is None:
        name = message.strip()
        save_name(name)
        response = f"Chatbot: Nice to meet you, {name}! Send 'Help' for commands.\n"
        bot_message = f"[{timestamp}] {response}" if show_timestamp.get() else f"{response}"
    # Process commands and generate responses
    elif "hello" in lower or "hi" in lower or "hey" in lower:
        responses = ["Hello!", "Hi there!", "Greetings!", "What is up!?", "Hey!", "Howdy!", "Good to see you!", "How are you doing?"]
        response = "Chatbot: " + random.choice(responses) + "\n"
        bot_message = f"[{timestamp}] {response}" if show_timestamp.get() else f"{response}"
    elif "what is my name" in lower:
        response = "Chatbot: Your name is " + name + ". You could change this by manually editing the name.txt file."
        bot_message = f"[{timestamp}] {response}" if show_timestamp.get() else f"{response}"
    #elif name in lower:
        #response = "Thanks for your name! Send 'Help' in the chat to see a list of commands.\n"
        #bot_message = f"[{timestamp}] {response}" if show_timestamp.get() else f"{response}"
    elif "how are you" in lower:
        responses = ["Great, what about yourself?", "I'm doing well, thank you!", "I'm good, how about you?", "I'm doing great, what about you?"]
        response = "Chatbot: " + random.choice(responses) + "\n"
        bot_message = f"[{timestamp}] {response}" if show_timestamp.get() else f"{response}"
    elif "what is your name" in lower:
        response = "Chatbot: I'm a simple Python chatbot without a name.\n"
        bot_message = f"[{timestamp}] {response}" if show_timestamp.get() else f"{response}"
    elif "tell me a joke" in lower:
        response = "Chatbot: Why did the scarecrow win an award? Because he was outstanding in his field!\n"
        bot_message = f"[{timestamp}] {response}" if show_timestamp.get() else f"{response}"
    elif "thanks" in lower or "thank" in lower:
        responses = ["You're welcome!", "No problem!", "No worries!", "Anytime!"]
        response = "Chatbot: " + random.choice(responses) + "\n"
        bot_message = f"[{timestamp}] {response}" if show_timestamp.get() else f"{response}"
    elif "chat background pink" in lower:
        text_area.configure(bg="pink")
        response = "Chatbot: Background color changed to pink!\n"
        bot_message = f"[{timestamp}] {response}" if show_timestamp.get() else f"{response}"
    elif "chat background default" in lower:
        text_area.configure(bg=original_text_bg)
        response = "Chatbot: Chat background color reset to default.\n"
        bot_message = f"[{timestamp}] {response}" if show_timestamp.get() else f"{response}"
    elif "help" in lower:
        response = "Chatbot: Here are some commands you \ can use:\n" \
                   "- Hello, Hi, Hey\n" \
                   "- What is my name?\n" \
                   "- How are you?\n" \
                   "- What is your name?\n" \
                   "- Tell me a joke\n" \
                   "- Thanks\n" \
                   "- Chat background pink\n" \
                   "- Chat background default\n" \
                   "- Help\n" \
                   "- Reset\n" \
                   "- Bye, Goodbye, Exit, Quit, Close, Leave\n"
        bot_message = f"[{timestamp}] {response}" if show_timestamp.get() else f"{response}"
    elif "bye" in lower or "goodbye" in lower or "exit" in lower or "quit" in lower or "close" in lower or "leave" in lower:
        response = "Chatbot: Goodbye! Have a great day!\n"
        text_area.config(state=tk.NORMAL)
        text_area.insert(tk.END, response)
        text_area.config(state=tk.DISABLED)
        # Schedule window to close after the configured delay
        window.after(close_delay.get(), close_window)
        return
    else:
        catch_all = ["That's interesting!", "Tell me more!", "I don't have an answer for that.", "Okay.", "Cool!", "I am not sure I understand.", "What?"]
        response = "Chatbot: " + random.choice(catch_all) + "\n"
        bot_message = f"[{timestamp}] {response}" if show_timestamp.get() else f"{response}"

    if align_right.get():
        bot_message = f"{' ' * 40}{bot_message}"

    # Schedule the bot's response with the configured delay
    window.after(message_delay.get(), lambda: send_bot_message(bot_message))


entry.bind("<Return>", send_message)

# Initial message
if name:
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, f"Chatbot: Welcome back, {name}! Send 'Help' in the chat to see a list of commands.\n")
    text_area.config(state=tk.DISABLED)
else:
    text_area.config(state=tk.NORMAL)
    text_area.insert(tk.END, "Chatbot: What's your name?\n")
    text_area.config(state=tk.DISABLED)

window.after(100, bring_to_front_non_topmost)

window.mainloop()