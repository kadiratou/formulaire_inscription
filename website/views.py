from flask import Blueprint,render_template
from flask_login import login_required , current_user
from .models import Note
import json
from . import db



views = Blueprint('views', __name__)


@views.route('/',methods=["GET","POST"])
@login_required
def home():
  return render_template("home.html", user= current_user)




