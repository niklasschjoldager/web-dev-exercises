from bottle import get, view
from g import ITEMS

############################################################
@get("/items")
@view("items")
def _():
    return dict(items=ITEMS)
