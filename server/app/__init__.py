"""
Top level of BQ manager
"""
import logging
from flask import Flask
from bq_manager.projects import blueprint as projects_blueprint


logging.getLogger().setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)


app = Flask(__name__)
app.register_blueprint(projects_blueprint)
