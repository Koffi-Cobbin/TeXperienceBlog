__author__ = "Cobbin"

from flask import session, url_for, redirect, request
from functools import wraps

def requires_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path)) # This allows the user to login and access the restricted path he wanted to access
        return func(*args, **kwargs)
    return decorated_function 


def requires_admin_permission(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in app.config['ADMINS']:
             return redirect(url_for('users.login_user'))
        return func(*args, **kwargs)
    return decorated_function 