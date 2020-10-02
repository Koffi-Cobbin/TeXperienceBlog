__author__ = "Cobbin"

from flask import Blueprint, render_template, redirect, request, url_for, session
from src.models.blogs.blog import BlogPost
from src.models.users.user import User
from src.models.comments.comment import Comment
from src.models.postImages.postImage import PostImage
import src.models.users.decorators as User_decorators
import json
#--------------------------------------------------
from src.app_constants import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, allowed_file
from werkzeug.utils import secure_filename
import base64, os
import tempfile


blog_blueprint = Blueprint('blogs', __name__)

@blog_blueprint.route('/blog/<string:blog_id>')
def blog_page(blog_id):
    return render_template('blogs/blog.html', blog=BlogPost.get_by_id(blog_id))


@blog_blueprint.route('/posts/new/<string:id>', methods = ['GET', 'POST'])
@User_decorators.requires_login
def new_post(id):
    user = User.find_by_id(id)
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']
        category = request.form['category']
        new_post_id = BlogPost(title, content, author, user.author_id, category).save_to_mongo() 
        image = request.files['image_file']
        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            
            with tempfile.TemporaryDirectory() as tmpdirname:
                path = os.path.join(tmpdirname, image_filename)
                image.save(path)
                with open(path, 'rb') as img:
                    encoded_image = base64.b64encode(img.read())
                    user.profile_image = encoded_image
                    post_image_id = PostImage(image_filename, new_post_id, user.author_id, encoded_image).save_to_mongo()  
                    post = BlogPost.get_by_id(new_post_id)
                    post.post_images.append(post_image_id)
                    post.save_to_mongo()
                
        return redirect(url_for('users.user_posts', author_id = user.author_id))  
    return render_template("blogs/new_post.html", user=user)


@blog_blueprint.route('/posts/editpost/<string:id>', methods = ['GET', 'POST'])
@User_decorators.requires_login
def editpost(id):
    blog_post = BlogPost.get_by_id(id)
    if request.method == 'POST':
        blog_post.title = request.form['title']
        blog_post.author = request.form['author']
        blog_post.content = request.form['content']
        
        image = request.files['image_file']
        if image and allowed_file(image.filename):
            image_filename = secure_filename(image.filename)
            with tempfile.TemporaryDirectory() as tmpdirname:
                path = os.path.join(tmpdirname, image_filename)
                image.save(path)
                with open(path, 'rb') as img:
                    encoded_image = base64.b64encode(img.read())
                    post_image_id = PostImage(image_filename, blog_post._id, blog_post.author_id, encoded_image).save_to_mongo()  
                    if blog_post.post_images is not None:
                        try:
                            print(PostImage.get_by_id(blog_post.post_images[0]))
                            
                        except:
                            pass
                        blog_post.post_images.pop() 
                    blog_post.post_images.append(post_image_id)
        
        blog_post.save_to_mongo()
        return redirect(url_for('users.user_posts', author_id = blog_post.author_id))
    return render_template('blogs/editpost.html', post = blog_post)

@blog_blueprint.route('/posts/delete/<string:id>')
@User_decorators.requires_login
def delete(id):
    user = User.find_by_email(session['email'])
    BlogPost.get_by_id(id).delete()
    return redirect(url_for('users.user_posts', author_id = user.author_id))

@blog_blueprint.route('/trending', methods = ['GET'])
def trending():
    all_posts = BlogPost.all()
    all_post_images = []        # This returns a list of lists
    post_indexes = []
    for idx,post in enumerate(all_posts):
        if post.post_images:
            post_images = [image.image_data.decode('utf-8') for image in post.post_images] # current_user.profile_image.decode('utf-8')
            all_post_images.append(post_images) 
            post_indexes.append(idx)
    post_indexes.reverse()
    post_indexes.reverse()
    return render_template('trendingposts.html', posts = all_posts, post_images=all_post_images, post_indexes=post_indexes, posts_length=len(all_posts), indexes_length=len(post_indexes))
 
@blog_blueprint.route('/readmore/<string:post_id>', methods = ['GET', 'POST'])
def readmore(post_id):
    post = BlogPost.get_by_id(post_id)
    try:
        if request.method == 'post':
            return render_template('readmore.html', post=post)
        if post.post_images:
            post_image = [image.image_data.decode('utf-8') for image in post.post_images]
        else:
            post_image = []
    except:
        post_image = []
    comments =  Comment.get_by_blog_id(post_id)  # This returns a list
    users = [User.find_by_id(comment.user_id) for comment in comments]
    total_comments = len(comments)
    return render_template('readmore.html', post=post, post_image=post_image, comments=comments, total_comments=total_comments, users=users)

@blog_blueprint.route('/like_post/<string:post_id>')
def like_post(post_id):
    post = BlogPost.get_by_id(post_id)
    already_liked =[0]
    if already_liked[0] == 0:
        already_liked.pop()
        post.likes.append(post.likes.pop()+1)
        post.save_to_mongo()
    already_liked.append(1)   
    return redirect(url_for('.readmore', post_id=post._id)) 
