import datetime
import math

from my_app.models import User, Order
from my_app import app, db
from flask_login import current_user
import hashlib
from flask import render_template, request, session, jsonify, render_template_string
from my_app import app, my_login, utils
from my_app.models import User, HANHKHACH, MyRole, PHIEUDATCHO, VECHUYENBAY, CHUYENBAY, TUYENBAY
from flask_login import login_user

from admin import *


@app.route("/", methods=['get', 'post'])
def home():
    session['solansai'] = 0
    data_chuyenbay = request.form.copy()
    session["info1"] = data_chuyenbay
    tb = TUYENBAY.query.all()
    hv = HANGVE.query.all()
    if data_chuyenbay:
        return redirect("/chuyenbay")
    return render_template("index.html", tb=tb, hv=hv)


@app.route("/register", methods=['get', 'post'])
def register():
    err_msg = ""
    if request.method == 'POST':
        try:
            password = request.form["password"]
            confirm_password = request.form['confirm-password']
            if password.strip() == confirm_password.strip():

                data = request.form.copy()
                del data['confirm-password']

                if utils.add_user(**data):
                    return redirect("/login")
                else:
                    err_msg = "Du lieu dau vao khong hop le!"
            else:
                err_msg = "Mat khau khong khop!"
        except:
            err_msg = "He thong dang co loi! Vui long quay lai sau!"

    return render_template('register.html', err_msg=err_msg)


@app.route("/login", methods=['get', 'post'])
def normal_user_login():
    err_msg = ""
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        data = request.form.copy()
        password = str(hashlib.md5(password.encode("utf-8")).digest())
        user = User.query.filter(User.username == username,
                                 User.password == password).first()
        if user:  # dang nhap thanh cong
            if user.Role == MyRole.ADMIN:
                login_user(user)
                return redirect(request.args.get("next", "/admin"))
            if user.Role == MyRole.USER:
                login_user(user)
                return redirect(request.args.get("next", "/user-profile"))
            if user.Role == MyRole.NHANVIEN:
                login_user(user)
                return redirect(request.args.get("next", "/user-nhanvien"))
        else:
            err_msg = "Username hoặc Password sai!"
            session['solansai'] = session['solansai'] + 1;
            solan = session['solansai']
            print(solan)
            if solan == 4:
                session['solansai'] = 0
                return redirect(request.args.get("next", "/"))

    return render_template("login.html", err_msg=err_msg)


# @app.route ("/login")
# def login():
#     return render_template("login.html")

@my_login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


# login
# @app.route("/login", methods=['post'])
# def login_exe():
#     username = request.form.get("username")
#     password = request.form.get("password")
#     password = str(hashlib.md5(password.encode("utf-8")).digest())
#
#     user = User.query.filter(User.username == username,
#                              User.password == password).first()
#
#     if user: # dang nhap thanh cong
#         login_user(user)
#     return redirect("/admin")
@app.route("/user-profile")
def user_profiles():
    info_hanhkhach = HANHKHACH.query.all()
    # user1 = User.query.filter(User.password == password).first()

    info_phieudat = PHIEUDATCHO.query.all()
    info_chuyenbay = CHUYENBAY.query.all()
    info_hangve = HANGVE.query.all()
    info_tuyenbay = TUYENBAY.query.all()
    info_dongia = DONGIA.query.all()
    info_vechuyenbay = VECHUYENBAY.query.all()
    for hk in info_hanhkhach:
        if (current_user.Cmnd == hk.Cmnd):
            get_mhk = hk.MaHanhKhach

    for vcb in info_vechuyenbay:
        if (get_mhk == vcb.MaHanhKhach):
            get_giatien = vcb.GiaTien
            get_mhv = vcb.MaHangVe
            get_mcb = vcb.MaChuyenBay

    for pd in info_hangve:
        if (get_mhv == pd.MaHangVe):
            get_thv = pd.TenHangVe

    for cb in info_chuyenbay:
        if (get_mcb == cb.MaChuyenBay):
            get_mtb = cb.MaTuyenBay
            get_tgbay = cb.Thoigianbay
            get_ngaybay = cb.NgayGio

    for tb in info_tuyenbay:
        if (get_mtb == tb.MaTuyenBay):
            get_sbd = tb.SanBayDi
            get_sbde = tb.SanBayDen

    return render_template("user-profile.html", info_hanhkhach=info_hanhkhach, get_thv=get_thv, get_giatien=get_giatien,
                           get_tgbay=get_tgbay, get_ngaybay=get_ngaybay, get_sbd=get_sbd, get_sbde=get_sbde)
    # return render_template("user-profile.html",info_hanhkhach=info_hanhkhach,info_phieudat=info_phieudat,info_chuyenbay=info_chuyenbay)


