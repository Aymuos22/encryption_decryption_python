import tkinter as tk
from PIL import Image, ImageTk

def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shifted = ord(char) + shift
            if char.islower():
                if shifted > ord('z'):
                    shifted -= 26
                elif shifted < ord('a'):
                    shifted += 26
            elif char.isupper():
                if shifted > ord('Z'):
                    shifted -= 26
                elif shifted < ord('A'):
                    shifted += 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def atbash_encrypt(text):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                encrypted_text += chr(219 - ord(char))
            elif char.isupper():
                encrypted_text += chr(155 - ord(char))
        else:
            encrypted_text += char
    return encrypted_text

def atbash_decrypt(text):
    return atbash_encrypt(text)

def affine_encrypt(text, a, b):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                encrypted_text += chr(((ord(char) - ord('a')) * a + b) % 26 + ord('a'))
            elif char.isupper():
                encrypted_text += chr(((ord(char) - ord('A')) * a + b) % 26 + ord('A'))
        else:
            encrypted_text += char
    return encrypted_text

def affine_decrypt(text, a, b):
    
    a_inv = None
    for i in range(26):
        if (a * i) % 26 == 1:
            a_inv = i
            break
    if a_inv is None:
        return "Error: 'a' value is not coprime with 26."

    decrypted_text = ""
    for char in text:
        if char.isalpha():
            if char.islower():
                decrypted_text += chr(((a_inv * (ord(char) - ord('a') - b)) % 26) + ord('a'))
            elif char.isupper():
                decrypted_text += chr(((a_inv * (ord(char) - ord('A') - b)) % 26) + ord('A'))
        else:
            decrypted_text += char
    return decrypted_text

def vigenere_encrypt(text, key):
    key = key.upper()
    encrypted_text = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            if char.islower():
                encrypted_text += chr(((ord(char) - ord('a') + ord(key[key_index]) - ord('A')) % 26) + ord('a'))
            elif char.isupper():
                encrypted_text += chr(((ord(char) - ord('A') + ord(key[key_index]) - ord('A')) % 26) + ord('A'))
            key_index = (key_index + 1) % len(key)
        else:
            encrypted_text += char
    return encrypted_text

def vigenere_decrypt(text, key):
    key = key.upper()
    decrypted_text = ""
    key_index = 0
    for char in text:
        if char.isalpha():
            if char.islower():
                decrypted_text += chr(((ord(char) - ord('a') - (ord(key[key_index]) - ord('A'))) % 26) + ord('a'))
            elif char.isupper():
                decrypted_text += chr(((ord(char) - ord('A') - (ord(key[key_index]) - ord('A'))) % 26) + ord('A'))
            key_index = (key_index + 1) % len(key)
        else:
            decrypted_text += char
    return decrypted_text

def create_playfair_matrix(key):
    alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # excluding 'J' as per Playfair cipher rules
    key = key.upper().replace("J", "I")  # replacing 'J' with 'I' in the key

    matrix = []
    for char in key:
        if char not in matrix and char in alphabet:
            matrix.append(char)

    for char in alphabet:
        if char not in matrix:
            matrix.append(char)

    playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
    return playfair_matrix

def find_char_positions(matrix, char):
    positions = []
    for i, row in enumerate(matrix):
        for j, val in enumerate(row):
            if val == char:
                positions.append((i, j))
    return positions

def playfair_encrypt(text, key):
    key = key.upper().replace("J", "I")  # replacing 'J' with 'I' in the key
    playfair_matrix = create_playfair_matrix(key)

    processed_text = []
    text = text.upper().replace("J", "I")  # replacing 'J' with 'I' in the plaintext
    i = 0
    while i < len(text):
        if i == len(text) - 1:
            processed_text.append(text[i] + 'X')
        elif text[i] == text[i + 1]:
            processed_text.append(text[i] + 'X')
            i += 1
        else:
            processed_text.append(text[i] + text[i + 1])
            i += 2

    encrypted_text = ""
    for pair in processed_text:
        char1, char2 = pair[0], pair[1]
        char1_positions = find_char_positions(playfair_matrix, char1)
        char2_positions = find_char_positions(playfair_matrix, char2)

        if char1_positions[0][0] == char2_positions[0][0]:  # same row
            encrypted_text += playfair_matrix[char1_positions[0][0]][(char1_positions[0][1] + 1) % 5]
            encrypted_text += playfair_matrix[char2_positions[0][0]][(char2_positions[0][1] + 1) % 5]
        elif char1_positions[0][1] == char2_positions[0][1]:  # same column
            encrypted_text += playfair_matrix[(char1_positions[0][0] + 1) % 5][char1_positions[0][1]]
            encrypted_text += playfair_matrix[(char2_positions[0][0] + 1) % 5][char2_positions[0][1]]
        else:
            encrypted_text += playfair_matrix[char1_positions[0][0]][char2_positions[0][1]]
            encrypted_text += playfair_matrix[char2_positions[0][0]][char1_positions[0][1]]

    return encrypted_text

