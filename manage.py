from flask import Flask,render_template,flash,redirect,url_for,session,logging,request,abort # pip install Flask
from flask_mysqldb import MySQL # pip install flask_mysqldb
from wtforms import Form,StringField,TextAreaField,PasswordField,validators,SelectField,TextField,SubmitField,ValidationError # pip install WTForms
from passlib.hash import sha256_crypt # pip install passlib
from functools import wraps # pip install wrap
from datetime import datetime
import locale
import os
from werkzeug.utils import secure_filename
import smtplib
from email.mime.multipart import MIMEMultipart # pip install MIME and email-to
from email.mime.text import MIMEText # pip install MIME and email-to
import random

# Kullanıcı Giriş Decorator'ı - User Login Decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            if session["en"] == True and session["tr"] == False:
                flash("Please login to view this page.","danger")
            else:
                flash("Bu sayfayı görüntülemek için lütfen giriş yapın.","danger")
            return redirect(url_for("login"))

    return decorated_function
# Kayıt Formu - Register Form
# Tr
class RegisterFormTr(Form):
    username = StringField("Kullanıcı Adı",validators=[validators.Length(min = 3,max = 35,message = "Kullanıcı adınızın uzunluğu en az 3 en fazla 35 karakter olmalıdır.")])
    name = StringField("İsim",validators=[validators.Length(min = 2,max = 25,message = "İsminizin uzunluğu en az 2 en fazla 25 karakter olmalıdır.")])
    surname = StringField("Soyisim",validators=[validators.Length(min = 2,max = 25,message = "Soyisminizin uzunluğu en az 2 en fazla 25 karakter olmalıdır.")])
    email = StringField("Email Adresi",validators=[validators.Email(message = "Lütfen Geçerli Bir Email Adresi Girin...")])
    password = PasswordField("Parola",validators=[
        validators.DataRequired(message = "Lütfen bir parola belirleyin"),
        validators.EqualTo(fieldname = "confirm",message="Parolanız Uyuşmuyor...")
    ])
    confirm = PasswordField("Parola Doğrula")
    message = TextAreaField("Açıklama",validators=[validators.Length(min = 10,max = 250)])
    imgname = StringField()

# En
class RegisterFormEn(Form):
    username = StringField("Username",validators=[validators.Length(min = 3,max = 35,message = "Your username must be between 3 and 25 characters in length.")])
    name = StringField("Name",validators=[validators.Length(min = 3,max = 25,message = "Your name must be between 2 and 25 characters in length.")])
    surname = StringField("Surname",validators=[validators.Length(min = 2,max = 25,message = "Your surname must be between 2 and 25 characters in length.")])
    email = StringField("Email",validators=[validators.Email(message = "Please enter a valid email address...")])
    password = PasswordField("Password",validators=[
        validators.DataRequired(message = "Please set a password."),
        validators.EqualTo(fieldname = "confirm",message="Your password doesn't match.")
    ])
    confirm = PasswordField("Password Confirm")
    message = TextAreaField("Explanation",validators=[validators.Length(min = 10,max = 250)])
    imgname = StringField()

# Giriş Formu - Login Form
# Tr
class LoginFormTr(Form):
    username = StringField("Kullanıcı Adı")
    password = PasswordField("Parola")

# En
class LoginFormEn(Form):
    username = StringField("Username")
    password = PasswordField("Password")

# Çizgi Roman Formu - Comic Form
# Tr
class ComicFormTr(Form):
    title = StringField("Çizgi Roman Adı",validators=[validators.Length(min = 5,max = 25,message = "Lütfen 5 ile 25 Karakter Arasında Bir İsim Giriniz."),validators.DataRequired()])
    brand = SelectField("Çizgi Roman Firması",choices=[("Marvel","Marvel"),("DC","DC"),("League Of Legends","League Of Legens"),("Star Wars","Star Wars"),("Diğer","Diğer")])
    crtype = SelectField("Çizgi Roman Türü",choices = [("Comics","Comics"),("Bilim Kurgu","Bilim Kurgu"),("Manga","Manga"),("Karikatür","Karikatür"),("Diğer","Diğer")])
    characters = StringField("Ana Karakterler",validators=[validators.Length(min = 5,max = 50,message = "Lütfen 5 ile 50 Karakter Arasında Bir İsim Giriniz."),validators.DataRequired()])
    content = TextAreaField("Çizgi Roman İçeriği",validators=[validators.Length(min = 10,max = 50,message = "Lütfen 5 ile 25 Karakter Arasında Bir İsim Giriniz.")])
    tags = TextAreaField("Etiketler")
    imgname = StringField()
    comicname = StringField()

# En
class ComicFormEn(Form):
    title = StringField("Comic Book Name",validators=[validators.Length(min = 5,max = 25,message = "Please enter a name between 5 and 25 characters."),validators.DataRequired()])
    brand = SelectField("Comic Book Company",choices=[("Marvel","Marvel"),("DC","DC"),("League Of Legends","League Of Legens"),("Star Wars","Star Wars"),("Diğer","Diğer")])
    crtype = SelectField("Comic Book Type",choices = [("Comics","Comics"),("Bilim Kurgu","Bilim Kurgu"),("Manga","Manga"),("Karikatür","Karikatür"),("Diğer","Diğer")])
    characters = StringField("Main Characters",validators=[validators.Length(min = 5,max = 50,message = "Please enter a name between 5 and 50 characters."),validators.DataRequired()])
    content = TextAreaField("Comic Book Content",validators=[validators.Length(min = 10,max = 50,message = "Please enter a name between 5 and 50 characters.")])
    tags = TextAreaField("Tags")
    imgname = StringField()
    comicname = StringField()

# İletişim Formu - Contact Form
# Tr
class ContactFormTr(Form):
    name = StringField("İsim",validators=[validators.Length(min = 4,max = 25,message = "İsminizin uzunluğu en az 4 en fazla 25 karakter olmalıdır.")])
    surname = StringField("Soyisim",validators=[validators.Length(min = 4,max = 25,message = "Soyisminizin uzunluğu en az 4 en fazla 25 karakter olmalıdır.")])
    subject = StringField("Konu Başlığı",validators=[validators.Length(min = 4,max = 50,message = "Konu Başlığı uzunluğu en az 4 en fazla 50 karakter olmalıdır.")])
    email = StringField("Email Adresi",validators=[validators.Email(message = "Lütfen Geçerli Bir Email Adresi Girin...")])
    message = TextAreaField("Mesajınız")

# En
class ContactFormEn(Form):
    name = StringField("Name",validators=[validators.Length(min = 2,max = 25,message = "Your name must be between 2 and 25 characters in length.")])
    surname = StringField("Surname",validators=[validators.Length(min = 2,max = 25,message = "Your surname must be between 2 and 25 characters in length.")])
    subject = StringField("Subject",validators=[validators.Length(min = 3,max = 50,message = "Your subject must be between 3 and 25 characters in length.")])
    email = StringField("Email",validators=[validators.Email(message = "Please enter a valid email address...")])
    message = TextAreaField("Message")

# Yönetici Paneli Formu - Admin Panel Form
# Tr
class AdminFormTr(Form):
    username = PasswordField("Kullanıcı Adı")
    password = PasswordField("Parola")

# En
class AdminFormEn(Form):
    username = PasswordField("Username")
    password = PasswordField("Password")

