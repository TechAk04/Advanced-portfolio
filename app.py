from flask import Flask, request, send_from_directory, redirect
from pathlib import Path
import os
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
# Load .env reliably from the application directory
load_dotenv(BASE_DIR / ".env")

app = Flask(__name__)

# Limit the amount of data accepted in one request (16KB)
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024


@app.get("/")
@app.get("/index.html")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/about.html")
def about():
    return send_from_directory(BASE_DIR, "about.html")


@app.get("/projects.html")
def projects():
    return send_from_directory(BASE_DIR, "projects.html")


@app.get("/contact.html")
def contact_page():
    return send_from_directory(BASE_DIR, "contact.html")


@app.get("/style.css")
def stylesheet():
    return send_from_directory(BASE_DIR, "style.css")


@app.get("/nav.js")
def javascript():
    return send_from_directory(BASE_DIR, "nav.js")


@app.get("/images/<path:filename>")
def images(filename):
    return send_from_directory(BASE_DIR / "images", filename)


@app.get("/ashish.jpg")
def root_photo():
    return send_from_directory(BASE_DIR / "images", "ashish.jpg")


@app.post("/contact")
def receive_message():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    message = request.form.get("message", "").strip()

    if not name or not email or not message:
        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Validation Error | Ashish's Portfolio</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <main class="container main-content">
    <section class="card contact-section-inner" style="text-align: center;">
      <h2 class="section-title">Validation Error</h2>
      <p>Please fill in all required fields (Name, Email, and Message).</p>
      <div class="btn-group" style="justify-content: center;">
        <a href="/contact.html" class="btn btn-primary">Return to Contact</a>
      </div>
    </section>
  </main>
</body>
</html>""", 400

    if len(name) > 100 or len(email) > 254 or len(message) > 5000:
        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Submission Error | Ashish's Portfolio</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <main class="container main-content">
    <section class="card contact-section-inner" style="text-align: center;">
      <h2 class="section-title">Submission Error</h2>
      <p>One or more fields exceed the allowed character limit.</p>
      <div class="btn-group" style="justify-content: center;">
        <a href="/contact.html" class="btn btn-primary">Return to Contact</a>
      </div>
    </section>
  </main>
</body>
</html>""", 400

    sender = os.getenv("SMTP_EMAIL")
    app_password = os.getenv("SMTP_APP_PASSWORD")
    receiver = os.getenv("CONTACT_RECEIVER")

    if not sender or not app_password or not receiver:
        app.logger.warning("Missing SMTP environment variables in .env")
        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Configuration Notice | Ashish's Portfolio</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <main class="container main-content">
    <section class="card contact-section-inner" style="text-align: center;">
      <h2 class="section-title">Service Notice</h2>
      <p>Email settings are not configured in .env. Please check your SMTP configuration.</p>
      <div class="btn-group" style="justify-content: center;">
        <a href="/contact.html" class="btn btn-primary">Return to Contact</a>
      </div>
    </section>
  </main>
</body>
</html>""", 500

    email_message = EmailMessage()
    email_message["Subject"] = "New message from your portfolio"
    email_message["From"] = sender
    email_message["To"] = receiver
    email_message["Reply-To"] = email

    email_message.set_content(
        f"Name: {name}\n"
        f"Email: {email}\n\n"
        f"Message:\n{message}"
    )

    try:
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(
            "smtp.gmail.com", 465,
            context=context, timeout=15
        ) as smtp:
            smtp.login(sender, app_password)
            smtp.send_message(email_message)

        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Message Sent | Ashish's Portfolio</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <main class="container main-content">
    <section class="card contact-section-inner" style="text-align: center;">
      <h2 class="section-title">Message Sent Successfully!</h2>
      <p>Thank you for getting in touch. I will reply to you as soon as possible.</p>
      <div class="btn-group" style="justify-content: center;">
        <a href="/contact.html" class="btn btn-primary">Return to Contact</a>
        <a href="/index.html" class="btn btn-secondary">Back to Home</a>
      </div>
    </section>
  </main>
</body>
</html>""", 200

    except (OSError, smtplib.SMTPException) as error:
        app.logger.error("Email delivery failed: %s", type(error).__name__)
        return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Delivery Notice | Ashish's Portfolio</title>
  <link rel="stylesheet" href="/style.css">
</head>
<body>
  <main class="container main-content">
    <section class="card contact-section-inner" style="text-align: center;">
      <h2 class="section-title">Delivery Status</h2>
      <p>Email delivery service is currently unavailable or network-restricted. Please reach out directly or try again later.</p>
      <div class="btn-group" style="justify-content: center;">
        <a href="/contact.html" class="btn btn-primary">Return to Contact</a>
        <a href="/index.html" class="btn btn-secondary">Back to Home</a>
      </div>
    </section>
  </main>
</body>
</html>""", 500


if __name__ == "__main__":
    app.run(debug=True)
