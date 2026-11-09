Penjelasan Struktur:

1. `main.py` : File utama yang dijalankan untuk menampilkan jendela GUI game Brick Breaker berbasis OOP dengan tema pastel.

* `import tkinter as tk` : Perintah buat ngambil modul Tkinter supaya komponen GUI jendela game bisa dipakai.
* `import random` : Modul buat ngatur posisi acak dan pergerakan partikel kembang api saat pemain menang.
* `class Ball` : Kelas yang ngatur objek bola, mulai dari posisi awal, kecepatan pergerakan (*speed_x* dan *speed_y*), hingga logika pantulan saat bola mengenai dinding, paddle, atau jatuh ke bawah.
* `class Paddle` : Kelas buat ngatur papan pemantul di bawah layar, termasuk *event listener* buat mendeteksi tombol panah kiri dan kanan dari keyboard.
* `class Brick` : Kelas buat ngebentuk dan ngatur bata berbentuk hati yang estetik menggunakan kombinasi oval, poligon segitiga, dan garis tepi putih.
* `class BrickBreakerGame` : Kelas utama yang ngatur alur permainan secara keseluruhan, mulai dari inisialisasi skor, nyawa, tombol mulai, level game, hingga animasi kembang api.
* `tk.Canvas()` : Area atau wadah kanvas interaktif tempat objek bola, paddle, bata hati, dan animasi kembang api digambar dan digerakkan.
* `tk.Button()` : Tombol interaktif bertuliskan `💖 Mulai Game 💖` yang kalau diklik bakal memulai jalannya permainan.
* `root.mainloop()` : Perintah penutup buat ngejalanin *event loop* utama supaya jendela aplikasinya tetap terbuka dan merespons interaksi dari user.