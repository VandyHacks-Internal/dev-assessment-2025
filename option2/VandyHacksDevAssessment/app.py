from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import json
from db import (
    initialize_database,
    get_connection,
    create_or_update_item,
    set_item_quantity,
    list_items,
    delete_item,
    checkout_item,
    get_item_by_name
)

app = Flask(__name__)
app.secret_key = 'swagtrackr_secret_key_2024'

# Initialize database on startup
initialize_database()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    with get_connection() as conn:
        items = list_items(conn)
    return render_template('dashboard.html', items=items)

@app.route('/api/items', methods=['GET'])
def api_get_items():
    """API endpoint to get all items"""
    with get_connection() as conn:
        items = list_items(conn)
        return jsonify([{'id': item[0], 'name': item[1], 'quantity': item[2]} for item in items])

@app.route('/api/items', methods=['POST'])
def api_add_item():
    """API endpoint to add/update an item"""
    data = request.get_json()
    name = data.get('name', '').strip()
    quantity = data.get('quantity', 0)
    
    if not name:
        return jsonify({'error': 'Item name is required'}), 400
    
    try:
        quantity = int(quantity)
        if quantity < 0:
            return jsonify({'error': 'Quantity must be non-negative'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid quantity'}), 400
    
    with get_connection() as conn:
        item_id, new_qty = create_or_update_item(conn, name, quantity)
        return jsonify({'id': item_id, 'name': name, 'quantity': new_qty})

@app.route('/api/items/<int:item_id>', methods=['PUT'])
def api_update_item(item_id):
    """API endpoint to update an item's quantity"""
    data = request.get_json()
    quantity = data.get('quantity')
    
    if quantity is None:
        return jsonify({'error': 'Quantity is required'}), 400
    
    try:
        quantity = int(quantity)
        if quantity < 0:
            return jsonify({'error': 'Quantity must be non-negative'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid quantity'}), 400
    
    with get_connection() as conn:
        # Find item by ID
        items = list_items(conn)
        item_name = None
        for item in items:
            if item[0] == item_id:
                item_name = item[1]
                break
        
        if not item_name:
            return jsonify({'error': 'Item not found'}), 404
        
        item_id, new_qty = set_item_quantity(conn, item_name, quantity)
        return jsonify({'id': item_id, 'name': item_name, 'quantity': new_qty})

@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def api_delete_item(item_id):
    """API endpoint to delete an item"""
    with get_connection() as conn:
        # Find item by ID
        items = list_items(conn)
        item_name = None
        for item in items:
            if item[0] == item_id:
                item_name = item[1]
                break
        
        if not item_name:
            return jsonify({'error': 'Item not found'}), 404
        
        success = delete_item(conn, item_name)
        if success:
            return jsonify({'message': 'Item deleted successfully'})
        else:
            return jsonify({'error': 'Failed to delete item'}), 500

@app.route('/api/checkout', methods=['POST'])
def api_checkout():
    """API endpoint to checkout items"""
    data = request.get_json()
    name = data.get('name', '').strip()
    amount = data.get('amount', 0)
    recipient = data.get('recipient', '').strip() or None
    
    if not name:
        return jsonify({'error': 'Item name is required'}), 400
    
    try:
        amount = int(amount)
        if amount <= 0:
            return jsonify({'error': 'Amount must be positive'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid amount'}), 400
    
    with get_connection() as conn:
        try:
            item_id, new_qty = checkout_item(conn, name, amount, recipient)
            return jsonify({'id': item_id, 'name': name, 'quantity': new_qty, 'checked_out': amount})
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    import sys
    port = 5001
    if len(sys.argv) > 1 and sys.argv[1] == '--port':
        port = int(sys.argv[2])
    app.run(debug=True, host='0.0.0.0', port=port)
