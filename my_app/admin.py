from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from flask import redirect
from my_app.models import VECHUYENBAY, CHUYENBAY, HANGVE, TUYENBAY, HANHKHACH, DONGIA,TINHTRANGVE,SANBAYTRUNGGIAN,PHIEUDATCHO,DOANHTHUTHANG
from my_app import db, admin

#mấy cái view có sãn thì kế thừa modelview

class AuthenticatedView(ModelView): #tạo một lớp để kế thừa modelview  chung cho tiện
    def is_accessible(self):
        return current_user.is_authenticated #current user đăng nhập vào dc phép xem view


class VeChuyenBayView(AuthenticatedView):
    can_export = True #cho phép export view  ra excel
class PhieuDatCho(AuthenticatedView):
    can_export = True
class SanBayTG(AuthenticatedView):
    can_export = True
class ChuyenBayView(AuthenticatedView):
    can_export = True

class TuyenBayView(AuthenticatedView):
    can_export = True

class HangVeView(AuthenticatedView):
    can_export = True



class HanhKhachView(AuthenticatedView):
    can_export = True

class DonGiaView(AuthenticatedView):
    can_export = True

class TinhTrangVeView(AuthenticatedView):
    can_export = True



class DoanhThuThangView(AuthenticatedView):
    can_export = True




#muốn tạo view mới thì phải kế thừa baseview
class LogoutView(BaseView):  #tao view logout
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated
class StatsView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/stats.html")

    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated
#thêm view bào trang admin
admin.add_view(VeChuyenBayView(VECHUYENBAY, db.session, name="Ve Chuyen Bay"))
admin.add_view(ChuyenBayView(CHUYENBAY, db.session, name="Chuyen Bay"))
admin.add_view(TuyenBayView(TUYENBAY, db.session, name="Tuyen Bay"))
admin.add_view(HangVeView(HANGVE, db.session, name="Hang Ve"))
admin.add_view(HanhKhachView(HANHKHACH, db.session, name="Hanh Khach"))
admin.add_view(DonGiaView(DONGIA, db.session, name="Don Gia"))
admin.add_view(TinhTrangVeView(TINHTRANGVE, db.session, name="Tinh Trang Ve"))
admin.add_view(PhieuDatCho(PHIEUDATCHO, db.session, name="Phieu Dat Cho"))
admin.add_view(SanBayTG(SANBAYTRUNGGIAN, db.session, name="San Bay Trung Gian"))
admin.add_view(DoanhThuThangView(DOANHTHUTHANG, db.session, name="Doanh Thu Thang"))
admin.add_view(LogoutView(name="Dang xuat"))