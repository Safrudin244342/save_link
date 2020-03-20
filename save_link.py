from tkinter import Tk, Label, Entry, Button
from tkinter.messagebox import askquestion, showinfo
from tkinter.ttk import Treeview, Scrollbar
import csv
from os import path
from datetime import datetime


class application:
    root = ""

    def __init__(self, root):
        self.root = root
        application.root = self.root
        self.root.title("Save Your Link")
        self.root.resizable(False, False)
        self.root.geometry('1000x300')

        # menyeting layout dari applikasi
        self.layout(self.root)
        application.layout.txt_nama.focus_set()

        # menngani proses exit user
        self.root.protocol('WM_DELETE_WINDOW', application.backproses().quit)
        application.backproses().baca_data()

    # class untuk setting layout
    class layout:

        # deklarasi semua komponen yang ada
        txt_nama = Entry
        txt_link = Entry
        txt_deskripsi = Entry
        table = Treeview

        def __init__(self, root):
            self.root = root

            # membuat label untuk memasukkan nama link
            Label(self.root, text="Masukkan Nama Link : ").place(x=10, y=10)
            application.layout.txt_nama = Entry(self.root)
            application.layout.txt_nama.place(x=10, y=30)

            # membuat label untuk memasukkan link
            Label(self.root, text="Masukkan Link yang akan di simpan : ").place(x=10, y=60)
            application.layout.txt_link = Entry(self.root)
            application.layout.txt_link['width'] = 34
            application.layout.txt_link.place(x=10, y=80)

            # membuat kolom untuk memasukkan deskripsi
            Label(self.root, text="Masukkan deskripsi link : ").place(x=10, y=110)
            application.layout.txt_deskripsi = Entry(self.root)
            application.layout.txt_deskripsi['width'] = 34
            application.layout.txt_deskripsi.place(x=10, y=130)

            # membuat fungsi untuk menangani keypress dari user
            application.layout.txt_deskripsi.bind('<Key>', application.commad().key_press)

            # menampilakn table
            Label(self.root, text="Daftar Link yang Sudah tersimpan : ").place(x=310, y=10)
            application.layout.table = Treeview(self.root, columns=('nama', 'link', 'deskripsi'), height=11)
            application.layout.table.place(x=300, y=30)

            ybs = Scrollbar(self.root, orient='vertical', command=application.layout.table.yview)
            application.layout.table.configure(yscroll=ybs.set)
            ybs.place(x=971, y=30, height=241)

            xbs = Scrollbar(self.root, orient='horizontal', command=application.layout.table.xview)
            application.layout.table.configure(xscroll=xbs.set)
            xbs.place(x=300, y=271, width=672)

            application.layout.table.heading('#0', text='Id')
            application.layout.table.column('#0', width=40, minwidth=40)

            application.layout.table.heading('nama', text='Nama')
            application.layout.table.column('nama', width=150, minwidth=150)

            application.layout.table.heading('link', text='Link')
            application.layout.table.column('link', width=240, minwidth=240)

            application.layout.table.heading('deskripsi', text='Deskripsi')
            application.layout.table.column('deskripsi', width=240, minwidth=240)

            application.layout.table.bind('<Double-1>', application.commad().select_table, add='+')

            # membuat button untuk eksekusi
            Button(self.root, text="Simpan Link", command=application.commad().save_link).place(x=90, y=165)
            Button(self.root, text="Cek select", command=application.commad().select_table).place(x=90, y=195)

    # class untuk menangani semua aksi dari user
    class commad:

        # fungsi untuk menampilkan item yang diselect user
        def select_table(self, event):
            item = application.layout.table.focus()
            konten = application.layout.table.item(item)
            detail_konten = konten['values']
            print(detail_konten)

        # fungsi untuk save link
        def save_link(self):
            # mengumpulkan semua data yang dibutuhkan
            nama = application.layout.txt_nama.get()
            link = application.layout.txt_link.get()
            deskripsi = application.layout.txt_deskripsi.get()

            # cek apakah semua kolom telah diisi
            if len(nama) > 0 and len(link) > 0 and len(deskripsi) > 0:
                # menyimpan link ke dalam file csv
                if application.backproses().cek_folder("/usr/project/python/save_link/link.csv"):
                    file = open("/usr/project/python/save_link/link.csv", "a")
                else:
                    file = open("/usr/project/python/save_link/link.csv", 'a')

                file_csv = csv.writer(file)

                file_csv.writerow((nama, link, deskripsi))
                print("\nAdd Data : ")
                print(" Nama : " + nama)
                print(" Link : " + link)
                print(" Deskripsi : " + deskripsi)
                application.layout.table.insert('', 'end', values=(nama, link, deskripsi))

                file.close()

                # menampilkan pesan bahwa link telah disipan
                showinfo('Success', 'Link telah tersimpan!')

                # membersihkan semua kolom
                application.layout.txt_nama.delete(0, 'end')
                application.layout.txt_link.delete(0, 'end')
                application.layout.txt_deskripsi.delete(0, 'end')
                application.layout.txt_nama.focus_set()
            # jika user belum mengisi semua kolom
            else:
                showinfo('Info', 'Kamu belum mengisi semua kolomnya!')

        # membuat fungsi untuk menangani keypress
        def key_press(self, huruf):
            if huruf.keycode == 36:
                self.save_link()

    # class untuk proses yang berjalan di latar belakang
    class backproses:

        def quit(self):
            cek = askquestion('Info', 'Apakah kamu akan keluar?')
            if cek == "yes":
                application.root.destroy()

        # membuat fungsi untuk mengecek apakah file sudah ada
        def cek_folder(self, file):
            file = path.dirname(file)
            if path.exists(file):
                return True
            else:
                return False

        # class untuk memasukkan data kedalam table
        def baca_data(self):
            if self.cek_folder('/usr/project/python/save_link/link.csv'):
                file = open('/usr/project/python/save_link/link.csv', 'r')
                file_csv = csv.reader(file)
                for data in file_csv:
                    application.layout.table.insert('', 'end', values=data)

print("========================================================================")
print(datetime.now())

root = Tk()
application(root)
root.mainloop()