# Şifre Değiştirme Formu - Password Change Form
# Tr
class PasswordFormTr(Form):
    username = StringField("Kullanıcı Adı")
    email = StringField("E-Posta")
    password = PasswordField("Parola",validators=[
        validators.DataRequired(message = "Lütfen bir parola belirleyin"),
        validators.EqualTo(fieldname = "confirm",message="Parolanız Uyuşmuyor...")
    ])
    confirm = PasswordField("Parola Doğrula")

# En
class PasswordFormEn(Form):
    username = StringField("Username")
    email = StringField("E-Mail")
    password = PasswordField("Password",validators=[
        validators.DataRequired(message = "Please set a password."),
        validators.EqualTo(fieldname = "confirm",message="Your password doesn't match.")
    ])
    confirm = PasswordField("Parola Doğrula")

# Şifre Değiştirme Formu - Password Change Form
# Eposta / Kullanıcı Adı - Email / Username
# Tr
class PasswordForgotTr(Form):
    username = StringField("Kullanıcı Adı")
    email = StringField("E-Posta")

# En
class PasswordForgotEn(Form):
    username = StringField("Username")
    email = StringField("E-Mail")

# Doğrulama Kodu / Yeni Şifre - Confirm Code / New Password
# Tr
class PasswordConfirmTr(Form):
    password = PasswordField("Yeni Parola",validators=[
        validators.DataRequired(message = "Lütfen bir parola belirleyin"),
        validators.EqualTo(fieldname = "confirm",message="Parolanız Uyuşmuyor..."),
        validators.Length(min = 5,max=18,message="Lütfen 5 ile 18 uzunluğun da bir parola giriniz.")
    ])
    confirm = PasswordField("Yeni Parola Doğrula")
    code = StringField("Doğrulama Kodu")

# En
class PasswordConfirmEn(Form):
    password = PasswordField("New Password",validators=[
        validators.DataRequired(message = "Please set a password."),
        validators.EqualTo(fieldname = "confirm",message="Your password doesn't match."),
        validators.Length(min = 5,max = 18,message="Your password must be between 5 and 18 characters in length.")
    ])
    confirm = PasswordField("New Password Confirm")
    code = StringField("Verification Code")

# Flask Bağlantıları - Flask Connections
app = Flask(__name__)

app.secret_key= "cradam"

YUKLEME_KLASORU = '/home/comicsman/comicsman/static/yuklemeler'
UZANTILAR = set(['png','jpg','jpeg','rar','zip','cbr'])

app.config["UPLOAD_FOLDER"] = YUKLEME_KLASORU

# Mysql Bağlantıları - Mysql Connections
app.config["MYSQL_HOST"] = "comicsman.mysql.pythonanywhere-services.com"
app.config["MYSQL_USER"] = "comicsman"
app.config["MYSQL_PASSWORD"] = "Ekox.54321"
app.config["MYSQL_DB"] = "comicsman$comicsman"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Fonksiyonlar
def error():
    if session["en"] == True and session["tr"] == False:
        flash("Error! There is a problem ","danger")
    else:
        flash("Hata! Bir Sorun Oluştu","danger")

def img_error():
    if session["en"] == True and session["tr"] == False:
        flash("No Pictures Selected","warning")
    else:
        flash("Resim Seçilmedi","warning")

def ext_error():
    if session["en"] == True and session["tr"] == False:
        flash("Disallowed file extension","warning")
    else:
        flash("İzin verilmeyen dosya uzantısı","warning")

def img_cr_error():
    if session["en"] == True and session["tr"] == False:
        flash("No pictures or comics selected.","warning")
    else:
        flash("Resim veya Çizgi Roman Seçilmedi","warning")

def login_success():
    if session["en"] == True and session["tr"] == False:
        flash("You have successfully logged in.","success")
    else:
        flash("Başarıyla Giriş Yaptınız.","success")

def report_success():
    if session["en"] == True and session["tr"] == False:
        flash("Reported, Thank you.","success")
    else:
        flash("Rapor Edildi, Teşekkür Ederiz.","success")

def aut_error():
    if session["en"] == True and session["tr"] == False:
        flash("You are not authorized to do so.","warning")
    else:
        flash("Böyle bir işleme yetkiniz yok.","warning")

# Anasayfa - Home Page
@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    sorgu = "Select * From comics ORDER BY id DESC"
    result = cursor.execute(sorgu)
    if result > 0:
        comics = cursor.fetchall()
        return render_template("index.html",comics = comics)
    else:
        return render_template("index.html")

# Hakkımızda - About
@app.route("/about")
def about():
    return render_template("about.html")

# Kurallar - Rules
@app.route("/rules")
def rules():
    return render_template("rules.html")

# Gizlilik - Privacy
@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# Bağış - Donate
@app.route("/donate")
def donate():
    return render_template("donate.html")

# Kayıt Olma - Register
@app.route("/register",methods = ["GET","POST"])
def register():
    try:
        try:
            if session["en"] == True and session["tr"] == False:
                form = RegisterFormEn(request.form)
            elif session["en"] == False and session["tr"] == True:
                form = RegisterFormTr(request.form)
            elif session["en"] != True and session["en"] != False and session["tr"] != True and session["tr"] != False:
                form = RegisterFormTr(request.form)
            if request.method == "POST" and form.validate() and request.form.get("agr_confirm"):
                username = form.username.data
                name = form.name.data
                surname = form.surname.data
                email = form.email.data
                password = sha256_crypt.hash(form.password.data)
                message = form.message.data

                cursor = mysql.connection.cursor()

                sorgu_alr = "Select * From users where username = %s"
                result_alr = cursor.execute(sorgu_alr,(username,))
                if result_alr == 0:
                    sorgu_alr_em = "Select * From users where email = %s"
                    result_alr_em = cursor.execute(sorgu_alr_em,(email,))
                    if result_alr_em == 0:
                        sorgu = "Insert into users(username,name,surname,email,password,content,image,imgname) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
                        cursor.execute(sorgu,(username,name,surname,email,password,message,"[BLOB - 46 B]","profile.png"))
                        mysql.connection.commit()
                        cursor.close()

                        cursor = mysql.connection.cursor()
                        mesaj = MIMEMultipart()
                        mesaj["From"] =  "bberkaykaya0@gmail.com" #
                        mesaj["To"] = "comicstheman@gmail.com"
                        mesaj["Subject"] = "Comics Man' e Yeni Kullanıcı Kayıt Olmuştur."
                        yazi = "Kullanıcı Bilgileri\n-----------------------\nKullanıcı Adı: " + username + "\nE-Posta: " + email +  "\nİsim: " + name + "\nSoyisim: " + surname + " "
                        mesaj_govdesi =  MIMEText(yazi,"plain")
                        mesaj.attach(mesaj_govdesi)
                        try:
                            mail =  smtplib.SMTP("smtp.gmail.com",587)
                            mail.starttls()
                            mail.ehlo()
                            mail.login("bberkaykaya0@gmail.com","nvvqlmhykyvdkrnh")
                            mail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())
                            mail.close()
                            if session["en"] == True and session["tr"] == False:
                                flash("You have successfully registered","success")
                            else:
                                flash("Başarıyla Kayıt Oldunuz....","success")
                            mail.close()
                            return redirect(url_for("login"))
                        except:
                            flash("Hata Bir Sorun Oluştu...","danger")
                            return redirect(url_for("register"))

                    else:
                        if session["en"] == True and session["tr"] == False:
                            flash("This email is already taken.","warning")
                        else:
                            flash("Bu E-Posta Zaten Alındı.","warning")

                        return redirect(url_for("register"))
                else:
                    if session["en"] == True and session["tr"] == False:
                        flash("This username is already taken.","warning")
                    else:
                        flash("Bu Kullanıcı Adı Zaten Alındı.","warning")

                    return redirect(url_for("register"))
            else:
                return render_template("register.html",form = form)
        except UnicodeEncodeError:
            if session["en"] == True and session["tr"] == False:
                flash("Please do not use special characters.","danger")
                return render_template("register.html",form = form)
            else:
                flash("Lütfen Özel Karakter Kullanmayınız.","warning")
                return render_template("register.html",form = form)
    except KeyError:
        session["en"] = True
        flash("Please Select a Language","warning")
        return redirect(url_for("index"))


