from flask import Flask  
from flask_cors import CORS  
from app.routes.auth_routes import auth_routes
from app.routes.event_routes import event_routes
from app.routes.user_routes import user_routes
from app.database import db 
from config import Config  

app = Flask(__name__)  
app.config.from_object(Config)  
CORS(app, supports_credentials=True, origins="*")

db.init_app(app)
with app.app_context():
    db.create_all()  

app.register_blueprint(auth_routes, url_prefix='/api/v1/auth')
app.register_blueprint(event_routes, url_prefix='/api/v1/events')
app.register_blueprint(user_routes, url_prefix='/api/v1/users')

@app.route("/")  
def home():  
    return {"message": "Flask API is running!"}  


if __name__ == "__main__":  
    app.run(debug=True)