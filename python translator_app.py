# translator_app_fixed.py
import tkinter as tk
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator
import pyperclip
import subprocess
import threading

# -------------------------------
# Text-to-Speech (Windows PowerShell)
# -------------------------------
def speak_text_win(text):
    """Use Windows PowerShell TTS (synchronous, reliable)."""
    if not text.strip():
        messagebox.showwarning("No Text", "Nothing to speak!")
        return
    try:
        # Escape double quotes in text for PowerShell
        escaped_text = text.replace('"', '`"')
        command = f'Add-Type -AssemblyName System.Speech; ' \
                  f'$speak=New-Object System.Speech.Synthesis.SpeechSynthesizer; ' \
                  f'$speak.Rate=-1; $speak.Speak("{escaped_text}");'
        subprocess.run(["powershell", "-Command", command], check=True)
    except Exception as e:
        messagebox.showerror("Speech Error", str(e))

def speak_text_async(text):
    """Run TTS in a separate thread to avoid GUI freeze."""
    threading.Thread(target=speak_text_win, args=(text,), daemon=True).start()

# -------------------------------
# Translator Functions
# -------------------------------
def translate_text():
    text = text_input.get("1.0", tk.END).strip()
    src = source_lang.get()
    dest = target_lang.get()
    if not text:
        messagebox.showwarning("Input Needed", "Please enter text to translate.")
        return
    try:
        translated = GoogleTranslator(source=src, target=dest).translate(text)
        text_output.delete("1.0", tk.END)
        text_output.insert(tk.END, translated)
    except Exception as e:
        messagebox.showerror("Translation Error", str(e))

def copy_text():
    text = text_output.get("1.0", tk.END).strip()
    if text:
        pyperclip.copy(text)
        messagebox.showinfo("Copied", "Text copied to clipboard!")
    else:
        messagebox.showwarning("Empty Output", "Nothing to copy!")

def speak_output():
    text = text_output.get("1.0", tk.END).strip()
    if text:
        speak_text_async(text)
    else:
        messagebox.showwarning("Empty Output", "Nothing to speak!")

# -------------------------------
# GUI Setup
# -------------------------------
root = tk.Tk()
root.title("AI Language Translator (VS Code Ready)")
root.geometry("700x500")
root.resizable(False, False)

# Supported languages
langs = ['en', 'hi', 'fr', 'es', 'de', 'mr', 'ta']

# Input Area
tk.Label(root, text="Enter text:", font=("Segoe UI", 10, "bold")).pack(pady=5)
text_input = tk.Text(root, height=5, width=80, wrap="word")
text_input.pack(pady=5)

# Language Selectors
frame = tk.Frame(root)
frame.pack(pady=10)
source_lang = ttk.Combobox(frame, values=langs, width=10)
source_lang.set('en')
source_lang.grid(row=0, column=0, padx=10)
target_lang = ttk.Combobox(frame, values=langs, width=10)
target_lang.set('hi')
target_lang.grid(row=0, column=1, padx=10)

# Translate Button
tk.Button(root, text="Translate", command=translate_text,
          bg="#0078D7", fg="white", font=("Segoe UI", 10, "bold"), width=15).pack(pady=5)

# Output Area
text_output = tk.Text(root, height=5, width=80, wrap="word")
text_output.pack(pady=5)

# Bottom Buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)
tk.Button(button_frame, text="📋 Copy", command=copy_text, width=12).grid(row=0, column=0, padx=40)
tk.Button(button_frame, text="🔊 Speak", command=speak_output, width=12).grid(row=0, column=1, padx=40)

# Run GUI
root.mainloop()
