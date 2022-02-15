from bottle import redirect, request, post
from g import ITEMS

############################################################
@post("/delete-item")
def _():
    # VALIDATION
    item_id = request.forms.get("item_id")

    # Delete item if exist
    for index, item in enumerate(ITEMS):
        if item["id"] == item_id:
            ITEMS.pop(index)
            return redirect("/items")

    return redirect("/items")
