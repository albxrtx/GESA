from flask import Flask, render_template, request, session, redirect, url_for

# pip install flask_sqlalchemy
# pip install SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.exc import IntegrityError

app = Flask(__name__, template_folder="templates")
# Clave secreta
app.secret_key = "clave_secreta"

from werkzeug.utils import secure_filename

app.config["UPLOAD_FOLDER"] = "static/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "webp"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.id} - {self.name}>"


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Company {self.id} - {self.name}>"


class Items(db.Model):
    id = db.Column(
        db.Integer,
        nullable=False,
        primary_key=True,
        autoincrement=False,
    )
    name = db.Column(db.String(100), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    supplier = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Item {self.id} - {self.name}>"


class Sales(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_item = db.Column(db.Integer, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Sale {self.id} - {self.name}>"


class Employees(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Employer {self.id} - {self.name}>"


class Departments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    color = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Department {self.id} - {self.name}>"


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<Project {self.id} - {self.name}>"


with app.app_context():
    db.create_all()


@app.route("/")
def home():
    if "user_name" not in session:
        return redirect(url_for("landing_page"))
    else:
        return redirect(url_for("company"))


@app.route("/landing_page")
def landing_page():
    return render_template("landing_page.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = Users.query.filter_by(email=email).first()

        if user and user.password == password:
            session["user_name"] = user.name
            session["email"] = user.email
            return redirect(url_for("company"))
        elif user:
            error = "Correo electrónico o contraseña no coinciden"
            return render_template("login.html", error=error)
        else:
            error = "Correo electrónico no registrado"
            return render_template("login.html", error=error)

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    default_img = "img/default-user.webp"
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        new_user = Users(name=name, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return "El correo ya está registrado."

        session["user_name"] = new_user.name
        session["email"] = new_user.email
        session["user_image"] = default_img
        return redirect(url_for("company"))

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("user_name", None)
    session.pop("email", None)
    return redirect(url_for("landing_page"))


@app.route("/company")
def company():
    company = Company.query.first()
    departments = Departments.query.all()
    if "user_name" not in session:
        return redirect(url_for("login"))
    return render_template(
        "company.html",
        name=session["user_name"],
        company=company,
        departments=departments,
    )


@app.route("/modify-company", methods=["GET", "POST"])
def modify_company():
    if request.method == "POST":
        name = request.form.get("name")
        location = request.form.get("location")
        contact = request.form.get("contact")

        company = Company.query.first()
        if not company:
            company = Company(name=name, location=location, contact=contact)
            db.session.add(company)
        else:
            company.name = name
            company.location = location
            company.contact = contact

        db.session.commit()

        return redirect(url_for("company"))

    company = Company.query.first()
    return render_template("modify_company.html", company=company)


@app.route("/add-department", methods=["GET", "POST"])
def add_department():
    departments = Departments.query.all()
    if request.method == "POST":

        name = request.form["name_department"]
        color = request.form["color_department"]
        new_department = Departments(name=name, color=color)

        try:
            db.session.add(new_department)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return redirect(url_for("company"))

        return redirect(url_for("company"))
    return render_template("company.html", departments=departments)


@app.route("/department-item/<int:department_id>", methods=["POST"])
def delete_department(department_id):
    department = Departments.query.get_or_404(department_id)
    db.session.delete(department)
    db.session.commit()
    return redirect(url_for("company"))


@app.route("/inventory")
def inventory():
    items = Items.query.all()
    return render_template("inventory.html", name=session["user_name"], items=items)


@app.route("/add-item", methods=["GET", "POST"])
def add_item():
    if request.method == "POST":
        items = Items.query.all()
        id = request.form["id"]
        name = request.form["name"]
        stock = request.form["stock"]
        supplier = request.form["supplier"]

        new_item = Items(id=int(id), name=name, stock=int(stock), supplier=supplier)

        try:
            db.session.add(new_item)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return redirect(url_for("inventory"))

        return redirect(url_for("inventory"))
    return render_template("inventory.html", items=items)


@app.route("/delete-item/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    item = Items.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("inventory"))


@app.route("/sales")
def sales():
    items = Items.query.all()
    sales = Sales.query.all()
    return render_template(
        "sales.html", name=session["user_name"], sales=sales, items=items
    )


@app.route("/add-sale", methods=["GET", "POST"])
def add_sale():
    if request.method == "POST":
        items = Items.query.all()
        sales = Sales.query.all()

        id_item = request.form["id"]
        client_name = request.form["client_name"]
        date = request.form["date"]
        state = request.form["sale_state"]

        new_sale = Sales(
            id_item=int(id_item), client_name=client_name, date=date, state=state
        )

        try:
            db.session.add(new_sale)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return redirect(url_for("sales"))

        return redirect(url_for("sales"))
    return render_template("sales.html", sales=sales, items=items)


@app.route("/delete-sale/<int:sale_id>", methods=["POST"])
def delete_sale(sale_id):
    sale = Sales.query.get_or_404(sale_id)
    db.session.delete(sale)
    db.session.commit()
    return redirect(url_for("sales"))


@app.route("/employees")
def employees():
    departments = Departments.query.all()
    employees = Employees.query.all()
    users = Users.query.all()
    return render_template(
        "employees.html",
        name=session["user_name"],
        users=users,
        employees=employees,
        departments=departments,
    )


@app.route("/add-employer", methods=["GET", "POST"])
def add_employer():
    employees = Employees.query.all()
    if request.method == "POST":
        id = request.form["id"]
        name = request.form["name"]
        department = request.form["department"]
        contact = request.form["contact"]

        new_employer = Employees(
            id=int(id), name=name, department=department, contact=contact
        )

        try:
            db.session.add(new_employer)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return redirect(url_for("employees"))

        return redirect(url_for("employees"))
    return render_template("employees.html", employees=employees)


@app.route("/delete-employer/<int:employer_id>", methods=["POST"])
def delete_employer(employer_id):
    employer = Employees.query.get_or_404(employer_id)
    db.session.delete(employer)
    db.session.commit()
    return redirect(url_for("employees"))


@app.route("/projects")
def projects():
    projects = Projects.query.all()
    employees = Employees.query.all()
    departments = Departments.query.all()
    return render_template(
        "projects.html",
        name=session["user_name"],
        projects=projects,
        employees=employees,
        departments=departments,
    )


@app.route("/add-project", methods=["GET", "POST"])
def add_projects():
    projects = Projects.query.all()
    employees = Employees.query.all()
    departments = Departments.query.all()
    if request.method == "POST":
        name = request.form["name"]
        date = request.form["date"]
        description = request.form["description"]
        department = request.form["department"]

        new_project = Projects(
            name=name, date=date, description=description, department=department
        )

        try:
            db.session.add(new_project)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return redirect(url_for("projects"))

        return redirect(url_for("projects"))
    return render_template(
        "projects.html",
        name=session["user_name"],
        projects=projects,
        employees=employees,
        departments=departments,
    )


@app.route("/delete-project/<int:project_id>", methods=["POST"])
def delete_project(project_id):
    project = Projects.query.get_or_404(project_id)
    db.session.delete(project)
    db.session.commit()
    return redirect(url_for("projects"))


@app.route("/account")
def account():
    users = Users.query.all()
    return render_template(
        "account.html", name=session["user_name"], email=session["email"], users=users
    )


@app.route("/modify-account", methods=["POST"])
def modify_account():
    if "user_name" not in session:
        return redirect(url_for("login"))

    user = Users.query.filter_by(email=session["email"]).first()
    if not user:
        return redirect(url_for("login"))

    name = request.form.get("user_name")
    email = request.form.get("user_email")
    image = request.files.get("user_image")

    if name:
        user.name = name
        session["user_name"] = name
    if email:
        user.email = email
        session["email"] = email

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        image_path = f"uploads/{filename}"
        image.save(f"static/{image_path}")

        user.image = image_path
        session["user_image"] = image_path

    db.session.commit()
    return redirect(url_for("account"))


if __name__ == "__main__":
    app.run(debug=True)
