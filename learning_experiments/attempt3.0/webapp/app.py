import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
# Importerer din eksisterende backend
from inventory_service import get_inventory, new_item, update_item, change_stock, search_item

app = Flask(__name__)
app.secret_key = "endre_denne_til_noe_hemmelig"  # Nødvendig for session/login

# Konfigurer opplasting av bilder
UPLOAD_FOLDER = os.path.join('webapp', 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- HJELPEFUNKSJONER ---
def is_admin():
    return session.get("role") == "admin"

def is_logged_in():
    return "role" in session

# --- RUTER (ROUTES) ---

@app.route("/")
def index():
    if not is_logged_in():
        return redirect(url_for("login"))
    
    # Hent søkeord hvis det finnes, ellers hent alt
    query = request.args.get("search")
    if query:
        inventory = search_item(query)
    else:
        inventory = get_inventory()
    
    # Vis admin-siden eller student-siden basert på rolle
    if is_admin():
        return render_template("admin.html", inventory=inventory)
    else:
        return render_template("index.html", inventory=inventory)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        role = request.form.get("role")
        password = request.form.get("password")
        
        if role == "student":
            session["role"] = "student"
            return redirect(url_for("index"))
        
        elif role == "admin":
            if password == "1234":
                session["role"] = "admin"
                return redirect(url_for("index"))
            else:
                error = "Feil passord for admin."
    
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --- API RUTER (Handlinger) ---

@app.route("/stock/change", methods=["POST"])
def stock_change():
    if not is_logged_in(): return redirect(url_for("login"))
    
    item_id = int(request.form.get("item_id"))
    amount = int(request.form.get("amount"))
    
    change_stock(item_id, amount)
    return redirect(url_for("index"))

@app.route("/item/add", methods=["POST"])
def item_add():
    if not is_admin(): return redirect(url_for("login"))
    
    # Håndter bildeopplasting (valgfritt)
    image_filename = None
    if 'image' in request.files:
        file = request.files['image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_filename = filename

    # Finn neste ledige ID (enkel logikk)
    current_inv = get_inventory()
    next_id = max([i['id'] for i in current_inv], default=0) + 1
    
    new_item(
        new_name=request.form.get("name"),
        new_id=next_id,
        new_quantity=int(request.form.get("quantity")),
        new_location=request.form.get("shelf"),
        image=image_filename
    )
    return redirect(url_for("index"))

@app.route("/item/update", methods=["POST"])
def item_update():
    if not is_admin(): return redirect(url_for("login"))
    
    update_item(
        old_id=int(request.form.get("id")),
        new_id=int(request.form.get("id")), # Vi endrer ikke ID her for enkelhets skyld
        new_name=request.form.get("name"),
        new_quantity=int(request.form.get("quantity")),
        new_shelf=request.form.get("shelf"),
        image=None # Vi ignorerer bildeoppdatering i denne omgang
    )
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)