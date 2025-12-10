import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Lead


def create_app():
    app = Flask(__name__)

    # 간단한 시크릿 키 (실서비스에서는 환경변수로 관리)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-key")

    # Render 등에서 제공하는 DATABASE_URL 사용
    database_url = os.environ.get("DATABASE_URL", "sqlite:///local.db")
    if database_url.startswith("postgres://"):
        # Render/Heroku 스타일 URL 보정
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    @app.route("/")
    def home():
        return render_template("home.html")

    @app.route("/callback", methods=["POST"])
    def submit_callback():
        name = request.form.get("name")
        company = request.form.get("company")
        phone = request.form.get("phone")
        email = request.form.get("email")
        interest = request.form.get("interest")
        fleet_size = request.form.get("fleet_size")
        message = request.form.get("message")

        if not name or not phone or not interest:
            flash("이름, 연락처, 관심 차량/영역은 필수 항목입니다.", "error")
            return redirect(url_for("home") + "#callback")

        lead = Lead(
            name=name,
            company=company,
            phone=phone,
            email=email,
            interest=interest,
            fleet_size=fleet_size,
            message=message,
            source="website",
        )
        db.session.add(lead)
        db.session.commit()

        flash("콜백 요청이 등록되었습니다. 빠르게 연락드리겠습니다.", "success")
        return redirect(url_for("home") + "#callback")

    # 간단 관리자 페이지 – 나중에 로그인 기능 붙이면 됨
    @app.route("/admin/leads")
    def admin_leads():
        leads = Lead.query.order_by(Lead.created_at.desc()).all()
        return render_template("admin_leads.html", leads=leads)

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
