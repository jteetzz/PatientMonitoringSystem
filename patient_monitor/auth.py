from functools import wraps

from flask import session, redirect, url_for, request

# Very simple demo user. For a real app you'd store users in a DB and hash passwords.
VALID_USER = {
    "username": "nurse",
    "password": "healthcare",
}


def check_credentials(username: str, password: str) -> bool:
    #Return True if the supplied credentials match the single demo user
    return username == VALID_USER["username"] and password == VALID_USER["password"]


def login_required(view_func):

    #Decorator to protect routes that require a logged-in user.
    #If not logged in, redirect to /login and include ?next=<original_path>
    #so we can send the user back after login.

    @wraps(view_func)
    def wrapped_view(*args, **kwargs):
        if not session.get("logged_in"):
            # `web.login` because the login view will live in the `web` blueprint
            return redirect(url_for("web.login", next=request.path))
        return view_func(*args, **kwargs)

    return wrapped_view
