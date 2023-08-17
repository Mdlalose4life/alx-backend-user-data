#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'bob@bob.com'
password = 'MyPwdOfBob'
auth = Auth()

auth.register_user(email, password)

print(auth.create_session(email))
print(auth.create_session("unknown@email.com"))

@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    This methods responds to GET /profile
    """
    # Let's get the session ID
    session_id = request.cookies.get("session_id")
    # find a user by session ID
    user = AUTH.get_user_from_session_id("session_id")
    # if the user or session id does not exist respond with 403.
    if user is None:
        abort(403)
    # if the user exists, respond with 200 status
    return jsonify({"email": user.email})
