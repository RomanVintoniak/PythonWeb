from flask import Blueprint
from .models import Post

post = Blueprint("post", __name__, template_folder="templates/post", \
                static_folder='static',  static_url_path='/post')