import logging
import os

from email_validator import validate_email, EmailNotValidError
from flask import (
    Flask,
    render_template,
    url_for,
    current_app,
    g,
    request,
    redirect,
    flash,
)
from flask_debugtoolbar import DebugToolbarExtension
from flask_mail import Mail, Message

app = Flask(__name__)

app.config["SECRET_KEY"] = "WJFDFJSA856H25"
# logging level 설정
app.logger.setLevel(logging.DEBUG)
# app.logger.critical('faltal error') # 로그를 출력함
# 리다이렉트를 중단하지 않도록
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
# 디버그툴바확장 클래스 인스턴스(객체) 생성 ; DebugToolbarExtension에 애플리케이션을 설정
toolbar = DebugToolbarExtension(app)

# Mail 클래스의 config를 환경 변수로 부터 얻어서 추가
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER")
app.config["MAIL_PORT"] = os.environ.get("MAIL_PORT")
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS")
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")
# Mail 클래스 인스턴스(객체) 생성 ; flask-mail 확장을 등록한다
mail = Mail(app)


# '127.0.0.1:5000:/'
@app.route("/")
def index():
    return "Hello, Flaskbook!"


# @app.route("/hello", methods=["GET", "POST"])
# def hello():
#     return "Hello, World!"


# app.get("/hello/<name>")
# app.post("/hello/<name>") 두 줄 적은 거랑 같은 거임
@app.route("/hello/<name>", methods=["GET", "POST"], endpoint="hello-endpoint")
def hello(name):
    return f"Hello, {name}!"


@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html", name=name)


# light is on/off를 웹페이지에 표시하는 연습
# 주소창에 http://127.0.0.1:5000/light_check/off으로 실험해보면 됨
@app.route("/light_check/<onoff>")
def light_check(onoff):
    return render_template("light_check.html", onoff=onoff)


# 55 page
with app.test_request_context():
    print(url_for("index"))
    print(url_for("hello-endpoint", name="world"))
    print(url_for("show_name", name="jimin", page="1"))
    print(url_for("show_name", name="AK", page="1"))


# 58 page
# ctx = app.app_context()
# ctx.push
# print(current_app.name)
# g.connection = "connection"
# print(g.connection)

with app.test_request_context("/user?update=true"):
    print(request.args.get("updated"))


# 62 page
@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":  # contact.html에서 문의 버튼 눌려서 post로 온 경우에만 실행
        # form 값 취득
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]
        print(username, email, description)

        # 입력체크
        is_valid = True
        if not username:
            flash("사용자명은 필수입니다")
            is_valid = False
        if not email:
            flash("메일 주소는 필수입니다")
            is_valid = False
        try:
            validate_email(email)
        except EmailNotValidError as e:
            flash("메일 주소의 형식으로 입력해주세요")
            flash(str(e))
            is_valid = False
        if not description:
            flash("문의 내용은 필수입니다")
            is_valid = False

        if not is_valid:  # 입력이 잘못된 경우 다시 contact.html 띄움
            return redirect(url_for("contact"))

        # 이메일을 보낸다
        send_email(
            email,
            "문의 감사합니다.",
            "contact_mail",
            username=username,
            description=description,
        )

        # post 입력값에 문제 없는 경우 실행됨
        flash("문의해 주셔서 감사합니다~!")
        return redirect(
            url_for("contact_complete")
        )  # contact_complete 엔드포인트로 리다이렉트하면 if문에 안걸리고
    return render_template("contact_complete.html")  # 여기 실행되서 contact_complete.html 띄워줌


# 78 page     누구에게, 제목, 내용
def send_email(to, subject, template, **kwargs):
    # 메일 송수신하는 함수
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
