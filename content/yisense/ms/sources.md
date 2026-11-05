---
version: "1.0"
updated: 2026-11-05
status: draft
---

# YiSense Sumber Kandungan dan Kaedah Pembentukan Heksagram

## Sumber dan renungan {#1}

Classics.json yang dibundel disusun daripada [data klasik meihua](https://github.com/toastedqu/meihua/blob/main/app/data/classics.json), diperoleh2026-09-19. Pautan Wikisource dan ID semakan dikekalkan bagi setiap heksagram (Qian:2404991). Hanya teks klasik domain awam digunakan, bukan ulasan moden pihak ketiga. Hak suntingan dan imej moden perlu diperiksa berasingan. Panduan ialah renungan, bukan ulasan lengkap atau AI. Tema harian menggunakan ordinal hari kalendar peranti: (ordinal−1) mod 64, bukan ramalan individu.

## Syiling dan nombor {#2}

Setiap garis mensimulasikan 3 syiling yang bebas antara satu sama lain, dengan peluang kepala dan ekor yang sama. Kepala bernilai 3 dan ekor 2. Jumlah 6, 7, 8 dan 9 masing-masing mewakili yin tua, yang muda, yin muda dan yang tua, dengan kebarangkalian teori 1/8, 3/8, 3/8 dan 1/8. Enam garis dibentuk dari bawah ke atas; garis bernilai 6 dan 9 bertukar polariti dalam heksagram berubah. Kaedah nombor menggunakan 3 integer positif dari 1 hingga 1,000,000. Baki nombor pertama dibahagi 8 menentukan trigram atas, baki nombor kedua dibahagi 8 menentukan trigram bawah, dan baki nombor ketiga dibahagi 6 menentukan garis berubah. Baki sifar dikira sebagai 8 atau 6. Urutan trigram ialah Qian, Dui, Li, Zhen, Xun, Kan, Gen, Kun. Garis bernombor 1–6 dari bawah ke atas. Jika ketiga-tiga ruang kosong, tiga nombor rawak dari 1 hingga 999 dijana secara automatik.

## Masa dan batasan {#3}

S ialah jumlah nombor cabang bumi tahun lunar (Zi = 1 hingga Hai = 12), nombor bulan lunar dan hari lunar. Bulan lompat menggunakan nombor bulan yang sama. Baki S dibahagi 8 menentukan trigram atas. Tambahkan nombor cabang waktu dua jam (Zi = 1 hingga Hai = 12) untuk mendapatkan T. Baki T dibahagi 8 menentukan trigram bawah, manakala baki dibahagi 6 menentukan garis berubah. Baki sifar mengikuti peraturan yang sama. Waktu Zi ialah 23:00–01:00, tetapi tarikh bertukar pada 00:00. Masa dan zon waktu peranti digunakan, termasuk peraturan waktu musim panas sistem, tanpa pelarasan waktu suria sebenar. Tahun lunar bertukar pada Tahun Baharu Lunar, bukan pada permulaan musim bunga (Li Chun). Bulan lunar tidak dianggap sebagai tiang bulan berdasarkan jieqi. Catatan menyimpan input, tarikh, zon waktu, nilai enam garis dan versi algoritma (kini 1). Tradisi mungkin berbeza; hasil bukan ramalan yang pasti. Hubungi [apw_service@163.com](mailto:apw_service@163.com).
