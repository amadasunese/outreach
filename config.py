import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///students.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://gpimamagementsys:Gentle&&08058767059@gpimamagementsystem.mysql.pythonanywhere-services.com/gpimamagementsys$default"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


