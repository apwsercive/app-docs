---
version: "1.0"
updated: 2026-11-03
status: draft
---

# YiSense Sumber Kandungan dan Kaedah Pembentukan Heksagram

## Sumber dan renungan {#1}

Classics.json yang dibundel disusun daripada [data klasik meihua](https://github.com/toastedqu/meihua/blob/main/app/data/classics.json), diperoleh2026-09-19. Pautan Wikisource dan ID semakan dikekalkan bagi setiap heksagram (Qian:2404991). Hanya teks klasik domain awam digunakan, bukan ulasan moden pihak ketiga. Hak suntingan dan imej moden perlu diperiksa berasingan. Panduan ialah renungan, bukan ulasan lengkap atau AI. Tema harian menggunakan ordinal hari kalendar peranti: (ordinal−1) mod 64, bukan ramalan individu.

## Syiling dan nombor {#2}

Setiap garis mensimulasikan3 syiling bebas dan seimbang: kepala3, ekor2. Jumlah6 yin tua,7 yang muda,8 yin muda,9 yang tua mempunyai kebarangkalian teori1/8,3/8,3/8,1/8. Enam garis dibina dari bawah;6 dan9 bertukar polariti. Tiga integer1–1,000,000: nombor pertama mod 8 memilih trigram atas, kedua mod 8 bawah, ketiga mod 6 garis berubah. Baki0 bermakna8 atau6. Urutan ialah Qian, Dui, Li, Zhen, Xun, Kan, Gen, Kun; garis1–6 dari bawah. Semua kosong menghasilkan nombor1–999 secara automatik.

## Masa dan batasan {#3}

S=nombor cabang bumi tahun lunar (Zi1–Hai12)+bulan lunar+hari lunar; bulan lompat menggunakan nombor bulan sama. S mod 8 memilih atas. T=S+nombor waktu dua jam (Zi1–Hai12); T mod 8 memilih bawah, T mod 6 garis berubah. Baki0 seperti di atas. Zi ialah23:00–01:00 tetapi hari bertukar00:00. Masa dan zon peranti termasuk peraturan waktu musim panas sistem digunakan, tanpa pembetulan suria sebenar. Tahun bertukar pada Tahun Baharu Lunar, bukan Awal Musim Bunga; bulan bukan tonggak bulan istilah suria. Input, tarikh, zon, enam garis dan algoritma versi1 disimpan. Tradisi boleh berbeza; bukan ramalan pasti. Hubungi [apw_service@163.com](mailto:apw_service@163.com).
