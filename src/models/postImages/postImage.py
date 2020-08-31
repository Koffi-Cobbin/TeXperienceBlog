__author__ = "Cobbin"
import requests
import re
import src.models.postImages.constants as imageConstants
from src.common.database import Database
import uuid
from src.models.blogs.blog import BlogPost

    
class PostImage(object):
    def __init__(self, image_filename, blog_id, author_id, image_data=None, _id=None):
        self._id = uuid.uuid4().hex if _id is None else _id
        self.image_filename = image_filename
        self.image_data = None if image_data is None else image_data
        self.blog_id = blog_id
        self.author_id = author_id
        

    def __repr__(self):
        return '< Image id={}, name={} >'.format(self._id, self.image_filename)
    
    def save_to_mongo(self):
        Database.update(imageConstants.COLLECTION, {"_id": self._id},  self.json())
        return self._id

    def json(self):
        return {
            "_id": self._id,
            "image_filename": self.image_filename,
            "image_data": self.image_data,
            "blog_id" : self.blog_id,
            "author_id": self.author_id
        }

    def from_mongo(self, query):
        Database.find_one("postImage", query)

    @classmethod
    def get_by_id(cls, image_id):
        return cls(**Database.find_one(imageConstants.COLLECTION, {"_id": image_id}))

    @classmethod
    def get_by_blog_id(cls, blog_id):
        return [cls(**elem) for elem in Database.find(imageConstants.COLLECTION, {'blog_id': blog_id})] 

    @classmethod
    def get_post_images(cls, query_name, other_id):
        return [cls(**elem) for elem in Database.find(imageConstants.COLLECTION, {f"{query_name}": other_id})] 

    def delete(self):
        Database.remove(imageConstants.COLLECTION, {'_id': self._id}) 
    
    @classmethod
    def delete_post_images(cls, query_name, other_id):
        img_lst = PostImage.get_post_images(query_name, other_id)
        for image in img_lst:
            image.delete()
        
