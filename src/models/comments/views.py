from flask import Blueprint, request, session, url_for, render_template
from werkzeug.utils import redirect
from src.models.comments.comment import Comment
from src.models.users.user import User
import src.models.users.decorators as user_decorators

comment_blueprint = Blueprint('comments', __name__)

@comment_blueprint.route('/comment/<string:blog_id>', methods = ['POST'])
@user_decorators.requires_login
def new_comment(blog_id):
    user = User.find_by_email(session['email'])
    content = request.form['content']
    Comment(content=content, user_id=user._id, blog_id=blog_id, author_id=user.author_id).save_to_mongo()
    return redirect(url_for('blogs.readmore', post_id=blog_id)) 
