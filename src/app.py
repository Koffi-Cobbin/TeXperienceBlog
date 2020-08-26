__author__ = "Cobbin"
from flask import Flask, render_template
from common.database import Database
from app_constants import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from models.blogs.blog import BlogPost
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
                post_images = [image.image_data.decode('utf-8') for image in post.post_images] # current_user.profile_image.decode('utf-8')
                all_post_images.append(post_images) 
                post_indexes.append(idx)
        except:
            post_images =[]
    post_indexes.reverse()
    post_indexes.reverse()
    return render_template('trendingposts.html', posts = all_posts, post_images=all_post_images, post_indexes=post_indexes, posts_length=len(all_posts), indexes_length=len(post_indexes))

@app.route('/help')
def help():
    return render_template('help.html')


from models.users.views import user_blueprint
from models.blogs.views import blog_blueprint
from models.comments.views import comment_blueprint
app.register_blueprint(user_blueprint, url_prefix="/users")
app.register_blueprint(blog_blueprint, url_prefix="/blogs")
app.register_blueprint(comment_blueprint, url_prefix="/comments")

