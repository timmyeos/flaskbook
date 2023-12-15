from flask import Blueprint, render_template, redirect, url_for

from apps.app import db  # db를 import한다
from apps.crud.models import User  # User 클래스를 import한다
from apps.crud.forms import UserForm

from flask_login import login_required  # 156 page: 로그인 필수로 만들기

# Blueprint로 crud 앱을 생성한다
crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


# index 엔드포인트를 작성하고 index.html을 반환한다
@crud.route("/")
@login_required
def index():
    return render_template("crud/index.html")


@crud.route("/sql")
@login_required
def sql():
    # # insert
    # # 사용자모델객체를 작성
    # user = User(username="jimin", email="2122@1212", password="fdsfad")
    # # 사용자 추가
    # db.session.add(user)
    # # 커밋
    # db.session.commit()

    # # update
    # user = db.session.query(User).filter_by(id=1).first()
    # user.username = "사용자명2"
    # user.email = "dfdkj@jdf"
    # user.password = "비밀번호2"
    # db.session.add(user)
    # db.session.commit()

    # # delete
    # user = db.session.query(User).filter_by(id=1).delete()
    # db.session.commit()

    db.session.query(User).all()
    db.session.query(User).filter_by(id=2, username="admin").all()
    return "콘솔 로그를 확인해 주세요"


@crud.route("/users/new", methods=["GET", "POST"])
@login_required
def create_user():
    # UserForm을 인스턴스화한다
    form = UserForm()
    # 폼의 값을 검증한다
    if form.validate_on_submit():
        # 사용자를 작성한다
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        # 사용자를 추가하고 커밋한다
        db.session.add(user)
        db.session.commit()
        # 사용자의 일람 화면으로 리다이렉트한다
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)


@crud.route("/users")
@login_required
def users():
    # 사용자의 일람을 취득한다
    users = User.query.all()
    return render_template("crud/index.html", users=users)


# 128 page
@crud.route("/users/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    form = UserForm()

    # User 모델을 이용하여 사용자를 취득한다
    user = User.query.filter_by(id=user_id).first()

    # form으로부터 제출된 경우는 사용자를 갱신하여 사용자의 일람 화면으로 리다이렉트한다
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))

    # GET의 경우는 HTML을 반환한다
    return render_template("crud/edit.html", user=user, form=form)


@crud.route("users/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))
