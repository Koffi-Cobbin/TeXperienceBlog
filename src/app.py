__author__ = "Cobbin"
from flask import Flask, render_template, request, url_for, flash
import requests
from common.database import Database
from app_constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from models.blogs.blog import BlogPost
from models.postImages.postImage import PostImage
import models.alerts.constants as AlertConstants
from werkzeug.utils import redirect
#---------------------------------------------------------------------------------------------

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "1234"
#----------------------------------------------
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#---------------------------------------------------

@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trending', methods=['GET'])
def trending():
    all_posts = BlogPost.all()
    all_post_images = []        # This returns a list of lists
    post_indexes = []
    for idx,post in enumerate(all_posts):
        try:
            if post.post_images:
                post_images = [PostImage.get_by_id(image_id).image_data.decode('utf-8') for image_id in post.post_images] # current_user.profile_image.decode('utf-8')
                all_post_images.append(post_images) 
                post_indexes.append(idx)
        except:
            post_images =[]
    all_posts.reverse()
    return render_template('trendingposts.html', posts = all_posts, post_images=all_post_images, post_indexes=post_indexes, posts_length=len(all_posts), indexes_length=len(post_indexes))

@app.route('/help')
def help():
    return render_template('help.html')

def send(name, email, content):
    return requests.post(
        AlertConstants.URL,
        auth = ("api", AlertConstants.API_KEY),
        data = {
            "from": AlertConstants.FROM,
            "to": AlertConstants.ADMINS_EMAIL,
            "subject": "Email from {}, {}.".format(name, email),
            "text": "{}".format(content)
        }
    )

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    content = request.form['content']
    send(name, email, content)
    flash('Message Sent (:')
    return redirect(url_for('trending'))


from models.users.views import user_blueprint
from models.blogs.views import blog_blueprint
from models.comments.views import comment_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(blog_blueprint, url_prefix="/blogs")
app.register_blueprint(comment_blueprint, url_prefix="/comments")
