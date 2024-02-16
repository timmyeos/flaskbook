from pathlib import Path

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

from apps.config import config

# SQLAlchemy를 인스턴스화 한다
db = SQLAlchemy()

# 117 page
csrf = CSRFProtect()

# 149 page: LoginManager를 인스턴스화 한다
login_manager = LoginManager()
# login_view 속성에 미로그인 시 회원가입 기능으로 리다이렉트하는 엔드포인트를 지정한다
login_manager.login_view = "auth.signup"
# login_message 속성에 로그인 후에 표시할 메세지 지정
login_manager.login_message = ""


# 90 page: create_app 함수를 작성한다
# 139 page: config의 키를 전달한다
def create_app(config_key):
    # flask 인스턴스 생성
    app = Flask(__name__)

    ### database ###
    # config_key에 매치하는 환경의 config 클래스를 읽어들인다
    app.config.from_object(config[config_key])

    # # 100 page. 앱의 config 설정을 한다
    # app.config.from_mapping(
    #     SECRET_KEY="1234",
    #     SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False,
    #     # SQL을 콘솔 로그에 출력하는 설정
    #     SQLALCHEMY_ECHO=True,
    #     WTF_CSRF_SECRET_KEY="qwer",
    # )

    # CSRFProtect와 앱을 연계한다
    csrf.init_app(app)

    # SQLAlchemy와 앱을 연계한다
    db.init_app(app)

    # Migrate와 앱을 연계한다
    Migrate(app, db)

    # login_manager를 앱과 연계한다
    login_manager.init_app(app)

    ### blueprint ###
    # apps폴더 밑의 crud 패키지로부터 views.py를 import 한다
    from apps.crud import views as crud_views

    # register_blueprint를 사용해 views의 crud를 앱에 등록한다
    app.register_blueprint(crud_views.crud, url_prefix="/crud")

    # 앞으로 작성하는 apps폴더 밑의 auth 패키지로부터 views.py를 import 한다
    from apps.auth import views as auth_views

    # register_blueprint를 사용해 views의 auth를 앱에 등록한다
    app.register_blueprint(auth_views.auth, url_prefix="/auth")

    # 앞으로 작성하는 apps폴더 밑의 detector 패키지로부터 views.py를 import 한다
    from apps.detector import views as dt_views

    # register_blueprint를 사용해 views의 auth를 앱에 등록한다
    app.register_blueprint(dt_views.dt)

    return app
