from config import create_app
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = create_app()

jwt = JWTManager(app)

from routes import routes_bp;
app.register_blueprint(routes_bp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
