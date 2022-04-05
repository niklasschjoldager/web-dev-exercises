from bottle import default_app, get, post, redirect, request, run, view, static_file
import os
import uuid
import imghdr

from g import APP_FOLDER_ABSOLUTE_PATH, IMAGE_FOLDER_ABSOLUTE_PATH, IMAGE_FOLDER_RELATIVE_PATH

############################################################
@get("/app.css")
def _():
    return static_file("app.css", root=APP_FOLDER_ABSOLUTE_PATH)


############################################################
@get("/images/<filepath:path>")
def server_static(filepath):
    return static_file(filepath, root=IMAGE_FOLDER_ABSOLUTE_PATH)


############################################################
@get("/")
@view("index")
def _():
    return


############################################################
@get("/about-us")
@view("about-us")
def _():
    return


############################################################
@get("/contact-us")
@view("contact-us")
def _():
    return


############################################################
@get("/gallery")
@view("gallery")
def _():
    images = os.listdir(IMAGE_FOLDER_ABSOLUTE_PATH)
    return dict(images=images)


############################################################
@get("/thank-you")
@view("thank-you")
def _():
    image_url = request.params.get("image-url")

    return dict(image_url=image_url)


############################################################
@post("/upload-image")
def _():
    image = request.files.get("my_image")

    # Get image extension woody-kelly.png
    file_name, file_extension = os.path.splitext(image.filename)  # .png .jpeg, .jpg

    # Validate image extension
    if file_extension not in (".png", ".jpeg", ".jpg"):
        return "Image not allowed"

    # Convert old .jpg extension to .jpeg, so it pass imghdr.what validation
    if file_extension == ".jpg":
        file_extension = ".jpeg"

    image_id = str(uuid.uuid4())
    # 4333343-434356-46564543534.png
    image_name = f"{image_id}{file_extension}"
    image_url = f"{IMAGE_FOLDER_ABSOLUTE_PATH}/{image_name}"

    # Save the image
    image.save(image_url)

    validated_file_extension = imghdr.what(image_url)

    # Make sure that the image is actually a valid image
    # by reading its mime type
    if file_extension != f".{validated_file_extension}":
        # Remove the invalid image from the folder
        os.remove(image_url)
        return "Hmm... got you! It was not an image"

    return redirect(f"/thank-you?image-url=images/{image_name}")


############################################################
try:
    # Production
    import production

    application = default_app()
except:
    # Development
    run(host="127.0.0.1", port=3333, debug=True, reloader=True)
