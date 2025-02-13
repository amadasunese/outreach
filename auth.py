from functools import wraps
from flask import abort, flash, redirect, url_for, render_template
from flask_login import current_user

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to log in first.", "warning")
            return redirect(url_for("auth.login"))
        
        if not getattr(current_user, "is_admin", False):
            flash("You do not have permission to access this page.", "danger")
            return render_template("403.html"), 403  # Redirect to custom error page

        return f(*args, **kwargs)
    
    return decorated_function
