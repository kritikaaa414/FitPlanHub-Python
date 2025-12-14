from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from auth import auth_bp
from plans import plans_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "secret123"

CORS(app)
JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(plans_bp)

@app.route("/")
def home():
    return "FitPlanHub Backend Running"

if __name__ == "__main__":
    app.run(debug=True)