# Giriş Yapma - Login
@app.route("/login",methods = ["GET","POST"])
def login():
    try:
        if session["en"] == True and session["tr"] == False:
            form = LoginFormEn(request.form)
        else:
            form = LoginFormTr(request.form)

        if request.method == "POST":
            username = form.username.data
            password_entered = form.password.data

            cursor = mysql.connection.cursor()
            sorgu = "Select * From users where username = %s"

            result = cursor.execute(sorgu,(username,))
            if result > 0:
                data = cursor.fetchone()
                real_password = data["password"]
                if sha256_crypt.verify(password_entered,real_password):
                    login_success()
                    session["logged_in"] = True
                    session["username"] = username
                    cursor_user = mysql.connection.cursor()
                    sorgu_user = "Select * From users where username = %s"
                    result_user = cursor_user.execute(sorgu_user,(session["username"],))
                    if result_user > 0:
                        user = cursor_user.fetchone()
                        session["id"] = user["id"]
                        sorgu_layout = "Select * From reports where username = %s"
                        result_layout = cursor.execute(sorgu_layout,(session["username"],))
                        if result_layout > 0:
                            user_info = cursor.fetchone()
                            user_banned = user_info["bansstatus"]
                            if user_banned == "true":
                                session["banned"] = True
                                return redirect(url_for("index"))
                            else:
                                session["banned"] = False
                                return redirect(url_for("index"))
                        else:
                            return redirect(url_for("index"))
                    else:
                        return redirect(url_for("index"))
                else:
                    if session["en"] == True and session["tr"] == False:
                        flash("You Wrong Your Password ...","danger")
                    else:
                        flash("Parolanızı Yanlış Girdiniz...","danger")

                    return redirect(url_for("login"))
            else:
                if session["en"] == True and session["tr"] == False:
                    flash("There is no such user.","danger")
                else:
                    flash("Böyle bir kullanıcı bulunmuyor.","danger")
                return redirect(url_for("login"))
        return render_template("login.html",form = form)
    except KeyError:
        session["en"] = True
        flash("Please Select a Language","warning")
        return redirect(url_for("index"))

# Çıkış - Logout
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# Kütüphanem - My Library
@app.route("/mylibrary")
def mylibrary():
    cursor = mysql.connection.cursor()
    sorgu = "Select * From comics where author = %s"
    result = cursor.execute(sorgu,(session["username"],))
    if result > 0:
        comics = cursor.fetchall()
        return render_template("controlboard.html",comics = comics)
    else:
        return render_template("controlboard.html")

# Uzantı Kontrolü
def uzanti_kontrol(dosyaadi):
   return '.' in dosyaadi and \
   dosyaadi.rsplit('.', 1)[1].lower() in UZANTILAR

# Çizgi Roman Ekleme - Add Comic
@app.route("/addcomic",methods = ["GET","POST"])
def addcomic():
    try:
        if session["en"] == True and session["tr"] == False:
            form = ComicFormEn(request.form)
        else:
            form = ComicFormTr(request.form)

        if request.method == "POST" and form.validate():
            title = form.title.data
            content = form.content.data
            brand = form.brand.data
            crtype = form.crtype.data
            characters = form.characters.data
            tags = form.tags.data
            if 'dosya' not in request.files or 'crdosya' not in request.files:
                img_cr_error()
                return redirect('addcomic')
            dosya = request.files["dosya"]
            crdosya = request.files["crdosya"]
            if dosya.filename == '' or crdosya.filename == '':
                img_cr_error()
                return redirect("addcomic")
            if dosya and uzanti_kontrol(dosya.filename) or crdosya and uzanti_kontrol(crdosya.filename):
                dosyaadi = secure_filename(dosya.filename)
                crdosyaadi = secure_filename(crdosya.filename)
                dosya.save(os.path.join(app.config["UPLOAD_FOLDER"],dosyaadi))
                crdosya.save(os.path.join(app.config["UPLOAD_FOLDER"],crdosyaadi))
            else:
                ext_error()
                return redirect("addcomic")

            cursor_second = mysql.connection.cursor()
            sorgu_second = "Select * From users where id = %s"
            result_second = cursor_second.execute(sorgu_second,(session["id"],))
            if result_second > 0:
                user_second = cursor_second.fetchone()
                user_second_id = user_second["id"]
                user_second_name = user_second["name"]
                cursor = mysql.connection.cursor()
                sorgu = "Insert into comics(title,author,content,brand,type,characters,tags,image,imgname,crname,authorid) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sorgu,(title,session["username"],content,brand,crtype,characters,tags,dosya,dosyaadi,crdosyaadi,user_second_id))
                mysql.connection.commit()
                cursor.close()
                # Çizgi Roman Kontrolü - Comic Control
                cursor_control = mysql.connection.cursor()
                sorgu_control = "Select * From comics where author = %s"
                result_control = cursor_control.execute(sorgu_control,(user_second_name,))
                if result_control > 0:
                    comic_control = cursor_control.fetchone()
                    comic_id = comic_control["id"]
                    mesaj = MIMEMultipart()
                    mesaj["From"] = "bberkaykaya0@gmail.com"
                    mesaj["To"] = "comicstheman@gmail.com"
                    mesaj["Subject"] = "Çizgi Roman Kontrolü"
                    text = user_second_name + " Tarafından Yayınlanmıştır." + "\n" + "Çizgi Roman Bağlantısı:" + "\n" + "http://www.comicsman.tk/comic/" + str(comic_id)
                    mesaj_body = MIMEText(text,"plain")
                    mesaj.attach(mesaj_body)
                    try:
                        mail_gmail = smtplib.SMTP("smtp.gmail.com",587)
                        mail_gmail.starttls()
                        mail_gmail.ehlo()
                        mail_gmail.login("bberkaykaya0@gmail.com","nvvqlmhykyvdkrnh")
                        mail_gmail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())
                        mail_gmail.close()
                        if session["en"] == True and session["tr"] == False:
                            flash("Comics Added Successfully.","success")
                        else:
                            flash("Çizgi Roman Başarıyla Eklendi.","success")
                        return redirect(url_for("mylibrary"))
                    except:
                        if session["en"] == True and session["tr"] == False:
                            flash("Çizgi Roman Başarıyla Güncellendi.","success")
                        else:
                            flash("Comics Updated Successfully.","success")
                        return redirect(url_for("mylibrary"))
                else:
                    error()
                    return redirect(url_for("mylibrary"))
            else:
                error()
                return redirect(url_for("mylibrary"))


        return render_template("addcomic.html",form = form)
    except KeyError:
        session["en"] = True
        flash("Please Select a Language","warning")
        return redirect(url_for("index"))
    except UnicodeEncodeError:
        flash("Please Use Latin Alphabet.","danger")
        return redirect(url_for("index"))


