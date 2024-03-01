from flask import Flask
from models import db, seedData, user_datastore, ContactSubmission, Product
from flask_migrate import Migrate, upgrade
from flask import  render_template, request, redirect, url_for
from flask_security import Security

app = Flask(__name__)
app.config.from_object('config.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app,db)

security = Security(app, user_datastore)



def validate_text_input(text:str) -> bool:
    if not isinstance(text, str):
        return False
    
    # It's a string, but empty
    if len(text) == 0:
        return False
    
    return True # Valid


def post_contact( data:dict ) -> None:
    email = request.form.get("email")
    tel = request.form.get("phone")

    if not (validate_text_input(email) or validate_text_input(tel)):
        data["message"] = "Du måste fylla i antingen email eller telefon!"
        return False

    try:
        name = request.form.get("name")
        subject = request.form.get("subject")
        text = request.form.get("text")

        contact_submit = ContactSubmission(name=name, subject=subject, text=text, email=email, phone=tel)
        db.session.add(contact_submit)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)
        data["message"] = "Ett fel uppstod, försök igen senare!"
        return False
    else:
        return True


@app.route("/", methods=["GET"])
def startSida() -> str:
    return render_template('startsida.html')


@app.route("/products", methods=["GET"])
def products():
    return render_template("products.html", products_table=Product.query.all())


@app.route("/contact_sucess", methods=["GET"])
def contact_thank_you():
    return render_template("contactUsSucess.html")


@app.route("/contact", methods=["GET", "POST"])
def contact_us() -> str:
    data = dict()

    contacted = False

    if request.method == "POST":
        contacted = post_contact( data )

    if contacted:
        return redirect(url_for("contact_thank_you"))
    else:
        return render_template("contactUs.html", **data)




if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData()
    app.run()


