from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, ForeignKey,Enum
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from my_app import db
from datetime import datetime
import enum


class MyRole(enum.Enum):
    ADMIN = 1
    NHANVIEN = 2
    USER = 3

class TUYENBAY (db.Model):
	MaTuyenBay =  Column(Integer, primary_key=True,autoincrement=True)
	SanBayDi = Column(String(50), nullable=False)
	SanBayDen = Column(String(50),nullable=False)


class HANGVE (db.Model):
    MaHangVe = Column(Integer, primary_key=True,autoincrement=True)
    TenHangVe = Column(String(50), nullable=False)

    def __str__(self):
        return self.TenHangVe

class CHUYENBAY (db.Model):
        MaChuyenBay =  Column(Integer, primary_key=True,autoincrement=True)
        MaTuyenBay =Column(Integer, ForeignKey(TUYENBAY.MaTuyenBay), nullable=False)
        NgayGio = Column(DateTime, default=datetime.now())
        Thoigianbay = Column(String(50), nullable=False)
        Soluongghehang1 = Column(Integer, nullable=False)
        Soluongghehang2 = Column(Integer, nullable=False)
        TuyenBay=relationship('TUYENBAY',backref='CHUYENBAY',lazy=True)

class HANHKHACH(db.Model):

    MaHanhKhach = Column(Integer, primary_key=True,autoincrement=True)
    Tenhanhhach = Column(String(50), nullable=False)
    Cmnd = Column(String(50), nullable=False,unique=True)
    Sdt= Column(String(10), nullable=False)
    Gmail= Column(String(50), nullable=False)

    def __str__(self):
        return self.Tenhanhhach


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    joined_date = Column(DateTime, default=datetime.now())
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    Cmnd = Column(String(50), nullable=False)
    Role = Column(Enum(MyRole), default=MyRole.USER)
    def __str__(self):
        return self.name



class VECHUYENBAY(db.Model):

    MaVe = Column(Integer, primary_key=True,autoincrement=True)
    MaChuyenBay = Column(Integer, ForeignKey(CHUYENBAY.MaChuyenBay), nullable=False)
    MaHangVe= Column(Integer, ForeignKey(HANGVE.MaHangVe), nullable=False)
    MaHanhKhach = Column(Integer, ForeignKey(HANHKHACH.MaHanhKhach), nullable=False)
    GiaTien= Column(Float ,nullable=False)
    Chuyenbay=relationship('CHUYENBAY',backref='VECHUYENBAY',lazy=True)
    Hangve = relationship('HANGVE', backref='VECHUYENBAY', lazy=True)
    Hanhkhach = relationship('HANHKHACH', backref='VECHUYENBAY', lazy=True)
    def __str__(self):
        return self.MaVe


class DONGIA (db.Model):
        MaDonGia =  Column(Integer, primary_key=True,autoincrement=True)
        MaTuyenBay =Column(Integer, ForeignKey(TUYENBAY.MaTuyenBay),nullable=False)
        MaHangVe =  Column(Integer, ForeignKey(HANGVE.MaHangVe), nullable=False)
        DonGia = Column(Float,default=0)
        HangVe=relationship('HANGVE',backref='DONGIA',lazy=True)
        TuyenBay=relationship('TUYENBAY',backref="DONGIA",lazy=True)




class TINHTRANGVE(db.Model):

     TinhTrangVe = Column(Integer, primary_key=True,autoincrement=True)
     MaChuyenBay =  Column(Integer, ForeignKey(CHUYENBAY.MaChuyenBay), nullable=False)
     Mahangve = Column(Integer,nullable=False)
     SoGheTrong = Column(Integer ,nullable=False)
     SoGheDat= Column(Integer ,nullable=False)
     def __str__(self):
        return self.name
class SANBAYTRUNGGIAN(db.Model):

     MaSanBayTG= Column(Integer, primary_key=True,autoincrement=True)
     MaChuyenBay = Column(Integer, ForeignKey(CHUYENBAY.MaChuyenBay), nullable=False)
     DiaDiem = Column(String(50),nullable=False)
     ThoiGianDung = Column(Integer ,nullable=False)
     def __str__(self):
        return self.name

class PHIEUDATCHO(db.Model):
    MaPhieuDat = Column(Integer, primary_key=True,autoincrement=True)
    MaHangVe = Column(Integer, ForeignKey(HANGVE.MaHangVe), nullable=False)
    MaHK = Column(Integer, ForeignKey(HANHKHACH.MaHanhKhach), nullable=False)
    MaChuyenBay = Column(Integer, ForeignKey(CHUYENBAY.MaChuyenBay), nullable=False)
    Ngaydat = Column(DateTime, default=datetime.now())

    def __str__(self):
        return self.name


class DOANHTHUTHANG(db.Model):
    MaDoanhThuThang = Column(Integer, primary_key=True,autoincrement=True)
    MaChuyenBay = Column(Integer, ForeignKey(CHUYENBAY.MaChuyenBay), nullable=False)
    SoVe = Column(Integer, nullable=False)
    TyLe = Column(String(10), nullable=False)
    DoanhThu = Column(Float, nullable=False)

    def __str__(self):
        return self.name
class Order(db.Model):
    OrderID = Column(Integer, primary_key=True, autoincrement=True)
    SoVe = Column(Integer, nullable=False )
    GiaTien = Column(Float, nullable=False )

if __name__ == '__main__':
    db.create_all()