# Çizgi Roman Silme - Delete Comic
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * from comics where author = %s and id = %s"

    result = cursor.execute(sorgu,(session["username"],id))
    if result > 0:
        sorgu2 = "Delete from comics where id = %s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()
        return redirect(url_for("mylibrary"))
    else:
        aut_error()
        return redirect(url_for("index"))

# Çizgi Roman Güncelleme - Comic Update
@app.route("/edit/<string:id>",methods = ["GET","POST"])
@login_required
def update(id):
    try:
        if request.method == "GET":
            cursor = mysql.connection.cursor()
            sorgu = "Select * from comics where id = %s and author = %s"
            result = cursor.execute(sorgu,(id,session["username"]))

            if result == 0:
                aut_error()
                return redirect(url_for("index"))
            else:
                comic = cursor.fetchone()
                if session["en"] == True and session["tr"] == False:
                    form = ComicFormEn()
                else:
                    form = ComicFormTr()

                form.title.data = comic["title"]
                form.content.data = comic["content"]
                form.brand.data = comic["brand"]
                form.crtype.data = comic["type"]
                form.characters.data = comic["characters"]
                form.tags.data = comic["tags"]
                imgname_prof = comic["imgname"]
                crname = comic["crname"]
                return render_template("updatecomics.html",form = form,imgname_prof = imgname_prof,crdosya = crname)
        else:
            # POST REQUEST
            if session["en"] == True and session["tr"] == False:
                form = ComicFormEn(request.form)
            else:
                form = ComicFormTr(request.form)

            newTitle = form.title.data
            newContent = form.content.data
            newBrand = form.brand.data
            newCrtype = form.crtype.data
            newCharacters = form.characters.data
            newTags = form.tags.data
            if 'dosya' not in request.files or 'crdosya' not in request.files:
                img_cr_error()
                return redirect('update')
            dosya = request.files["dosya"]
            crdosya = request.files["crdosya"]
            if dosya.filename == '' or crdosya.filename == '':
                img_cr_error()
                return redirect("update")
            if dosya and uzanti_kontrol(dosya.filename) or crdosya and uzanti_kontrol(crdosya.filename):
                dosyaadi = secure_filename(dosya.filename)
                crdosyaadi = secure_filename(crdosya.filename)
                dosya.save(os.path.join(app.config["UPLOAD_FOLDER"],dosyaadi))
                crdosya.save(os.path.join(app.config["UPLOAD_FOLDER"],crdosyaadi))
            else:
                ext_error()
                return redirect("update")

            sorgu2 = "Update comics Set title = %s,content = %s,brand = %s,type = %s,characters = %s,tags = %s,image = %s,imgname = %s,crname = %s where id = %s"
            cursor = mysql.connection.cursor()
            cursor.execute(sorgu2,(newTitle,newContent,newBrand,newCrtype,newCharacters,newTags,dosya,dosyaadi,crdosyaadi,id))
            sorgu4 = "Update lists Set title = %s,content = %s,type = %s,image = %s,imgname = %s where comicid = %s"
            cursor.execute(sorgu4,(newTitle,newContent,newCrtype,dosya,dosyaadi,id))
            mysql.connection.commit()
            cursor_control = mysql.connection.cursor()
            sorgu_control = "Select * From comics where id = %s"
            result_control = cursor_control.execute(sorgu_control,(id,))
            if result_control > 0:
                comic_control = cursor_control.fetchone()
                comic_id = comic_control["id"]
                user_second_name = comic_control["author"]
                mesaj = MIMEMultipart()
                mesaj["From"] = "bberkaykaya0@gmail.com"
                mesaj["To"] = "comicstheman@gmail.com"
                mesaj["Subject"] = "Çizgi Roman Kontrolü"
                text = user_second_name + " Tarafından Güncellenmiştir.." + "\n" + "Çizgi Roman Bağlantısı:" + "\n" + "http://www.comicsman.tk/comic/" + str(comic_id)
                mesaj_body = MIMEText(text,"plain")
                mesaj.attach(mesaj_body)
                try:
                    mail_gmail = smtplib.SMTP("smtp.gmail.com",587)
                    mail_gmail.starttls()
                    mail_gmail.ehlo()
                    mail_gmail.login("bberkaykaya0@gmail.com","nvvqlmhykyvdkrnh")
                    mail_gmail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())
                    mail_gmail.close()
                    if session["en"] == True and session["tr"] == False:
                        flash("Çizgi Roman Başarıyla Güncellendi.","success")
                    else:
                        flash("Comics Updated Successfully.","success")
                    return redirect(url_for("mylibrary"))
                except:
                    if session["en"] == True and session["tr"] == False:
                        flash("Comics Updated Successfully.","success")
                        return redirect(url_for("mylibrary"))
                    else:
                        flash("Çizgi Roman Başarıyla Güncellendi.","success")
                        return redirect(url_for("mylibrary"))
            else:
                error()
                return redirect(url_for("mylibrary"))
    except KeyError:
        session["en"] = True
        flash("Please Select a Language","warning")
        return redirect(url_for("index"))
    except UnicodeEncodeError:
        flash("Please Use Latin Alphabet.","danger")
        return redirect(url_for("index"))

