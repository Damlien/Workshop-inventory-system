from flask import Flask, render_template_string, request, redirect, url_for, session
from inventory_service import get_inventory, search_item, new_item, update_item, change_stock
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "lab_secret_key_123" 
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

COMMON_STYLE = """
<style>
    body { font-family: sans-serif; background: #f4f4f4; padding: 20px; }
    nav { background: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
    nav a { margin-right: 15px; text-decoration: none; color: #3498db; font-weight: bold; }
    .card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 20px; }
    .card { background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; }
    .card img { width: 100%; height: 150px; object-fit: cover; border-radius: 4px; background: #eee; }
    .stock-count { font-size: 1.2em; font-weight: bold; margin: 10px 0; }
    .low-stock { color: #e74c3c; }
    .btn { padding: 8px 12px; border-radius: 4px; border: none; cursor: pointer; background: #3498db; color: white; }
    table { width: 100%; background: white; border-collapse: collapse; margin-top: 20px; }
    th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
</style>
"""

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        if role == "admin" and request.form.get("password") == "1234":
            session["role"] = "admin"
            return redirect(url_for("admin_dashboard"))
        elif role == "student":
            session["role"] = "student"
            return redirect(url_for("data_retrival"))
    return render_template_string(COMMON_STYLE + """
        <div style="text-align:center; margin-top:100px;">
            <h1>Lab Login</h1>
            <form method="POST"><button type="submit" name="role" value="student" class="btn">Student Entry</button></form>
            <form method="POST" style="margin-top:20px;">
                <input type="password" name="password" placeholder="Admin Pass">
                <button type="submit" name="role" value="admin" class="btn" style="background:#2c3e50;">Admin Login</button>
            </form>
        </div>
    """)

@app.route("/")
def data_retrival():
    if "role" not in session: return redirect(url_for("login"))
    query = request.args.get("search")
    data = search_item(query) if query else get_inventory()
    
    html = COMMON_STYLE + """
    <nav>
        <a href="/">Catalog</a>
        {% if session.role == 'admin' %}<a href="/admin">Dashboard</a>{% endif %}
        <a href="/logout">Logout</a>
    </nav>
    <div class="card-grid">
        {% for item in in_storage %}
        <div class="card">
            <img src="/static/{{ item.image or '' }}" onerror="this.src='https://via.placeholder.com/150?text=No+Image'">
            <h3>{{ item.name }}</h3>
            <p>Shelf: {{ item.shelf }}</p>
            <div class="stock-count {% if item.quantity < 3 %}low-stock{% endif %}">{{ item.quantity }}</div>
            <form action="/adjust_stock" method="POST">
                <input type="hidden" name="item_id" value="{{ item.id }}">
                <button type="submit" name="change" value="-1" class="btn">-</button>
                <button type="submit" name="change" value="1" class="btn">+</button>
            </form>
        </div>
        {% endfor %}
    </div>
    """
    return render_template_string(html, in_storage=data)

@app.route("/admin")
def admin_dashboard():
    if session.get("role") != "admin": return redirect(url_for("login"))
    inventory = get_inventory()
    
    html = COMMON_STYLE + """
    <nav><a href="/">Back to Catalog</a> | <a href="/logout">Logout</a></nav>
    <h2>Admin Dashboard</h2>
    <form action="/add_item" method="POST" enctype="multipart/form-data" style="background:white; padding:15px; border-radius:8px;">
        <input type="text" name="name" placeholder="Name" required>
        <input type="number" name="qty" placeholder="Qty" required style="width:60px;">
        <input type="text" name="shelf" placeholder="Shelf" required style="width:80px;">
        <input type="file" name="item_image">
        <button type="submit" class="btn">Add New Item</button>
    </form>

    <table>
        <tr><th>ID</th><th>Preview</th><th>Name</th><th>Qty</th><th>Shelf</th><th>New Photo</th><th>Save</th></tr>
        {% for item in in_storage %}
        <tr>
            <form action="/edit_item" method="POST" enctype="multipart/form-data">
                <input type="hidden" name="old_id" value="{{ item.id }}">
                <td>{{ item.id }}</td>
                <td><img src="/static/{{ item.image or '' }}" style="height:40px; width:40px; object-fit:cover;"></td>
                <td><input type="text" name="new_name" value="{{ item.name }}"></td>
                <td><input type="number" name="new_qty" value="{{ item.quantity }}" style="width:60px;"></td>
                <td><input type="text" name="new_shelf" value="{{ item.shelf }}" style="width:80px;"></td>
                <td><input type="file" name="new_image" style="font-size:0.7em;"></td>
                <td><button type="submit" class="btn" style="background:#27ae60;">Save</button></td>
            </form>
        </tr>
        {% endfor %}
    </table>
    """
    return render_template_string(html, in_storage=inventory)

@app.route("/edit_item", methods=["POST"])
def edit_existing_item():
    old_id = int(request.form.get("old_id"))
    image_file = request.files.get("new_image")
    filename = secure_filename(image_file.filename) if image_file and image_file.filename != '' else None
    if filename: image_file.save(os.path.join(UPLOAD_FOLDER, filename))
    
    # Preserve old image if no new one uploaded
    inventory = get_inventory()
    item = next((i for i in inventory if i["id"] == old_id), None)
    final_img = filename if filename else (item.get("image") if item else None)

    update_item(old_id, old_id, request.form.get("new_name"), int(request.form.get("new_qty")), request.form.get("new_shelf"), image=final_img)
    return redirect(url_for('admin_dashboard'))

@app.route("/add_item", methods=["POST"])
def handle_add_item():
    image_file = request.files.get("item_image")
    filename = secure_filename(image_file.filename) if image_file else None
    if filename: image_file.save(os.path.join(UPLOAD_FOLDER, filename))
    new_id = max([i["id"] for i in get_inventory()], default=0) + 1
    new_item(request.form.get("name"), new_id, int(request.form.get("qty")), request.form.get("shelf"), image=filename)
    return redirect(url_for('admin_dashboard'))

@app.route("/adjust_stock", methods=["POST"])
def adjust_stock():
    change_stock(int(request.form.get("item_id")), int(request.form.get("change")))
    return redirect(url_for('data_retrival'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
