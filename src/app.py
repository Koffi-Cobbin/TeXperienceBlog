__author__ = "Cobbin"
from flask import Flask, render_template, request, url_for, flash
import requests
from src.common.database import Database
from src.app_constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from src.models.blogs.blog import BlogPost
from src.models.postImages.postImage import PostImage
import src.models.alerts.constants as AlertConstants
from werkzeug.utils import redirect
import os
import smtplib, ssl
#---------------------------------------------------------------------------------------------

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = os.environ.get("SECRETE_KEY")
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
    """
        Using SMTP_SSL()
    """
    smtp_server = "smtp.gmail.com"
    sender_email = os.environ.get("SENDER_EMAIL") 
    receiver_email = os.environ.get("ADMINS_EMAIL")
    password = os.environ.get("PASSWORD")
    message = """\
    {}

    Hi there,
    A message from {}, {}. 
    {}.""".format(sender_email, name, email, content)

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    flash('Message Sent (:')
    return redirect(url_for('trending'))


from src.models.users.views import user_blueprint
from src.models.blogs.views import blog_blueprint
from src.models.comments.views import comment_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(blog_blueprint, url_prefix="/blogs")
app.register_blueprint(comment_blueprint, url_prefix="/comments")