# Çizgi Roman Detay - Comic Detail
@app.route("/comic/<string:id>")
def comic_detail(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * from comics where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        comic = cursor.fetchone()
        dosya = comic["imgname"]
        crdosya = comic["crname"]
        views = comic["views"]
        views = views + 1
        sorgu_second = "Update comics Set views = %s where id = %s"
        cursor.execute(sorgu_second,(views,id))
        mysql.connection.commit()
        return render_template("comiclayout.html",comic = comic,dosya = dosya,crdosya = crdosya)
    else:
        return render_template("comiclayout.html")

# Tüm Çizgi Romanlar - All Comics
@app.route("/comics")
def all_comics():
    cursor = mysql.connection.cursor()
    sorgu = "Select * From comics"
    result = cursor.execute(sorgu)
    if result > 0:
        comics = cursor.fetchall()
        return render_template("comics.html",comics = comics)
    else:
        return render_template("comics.html")

# Marvel - DC - LOL - SW - OTH Comics
@app.route("/cate-marvel")
def cate_marvel():
    r_brand = "Marvel"
    cursor = mysql.connection.cursor()
    sorgu = "Select * from comics where brand = %s"
    result = cursor.execute(sorgu,(r_brand,))
    if result > 0:
        comics = cursor.fetchall()
        return render_template("cate-marvel.html",comics = comics)
    else:
        return render_template("cate-marvel.html")
@app.route("/cate-dc")
def cate_dc():
    r_brand = "DC"
    cursor = mysql.connection.cursor()
    sorgu = "Select * from comics where brand = %s"
    result = cursor.execute(sorgu,(r_brand,))
    if result > 0:
        comics = cursor.fetchall()
        return render_template("cate-dc.html",comics = comics)
    else:
        return render_template("cate-dc.html")
@app.route("/cate-lol")
def cate_lol():
    r_brand = "League Of Legends"
    cursor = mysql.connection.cursor()
    sorgu = "Select * from comics where brand = %s"
    result = cursor.execute(sorgu,(r_brand,))
    if result > 0:
        comics = cursor.fetchall()
        return render_template("cate-lol.html",comics = comics)
    else:
        return render_template("cate-lol.html")
@app.route("/cate-sw")
def cate_sw():
    r_brand = "Star Wars"
    cursor = mysql.connection.cursor()
    sorgu = "Select * from comics where brand = %s"
    result = cursor.execute(sorgu,(r_brand,))
    if result > 0:
        comics = cursor.fetchall()
        return render_template("cate-sw.html",comics = comics)
    else:
        return render_template("cate-sw.html")
@app.route("/cate-oth")
def cate_oth():
    r_brand = "Diğer"
    cursor = mysql.connection.cursor()
    sorgu = "Select * from comics where brand = %s"
    result = cursor.execute(sorgu,(r_brand,))
    if result > 0:
        comics = cursor.fetchall()
        return render_template("cate-oth.html",comics = comics)
    else:
        return render_template("cate-oth.html")

# Todo App
# Profil - Profile
@app.route("/profile/<string:id>",methods = ["GET","POST"])
@login_required
def myprofile(id):
    cursor = mysql.connection.cursor()
    cursor_second = mysql.connection.cursor()

    sorgu = "Select * From users where id = %s"
    sorgu_second = "Select * From comics where authorid = %s"

    result = cursor.execute(sorgu,(id,))
    result_second = cursor_second.execute(sorgu_second,(id,))

    if result > 0 and result_second > 0:
        user = cursor.fetchone()
        comic = cursor_second.fetchall()
        dosya = user["imgname"]
        return render_template("profile.html",users = user,comics = comic,dosya = dosya,main_id = session["id"])
    elif result > 0:
        user = cursor.fetchone()
        dosya = user["imgname"]
        return render_template("profile.html",users = user,dosya = dosya)
    else:
        return render_template("profile.html")

# Profil Düzenle - Edit
@app.route("/editprofile/<string:id>",methods = ["GET","POST"])
@login_required
def editprofile(id):
    try:
        if request.method == "GET":
            cursor = mysql.connection.cursor()
            sorgu = "Select * From users where id = %s and username = %s"
            result = cursor.execute(sorgu,(id,session["username"]))
            if result == 0:
                aut_error()
                return redirect(url_for("index"))
            else:
                user = cursor.fetchone()
                if session["en"] == True and session["tr"] == False:
                    form = RegisterFormEn()
                else:
                    form = RegisterFormTr()
                user_id = user["id"]
                form.name.data = user["name"]
                form.surname.data = user["surname"]
                form.message.data = user["content"]
                imgname_prof = user["imgname"]

                return render_template("prof-edit.html",form = form,imgname_prof = imgname_prof,user_id = user_id)
        else:
            # POST REQUEST
            if session["en"] == True and session["tr"] == False:
                form = RegisterFormEn(request.form)
            else:
                form = RegisterFormTr(request.form)

            newName = form.name.data
            newSurname = form.surname.data
            newMessage = form.message.data
            if 'dosya' not in request.files:
                img_error()
                return redirect('editprofile')
            dosya = request.files["dosya"]
            if dosya.filename == '':
                img_error()
                return redirect("editprofile")
            if dosya and uzanti_kontrol(dosya.filename):
                dosyaadi = secure_filename(dosya.filename)
                dosya.save(os.path.join(app.config["UPLOAD_FOLDER"],dosyaadi))
            else:
                ext_error()
                return redirect("editprofile")

            sorgu_second = "Update users Set name = %s,surname = %s,content = %s,image = %s,imgname = %s where id = %s"
            cursor = mysql.connection.cursor()
            cursor.execute(sorgu_second,(newName,newSurname,newMessage,dosya,dosyaadi,id))
            mysql.connection.commit()
            cursor = mysql.connection.cursor()
            mesaj = MIMEMultipart()
            mesaj["From"] =  "bberkaykaya0@gmail.com" #
            mesaj["To"] = "comicstheman@gmail.com"
            mesaj["Subject"] = "Comics Man' e Profil Güncelleme"
            yazi = "Kullanıcı Bilgileri\n-----------------------\nİd: " + id + "\nİsim: " + newName + "\nSoyisim: " + newSurname + "\nAçıklama: " + newMessage
            mesaj_govdesi =  MIMEText(yazi,"plain")
            mesaj.attach(mesaj_govdesi)
            try:
                mail =  smtplib.SMTP("smtp.gmail.com",587)
                mail.starttls()
                mail.ehlo()
                mail.login("bberkaykaya0@gmail.com","nvvqlmhykyvdkrnh")
                mail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())
                mail.close()
                if session["en"] == True and session["tr"] == False:
                    flash("Profile Successfully Updated.","success")
                    return redirect(url_for("index"))
                else:
                    flash("Profil Başarıyla Güncellendi.","success")
                    return redirect(url_for("index"))
            except:
                flash("Hata Bir Sorun Oluştu...","danger")
                return redirect(url_for("index"))
    except KeyError:
        session["en"] = True
        flash("Please Select a Language","warning")
        return redirect(url_for("index"))
    except UnicodeEncodeError:
        flash("Please Use Latin Alphabet.","danger")
        return redirect(url_for("index"))

# Arama - Search
@app.route("/search",methods = ["GET","POST"])
def search():
    if request.method == "GET":
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        sorgu = "Select * from comics where title like '%" + keyword + "%'"
        result = cursor.execute(sorgu)
        if result == 0:
            if session["en"] == True and session["tr"] == False:
                flash("No comics matched the search term.","warning")
            else:
                flash("Aranan kelimeye uygun çizgi roman bulunamadı.","warning")
            return redirect(url_for("index"))
        else:
            comics = cursor.fetchall()
            return render_template("index.html",comics = comics)

# Kullanıcı Arama(Yönetici Paneli) - Search User(Admin Panel)
@app.route("/search-user",methods = ["GET","POST"])
def search_user():
    if request.method == "GET":
        return redirect(url_for("adminpanel"))
    else:
        keyword = request.form.get("keyword_user")
        cursor = mysql.connection.cursor()
        sorgu = "Select * from reports where username like '%" + keyword + "%'"
        result = cursor.execute(sorgu)
        if result == 0:
            if session["en"] == True and session["tr"] == False:
                flash("No users were found matching the search terms.","warning")
            else:
                flash("Aranan kelimeye uygun kullanıcı bulunamadı.","warning")
            return redirect(url_for("adminpanel"))
        else:
            users = cursor.fetchall()
            return render_template("adminpanel.html",users = users)

# Çizgi Roman Arama(Yönetici Paneli) - Search Comic(Admin Panel)
@app.route("/search-comic",methods = ["GET","POST"])
def search_comic():
    if request.method == "GET":
        return redirect(url_for("adminpanel"))
    else:
        keyword = request.form.get("keyword_comic")
        cursor = mysql.connection.cursor()
        sorgu = "Select * from reportscomics where title like '%" + keyword + "%'"
        result = cursor.execute(sorgu)
        if result == 0:
            if session["en"] == True and session["tr"] == False:
                flash("No comics matched the search term.","warning")
            else:
                flash("Aranan kelimeye uygun çizgi roman bulunamadı.","warning")
            return redirect(url_for("adminpanel"))
        else:
            comics = cursor.fetchall()
            return render_template("adminpanel.html",comics = comics)

