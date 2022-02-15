from bottle import post, redirect, request
from g import USERS
import uuid

############################################################
@post("/signup")
def _():
    user_name = request.forms.get("user_name")
    user_email = request.forms.get("user_email")
    user_id = str(uuid.uuid4())

    user = {"name": user_name, "email": user_email, "id": user_id}
    USERS.append(user)

    redirect("/users")
