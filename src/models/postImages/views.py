__author__ = "Cobbin"

from flask import Blueprint

postImage_blueprint = Blueprint('postImages', __name__)


@item_blueprint.route('/postImage/<string:name>')
def item_page(name):
    pass

