from bottle import error, get, run, static_file, view

############################################################
# GET
import index_get
import items_get
import login_get
import signup_get
import users_get

# POST
import add_item_post
import delete_item_post
import signup_post


############################################################
@get("/app.css")
def _():
    return static_file("app.css", root=".")


############################################################
@error(404)
@view("404")
def _(error):
    print(error)
    return


run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")
