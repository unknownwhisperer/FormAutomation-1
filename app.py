from flask import *  
from fpdf import FPDF
from datetime import date
import sqlite3
  
app = Flask(__name__)  
 
@app.route("/")
def index():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employees")
    rows = cur.fetchall()
    con.close()
    return render_template("index.html",rows = rows) 
 
@app.route("/add")
def add():
    return render_template("add.html")

@app.route("/insert",methods = ["POST"])
def insert():
    if request.method == "POST":
        try:
            no_registrasi = request.form["no_registrasi"]
            nama = request.form["nama"]
            tempat_tanggal_lahir = request.form["tempat_tanggal_lahir"]
            nik_nip = request.form["nik_nip"]
            email = request.form["email"]
            hp = request.form["hp"]
            hp_wali_atasan = request.form["hp_wali_atasan"]
            pekerjaan = request.form["pekerjaan"]
            alamat = request.form["alamat"]
            program_akademi = request.form["program_akademi"]
            tema_pelatihan = request.form["tema_pelatihan"]
            mitra_pelatihan = request.form["mitra_pelatihan"]
            kota_sekarang = request.form["kota_sekarang"]
            bulan_pelaksanaan = request.form["bulan_pelaksanaan"]
            saran = request.form["saran"] 
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO Employees (no_registrasi,nama,tempat_tanggal_lahir,nik_nip,email,hp,hp_wali_atasan,pekerjaan,alamat,program_akademi,tema_pelatihan,mitra_pelatihan,kota_sekarang,bulan_pelaksanaan,saran) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(no_registrasi,nama,tempat_tanggal_lahir,nik_nip,email,hp,hp_wali_atasan,pekerjaan,alamat,program_akademi,tema_pelatihan,mitra_pelatihan,kota_sekarang,bulan_pelaksanaan,saran))
                con.commit()
        except:
            con.rollback()
        finally:
            con.close()
            return redirect('/')

@app.route("/edit/<int:id_employees>")
def edit(id_employees):
    con = sqlite3.connect("database.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Employees where id_employees = ?",(id_employees,))
    rows = cur.fetchall()
    con.close()
    return render_template("edit.html",rows = rows)

@app.route("/update",methods = ["POST"])
def update():
    if request.method == "POST":
        try:
            id_employees = request.form["id_employees"]
            no_registrasi = request.form["no_registrasi"]
            nama = request.form["nama"]
            tempat_tanggal_lahir = request.form["tempat_tanggal_lahir"]
            nik_nip = request.form["nik_nip"]
            email = request.form["email"]
            hp = request.form["hp"]
            hp_wali_atasan = request.form["hp_wali_atasan"]
            pekerjaan = request.form["pekerjaan"]
            alamat = request.form["alamat"]
            program_akademi = request.form["program_akademi"]
            tema_pelatihan = request.form["tema_pelatihan"]
            mitra_pelatihan = request.form["mitra_pelatihan"]
            kota_sekarang = request.form["kota_sekarang"]
            bulan_pelaksanaan = request.form["bulan_pelaksanaan"]
            saran = request.form["saran"] 
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE Employees SET no_registrasi = ?,nama = ?,tempat_tanggal_lahir = ?,nik_nip = ?,email = ?,hp = ?,hp_wali_atasan = ?,pekerjaan = ?,alamat = ?,program_akademi = ?,tema_pelatihan = ?,mitra_pelatihan = ?,kota_sekarang = ?,bulan_pelaksanaan = ?,saran = ? WHERE id_employees = ?",(no_registrasi,nama,tempat_tanggal_lahir,nik_nip,email,hp,hp_wali_atasan,pekerjaan,alamat,program_akademi,tema_pelatihan,mitra_pelatihan,kota_sekarang,bulan_pelaksanaan,saran,id_employees))
                con.commit()
        except:
            con.rollback()
        finally:
            con.close()
            return redirect('/')
 
@app.route("/delete/<int:id_employees>")
def delete(id_employees):
    with sqlite3.connect("database.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from Employees where id_employees = ?",(id_employees,))
        except:  
            con.rollback()
        finally:
            return redirect('/')

