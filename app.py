from flask import *  
from fpdf import FPDF
import sqlite3  
  
app = Flask(__name__)  
 
@app.route("/")
def index():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employees")
    rows = cur.fetchall()
    return render_template("index.html",rows = rows) 
 
@app.route("/add")
def add():
    return render_template("add.html")
 
@app.route("/insert",methods = ["POST"])
def saveDetails():
    msg = "msg"
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
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Employees (no_registrasi,nama,tempat_tanggal_lahir,nik_nip,email,hp,hp_wali_atasan,pekerjaan,alamat,program_akademi,tema_pelatihan,mitra_pelatihan) values (?,?,?,?,?,?,?,?,?,?,?,?)",(no_registrasi,nama,tempat_tanggal_lahir,nik_nip,email,hp,hp_wali_atasan,pekerjaan,alamat,program_akademi,tema_pelatihan,mitra_pelatihan))
                con.commit()
                con.close()
                msg = "Employee successfully Added"
        except:
            con.rollback()
            con.close()
            msg = "We can not add the employee to the list"
        finally:
            return redirect('/')
            
 
@app.route("/delete/<int:id_employees>")  
def delete(id_employees):
    with sqlite3.connect("database.db") as con:  
        try:  
            cur = con.cursor()  
            cur.execute("delete from Employees where id_employees = ?",(id_employees,))  
            msg = "Employees successfully deleted"  
        except:  
            msg = "can't be deleted"  
        finally:  
            return redirect('/')

@app.route("/fk/<int:id_employees>")
def fk(id_employees):
    con = sqlite3.connect("database.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Employees where id_employees = ?",(id_employees,))   
    rows = cur.fetchall()
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.l_margin = pdf.l_margin*2.0
    pdf.r_margin = pdf.r_margin*2.0
    pdf.t_margin = pdf.t_margin*2.0
    pdf.b_margin = pdf.b_margin*2.0

    pdf.add_page()
    pdf.set_font("Arial",style='B', size=12)
    pdf.multi_cell(100,5, txt="FORM KOMITMEN PARTISIPASI PROGRAM PEMBERIAN BANTUAN PEMERINTAH DIGITAL TALENT SCHOLARSHIP TAHUN 2021", align="C")
    # pdf.cell(100,5, txt="FORM KOMITMEN PARTISIPASI PROGRAM PEMBERIAN BANTUAN PEMERINTAH DIGITAL TALENT SCHOLARSHIP TAHUN 2021", align="C")
    
    for row in rows:
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=row["nama"], ln=1)
        pdf.cell(200, 10, txt=row["tempat_tanggal_lahir"], ln=1)
        pdf.cell(200, 10, txt=row["nik_nip"], ln=1)
        pdf.cell(200, 10, txt=row["email"], ln=1)
        pdf.cell(200, 10, txt=row["hp"], ln=1)
        pdf.cell(200, 10, txt=row["hp_wali_atasan"], ln=1)
        pdf.cell(200, 10, txt=row["pekerjaan"], ln=1)
        pdf.multi_cell(150, 10, txt=row["alamat"],align="J")
        # pdf.ln()
        pdf.cell(200, 10, txt=row["program_akademi"], ln=1)
        pdf.cell(200, 10, txt=row["tema_pelatihan"], ln=1)
        pdf.cell(200, 10, txt=row["mitra_pelatihan"], ln=1)
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=Form Komitmen '+ row["nama"] +'.pdf'})

@app.route("/fpj/<int:id_employees>")
def fpj(id_employees):
    con = sqlite3.connect("database.db")  
    con.row_factory = sqlite3.Row  
    cur = con.cursor()  
    cur.execute("select * from Employees where id_employees = ?",(id_employees,))   
    rows = cur.fetchall()
    
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_font("Arial", size=9)
    pdf.cell(200, 10, txt="Form Komitmen", ln=1, align="C")
    
    for row in rows:
        pdf.cell(200, 10, txt=row["nama"], ln=1)
        pdf.cell(200, 10, txt=row["tempat_tanggal_lahir"], ln=1)
        pdf.cell(200, 10, txt=row["nik_nip"], ln=1)
        pdf.cell(200, 10, txt=row["email"], ln=1)
        pdf.cell(200, 10, txt=row["hp"], ln=1)
        pdf.cell(200, 10, txt=row["hp_wali_atasan"], ln=1)
        pdf.cell(200, 10, txt=row["pekerjaan"], ln=1)
        pdf.multi_cell(150, 10, txt=row["alamat"],align="J")
        # pdf.ln()
        pdf.cell(200, 10, txt=row["program_akademi"], ln=1)
        pdf.cell(200, 10, txt=row["tema_pelatihan"], ln=1)
        pdf.cell(200, 10, txt=row["mitra_pelatihan"], ln=1)
    
    return Response(pdf.output(dest='S').encode('latin-1'), mimetype='application/pdf', headers={'Content-Disposition':'attachment;filename=Form PertanggungJawaban ' + row["nama"] + '.pdf'})
  
if __name__ == "__main__":  
    app.run(debug = True)  