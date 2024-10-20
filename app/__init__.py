from flask import Flask
from dotenv import load_dotenv
import os

#Variables de entorno
load_dotenv()

app = Flask(__name__)

from .routes import*