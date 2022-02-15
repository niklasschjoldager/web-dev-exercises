from bottle import get, view
from g import USERS

############################################################
@get("/users")
@view("users")
def _():
    return dict(users=USERS)