@app.route("/fk/<int:id_employees>")
def fk(id_employees):
    con = sqlite3.connect("database.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Employees where id_employees = ?",(id_employees,))
    rows = cur.fetchall()
    con.close()

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.l_margin = pdf.l_margin*2.0
    pdf.r_margin = pdf.r_margin*2.0
    pdf.t_margin = pdf.t_margin*1.0
    pdf.b_margin = pdf.b_margin*1.0

    pdf.add_page()
    pdf.set_font("Arial",style='B', size=12)
    pdf.multi_cell(170,5, txt="FORM KOMITMEN PARTISIPASI PROGRAM PEMBERIAN BANTUAN PEMERINTAH DIGITAL TALENT SCHOLARSHIP TAHUN 2021", align="C")
    pdf.ln()
    pdf.set_font("Arial",style='I', size=10)
    pdf.multi_cell(170,5, txt="Formulir ini untuk diisi (diketik atau tulis tangan dengan jelas) kemudian diunggah/upload di akun digitalent.kominfo.go.id oleh masing-masing peserta di awal pelaksanaan pelatihan",border=1, align="J")
    pdf.ln()
    pdf.set_font("Arial", size=10)
    pdf.cell(170, 5, txt="Saya yang bertandatangan di bawah ini:",ln=1)

    for row in rows:
        pdf.cell(50, 5, txt="Nama Lengkap (Sesuai KTP)  :")
        pdf.cell(100, 5, txt=row["nama"],ln=1)
        pdf.cell(50, 5, txt="Tempat/Tanggal Lahir              :")
        pdf.cell(100, 5, txt=row["tempat_tanggal_lahir"], ln=1)
        pdf.cell(50, 5, txt="NIK/NIP                                    :")
        pdf.cell(100, 5, txt=row["nik_nip"], ln=1)
        pdf.cell(50, 5, txt="Email Aktif                                :")
        pdf.cell(100, 5, txt=row["email"], ln=1)
        pdf.cell(50, 5, txt="No HP Aktif                              :")
        pdf.cell(100, 5, txt=row["hp"], ln=1)
        pdf.cell(50, 5, txt="No HP Wali/Atasan                  :")
        pdf.cell(100, 5, txt=row["hp_wali_atasan"], ln=1)
        pdf.cell(50, 5, txt="Pekerjaan                                 :")
        pdf.cell(100, 5, txt=row["pekerjaan"], ln=1)
        pdf.cell(50, 5, txt="Alamat Domisili                        :")
        pdf.multi_cell(120, 5, txt=row["alamat"])
        pdf.cell(50, 5, txt="Program Akademi                    :")
        pdf.cell(100, 5, txt=row["program_akademi"], ln=1)
        pdf.cell(50, 5, txt="Tema Pelatihan                        :")
        pdf.cell(100, 5, txt=row["tema_pelatihan"], ln=1)
        pdf.cell(50, 5, txt="Mitra Pelatihan                         :")
        pdf.cell(100, 5, txt=row["mitra_pelatihan"], ln=1)
    
    pdf.ln()
    pdf.cell(170, 5, txt="Menyatakan : ",ln=1)
    pdf.cell(170, 5, txt="1. Bersedia mengikuti seluruh tahapan pelatihan sejak awal hingga selesai;",ln=1)
    pdf.cell(170, 5, txt="2. Bersedia menjadi calon Penerima Bantuan Pemerintah Digital Talent Scholarship Tahun 2021;",ln=1)
    pdf.cell(170, 5, txt="3. Bersedia memenuhi persyaratan administratif serta Syarat dan Ketentuan yang berlaku;",ln=1)
    pdf.cell(170, 5, txt="4. Bersedia memenuhi Kewajiban dan Tata Tertib sebagai peserta pelatihan;",ln=1)
    pdf.multi_cell(170,5,txt="5. Bersedia menerima dan tidak akan mengganggu-gugat segala keputusan Panitia Digital Talent Scholarship Tahun 2021;")
    pdf.multi_cell(170,5,txt="6. Bersedia memberikan informasi pribadi yang tercantum dalam form pendaftaran kepada Panitia Digital Talent Scholarship 2021 untuk kepentingan pelaksanaan pelatihan dan pasca pelatihan;")
    pdf.cell(170, 5, txt="7. Menaati segala ketentuan dan tata tertib yang diterapkan di lingkungan mitra penyelenggara; ",ln=1)
    pdf.multi_cell(170,5,txt="8. Mengerti dan setuju bahwa konten pelatihan digunakan hanya untuk kebutuhan Digital Talent Scholarship Kementerian Komunikasi dan Informatika. Segala konten pelatihan termasuk tidak terbatas pada soal tes substansi, soal kuis, soal mid exam, soal final exam, materi pelatihan, video, gambar dan kode ini mengandung Kekayaan Intelektual, peserta tunduk kepada undang-undang hak cipta, merek dagang atau hak kekayaan intelektual lainnya. Peserta dilarang untuk mereproduksi, memodifikasi, menyebarluaskan, atau mengeksploitasi konten ini dengan cara atau bentuk apapun tanpa persetujuan tertulis dari Panitia Digital Talent Scholarship Kementerian Komunikasi dan Informatika Republik Indonesia. Peserta yang terbukti melakukan pelanggaran ini akan dicabut Hak sebagai penerima beasiswa dan akan menerima konsekuensi sesuai aturan yang berlaku;")
    pdf.multi_cell(170,5,txt="9. Tidak terlibat dalam penyalahgunaan narkotika, obat-obatan terlarang, kriminal, dan paham radikal dan terorisme.")
    pdf.ln()

    pdf.multi_cell(170,5,txt="Demikian Form Komitmen Partisipasi ini dibuat dengan sebenarnya secara sadar dan tanpa paksaan. Apabila dikemudian hari pernyataan ini terbukti tidak benar, maka saya bersedia untuk dicabut haknya sebagai peserta pelatihan dan menerima sanksi sesuai ketentuan Kementerian Komunikasi dan Informatika.")
    pdf.ln()
    
    for row in rows:
        pdf.cell(145, 5, txt=row["kota_sekarang"] + ", ",align="R")
        pdf.cell(25, 5, txt=date.today().strftime("%d %B %Y"),align="R",ln=1)
    
    pdf.ln()
    pdf.ln()
    pdf.ln()

    for row in rows:
        pdf.cell(170, 5, txt=row["nama"],align="R",ln=1)

    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=Form Komitmen '+ row["nama"] +'.pdf'})

