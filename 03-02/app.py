from bottle import run, get, request, response, post, delete
import json, uuid  # 1 billion per second will take 100 years to get 50%

items = [{"id": "1", "name": "a"}, {"id": "2", "name": "b"}, {"id": "3", "name": "c"}]

##########################################################################
# decorator
@get("/")
def _():
    return "home"


##########################################################################
@get("/items")
# @get("/items/")
def _():
    return json.dumps(items)


##########################################################################
# Query strings
# every other varible after the 1st one starts with &
# 127.0.0.1:4444/test?id=1&name=a
@get("/test")
def _():
    school_name = request.params.get("school-name")
    year = request.params.get("year")
    age = request.params.get("age")
    return f"Hi, you are at {school_name}. The year is {year} and you are {age} years old"


##########################################################################
# 127.0.0.1:4444/friendly/brand/xxx/color/xxx
@get("/friendly/brand/<brand_name>/color/<item_color>")
def _(brand_name, item_color):
    return f"You want for brand: {brand_name} color is: {item_color}"
    # You want for brand xxx and the color is: xxx


##########################################################################
@post("/items")
def _():
    item_name = request.forms.get("item_name")

    # Validation
    if not item_name:
        response.status = 400
        return "item_name is missing"
    if len(item_name) < 2:
        response.status = 400
        return "item_name must be at least 2 characters"
    if len(item_name) > 20:
        response.status = 400
        return "item_name must be 20 characters or less"

    item_id = str(uuid.uuid4())
    item_price = request.forms.get("item_price")
    item = {"id": item_id, "name": item_name, "price": item_price}
    items.append(item)

    # print("#"*30)
    # print(type(item_id))

    return item_id


##########################################################################
@get("/items/<item_id>")
def _(item_id):

    # Validation
    if not item_id:
        response.status = 400
        return "item_id is missing"

    # {"id":"1", "name":"a"},
    for item in items:
        if item["id"] == item_id:
            return item

    response.status = 400
    return "Item not found"


##########################################################################
@delete("/items/<item_id>")
def _(item_id):
    # Validation
    for index, item in enumerate(items):
        if item["id"] == item_id:
            items.pop(index)
            return "Item deleted"

    # No item found
    return "Item not found"


##########################################################################
# Port from 0 to 65535
# Reserved from 0 to 1024
run(host="127.0.0.1", port=4444, debug=True, reloader=True)
