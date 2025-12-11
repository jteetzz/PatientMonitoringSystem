# auth.py
# Minimal demo role-based auth for the project.  Intended for educational/demo use only.
from functools import wraps
from flask import request, jsonify

# Demo token->role mapping (replace with real auth in production).
# Students should document this and replace with proper auth + secure storage.
TOKENS = {
    "nurse-token": "nurse",
    "admin-token": "admin"
}

def get_role_from_request():
    # Look for a demo token in X-Auth-Token or Authorization header (Bearer)
    token = request.headers.get("X-Auth-Token") or request.headers.get("Authorization")
    if not token:
        return None
    if token.startswith("Bearer "):
        token = token.split(" ", 1)[1]
    return TOKENS.get(token)

def require_role(min_role: str):
    """
    Decorator to require at least the given role.
    Roles (simple hierarchy): admin > nurse
    """
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            role = get_role_from_request()
            if not role:
                return jsonify({"error": "unauthorized"}), 401
            # simple role hierarchy
            allowed = False
            if min_role == "nurse":
                allowed = role in ("nurse", "admin")
            elif min_role == "admin":
                allowed = role == "admin"
            else:
                allowed = role == min_role
            if not allowed:
                return jsonify({"error": "forbidden"}), 403
            return f(*args, **kwargs)
        return wrapped
    return decorator
