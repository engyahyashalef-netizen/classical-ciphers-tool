import tkinter as tk
from tkinter import ttk
import numpy as np
from pycipher import Vigenere, Autokey, Affine, Caesar

def hill_cipher(text, key_str, encrypt=True):
    try:
        key_vals = list(map(int, key_str.split(',')))
        if len(key_vals) != 4:
            return "المفتاح يجب أن يحتوي على 4 أرقام مفصولة بفواصل"
    except ValueError:
        return "مفتاح غير صالح"

    key_matrix = np.array(key_vals).reshape(2, 2)
    text = text.upper().replace(" ", "")
    if len(text) % 2 != 0:
        text += 'X'
    
    result = ""
    if encrypt:
        for i in range(0, len(text), 2):
            block = [ord(text[i]) - ord('A'), ord(text[i+1]) - ord('A')]
            vec = np.dot(key_matrix, block) % 26
            result += chr(vec[0] + ord('A')) + chr(vec[1] + ord('A'))
    else:
        det = int(round(np.linalg.det(key_matrix))) % 26
        try:
            det_inv = pow(det, -1, 26)
        except ValueError:
            return "مفتاح غير صالح"
        inv_matrix = (det_inv * np.linalg.inv(key_matrix) * det) % 26
        for i in range(0, len(text), 2):
            block = [ord(text[i]) - ord('A'), ord(text[i+1]) - ord('A')]
            vec = np.dot(inv_matrix, block) % 26
            result += chr(int(vec[0]) + ord('A')) + chr(int(vec[1]) + ord('A'))
    return result

def playfair_cipher_encrypt(text, key):
    text = text.replace(" ", "").lower()
    key = key.lower()
    alphabet = "abcdefghiklmnopqrstuvwxyz"
    matrix, key_set = [], set()
    
    for char in key + alphabet:
        if char not in key_set:
            key_set.add(char)
            matrix.append(char)
    
    matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
    pos_map = {matrix[i][j]: (i, j) for i in range(5) for j in range(5)}
    
    processed_text = ""
    i = 0
    while i < len(text):
        if i == len(text) - 1 or text[i] == text[i+1]:
            processed_text += text[i] + "x"
            i += 1
        else:
            processed_text += text[i] + text[i+1]
            i += 2
    
    cipher_text = ""
    for i in range(0, len(processed_text), 2):
        a, b = processed_text[i], processed_text[i+1]
        row1, col1 = pos_map[a]
        row2, col2 = pos_map[b]
        
        if row1 == row2:
            cipher_text += matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            cipher_text += matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2]
        else:
            cipher_text += matrix[row1][col2] + matrix[row2][col1]
    
    return cipher_text

def process_text():
    text, key = text_entry.get(), key_entry.get()
    operation = operation_var.get() == "Encrypt"
    cipher = cipher_var.get()
    
    try:
        if cipher == "Playfair":
            result = playfair_cipher_encrypt(text, key) if operation else "غير مدعوم حاليًا"
        else:
            result = "يرجى اختيار خوارزمية"
    except Exception as e:
        result = f"خطأ: {str(e)}"
    
    result_label.config(text=f"النتيجة: {result}")

root = tk.Tk()
root.title("تطبيق التشفير")
root.geometry("400x400")

tk.Label(root, text="اختر الخوارزمية:").pack()
cipher_var = tk.StringVar()
ciphers = ["Vigenere", "Playfair", "Autokey", "Affine", "Multiplicative", "Caesar", "Hill"]
ttk.Combobox(root, textvariable=cipher_var, values=ciphers, state="readonly").pack()

tk.Label(root, text="النص:").pack()
text_entry = tk.Entry(root, width=40)
text_entry.pack()

tk.Label(root, text="المفتاح:").pack()
key_entry = tk.Entry(root, width=40)
key_entry.pack()

operation_var = tk.StringVar(value="Encrypt")
ttk.Radiobutton(root, text="تشفير", variable=operation_var, value="Encrypt").pack()
ttk.Radiobutton(root, text="فك التشفير", variable=operation_var, value="Decrypt").pack()

result_label = tk.Label(root, text="النتيجة:")
result_label.pack()

tk.Button(root, text="تنفيذ", command=process_text).pack()
root.mainloop()
