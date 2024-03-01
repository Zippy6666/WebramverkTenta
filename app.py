from flask import Flask
from models import db, seedData, user_datastore
from flask_migrate import Migrate, upgrade
from flask import  render_template
from flask_security import Security

app = Flask(__name__)
app.config.from_object('config.ConfigDebug')

db.app = app
db.init_app(app)
migrate = Migrate(app,db)

security = Security(app, user_datastore)

@app.route("/", methods=["GET"])
def startSida():
    return render_template('startsida.html')




if __name__  == "__main__":
    with app.app_context():
        upgrade()
        seedData()
    app.run()


