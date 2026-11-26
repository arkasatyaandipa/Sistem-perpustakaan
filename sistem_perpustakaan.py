"""
Sistem Perpustakaan Sederhana (OOP Python)
Konsep: class, object, constructor, attribute, method, encapsulation,
        property/setter, class method, static method
"""


class Buku:
    # Class attribute: menghitung total buku yang dibuat
    jumlah_buku = 0

    def __init__(self, kode, judul, penulis, stok):
        self.kode = kode
        self.judul = judul
        self.penulis = penulis
        self.__stok = 0          # private attribute (encapsulation)
        self.stok = stok         # lewat setter agar divalidasi
        Buku.jumlah_buku += 1

    # ---------- property & setter ----------
    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, nilai):
        if nilai < 0:
            raise ValueError("Stok tidak boleh negatif!")
        self.__stok = nilai

    # ---------- method ----------
    def kurangi_stok(self):
        if self.__stok > 0:
            self.__stok -= 1
            return True
        return False

    def tambah_stok(self):
        self.__stok += 1

    def info(self):
        return f"[{self.kode}] {self.judul} - {self.penulis} (stok: {self.__stok})"

    # ---------- class method ----------
    @classmethod
    def dari_string(cls, data):
        """Buat object Buku dari string 'kode;judul;penulis;stok'."""
        kode, judul, penulis, stok = data.split(";")
        return cls(kode, judul, penulis, int(stok))

    # ---------- static method ----------
    @staticmethod
    def validasi_kode(kode):
        """Kode buku harus diawali 'B' dan diikuti angka, contoh: B001."""
        return len(kode) >= 2 and kode[0] == "B" and kode[1:].isdigit()


class Anggota:
    MAKS_PINJAM = 3

    def __init__(self, nim, nama):
        self.nim = nim
        self.nama = nama
        self.__daftar_pinjam = []   # private attribute

    @property
    def daftar_pinjam(self):
        return list(self.__daftar_pinjam)   # read-only (salinan)

    def bisa_pinjam(self):
        return len(self.__daftar_pinjam) < Anggota.MAKS_PINJAM

    def tambah_pinjam(self, buku):
        self.__daftar_pinjam.append(buku)

    def hapus_pinjam(self, buku):
        self.__daftar_pinjam.remove(buku)

    def info(self):
        judul = ", ".join(b.judul for b in self.__daftar_pinjam) or "-"
        return f"{self.nim} | {self.nama} | Pinjam: {judul}"


class Perpustakaan:
    def __init__(self, nama):
        self.nama = nama
        self.__buku = {}
        self.__anggota = {}

    @staticmethod
    def cetak_struk(anggota, buku):
        from datetime import date, timedelta
        hari_ini = date.today()
        kembali = hari_ini + timedelta(days=7)
        print("\n" + "=" * 36)
        print("     STRUK PEMINJAMAN BUKU")
        print("     Perpustakaan UNIBA")
        print("=" * 36)
        print(f"Tanggal pinjam : {hari_ini.strftime('%d-%m-%Y')}")
        print(f"Nama           : {anggota.nama}")
        print(f"NIM            : {anggota.nim}")
        print("-" * 36)
        print(f"Kode buku      : {buku.kode}")
        print(f"Judul          : {buku.judul}")
        print(f"Penulis        : {buku.penulis}")
        print("-" * 36)
        print(f"Batas kembali  : {kembali.strftime('%d-%m-%Y')}")
        print("=" * 36)
        print("   Harap kembalikan tepat waktu!")
        print("=" * 36)

    def tambah_buku(self, buku):
        if not Buku.validasi_kode(buku.kode):
            print(f"Kode '{buku.kode}' tidak valid!")
            return
        self.__buku[buku.kode] = buku

    def daftar_anggota(self, anggota):
        self.__anggota[anggota.nim] = anggota

    def pinjam(self, nim, kode):
        anggota = self.__anggota.get(nim)
        buku = self.__buku.get(kode)
        if not anggota or not buku:
            print("Anggota atau buku tidak ditemukan.")
        elif not anggota.bisa_pinjam():
            print(f"{anggota.nama} sudah mencapai batas pinjam ({Anggota.MAKS_PINJAM}).")
        elif not buku.kurangi_stok():
            print(f"Stok '{buku.judul}' habis.")
        else:
            anggota.tambah_pinjam(buku)
            print(f"{anggota.nama} berhasil meminjam '{buku.judul}'.")
            Perpustakaan.cetak_struk(anggota, buku)

    def kembalikan(self, nim, kode):
        anggota = self.__anggota.get(nim)
        buku = self.__buku.get(kode)
        if anggota and buku and buku in anggota.daftar_pinjam:
            anggota.hapus_pinjam(buku)
            buku.tambah_stok()
            print(f"{anggota.nama} mengembalikan '{buku.judul}'.")
        else:
            print("Data pengembalian tidak valid.")

    def tampilkan_buku(self):
        print(f"\n=== List Buku {self.nama} ===")
        if not self.__buku:
            print("Belum ada buku.")
            return
        print(f"{'No':<4}{'Kode':<8}{'Judul':<26}{'Penulis':<18}{'Stok':<5}")
        print("-" * 61)
        for i, b in enumerate(self.__buku.values(), 1):
            print(f"{i:<4}{b.kode:<8}{b.judul:<26}{b.penulis:<18}{b.stok:<5}")

    def tampilkan_semua(self):
        print(f"\n=== Daftar Buku {self.nama} ===")
        for b in self.__buku.values():
            print(b.info())
        print("\n=== Daftar Anggota ===")
        for a in self.__anggota.values():
            print(a.info())
        print(f"\nTotal judul buku dibuat: {Buku.jumlah_buku}")


# ================== PROGRAM UTAMA ==================
def menu():
    perpus = Perpustakaan("Perpustakaan UNIBA")
    perpus.tambah_buku(Buku("B001", "Pemrograman Java", "Budi Santoso", 2))
    perpus.tambah_buku(Buku("B002", "Basis Data", "Siti Rahma", 1))
    perpus.tambah_buku(Buku.dari_string("B003;Pengembangan Web;Andi Wijaya;3"))
    perpus.daftar_anggota(Anggota("2024001", "Lvoid"))
    perpus.daftar_anggota(Anggota("2024002", "Rina"))

    while True:
        print("\n===== MENU PERPUSTAKAAN =====")
        print("1. List buku")
        print("2. Tambah buku")
        print("3. Pinjam buku")
        print("4. Kembalikan buku")
        print("5. Data anggota & peminjaman")
        print("0. Keluar")
        pilih = input("Pilih menu: ").strip()

        if pilih == "1":
            perpus.tampilkan_buku()
        elif pilih == "2":
            kode = input("Kode (contoh B004): ").strip()
            judul = input("Judul: ").strip()
            penulis = input("Penulis: ").strip()
            try:
                perpus.tambah_buku(Buku(kode, judul, penulis, int(input("Stok: "))))
                print("Buku ditambahkan.")
            except ValueError as e:
                print("Error:", e)
        elif pilih == "3":
            perpus.pinjam(input("NIM: ").strip(), input("Kode buku: ").strip())
        elif pilih == "4":
            perpus.kembalikan(input("NIM: ").strip(), input("Kode buku: ").strip())
        elif pilih == "5":
            perpus.tampilkan_semua()
        elif pilih == "0":
            print("Terima kasih!")
            break
        else:
            print("Menu tidak valid.")


if __name__ == "__main__":
    menu()