# İletişim - Contact
@app.route("/contact",methods = ["GET","POST"])
def contact():
    try:
        if session["en"] == True and session["tr"] == False:
            form = ContactFormEn(request.form)
        else:
            form = ContactFormTr(request.form)

        if request.method == "POST" and form.validate():
            name = form.name.data
            surname = form.surname.data
            subject = form.subject.data
            email = form.email.data
            message = form.message.data

            cursor = mysql.connection.cursor()
            sorgu = "Select * From users where email = %s"
            result = cursor.execute(sorgu,(email,))
            if result > 0:
                mesaj = MIMEMultipart()
                sender_email = email
                mesaj["From"] = sender_email
                mesaj["To"] = "comicstheman@gmail.com"
                mesaj["Subject"] = subject
                user_result = cursor.fetchone()
                user_id = user_result["id"]
                user_username = user_result["username"]
                text = "Kullanıcı Bilgileri \n --------------------------------------------\n" + "İd: " + str(user_id) + "\nKullanıcı Adı: " + user_username + "\n" + name + " " + surname + " Tarafından Gönderilmiştir." + "\nKonu Başlığı: " + subject + "\nMesajı:\n" + message
                mesaj_body = MIMEText(text,"plain")
                mesaj.attach(mesaj_body)
                try:
                    mail_gmail = smtplib.SMTP("smtp.gmail.com",587)
                    mail_gmail.starttls()
                    mail_gmail.ehlo()
                    mail_gmail.login("comicstheman@gmail.com","cyroghwyagmtehsu")
                    mail_gmail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())
                    mail_gmail.close()
                    if session["en"] == True and session["tr"] == False:
                        flash("Mail Successfully Sent.","success")
                    else:
                        flash("Mail Başarıyla Gönderildi.","success")
                    return render_template("contact.html",form = form)
                except:
                    if session["en"] == True and session["tr"] == False:
                        flash("Your Mail Submission Failed.","danger")
                    else:
                        flash("Mail Gönderiminiz Başarısız Oldu.","danger")
                    return render_template("contact.html",form = form)
            else:
                if session["en"] == True and session["tr"] == False:
                    flash("Please Login to Contact.","warning")
                else:
                    flash("İletişime Geçmek Lütfen için Giriş Yapın.","warning")
                return render_template("contact.html",form = form)
        else:
            return render_template("contact.html",form = form)
    except KeyError:
        session["en"] = True
        flash("Please Select a Language","warning")
        return redirect(url_for("index"))

