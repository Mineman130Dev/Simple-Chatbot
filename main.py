import random
import os
import tkinter as tk

def load_name(): #loading the name from the text file
    if os.path.exists("name.txt"):
        with open("name.txt", "r") as file:
            return file.read().strip()
    return None

def save_name(name): #saving the name in the text file
    with open("name.txt", "w") as file:
        file.write(name)

name = load_name()  # load the name

window = tk.Tk()
window.title("Chatbot")

window.attributes("-topmost", True) # make the window on top of others

window.resizable(False, False) #window is not resizable

text_area = tk.Text(window)
text_area.pack()

entry = tk.Entry(window)
entry.pack()

def send_message(event=None):
    message = entry.get()
    text_area.insert(tk.END, "You: " + message + "\n")
    entry.delete(0, tk.END)

    lower = message.lower()

    if "hello" in lower or "hi" in lower:
        responses = ["Hello!", "Hi there!", "Greetings!"]
        response = "Chatbot: " + random.choice(responses) + "\n"
    elif "what is my name" in lower:
        response = "Chatbot: Your name is, " + name + ".\n"
    elif "how are you" in lower:
        responses = ["I'm just a computer program, but thanks for asking!", "Doing well, how about you?", "I'm here to help you!"]
        response = "Chatbot: " + random.choice(responses) + "\n"
    elif "what is your name" in lower:
        response = "Chatbot: I'm a simple Python chatbot without a name.\n"
    elif "tell me a joke" in lower:
        response = "Chatbot: Why did the scarecrow win an award? Because he was outstanding in his field!\n"
    elif "bye" in lower:
        response = "Chatbot: Goodbye! Have a great day!\n"
        text_area.insert(tk.END, response)
        window.destroy()
        return
    else:
        response = "Chatbot: I'm sorry, I don't understand that.\n"

    text_area.insert(tk.END, response)

send_button = tk.Button(window, text="Send", command=send_message)
send_button.pack()

entry.bind("<Return>", send_message) #return/enter key to send the message

if name:
    text_area.insert(tk.END, f"Chatbot: Welcome back, {name}!\n")
else:
    text_area.insert(tk.END, "Chatbot: What's your name?\n")

window.mainloop()