def playfair_decrypt(text, key):
    key = key.upper().replace("J", "I")  # replacing 'J' with 'I' in the key
    playfair_matrix = create_playfair_matrix(key)

    processed_text = []
    text = text.upper().replace("J", "I")  # replacing 'J' with 'I' in the ciphertext
    i = 0
    while i < len(text):
        processed_text.append(text[i] + text[i + 1])
        i += 2

    decrypted_text = ""
    for pair in processed_text:
        char1, char2 = pair[0], pair[1]
        char1_positions = find_char_positions(playfair_matrix, char1)
        char2_positions = find_char_positions(playfair_matrix, char2)

        if char1_positions[0][0] == char2_positions[0][0]:  # same row
            decrypted_text += playfair_matrix[char1_positions[0][0]][(char1_positions[0][1] - 1) % 5]
            decrypted_text += playfair_matrix[char2_positions[0][0]][(char2_positions[0][1] - 1) % 5]
        elif char1_positions[0][1] == char2_positions[0][1]:  # same column
            decrypted_text += playfair_matrix[(char1_positions[0][0] - 1) % 5][char1_positions[0][1]]
            decrypted_text += playfair_matrix[(char2_positions[0][0] - 1) % 5][char2_positions[0][1]]
        else:
            decrypted_text += playfair_matrix[char1_positions[0][0]][char2_positions[0][1]]
            decrypted_text += playfair_matrix[char2_positions[0][0]][char1_positions[0][1]]

    return decrypted_text

# Tkinter setup
root = tk.Tk()
root.title("Encryption and Decryption")
root.geometry("500x400")
root.resizable(False, False)


bg_image = Image.open("background_image.jpg")  
bg_image = bg_image.resize((500, 400), Image.ANTIALIAS)
bg_photo = ImageTk.PhotoImage(bg_image)
background_label = tk.Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

made_by_label = tk.Label(root, text="Made by Soumya Darshan", font=("Arial", 10))
made_by_label.pack(side=tk.BOTTOM, pady=10)

input_label = tk.Label(root, text="Enter Text:")
input_label.pack()
input_text = tk.Text(root, height=5, width=40)
input_text.pack()

output_label = tk.Label(root, text="Output:")
output_label.pack()

output_text = tk.Text(root, height=5, width=40)
output_text.pack()

method_var = tk.StringVar()
methods = ["Caesar", "Atbash", "Affine", "Vigenère", "Playfair"]
method_dropdown = tk.OptionMenu(root, method_var, *methods)
method_var.set(methods[0])
method_dropdown.pack()

# Function to perform encryption or decryption based on the selected method
def perform_operation():
    selected_method = method_var.get()
    text = input_text.get("1.0", "end-1c")
    output_text.delete("1.0", tk.END)
    if selected_method == "Caesar":
        encrypted_text = caesar_encrypt(text, 3)  # You can adjust the shift value here
        output_text.insert(tk.END, f"Encrypted Text: {encrypted_text}")
    elif selected_method == "Atbash":
        encrypted_text = atbash_encrypt(text)
        output_text.insert(tk.END, f"Encrypted Text: {encrypted_text}")
    elif selected_method == "Affine":
        encrypted_text = affine_encrypt(text, 5, 8)  # You can adjust 'a' and 'b' values here
        output_text.insert(tk.END, f"Encrypted Text: {encrypted_text}")
    elif selected_method == "Vigenère":
        encrypted_text = vigenere_encrypt(text, "KEY")  # You can adjust the key here
        output_text.insert(tk.END, f"Encrypted Text: {encrypted_text}")
    elif selected_method == "Playfair":
        encrypted_text = playfair_encrypt(text, "KEYWORD")  # You can adjust the keyword here
        output_text.insert(tk.END, f"Encrypted Text: {encrypted_text}")

def perform_decryption():
    selected_method = method_var.get()
    text = input_text.get("1.0", "end-1c")
    output_text.delete("1.0", tk.END)
    if selected_method == "Caesar":
        decrypted_text = caesar_decrypt(text, 3)  # You can adjust the shift value here
        output_text.insert(tk.END, f"Decrypted Text: {decrypted_text}")
    elif selected_method == "Atbash":
        decrypted_text = atbash_decrypt(text)
        output_text.insert(tk.END, f"Decrypted Text: {decrypted_text}")
    elif selected_method == "Affine":
        decrypted_text = affine_decrypt(text, 5, 8)  # You can adjust 'a' and 'b' values here
        output_text.insert(tk.END, f"Decrypted Text: {decrypted_text}")
    elif selected_method == "Vigenère":
        decrypted_text = vigenere_decrypt(text, "KEY")  # You can adjust the key here
        output_text.insert(tk.END, f"Decrypted Text: {decrypted_text}")
    elif selected_method == "Playfair":
        decrypted_text = playfair_decrypt(text, "KEYWORD")  # You can adjust the keyword here
        output_text.insert(tk.END, f"Decrypted Text: {decrypted_text}")

encrypt_button = tk.Button(root, text="Encrypt", command=perform_operation)
encrypt_button.pack()

decrypt_button = tk.Button(root, text="Decrypt", command=perform_decryption)
decrypt_button.pack()

root.mainloop()

