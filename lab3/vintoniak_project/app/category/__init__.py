from flask import Blueprint
from .models import Category

category = Blueprint("category", __name__, template_folder="templates/category")