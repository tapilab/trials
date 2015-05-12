from flask import Flask

from trialsearcher import TrialSearcher
searcher = TrialSearcher()

app = Flask(__name__)
from app import views