@app.route("/user-nhanvien")
def user_nhanvien():
    tinhtrangve = TINHTRANGVE.query.all()
    hanhkhach = HANHKHACH.query.all()
    info_hanhkhach = HANHKHACH.query.all()
    # user1 = User.query.filter(User.password == password).first()
    info_chuyenbay = CHUYENBAY.query.all()
    info_tuyenbay = TUYENBAY.query.all()
    info_vechuyenbay = VECHUYENBAY.query.all()
    data_sbd = {}
    data_sbde = {}
    data_tgb = {}
    data_sgt = {}
    data_sgd = {}
    ket = {}
    i = 0
    for tb in info_tuyenbay:
        for cb in info_chuyenbay:
            for tt in tinhtrangve:
                if (tt.MaChuyenBay == cb.MaChuyenBay and tb.MaTuyenBay == cb.MaTuyenBay):
                    data_sbd[i] = tb.SanBayDi
                    data_sbde[i] = tb.SanBayDen
                    data_tgb[i] = cb.Thoigianbay
                    data_sgt[i] = tt.SoGheTrong
                    data_sgd[i] = tt.SoGheDat
                    ket[i] = [data_sbd[i], data_sbde[i], data_tgb[i], data_sgt[i], data_sgd[i]]
                    i = i + 1;

    return render_template("user-nhanvien.html", hanhkhach=hanhkhach, ket=ket)


@app.route("/Tracuu", methods=['get', 'post'])
def user_tracuu():
    err = ""
    check = False
    if request.method == 'POST':
        session['tracuu'] = request.form.copy()
        tracuu = session['tracuu']
        sbd = tracuu['SanBayDi']
        sbde = tracuu['SanBayDen']
        info_chuyenbay = CHUYENBAY.query.all()
        info_tuyenbay = TUYENBAY.query.all()
        for tb in info_tuyenbay:
            if tb.SanBayDi == sbd and tb.SanBayDen == sbde:
                check = True
                err = f"Chúng tôi có chuyến bay từ {sbd} đến {sbde} mời khách hàng đến quầy mua vé"
                break
            else:
                check = False
        if (check == False):
            err = "Xin lỗi!!Chúng tôi chưa cập nhật tuyến bay này"

    session['tracuu'] = ""
    return render_template("Tracuu.html", err=err)


@app.route('/upload', methods=['post'])
def upload():
    avatar = request.files.get("avatar")
    if avatar:
        avatar.save("%s/static/images/%s" % (app.root_path, avatar.filename))
        return "SUCCESSFUL"

    return "FAILED"


@app.route('/sell', methods=['get', 'post'])
def sell():
    # err_msg = ""
    b = session['info1']
    sbdi = b['SanBayDi']
    sbden = b['SanBayDen']
    hangve = b['hangve']
    kt = TUYENBAY.query.all()
    d = 0
    for l in kt:
        if sbdi == l.SanBayDi and sbden == l.SanBayDen:
            d = l.MaTuyenBay
    if d == 0:
        return redirect('/tuyenbay')
    tg = session['tg']
    tv = HANGVE.query.all()
    for i in tv:
        if i.TenHangVe == hangve:
            thv = i.MaHangVe
    hv = DONGIA.query.filter(DONGIA.MaTuyenBay == d).filter(DONGIA.MaHangVe == thv)
    cb = CHUYENBAY.query.all()
    ttv = TINHTRANGVE.query.all()
    for u in cb:
        if d == u.MaTuyenBay:
            if u.Thoigianbay == tg['Thoigianbatdau']:
                for y in ttv:
                    if u.MaChuyenBay == y.MaChuyenBay:
                        sgt = TINHTRANGVE.query.filter(TINHTRANGVE.MaChuyenBay == u.MaChuyenBay)
    data = request.form.copy()
    session["info"] = data
    if data:
        return redirect('/info')
    # if request.method == 'POST':
    #     try:
    #         data = request.form.copy()
    #         if utils.add_HK(**data):
    #             return redirect("/")
    #     except:
    #         err_msg="Loi"
    return render_template("sell.html", hv=hv, sgt=sgt)


@app.route('/tuyenbay', methods=['get', 'post'])
def tuyenbay():
    tb = TUYENBAY.query.all()
    data1 = request.form.copy()
    session["info1"] = data1
    hv = HANGVE.query.all()
    if data1:
        return redirect("/chuyenbay")
    return render_template('tuyenbay.html', tb=tb, hv=hv)


@app.route("/chuyenbay", methods=['get', 'post'])
def chuyenbay():
    b = session['info1']
    sbdi = b['SanBayDi']
    sbden = b['SanBayDen']
    if 'Ngaydi' not in b:
        ngay_di=datetime.date.today()
    else:
        ngay_di = b['Ngaydi']

    kt = TUYENBAY.query.all()
    d = 0
    session['2'] = 0
    for l in kt:
        if sbdi == l.SanBayDi and sbden == l.SanBayDen:
            d = l.MaTuyenBay
    if d == 0:
        return redirect('/tuyenbay')
    cb = CHUYENBAY.query.filter(CHUYENBAY.MaTuyenBay == d)
    cb=cb.filter(CHUYENBAY.NgayGio>ngay_di)
    for p in cb:
        session['2'] = p.MaChuyenBay
    return render_template('chuyenbay.html', cb=cb)


@app.route("/chuyenbaycuatoi", methods=['get', 'post'])
def chuyenbaycuatoi():
    return render_template('chuyenbaycuatoi.html')


