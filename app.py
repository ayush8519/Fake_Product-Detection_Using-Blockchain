"""
app.py  –  Fake Product Identification using Blockchain
Flask web application
"""

import os
from flask import (Flask, render_template, request, redirect,
                   url_for, session, flash)
from werkzeug.utils import secure_filename

import blockchain
from signature_utils import generate_signature

# ----------------------------------------------------------------
app = Flask(__name__)
app.secret_key = "blockchain_secret_key_2024"

UPLOAD_FOLDER = os.path.join("static", "uploads")
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ----------------------------------------------------------------
# HELPERS
# ----------------------------------------------------------------

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_uploaded_file(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(path)
        return path
    return None


# ================================================================
# PUBLIC ROUTES
# ================================================================

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


# ----------------------------------------------------------------
# ADMIN
# ----------------------------------------------------------------

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        uname = request.form.get("username", "")
        pwd   = request.form.get("password", "")
        if uname == "admin" and pwd == "admin":
            session["admin"] = True
            return redirect(url_for("admin_home"))
        flash("Invalid admin credentials.", "danger")
    return render_template("admin_login.html")


@app.route("/admin_home")
def admin_home():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    return render_template("admin_home.html")


@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    message = None
    product_id = None
    signature  = None

    if request.method == "POST":
        product_name  = request.form.get("productName", "")
        product_desc  = request.form.get("productDesc", "")
        product_price = request.form.get("productPrice", "")
        barcode_file  = request.files.get("barcodeImage")

        path = save_uploaded_file(barcode_file)
        if not path:
            flash("Please upload a valid barcode image.", "warning")
            return render_template("add_product.html")

        # Generate digital signature from barcode
        signature = generate_signature(path)

        # Store on Blockchain
        product_id = blockchain.add_product(product_name, product_desc,
                                            product_price, signature)
        message = (f"Product added to Blockchain! "
                   f"Product ID: {product_id} | Signature: {signature}")

    return render_template("add_product.html", message=message,
                           product_id=product_id, signature=signature)


@app.route("/view_products")
def view_products():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    products = blockchain.get_all_products()
    return render_template("view_products.html", products=products)


@app.route("/view_users")
def view_users():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    users = blockchain.get_all_users()
    return render_template("view_users.html", users=users)


@app.route("/admin_logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("index"))


# ----------------------------------------------------------------
# USER
# ----------------------------------------------------------------

@app.route("/user_signup", methods=["GET", "POST"])
def user_signup():
    message = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        email    = request.form.get("email", "")
        contact  = request.form.get("contact", "")

        blockchain.add_user(username, password, email, contact)
        message = "Signup successful! You can now login."
    return render_template("user_signup.html", message=message)


@app.route("/user_login", methods=["GET", "POST"])
def user_login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        user = blockchain.login_user(username, password)
        if user:
            session["user"] = user
            return redirect(url_for("user_home"))
        flash("Invalid credentials.", "danger")
    return render_template("user_login.html")


@app.route("/user_home")
def user_home():
    if not session.get("user"):
        return redirect(url_for("user_login"))
    return render_template("user_home.html", user=session["user"])


@app.route("/retrieve_product", methods=["GET", "POST"])
def retrieve_product():
    if not session.get("user"):
        return redirect(url_for("user_login"))

    product = None
    if request.method == "POST":
        product_id = request.form.get("productId", "")
        product = blockchain.get_product(product_id)
        if not product:
            flash(f"No product found with ID: {product_id}", "warning")

    return render_template("retrieve_product.html", product=product)


@app.route("/authenticate_scan", methods=["GET", "POST"])
def authenticate_scan():
    if not session.get("user"):
        return redirect(url_for("user_login"))

    result   = None
    product  = None
    signature = None

    if request.method == "POST":
        product_id   = request.form.get("productId", "")
        barcode_file = request.files.get("barcodeImage")

        path = save_uploaded_file(barcode_file)
        if not path:
            flash("Please upload a valid barcode image.", "warning")
            return render_template("authenticate_scan.html")

        # Generate signature from uploaded barcode
        signature = generate_signature(path)

        # Authenticate against Blockchain
        is_authentic = blockchain.authenticate_barcode(product_id, signature)

        if is_authentic:
            product = blockchain.get_product(product_id)
            result  = "AUTHENTIC"
        else:
            result = "FAKE"

    return render_template("authenticate_scan.html",
                           result=result, product=product, signature=signature)


@app.route("/user_logout")
def user_logout():
    session.pop("user", None)
    return redirect(url_for("index"))


# ----------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
