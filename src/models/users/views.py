__author__ = "Cobbin"

from flask import Blueprint, request, session, url_for, flash, render_template
from werkzeug.utils import redirect
from src.models.users.user import User
import src.models.users.errors as UserErrors
import src.models.users.decorators as user_decorators
from src.models.blogs.blog import BlogPost
from src.models.postImages.postImage import PostImage
from src.models.comments.comment import Comment
#------------------------------------------------
from src.app_constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, allowed_file
from werkzeug.utils import secure_filename
from PIL import Image
import base64, os, io
import tempfile

user_blueprint = Blueprint('users', __name__)

@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        # Check if login is valid
        # Send user an error message if login ids invalid
        email = request.form['email']
        password = request.form['password']
        # this try part catches errors and displays them in a user 
        # friendly way. 
        try:
            if User.is_login_valid(email, password):
                session['email'] = email
                return redirect(url_for('users.profile'))
        except UserErrors.UserError as e:
            flash('{}'.format(e.message))
            return render_template("users/login.html")
    return render_template("users/login.html")


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Check if login is valid
        # Send user an error message if login ids invalid
        name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # this try part catches errors and displays them in a user 
        # friendly way. 
        try:
            if User.register_user(name, email, password):
                session['email'] = email
                return redirect(url_for('users.profile'))
        except UserErrors.UserError as e:
            flash('{}'.format(e.message))
            return render_template("users/signup.html")
    return render_template("users/signup.html")


# The profile page section 
@user_blueprint.route('/profile')
@user_decorators.requires_login
def profile():
    user = User.find_by_email(session['email'])
    all_posts = BlogPost.get_author_posts(user.author_id)
    all_posts.reverse()
    try:
        if user.profile_image:
            profile_img = user.profile_image.decode('utf-8')
        else:
            profile_img = None
    except:
        profile_img = None
    return render_template('users/profile.html', user = user, profile_image=profile_img, posts=all_posts)

@user_blueprint.route('/edit_profile', methods=['POST', 'GET'])
@user_decorators.requires_login
def edit_profile():
    user = User.find_by_email(session['email'])
    name = user.name
    email = user.email
    if request.method == 'POST':
        image = request.files['image_file']
        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            
            with tempfile.TemporaryDirectory() as tmpdirname:
                #print('created temporary directory', tmpdirname)
                path = os.path.join(tmpdirname, image_filename)
                image.save(path)
                with open(path, 'rb') as img:
                    encoded_image = base64.b64encode(img.read())
                    user.profile_image = encoded_image 
                    
        user.name = request.form['name']
        user.email = request.form['email']
        user.save_to_db()
        return redirect(url_for('.profile'))
    return render_template('users/edit_profile.html', name=name, email=email)
                                            
            
                                            
@user_blueprint.route('/logout')
def logout_user():
    session['email'] = None
    return render_template('index.html')

# The Delete User section
@user_blueprint.route('/delete_user/<string:author_id>')
@user_decorators.requires_login
def delete_user(author_id): 
    BlogPost.delete_author_posts(author_id)
    PostImage.delete_post_images("author_id", author_id)
    Comment.delete_post_comments("author_id", author_id)
    User.find_by_email(session['email']).delete()
    session['email'] = None
    return render_template('index.html')

@user_blueprint.route('/help')
def help():
    return render_template('users/help.html')

@user_blueprint.route("/user_posts/<string:author_id>", methods = ['GET'])
@user_decorators.requires_login
def user_posts(author_id):
    user = User.find_by_email(session['email'])
    all_posts = BlogPost.get_author_posts(author_id)
    return render_template('blogs/posts.html', posts = all_posts, user=user)

#==============================================================================================
@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    user = User.find_by_email(session['email'])
    alerts = user.get_alerts()
    return render_template('users/alerts.html', alerts=alerts)

@user_blueprint.route('/all', methods=['GET'])
@user_decorators.requires_login
def all_users():
    details = User.all()
    return render_template('users/users.html', details=details)
