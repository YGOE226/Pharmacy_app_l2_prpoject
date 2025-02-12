from flask import Flask

app = Flask(__name__)

# Configuration
app.config.from_object('config')

# Importer les routes
from app import routes