@app.route("/chuyenbaytoi", methods=['get', 'post'])
def chuyenbaytoi():
    if request.method == "POST":
        cmnd = request.form.get('cmnd')
        hanhkhach=HANHKHACH.query.all()
        makhachhang=0
        for hk in hanhkhach:
            if hk.Cmnd==cmnd:
                makhachhang=hk.MaHanhKhach
        vechuyenbay = VECHUYENBAY.query.filter(VECHUYENBAY.MaHanhKhach == makhachhang) \
            .add_columns(VECHUYENBAY.GiaTien.label('giatien'))
        vechuyenbay = vechuyenbay.join(CHUYENBAY) \
            .join(TUYENBAY) \
            .filter(CHUYENBAY.MaTuyenBay == TUYENBAY.MaTuyenBay) \
            .add_columns(CHUYENBAY.MaTuyenBay.label('matuyenbay')) \
            .add_columns(CHUYENBAY.NgayGio.label('ngaygio')) \
            .add_columns(CHUYENBAY.Thoigianbay.label('thoigianbay')) \
            .add_columns(TUYENBAY.SanBayDi, TUYENBAY.SanBayDen)
        if (vechuyenbay.count()==0):
            vechuyenbay=None
    return render_template('chuyenbaytoi.html', vechuyenbay=vechuyenbay, makhachhang=makhachhang)


@app.route('/api/chuyenbay', methods=['post'])
def thoigianbay():
    data = request.json
    cart = {
        "Thoigianbatdau": data["Thoigianbatdau"]
    }
    session['tg'] = cart
    return cart


@app.route('/api/pay', methods=['post'])
def pay1():
    b = session['info1']
    sbdi = b['SanBayDi']
    sbden = b['SanBayDen']
    hangve = b['hangve']
    kt = TUYENBAY.query.all()
    cb = CHUYENBAY.query.all()
    d = 0
    for l in kt:
        if sbdi == l.SanBayDi and sbden == l.SanBayDen:
            d = l.MaTuyenBay
    tv = HANGVE.query.all()
    for i in tv:
        if i.TenHangVe == hangve:
            thv = i.MaHangVe
    data2 = session['info']
    gt = data2['giave']
    Tenhanhkhach = data2['Tenhanhhach']
    SDT = data2['Sdt']
    CMND = data2['Cmnd']
    GMAIL = data2['Gmail']
    if request.method == 'POST':
        if utils.add_HK(Tenhanhkhach, CMND, SDT, GMAIL):
            hk = HANHKHACH.query.all()
            for i in hk:
                if i.Tenhanhhach == Tenhanhkhach:
                    if i.Sdt == SDT:
                        if i.Cmnd == CMND:
                            if i.Gmail == GMAIL:
                                session['hk'] = i.MaHanhKhach

        if utils.add_vcb(session['2'], thv, session['hk'], gt):
            return jsonify({
                "error_code": 200
            })
    return jsonify({
        "error_code": 400
    })


@app.route('/pay')
def pay():
    return render_template("pay.html")


# @app.route('/api/info',methods=['post'])
# def info():
#     info = session.get("info")
#     if not info:
#         info={}
#
#     data = request.json
#     Tenhanhhach=data["Tenhanhhach"]
#     info[Tenhanhhach]={
#         "Tenhanhach":data["Tenhanhhach"],
#         "Sdt":data["Sdt"],
#         "Cmnd":data["Cmnd"],
#         "Gmail":data["Gmail"]
#     }
#     session["info"] = info


@app.route('/info', methods=['get', 'post'])
def info():
    data2 = session['info']
    data3 = session['info1']
    tien = float(data2['giave'])
    session['doanhthu'] = tien
    data4 = request.form.copy()
    if not data2:
        return redirect('/sell')
    if request.method == 'POST':
        if data2:
            if data3:
                return redirect('/pay')

    # if request.method == 'POST':
    #     try:
    #         if utils.add_HK(tenhanhkhach,cmnd,sdt,gmail):
    #             return redirect('/')
    #     except:
    #         print('Loi')
    return render_template('info.html')


# SANG
# Khi đã thanh toán thì import dữ liệu xuống bảng ORDER
@app.route('/payed', methods=['get', 'post'])
def report():
    sv = int(0)
    global gt

    if 'doanhthu' in session:
        gt = float(session['doanhthu'])
        sv += 1
    order = Order(SoVe=sv, GiaTien=gt)
    db.session.add(order)
    db.session.commit()
    session.pop('doanhthu', None)
    #     mes = "Thanh toán thành công !"
    return redirect('/')


# Doanh thu gồm tổng số vé và tổng tiền
@app.route('/doanhthuthang', methods=['get', 'post'])
def doanhthu():
    sum = float(0)
    sv = int(0)
    dt = Order.query.all()

    for i in range(1, (len(dt) + 1)):
        sum += float(Order.query.get(i).GiaTien)
        sv += 1

    return render_template('report.html', gt=sum, sv=sv)


if __name__ == '__main__':
    app.run(debug=True)
