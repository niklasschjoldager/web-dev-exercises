from bottle import get, post, request, response, run
import os
import uuid
import imghdr

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from password import gmail_password

##############################
@get("/send-email")
def _():

    sender_email = "mycoolkeamail@gmail.com"
    receiver_email = "mycoolkeamail@gmail.com"
    password = gmail_password

    message = MIMEMultipart("alternative")
    message["Subject"] = "My cool mail sent from Python"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
  Hi,
  Thank you.
  """

    html = """\
  <html>
    <body>
      <p>
        Hi,<br>
        <b>How are you?</b><br>
      </p>
    </body>
  </html>
  """

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            return "yes, email sent"
        except Exception as ex:
            print("ex")
            return "uppps... could not send the email"


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

    # Save the image
    image.save(f"images/{image_name}")

    validated_file_extension = imghdr.what(f"images/{image_name}")

    print("imghdr", imghdr.what(f"images/{image_name}"))
    print("file_extension", file_extension)

    # Make sure that the image is actually a valid image
    # by reading its mime type
    if file_extension != f".{validated_file_extension}":
        print("Hmmm... suspicious it is not a real image")
        # Remove the invalid image from the folder
        os.remove(f"images/{image_name}")
        return "Hmm... got you! It was not an image"

    return "yes"


############################################################
run(host="127.0.0.1", port=3333, debug=True, reloader=True, server="paste")
