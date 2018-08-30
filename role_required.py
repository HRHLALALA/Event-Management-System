from flask import redirect, url_for,flash
from route import current_user
from functools import wraps

def trainer_only(f):
    """This is used to check the admin status of the user"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = current_user
        if current_user.role =="trainee":
            flash("Don't think about it!!!!")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