# Kullanıcı Raporlama - User Reporting
@app.route("/report/<string:id>")
def report(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * From reports where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        user = cursor.fetchone()
        user_username = user["username"]
        user_email = user["email"]
        user_bansstatus = user["bansstatus"]
        user_warningcount = user["warningcount"]
        user_reportcount = user["reportcount"] + 1
        sorgu_update = "Update reports Set username = %s,email = %s,bansstatus = %s,warningcount = %s,reportcount = %s where id = %s"
        cursor.execute(sorgu_update,(user_username,user_email,user_bansstatus,user_warningcount,user_reportcount,id))
        mysql.connection.commit()
        cursor.close()
        report_success()
        return redirect(url_for("index"))
    else:
        cursor = mysql.connection.cursor()
        sorgu = "Select * From users where id = %s"
        result = cursor.execute(sorgu,(id,))
        if result > 0:
            user = cursor.fetchone()
            user_id = user["id"]
            user_username = user["username"]
            user_email = user["email"]
            sorgu_user = "Select * From users where id = %s"
            result_user = cursor.execute(sorgu_user,(session["id"],))
            if result_user > 0:
                useremail_info = cursor.fetchone()
                useremail = useremail_info["email"]
                sorgu_insert = "Insert into reports(id,username,email,useremail,reportcount) VALUES(%s,%s,%s,%s,%s)"
                cursor.execute(sorgu_insert,(user_id,user_username,user_email,useremail,1))
                mysql.connection.commit()
                cursor.close()
                report_success()
                return redirect(url_for("index"))
            else:
                error()
                return redirect(url_for("index"))
        else:
            error()
            return redirect(url_for("index"))

# Çizgi Roman Raporlama - Comic Reporting
@app.route("/reportcomic/<string:id>")
def reportcomic(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * From reportscomics where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        comic = cursor.fetchone()
        comic_title = comic["title"]
        comic_author = comic["author"]
        comic_reportcount = comic["reportcount"] + 1
        sorgu_user = "Select * From users where id = %s"
        result_user = cursor.execute(sorgu_user,(session["id"],))
        if result_user > 0:
            useremail_info = cursor.fetchone()
            useremail = useremail_info["email"]
            sorgu_update = "Update reportscomics Set title = %s,author = %s,useremail = %s,reportcount = %s where id = %s"
            cursor.execute(sorgu_update,(comic_title,comic_author,useremail,comic_reportcount,id))
            mysql.connection.commit()
            cursor.close()
            report_success()
            return redirect(url_for("index"))
    else:
        cursor = mysql.connection.cursor()
        sorgu = "Select * From comics where id = %s"
        result = cursor.execute(sorgu,(id,))
        if result > 0:
            comic = cursor.fetchone()
            comic_id = comic["id"]
            comic_title = comic["title"]
            comic_author = comic["author"]
            sorgu_user = "Select * From users where id = %s"
            result_user = cursor.execute(sorgu_user,(session["id"],))
            if result_user > 0:
                useremail_info = cursor.fetchone()
                useremail = useremail_info["email"]
                sorgu_insert = "Insert into reportscomics(id,title,author,useremail) VALUES(%s,%s,%s,%s)"
                cursor.execute(sorgu_insert,(comic_id,comic_title,comic_author,useremail))
                mysql.connection.commit()
                cursor.close()
                report_success()
                return redirect(url_for("index"))
        else:
            error()
            return redirect(url_for("index"))

# Yönetici Giriş Form - Login Admin Form
@app.route("/adminpanel-login/3CDba22XM",methods = ["GET","POST"])
def adminpanel_login():
    try:
        if session["en"] == True and session["tr"] == False:
            form = AdminFormEn(request.form)
        else:
            form = AdminFormTr(request.form)

        if request.method == "POST":
            username = form.username.data
            password_entered = form.password.data

            cursor = mysql.connection.cursor()
            sorgu = "Select * From moderators where username = %s"
            result = cursor.execute(sorgu,(username,))
            if result > 0:
                data = cursor.fetchone()
                real_password = data["password"]
                if password_entered == real_password:
                    login_success()
                    session["moderators"] = True
                    session["logged_in"] = True
                    return redirect(url_for("adminpanel"))
                else:
                    if session["en"] == True and session["tr"] == False:
                        flash("You Wrong Your Password ...","danger")
                    else:
                        flash("Parolanızı Yanlış Girdiniz...","danger")
                    return redirect(url_for("adminpanel-login"))
            else:
                if session["en"] == True and session["tr"] == False:
                    flash("There is no such user.","danger")
                else:
                    flash("Böyle bir kullanıcı bulunmuyor.","danger")
                return redirect(url_for("adminpanel_login"))
        return render_template("adminpanel_login.html",form = form)
    except KeyError:
        session["en"] = True
        flash("Please Select a Language","warning")
        return redirect(url_for("index"))

# Yönetici Paneli - Admin Panel
@app.route("/adminpanel/33CDba2XM")
def adminpanel():
    cursor = mysql.connection.cursor()
    sorgu = "Select * From reports"
    result = cursor.execute(sorgu)
    cursor_second = mysql.connection.cursor()
    sorgu_second = "Select * From reportscomics"
    result_second = cursor_second.execute(sorgu_second)
    if result > 0 and result_second > 0:
        users = cursor.fetchall()
        comics = cursor_second.fetchall()
        return render_template("adminpanel.html",users = users,comics = comics)
    elif result > 0:
        users = cursor.fetchall()
        return render_template("adminpanel.html",users = users)
    elif result_second > 0:
        comics = cursor_second.fetchall()
        return render_template("adminpanel.html",comics = comics)
    else:
        return render_template("adminpanel.html")

# Yönetici Paneli Kullanıcı Banlama Sistemi - Admin Panel User Banned System
@app.route("/banned-user/<string:id>")
def user_banned(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * From reports where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        user = cursor.fetchone()
        user_id = user["id"]
        user_username = user["username"]
        user_email = user["email"]
        user_contact_email = user["useremail"]
        user_bansstatus = "true"
        sorgu_update = "Update reports Set username = %s,email = %s,bansstatus = %s where id = %s"
        cursor.execute(sorgu_update,(user_username,user_email,user_bansstatus,user_id))
        mysql.connection.commit()
        flash("Kullanıcı Başarıyla Banlandı","success")
        mesaj = MIMEMultipart()
        mesaj["From"] = "comicstheman@gmail.com"
        mesaj["To"] = user_contact_email
        mesaj["Subject"] = "COMICS MAN - Teşşekür Ederiz."
        text = user_username + " adlı Kullanıcıyı bildirdiğiniz için teşekkür ederiz kendisi hakkında gerekli işlemler yapıldı. Size bir teşekkür borçluyuz."
        mesaj_body = MIMEText(text,"plain")
        mesaj.attach(mesaj_body)
        try:
            mail_gmail = smtplib.SMTP("smtp.gmail.com",587)
            mail_gmail.starttls()
            mail_gmail.ehlo()
            mail_gmail.login("comicstheman@gmail.com","cyroghwyagmtehsu")
            mail_gmail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())
            mail_gmail.close()
            return redirect(url_for("adminpanel"))
        except:
            flash("Hata! Bir Sorun Oluştu","danger")
            return redirect(url_for("adminpanel"))
    else:
        flash("Hata! Bir Sorun Oluştu Daha Sonra Tekrar Deneyiniz.","danger")
        return redirect(url_for("adminpanel"))

# Yönetici Paneli Çizgi Roman Banlama Sistemi - Admin Panel Comic Banned System
@app.route("/banned-comic/<string:id>")
def comic_banned(id):
    cursor = mysql.connection.cursor()
    cursor_second = mysql.connection.cursor()
    sorgu = "Select * From reportscomics where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        comic_info = cursor.fetchone()
        comic_useremail = comic_info["useremail"]
        comic_title = comic_info["title"]
        sorgu_del = "Delete from comics where id = %s"
        sorgu_del_second = "Delete from reportscomics where id = %s"
        cursor.execute(sorgu_del,(id,))
        cursor_second.execute(sorgu_del_second,(id,))
        mysql.connection.commit()
        cursor.close()
        cursor_second.close()
        flash("Çizgi Roman Başarıyla Banlandı","success")
        mesaj = MIMEMultipart()
        mesaj["From"] = "comicstheman@gmail.com"
        mesaj["To"] = comic_useremail
        mesaj["Subject"] = "COMICS MAN - Teşşekür Ederiz."
        text = comic_title + " adlı çizgi Romanı bildirdiğiniz için teşekkür ederiz çizgi roman hakkında gerekli işlemler yapıldı. Size bir teşekkür borçluyuz."
        mesaj_body = MIMEText(text,"plain")
        mesaj.attach(mesaj_body)
        try:
            mail_gmail = smtplib.SMTP("smtp.gmail.com",587)
            mail_gmail.starttls()
            mail_gmail.ehlo()
            mail_gmail.login("comicstheman@gmail.com","cyroghwyagmtehsu")
            mail_gmail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())
            mail_gmail.close()
            return redirect(url_for("adminpanel"))
        except:
            flash("Hata! Bir Sorun Oluştu","danger")
            return redirect(url_for("adminpanel"))
        return redirect(url_for("adminpanel"))
    else:
        flash("Hata! Bir Sorun Oluştu.","danger")
        return redirect(url_for("adminpanel"))

# Yönetici Paneli Çizgi Roman Yoksay Sistemi - Admin Panel Comic Ignore System
@app.route("/ignore-comic/<string:id>")
def ignore_comic(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * From reportscomics where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        sorgu_del = "Delete From reportscomics where id = %s"
        cursor.execute(sorgu_del,(id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("adminpanel"))
    else:
        flash("Hata! Bir Sorun Oluştu","danger")
        return redirect(url_for("adminpanel"))

# Yönetici Paneli Kullanıcı Yoksay Sistemi - Admin Panel User Ignore System
@app.route("/ignore-user/<string:id>")
def ignore_user(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * From reports where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        sorgu_del = "Delete From reports where id = %s"
        cursor.execute(sorgu_del,(id,))
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for("adminpanel"))
    else:
        flash("Hata! Bir Sorun Oluştu","danger")
        return redirect(url_for("adminpanel"))

# Yönetici Paneli Kullanıcı Ban Kaldırma - Admin Panel User Ban Remove
@app.route("/remove-user-banned/<string:id>")
def remove_user_banned(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * From reports where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        sorgu_delete = "Delete from reports where id = %s"
        cursor.execute(sorgu_delete,(id,))
        mysql.connection.commit()
        cursor.close()
        flash("Kullanıcı Banı Başarıyla Kaldırıldı","success")
        return redirect(url_for("adminpanel"))
    else:
        flash("Hata! Bir Sorun Oluştu","danger")
        return redirect(url_for("adminpanel"))

# Profil Şifre Değiştime - Profile Password Change
@app.route("/password-change/<string:id>",methods = ["GET","POST"])
def password_change(id):
    try:
        if request.method == "GET":
            cursor = mysql.connection.cursor()
            sorgu = "Select * From users where id = %s"
            result = cursor.execute(sorgu,(id,))
            if result > 0:
                user = cursor.fetchone()
                if session["en"] == True and session["tr"] == False:
                    form = PasswordFormEn()
                else:
                    form = PasswordFormTr()
                form.username.data = user["username"]
                form.email.data = user["email"]
                return render_template("password-change.html",form = form)
        else:
            # POST REQUEST
            if session["en"] == True and session["tr"] == False:
                form = PasswordFormEn(request.form)
            else:
                form = PasswordFormTr(request.form)

            confirm = form.confirm.data
            newPassword = form.password.data
            if newPassword == confirm:
                newPassword = sha256_crypt.encrypt(form.password.data)
                sorgu_pass = "Update users Set password = %s where id = %s"
                cursor_second = mysql.connection.cursor()
                cursor_second.execute(sorgu_pass,(newPassword,id))
                mysql.connection.commit()
                cursor_second.close()
                flash("Şifre Başarıyla Değiştirildi","success")
                return redirect(url_for("index"))
            else:
                flash("Parololar Uyuşmuyor","warning")
                return redirect(url_for("index"))
    except KeyError:
        session["en"] = True
        flash("Please Select a Language","warning")
        return redirect(url_for("index"))

# Parola Değiştirme Giriş - Login Password Change
@app.route("/forgot-password",methods = ["GET","POST"])
def forgot_password():
    try:
        if session["en"] == True and session["tr"] == False:
            form = PasswordForgotEn(request.form)
        else:
            form = PasswordForgotTr(request.form)

        if request.method == "POST":
            username = form.username.data
            email_entered = form.email.data
            cursor = mysql.connection.cursor()
            sorgu = "Select * From users where username = %s"
            result = cursor.execute(sorgu,(username,))
            if result > 0:
                user = cursor.fetchone()
                real_email = user["email"]
                user_id = user["id"]
                if email_entered == real_email:
                    mesaj = MIMEMultipart()
                    mesaj["From"] = "comicstheman@gmail.com"
                    mesaj["To"] = email_entered
                    mesaj["Subject"] = "COMICS MAN - Doğrulama Kodu"
                    r_number = random.randint(1001,9999)
                    r_number_hide_first = random.randint(10000,999999)
                    r_number_hide_second = random.randint(10000,999999)
                    text = "Doğrulama Kodunuz: " + str(r_number)
                    mesaj_body = MIMEText(text,"plain")
                    mesaj.attach(mesaj_body)
                    try:
                        mail_gmail = smtplib.SMTP("smtp.gmail.com",587)
                        mail_gmail.starttls()
                        mail_gmail.ehlo()
                        mail_gmail.login("comicstheman@gmail.com","cyroghwyagmtehsu")
                        mail_gmail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())
                        mail_gmail.close()
                        flash("Doğrulama Kodu E-Postanıza Gönderildi","success")
                        return redirect(url_for("forgot_password_confirm",r_number = r_number,user_id=user_id,r_number_hide_first = r_number_hide_first,r_number_hide_second = r_number_hide_second))
                    except:
                        flash("Mail Gönderiminiz Başarısız Oldu.","danger")
                        return redirect(url_for("index"))
            else:
                if session["en"] == True and session["tr"] == False:
                    flash("There is no such user.","danger")
                else:
                    flash("Böyle bir kullanıcı bulunmuyor.","danger")
                return redirect(url_for("index"))
        return render_template("password-forgot.html",form = form)
    except KeyError:
        session["en"] = True
        flash("Please Select a Language","warning")
        return redirect(url_for("index"))

# Parola Değiştirme Doğrulama Sistemi - Password Change Confirm System
@app.route("/forgot-password-confirm/<string:r_number_hide_first>,<string:r_number>,<string:r_number_hide_second>,<string:user_id>",methods = ["GET","POST"])
def forgot_password_confirm(r_number_hide_first,r_number,r_number_hide_second,user_id):
    try:
        if session["en"] == True and session["tr"] == False:
            form = PasswordConfirmEn(request.form)
        else:
            form = PasswordConfirmTr(request.form)

        if request.method == "POST":
            code_entered = form.code.data
            confirm = form.confirm.data
            newPassword = form.password.data
            if code_entered == r_number and newPassword == confirm:
                newPassword = sha256_crypt.encrypt(form.password.data)
                cursor = mysql.connection.cursor()
                sorgu = "Update users Set password = %s where id = %s"
                cursor.execute(sorgu,(newPassword,user_id))
                mysql.connection.commit()
                cursor.close()
                if session["en"] == True and session["tr"] == False:
                    flash("Password Changed Successfully","success")
                else:
                    flash("Şifre Başarıyla Değiştirildi","success")
                return redirect(url_for("login"))
            else:
                if session["en"] == True and session["tr"] == False:
                    flash("Error! Incorrect information","warning")
                else:
                    flash("Hata! Yanlış Bilgi","warning")
                return redirect(url_for("index"))
        return render_template("password-forgot-confirm.html",form = form)
    except KeyError:
        session["en"] = True
        flash("Please Select a Language","warning")
        return redirect(url_for("index"))

# Listem - My List
@app.route("/mylist")
@login_required
def mylist():
    cursor = mysql.connection.cursor()
    sorgu = "Select * From lists where username = %s"
    result = cursor.execute(sorgu,(session["username"],))
    if result > 0:
        comics = cursor.fetchall()
        return render_template("mylist.html",comics = comics)
    else:
        if session["en"] == True and session["tr"] == False:
            flash("Your list is empty","warning")
        else:
            flash("Listeniz Boş","warning")
        return redirect(url_for("index"))

# Listeye Ekleme - Add to List
@app.route("/addtolist/<string:id>")
@login_required
def addtolist(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * From comics where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        comic_infos = cursor.fetchone()
        comic_id = comic_infos["id"]
        comic_title = comic_infos["title"]
        comic_content = comic_infos["content"]
        comic_type = comic_infos["type"]
        comic_image = comic_infos["image"]
        comic_imgname = comic_infos["imgname"]
        sorgu_control = "Select * From lists where comicid = %s"
        result_control = cursor.execute(sorgu_control,(comic_id,))
        if result_control > 0:
            if session["en"] == True and session["tr"] == False:
                flash("Already added to the list.","warning")
            else:
                flash("Listeye Zaten Eklenildi.","warning")
            return redirect(url_for("mylist"))
        else:
            sorgu_second = "Insert into lists(usernameid,username,comicid,title,content,type,image,imgname) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sorgu_second,(session["id"],session["username"],id,comic_title,comic_content,comic_type,comic_image,comic_imgname))
            mysql.connection.commit()
            cursor.close()
            return redirect(url_for("mylist"))
    else:
        error()
        return redirect(url_for("index"))

# Listeden Silme - Delete from List
@app.route("/deletefromlist/<string:id>")
@login_required
def delete_from_list(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * From lists where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        sorgu_del = "Delete from lists where id = %s"
        cursor.execute(sorgu_del,(id,))
        mysql.connection.commit()
        cursor.close()
        if session["en"] == True and session["tr"] == False:
            flash("Successfully Deleted from List","success")
        else:
            flash("Başarıyla Listeden Silindi","success")

        return redirect(url_for("mylist"))
    else:
        error()
        return redirect(url_for("mylist"))

# Kullanıcı Uyarı Sistemi - User Warning System
@app.route("/warning-user/<string:id>")
def warning_user(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * From reports where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        user = cursor.fetchone()
        user_warning = user["warningcount"]
        user_email = user["email"]
        user_warning = user_warning + 1
        sorgu_update = "Update reports Set warningcount = %s where id = %s"
        cursor.execute(sorgu_update,(user_warning,id))
        mysql.connection.commit()
        cursor.close()
        if session["en"] == True and session["tr"] == False:
            flash("User Successfully Alerted.","success")
        else:
            flash("Kullanıcı Başarıyla Uyarıldı.","success")
        mesaj = MIMEMultipart()
        mesaj["From"] = "comicstheman@gmail.com"
        mesaj["To"] = user_email
        mesaj["Subject"] = "COMICS MAN - Uyarı"
        text = "Toplam Uyarı Sayınız: " + str(user_warning) + "\nDikkat! COMICS MAN sitesinde kötü amaçlı içerik paylaştığınız için uyarıldınız.\nToplamda 3 defa uyarılırsanız hesabınız süresiz olarak askıya alınacaktır. Daha Dikkatli Olmanız Dileğiyle!"
        mesaj_body = MIMEText(text,"plain")
        mesaj.attach(mesaj_body)
        try:
            mail_gmail = smtplib.SMTP("smtp.gmail.com",587)
            mail_gmail.starttls()
            mail_gmail.ehlo()
            mail_gmail.login("comicstheman@gmail.com","cyroghwyagmtehsu")
            mail_gmail.sendmail(mesaj["From"],mesaj["To"],mesaj.as_string())
            mail_gmail.close()
            return redirect(url_for("index"))
        except:
            error()
            return redirect(url_for("index"))
    else:
        error()
        return redirect(url_for("index"))


# İngilizce Dil Desteği
@app.route("/en")
def en():
    session["en"] = True
    session["tr"] = False
    return redirect(url_for("index"))

@app.route("/tr")
def tr():
    session["tr"] = True
    session["en"] = False
    return redirect(url_for("index"))

# Çalıştırma Fonksiyonu - Operation Functions
if __name__ == "__main__":
    app.run(debug=True)







