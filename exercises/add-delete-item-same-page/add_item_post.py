from bottle import post, request
import uuid
from g import ITEMS

###########################################################
@post("/add-item")
def _():
    item_name = request.forms.get("item_name")
    item_price = request.forms.get("item_price")

    # VALIDATION
    if not item_name:
        response.status = 400
        return "Item name is missing"

    if not item_price:
        response.status = 400
        return "Item price is missing"

    item_id = str(uuid.uuid4())
    item = {"id": item_id, "name": item_name, "price": item_price}
    ITEMS.append(item)

    return f"{item_name} added to items"
