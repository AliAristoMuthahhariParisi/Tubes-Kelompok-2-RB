import tkinter as tk
from tkinter import messagebox
from queue import Queue

# Struktur data queue untuk menyimpan soal
question_queue = Queue()
score = 0

# Data login (username dan password sederhana)
users = {}

# Fungsi untuk registrasi user baru
def register_user():
    new_username = reg_username_entry.get()
    new_password = reg_password_entry.get()

    if new_username and new_password:
        if new_username in users:
            messagebox.showerror("Error", "Username sudah terdaftar")
        else:
            users[new_username] = new_password
            messagebox.showinfo("Berhasil", "Registrasi berhasil! Silakan login.")
            register_window.destroy()
    else:
        messagebox.showerror("Error", "Username dan password tidak boleh kosong")

# Fungsi login
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username in users and users[username] == password:
        messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
        login_window.destroy()
        main_app(username)
    else:
        messagebox.showerror("Login Gagal", "Username atau password salah")

# Fungsi utama aplikasi setelah login
def main_app(username):
    global question_entry, answer_entry, score_label, question_label, answer_input, main_window

    main_window = tk.Tk()
    main_window.title("Sistem Manajemen Soal")
    
    # Full screen mode
    main_window.attributes("-fullscreen", True)
    main_window.configure(bg="#2E2E2E")  # Dark grey background

    tk.Label(main_window, text=f"Halo, {username}!", font=("Arial", 16, "bold"), fg="#FFF", bg="#2E2E2E").grid(row=0, column=0, columnspan=2, pady=20)

    # Input soal
    tk.Label(main_window, text="Soal", fg="#FFF", bg="#2E2E2E").grid(row=1, column=0, pady=5)
    question_entry = tk.Entry(main_window, width=50, font=("Arial", 12), bd=2)
    question_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(main_window, text="Jawaban", fg="#FFF", bg="#2E2E2E").grid(row=2, column=0, pady=5)
    answer_entry = tk.Entry(main_window, width=50, font=("Arial", 12), bd=2)
    answer_entry.grid(row=2, column=1, padx=10, pady=5)

    # Tombol operasi
    tk.Button(main_window, text="Tambah Soal", command=add_question, bg="#4CAF50", fg="white").grid(row=3, column=0, pady=10)
    tk.Button(main_window, text="Simpan Soal", command=save_questions, bg="#2196F3", fg="white").grid(row=3, column=1, pady=10)

    # Menjawab soal
    tk.Label(main_window, text="Pertanyaan Saat Ini", fg="#FFF", font=("Arial", 14), bg="#2E2E2E").grid(row=5, column=0, columnspan=2, pady=15)
    question_label = tk.Label(main_window, text="Belum ada soal", fg="#FFF", font=("Arial", 12), bg="#2E2E2E")
    question_label.grid(row=6, column=0, columnspan=2, pady=10)

    tk.Label(main_window, text="Jawaban Anda", fg="#FFF", bg="#2E2E2E").grid(row=7, column=0, pady=5)
    answer_input = tk.Entry(main_window, width=50, font=("Arial", 12), bd=2)
    answer_input.grid(row=7, column=1, padx=10, pady=5)

    tk.Button(main_window, text="Jawab Soal", command=answer_question, bg="#4CAF50", fg="white").grid(row=8, column=0, pady=10)

    score_label = tk.Label(main_window, text=f"Skor: {score}", font=("Arial", 12, "bold"), fg="#FFF", bg="#2E2E2E")
    score_label.grid(row=8, column=1, pady=10)

    main_window.mainloop()

# Fungsi untuk menambah soal ke dalam queue
def add_question():
    question = question_entry.get()
    answer = answer_entry.get()

    if question and answer:
        question_queue.put((question, answer))
        messagebox.showinfo("Berhasil", "Soal berhasil ditambahkan")
        question_entry.delete(0, tk.END)
        answer_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Soal dan jawaban tidak boleh kosong")

# Fungsi untuk menyimpan semua soal ke file
def save_questions():
    if question_queue.empty():
        messagebox.showerror("Error", "Tidak ada soal untuk disimpan")
        return

    with open("questions.txt", "w") as file:
        temp_queue = Queue()
        while not question_queue.empty():
            question, answer = question_queue.get()
            file.write(f"{question}|{answer}\n")
            temp_queue.put((question, answer))
        while not temp_queue.empty():
            question_queue.put(temp_queue.get())

    messagebox.showinfo("Berhasil", "Soal berhasil disimpan ke file")

# Fungsi untuk menjawab soal dan menampilkan skor
def answer_question():
    global score

    if question_queue.empty():
        messagebox.showinfo("Info", "Tidak ada soal yang tersedia")
        return

    question, correct_answer = question_queue.get()
    question_label.config(text=question)

    def check_answer():
        user_answer = answer_input.get()

        if user_answer.lower() == correct_answer.lower():
            global score
            score += 1
            messagebox.showinfo("Benar", "Jawaban benar!")
        else:
            messagebox.showerror("Salah", f"Jawaban salah! Jawaban benar: {correct_answer}")

        score_label.config(text=f"Skor: {score}")
        answer_input.delete(0, tk.END)

    tk.Button(main_window, text="Submit Jawaban", command=check_answer, bg="#4CAF50", fg="white").grid(row=7, column=1, pady=5)

# Fungsi untuk membuka jendela registrasi
def open_register_window():
    global reg_username_entry, reg_password_entry, register_window

    register_window = tk.Toplevel()
    register_window.title("Registrasi")
    register_window.configure(bg="#2E2E2E")

    tk.Label(register_window, text="Username", fg="#FFF", bg="#2E2E2E").grid(row=0, column=0)
    reg_username_entry = tk.Entry(register_window)
    reg_username_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(register_window, text="Password", fg="#FFF", bg="#2E2E2E").grid(row=1, column=0)
    reg_password_entry = tk.Entry(register_window, show="*")
    reg_password_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(register_window, text="Daftar", command=register_user, bg="#4CAF50", fg="white").grid(row=2, column=0, columnspan=2, pady=10)

# Login window
login_window = tk.Tk()
login_window.title("Login")
login_window.configure(bg="#2E2E2E")

# Full screen mode for login
login_window.attributes("-fullscreen", True)

# Username input
tk.Label(login_window, text="Username", fg="#FFF", bg="#2E2E2E").grid(row=0, column=0)
username_entry = tk.Entry(login_window)
username_entry.grid(row=0, column=1, padx=10, pady=5)

# Password input
tk.Label(login_window, text="Password", fg="#FFF", bg="#2E2E2E").grid(row=1, column=0)
password_entry = tk.Entry(login_window, show="*")
password_entry.grid(row=1, column=1, padx=10, pady=5)

# Login and Register buttons
tk.Button(login_window, text="Login", command=login, bg="#4CAF50", fg="white").grid(row=2, column=0, pady=10)
tk.Button(login_window, text="Daftar", command=open_register_window, bg="#2196F3", fg="white").grid(row=2, column=1, pady=10)

login_window.mainloop()