@app.route("/fpj/<int:id_employees>")
def fpj(id_employees):
    con = sqlite3.connect("database.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Employees where id_employees = ?",(id_employees,))   
    rows = cur.fetchall()
    con.close()
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.l_margin = pdf.l_margin*2.0
    pdf.r_margin = pdf.r_margin*2.0
    pdf.t_margin = pdf.t_margin*1.0
    pdf.b_margin = pdf.b_margin*1.0

    pdf.add_page()
    pdf.set_font("Arial",style='B', size=12)
    pdf.multi_cell(170,5, txt="LAPORAN PERTANGGUNGJAWABAN PESERTA PROGRAM PEMBERIAN BANTUAN PEMERINTAH DIGITAL TALENT SCHOLARSHIP TAHUN 2021", align="C")
    pdf.ln()
    pdf.set_font("Arial",style='I', size=10)
    pdf.multi_cell(170,5, txt="Formulir ini untuk diisi (diketik atau tulis tangan dengan jelas) kemudian diunggah/upload di akun digitalent.kominfo.go.id oleh masing-masing peserta di akhir pelaksanaan pelatihan",border=1, align="J")
    pdf.ln()
    pdf.set_font("Arial",style='B', size=10)
    pdf.cell(170, 5, txt="I. Identitas Diri",ln=1)
    pdf.set_font("Arial", size=10)

    for row in rows:
        pdf.cell(50, 5, txt="NIK/NIP                                    :")
        pdf.cell(100, 5, txt=row["nik_nip"], ln=1)
        pdf.cell(50, 5, txt="Nama Lengkap                         :")
        pdf.cell(100, 5, txt=row["nama"],ln=1)
        pdf.cell(50, 5, txt="Alamat                                      :")
        pdf.multi_cell(120, 5, txt=row["alamat"])
        pdf.cell(50, 5, txt="No HP Aktif                              :")
        pdf.cell(100, 5, txt=row["hp"], ln=1)
        pdf.cell(50, 5, txt="No HP Wali/Atasan                  :")
        pdf.cell(100, 5, txt=row["hp_wali_atasan"], ln=1)
        pdf.cell(50, 5, txt="Email Aktif                                :")
        pdf.cell(100, 5, txt=row["email"], ln=1)

    pdf.ln()
    pdf.set_font("Arial",style='B', size=10)
    pdf.cell(170, 5, txt="II. Program Akademi",ln=1)

    for row in rows:
        pdf.set_font("Arial", size=10)
        pdf.cell(50, 5, txt="Akademi                                   :")
        pdf.cell(100, 5, txt=row["program_akademi"], ln=1)
        pdf.cell(50, 5, txt="Mitra Pelatihan                         :")
        pdf.cell(100, 5, txt=row["mitra_pelatihan"], ln=1)
        pdf.cell(50, 5, txt="Tema Pelatihan                        :")
        pdf.cell(100, 5, txt=row["tema_pelatihan"], ln=1)
        pdf.cell(50, 5, txt="Bulan Pelaksanaan                  :" )
        pdf.cell(100, 5, txt=row["bulan_pelaksanaan"], ln=1)
    
    pdf.ln()
    pdf.set_font("Arial",style='B', size=10)
    pdf.cell(170, 5, txt="III. Pelaksanaan Kegiatan",ln=1)
    pdf.set_font("Arial", size=10)
    pdf.cell(170, 5, txt="Dengan ini menyatakan telah menerima hak:",ln=1)
    pdf.set_font("Arial",style='B', size=10)
    pdf.cell(10, 5, txt="No",border=1, ln=0,align="C")
    pdf.cell(120, 5, txt="Uraian",border=1, ln=0,align="C")
    pdf.cell(40, 5, txt="Beri Tanda Check List",border=1,ln=1,align="C")
    
    pdf.set_font("Arial", size=10)
    top = pdf.y
    pdf.multi_cell(10, 15, txt="1.",border=1,align="C")
    pdf.y = top
    pdf.x = pdf.x + 10
    pdf.multi_cell(120, 5, txt="Self-paced Learning : Peserta pelatihan belajar secara mandiri melalui laptop/komputer, jadwal pelaksanaan Self-paced Learning diatur secara mandiri oleh peserta dalam batas durasi pelatihan Professional Academy",border=1)
    pdf.y = top
    pdf.x = pdf.x + 130
    pdf.set_font("ZapfDingbats", size=10)
    pdf.multi_cell(40, 15, txt="4",border=1,align="C")
    
    pdf.set_font("Arial", size=10)
    top = pdf.y
    pdf.multi_cell(10, 20, txt="2.",border=1,align="C")
    pdf.y = top
    pdf.x = pdf.x + 10
    pdf.multi_cell(120, 5, txt="Live Session : Sesi tatap muka secara daring/online antara instruktur dan peserta pelatihan, peserta pelatihan mendapatkan kesempatan bertanya dan berinteraksi dengan instruktur pada tema pelatihan tertentu di Program Professional Academy",border=1)
    pdf.y = top
    pdf.x = pdf.x + 130
    pdf.set_font("ZapfDingbats", size=10)
    pdf.multi_cell(40, 20, txt="4",border=1,align="C")

    pdf.set_font("Arial", size=10)
    top = pdf.y
    pdf.multi_cell(10, 10, txt="3.",border=1,align="C")
    pdf.y = top
    pdf.x = pdf.x + 10
    pdf.multi_cell(120, 5, txt="Hands-on Lab: Peserta akan mengerjakan suatu project secara mandiri pada Virtual Lab",border=1)
    pdf.y = top
    pdf.x = pdf.x + 130
    pdf.set_font("ZapfDingbats", size=10)
    pdf.multi_cell(40, 10, txt="4",border=1,align="C")

    pdf.set_font("Arial", size=10)
    top = pdf.y
    pdf.multi_cell(10, 15, txt="4.",border=1,align="C")
    pdf.y = top
    pdf.x = pdf.x + 10
    pdf.multi_cell(120, 5, txt="Certificate of Completion : diberikan kepada peserta yang menyelesaikan seluruh sesi pelatihan, mengisi survey dan mengunggah/upload Laporan Pertanggungjawaban (form ini) di digitalent.kominfo.go.id",border=1)
    pdf.y = top
    pdf.x = pdf.x + 130
    pdf.set_font("ZapfDingbats", size=10)
    pdf.multi_cell(40, 15, txt="4",border=1,align="C")
    
    pdf.ln()
    pdf.set_font("Arial",style='B', size=10)
    pdf.cell(170, 5, txt="IV. Saran/Rekomendasi Pelaksanaan Kegiatan (diketik)",ln=1)
    pdf.set_font("Arial", size=10)

    for row in rows:
        pdf.multi_cell(170, 5, txt=row["saran"])
    
    pdf.ln()
    pdf.ln()

    for row in rows:
        pdf.cell(145, 5, txt=row["kota_sekarang"] + ", ",align="R")
        pdf.cell(25, 5, txt=date.today().strftime("%d %B %Y"),align="R",ln=1)
    
    pdf.ln()
    pdf.ln()
    pdf.ln()

    for row in rows:
        pdf.cell(170, 5, txt=row["nama"],align="R",ln=1)
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=Form PertanggungJawaban ' + row["nama"] + '.pdf'})
  
if __name__ == "__main__":
    app.run(debug = True)