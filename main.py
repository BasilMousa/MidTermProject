from flask import Flask, request, redirect, url_for, render_template_string
from functions import (
    add_jewelry_item,
    remove_jewelry_item,
    update_item,
    calculate_profit_summary
)

app = Flask(__name__)
inventory = []

STYLE = """
<style>
    body {
        font-family: Arial, sans-serif;
        background: #eef2f3;
        padding: 20px;
        text-align: center;
    }
    h1, h2, h3 {
        color: #222;
    }
    a {
        margin-right: 10px;
        text-decoration: none;
        color: #2a7ae2;
        font-weight: bold;
    }
    a:hover {
        text-decoration: underline;
    }
    table {
        border-collapse: collapse;
        margin: 0 auto;
        background: #ffffff;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        border-radius: 8px;
        overflow: hidden;
    }
    th, td {
        padding: 12px;
        border: 1px solid #d1d1d1;
        text-align: center;
    }
    th {
        background-color: #d7e4f0;
    }
    tr:nth-child(even) {
        background-color: #f4f9fd;
    }
    form {
        background: #ffffff;
        padding: 25px;
        margin: 0 auto;
        max-width: 420px;
        border-radius: 10px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    }
    input, select, button {
        width: 100%;
        padding: 10px;
        margin-top: 8px;
        margin-bottom: 18px;
        border: 1px solid #bbb;
        border-radius: 5px;
        font-size: 14px;
    }
    input, select {
        background-color: #f5faff;
    }
    button {
        background-color: #2a7ae2;
        color: white;
        font-weight: bold;
        cursor: pointer;
    }
    button:hover {
        background-color: #1d5fbf;
    }
</style>
"""

@app.route('/')
def index():
    summary = calculate_profit_summary(inventory)

    html = """
    <html>
    <head><title>Jewelry Inventory</title>{{ style|safe }}</head>
    <body>
        <h1>✨ Jewelry Inventory ✨</h1>
        <a href="/add">➕ Add New Item</a>
        <a href="/summary">📊 Profit Summary</a>
        <br><br>

        <h3>Summary</h3>
        <p>Total Cost (All): ${{ summary['total_cost_all'] }}<br>
           Total Cost (Available): ${{ summary['total_cost_available'] }}<br>
           Total Cost (Sold): ${{ summary['total_cost_sold'] }}<br>
           Total Selling: ${{ summary['total_selling'] }}<br>
           Total Profit: ${{ summary['total_profit'] }}</p>

        {% if inventory %}
        <table>
            <tr>
                <th>ID</th><th>Type</th><th>Category</th><th>Cost</th><th>Selling</th><th>Status</th><th>Profit</th><th>Actions</th>
            </tr>
            {% for item in inventory %}
            <tr>
                <td>{{ item['id'] }}</td>
                <td>{{ item['type'] }}</td>
                <td>{{ item['category'] }}</td>
                <td>${{ '%.2f' % item['cost_price'] }}</td>
                <td>{% if item['selling_price'] is not none %} ${{ '%.2f' % item['selling_price'] }} {% else %}-{% endif %}</td>
                <td>{{ item['status'] }}</td>
                <td>{% if item['selling_price'] is not none %} ${{ '%.2f' % (item['selling_price'] - item['cost_price']) }} {% else %}-{% endif %}</td>
                <td>
                    <a href="/edit/{{ item['id'] }}">✏️ Edit</a>
                    <a href="/remove/{{ item['id'] }}">❌ Delete</a>
                </td>
            </tr>
            {% endfor %}
        </table>
        {% else %}
        <p>No items in inventory.</p>
        {% endif %}
    </body>
    </html>
    """
    return render_template_string(html, inventory=inventory, summary=summary, style=STYLE)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        item_type = request.form['type']
        category = request.form['category']
        cost_price = float(request.form['cost_price'])
        global inventory
        inventory, _ = add_jewelry_item(inventory, item_type, category, cost_price)
        return redirect(url_for('index'))

    html = """
    <html><head><title>Add Item</title>{{ style|safe }}</head><body>
    <h1>➕ Add New Jewelry Item</h1>
    <form method="POST">
        <label>Type:</label>
        <input name="type" required>
        <label>Category:</label>
        <input name="category" required>
        <label>Cost Price:</label>
        <input name="cost_price" type="number" step="0.01" required>
        <button type="submit">Add Item</button>
    </form>
    <a href="/">Back to Inventory</a>
    </body></html>
    """
    return render_template_string(html, style=STYLE)

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    item = next((i for i in inventory if i['id'] == item_id), None)
    if not item:
        return "Item not found", 404

    if request.method == 'POST':
        updated_data = {
            'type': request.form['type'],
            'category': request.form['category'],
            'cost_price': float(request.form['cost_price']),
            'status': request.form['status']
        }
        selling_price = request.form.get('selling_price')
        if selling_price:
            updated_data['selling_price'] = float(selling_price)
        update_item(inventory, item_id, updated_data)
        return redirect(url_for('index'))

    html = f"""
    <html><head><title>Edit Item</title>{{{{ style|safe }}}}</head><body>
    <h1>✏️ Edit Jewelry Item</h1>
    <form method="POST">
        <label>Type:</label>
        <input name="type" value="{item['type']}" required>
        <label>Category:</label>
        <input name="category" value="{item['category']}" required>
        <label>Cost Price:</label>
        <input name="cost_price" type="number" step="0.01" value="{item['cost_price']}" required>
        <label>Selling Price:</label>
        <input name="selling_price" type="number" step="0.01" value="{item.get('selling_price', '') or ''}">
        <label>Status:</label>
        <select name="status">
            <option value="available" {'selected' if item['status'] == 'available' else ''}>Available</option>
            <option value="sold" {'selected' if item['status'] == 'sold' else ''}>Sold</option>
        </select>
        <button type="submit">Save Changes</button>
    </form>
    <a href="/">Back to Inventory</a>
    </body></html>
    """
    return render_template_string(html, style=STYLE)

@app.route('/remove/<int:item_id>')
def remove(item_id):
    global inventory
    inventory, _ = remove_jewelry_item(inventory, item_id)
    return redirect(url_for('index'))

@app.route('/summary')
def summary():
    summary = calculate_profit_summary(inventory)
    html = """
    <html>
    <head><title>Profit Summary</title>{{ style|safe }}</head>
    <body>
        <h1>📊 Profit Summary</h1>
        <p>Total Inventory Cost (Available): ${{ summary['total_cost_available'] }}</p>
        <p>Total Cost (Sold): ${{ summary['total_cost_sold'] }}</p>
        <p>Total Cost (All): ${{ summary['total_cost_all'] }}</p>
        <p>Total Revenue (Sold): ${{ summary['total_selling'] }}</p>
        <p>Total Profit: ${{ summary['total_profit'] }}</p>

        <h2>Profit Per Sold Item</h2>
        {% if summary['profit_per_item'] %}
            <ul>
            {% for item in summary['profit_per_item'] %}
                <li>ID {{ item['id'] }} ({{ item['type'] }}): ${{ item['profit'] }}</li>
            {% endfor %}
            </ul>
        {% else %}
            <p>No items sold yet.</p>
        {% endif %}

        <br><a href="/">🔙 Back to Inventory</a>
    </body>
    </html>
    """
    return render_template_string(html, summary=summary, style=STYLE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
