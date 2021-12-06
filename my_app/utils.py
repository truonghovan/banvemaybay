
from my_app.models import User
from my_app import app, db
from flask_login import current_user
import hashlib
from flask import render_template, request, session, jsonify
from my_app import app, my_login,utils
from my_app.models import User,HANHKHACH,MyRole,PHIEUDATCHO,VECHUYENBAY,CHUYENBAY,DONGIA,HANGVE,TUYENBAY,DOANHTHUTHANG
from flask_login import login_user
def add_user(name, username, password, Cmnd):
    password = str(hashlib.md5(password.encode("utf-8")).digest())
    user = User(name=name,
                username=username,
                password=password,
                Cmnd=Cmnd
                )
    db.session.add(user)

    try:
        db.session.commit()
        return True
    except:
        return False

def add_HK(Tenhanhhach,Cmnd,Sdt,Gmail):
    hanhkhach = HANHKHACH(Tenhanhhach=Tenhanhhach,
                        Cmnd=Cmnd,
                        Sdt=Sdt,
                        Gmail=Gmail
                        )
    db.session.add(hanhkhach)
    try:
        db.session.commit()
        return True
    except:
        return False

def get_products(SanBayDi=None, SanBayDen=None):
    products = TUYENBAY.query
    if SanBayDi and SanBayDen:
        products = products.filter(TUYENBAY.SanBayDi == SanBayDi,TUYENBAY.SanBayDen == SanBayDen)
    return products


def add_vcb(chuyenbay,hangve,hanhkhach,giatien):
    vechuyenbay=VECHUYENBAY(MaChuyenBay=chuyenbay,
                            MaHangVe=hangve,
                            MaHanhKhach=hanhkhach,
                            GiaTien=giatien)
    db.session.add(vechuyenbay)
    try:
        db.session.commit()
        return True
    except:
        return False


def get_tb():
    return TUYENBAY.query.all()

def get_hv(hangve=None,Dongia=None,tuyenbay=None):
    return DONGIA.query.all()
def get_DoanhThuThang():
    return DOANHTHUTHANG.query.all()