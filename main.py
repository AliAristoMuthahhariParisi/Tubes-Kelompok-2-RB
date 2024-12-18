# Kelompok 2 RB

import tkinter as tk
from tkinter import messagebox, simpledialog

# DATA
# Dictionary untuk menyimpan username dan password
users = {"admin": "1234"}  # Username dan password
questions = []  # List soal, setiap soal adalah dictionary dengan kunci 'question' dan 'answer'
current_user = None  # Variabel untuk menyimpan user yang sedang login
score = 0  # Skor pengguna saat menjawab kuis

# FUNCTIONALITY
# Fungsi untuk login ke aplikasi
def login():
    global current_user
    username = simpledialog.askstring("Login", "Masukkan username:")
    password = simpledialog.askstring("Login", "Masukkan password:", show='*')
    if username in users and users[username] == password:
        current_user = username  # Set user yang sedang login
        messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
        show_main_menu()  # Tampilkan menu utama setelah login berhasil
    else:
        messagebox.showerror("Login Gagal", "Username atau password salah")

# Fungsi untuk menambahkan soal baru
def add_question():
    question = simpledialog.askstring("Tambah Soal", "Masukkan soal:")
    answer = simpledialog.askstring("Tambah Jawaban", "Masukkan jawaban benar:")
    if question and answer:
        questions.append({"question": question, "answer": answer})  # Tambahkan soal ke list
        messagebox.showinfo("Sukses", "Soal berhasil ditambahkan")
    else:
        messagebox.showerror("Error", "Soal atau jawaban tidak boleh kosong")

# Fungsi untuk mengedit soal yang sudah ada
def edit_question():
    show_questions()  # Tampilkan semua soal
    index = simpledialog.askinteger("Edit Soal", "Masukkan nomor soal yang ingin diubah:")
    if index and 0 < index <= len(questions):
        new_question = simpledialog.askstring("Edit Soal", "Masukkan soal baru:")
        new_answer = simpledialog.askstring("Edit Jawaban", "Masukkan jawaban baru:")
        if new_question and new_answer:
            questions[index - 1]["question"] = new_question  # Update soal
            questions[index - 1]["answer"] = new_answer  # Update jawaban
            messagebox.showinfo("Sukses", "Soal berhasil diubah")
        else:
            messagebox.showerror("Error", "Soal atau jawaban tidak boleh kosong")
    else:
        messagebox.showerror("Error", "Nomor soal tidak valid")

# Fungsi untuk menghapus soal
def delete_question():
    show_questions()  # Tampilkan semua soal
    index = simpledialog.askinteger("Hapus Soal", "Masukkan nomor soal yang ingin dihapus:")
    if index and 0 < index <= len(questions):
        questions.pop(index - 1)  # Hapus soal berdasarkan indeks
        messagebox.showinfo("Sukses", "Soal berhasil dihapus")
    else:
        messagebox.showerror("Error", "Nomor soal tidak valid")

# Fungsi untuk menampilkan daftar semua soal
def show_questions():
    if not questions:
        messagebox.showinfo("Soal Kosong", "Belum ada soal yang ditambahkan")
        return
    text = "\n".join([f"{i+1}. {q['question']}" for i, q in enumerate(questions)])  # Format daftar soal
    messagebox.showinfo("Daftar Soal", text)

# Fungsi untuk memulai kuis
def quiz():
    global score
    score = 0  # Reset skor
    if not questions:
        messagebox.showinfo("Soal Kosong", "Belum ada soal untuk dijawab")
        return
    for q in questions:
        answer = simpledialog.askstring("Kuis", q['question'])  # Tanya soal kepada user
        if answer and answer.lower() == q['answer'].lower():  # Cek jawaban (case-insensitive)
            score += 1
    messagebox.showinfo("Skor", f"Kuis selesai! Skor Anda: {score}/{len(questions)}")

# MAIN MENU
# Fungsi untuk menampilkan menu utama aplikasi
def show_main_menu():
    window = tk.Toplevel(root)  # Buat window baru untuk menu utama
    window.title("Menu Utama")
    tk.Label(window, text=f"Selamat datang, {current_user}!", font=("Arial", 14)).pack()

    # Tombol-tombol di menu utama
    tk.Button(window, text="Tambah Soal", command=add_question).pack(fill="x")
    tk.Button(window, text="Edit Soal", command=edit_question).pack(fill="x")
    tk.Button(window, text="Hapus Soal", command=delete_question).pack(fill="x")
    tk.Button(window, text="Lihat Semua Soal", command=show_questions).pack(fill="x")
    tk.Button(window, text="Mulai Kuis", command=quiz).pack(fill="x")
    tk.Button(window, text="Keluar", command=window.destroy).pack(fill="x")

# ROOT WINDOW
root = tk.Tk()
root.withdraw()  # Sembunyikan root window utama
root.title("Aplikasi Kuis")
login()  # Panggil fungsi login pertama kali
root.mainloop()
