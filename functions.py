"""
Jewelry Shop Inventory Management 
Functions File
"""

def generate_next_id(inventory):
    if not inventory:
        return 1
    return max(item['id'] for item in inventory) + 1

def add_jewelry_item(inventory, item_type, category, cost_price, selling_price=None):
    new_item = {
        "id": generate_next_id(inventory),
        "type": item_type.strip(),
        "category": category.strip(),
        "cost_price": round(cost_price, 2),
        "selling_price": round(selling_price, 2) if selling_price is not None else None,
        "status": "available"
    }
    inventory.append(new_item)
    return inventory, new_item

def remove_jewelry_item(inventory, item_id):
    if not str(item_id).isdigit():
        return inventory, None

    item_id = int(item_id)
    for i, item in enumerate(inventory):
        if item['id'] == item_id:
            removed = inventory.pop(i)
            return inventory, removed

    return inventory, None

def calculate_profit_summary(inventory):
    total_cost_all = sum(item['cost_price'] for item in inventory)
    total_cost_available = sum(item['cost_price'] for item in inventory if item['status'] == 'available')
    total_cost_sold = sum(item['cost_price'] for item in inventory if item['status'] == 'sold')
    total_revenue = sum(item['selling_price'] for item in inventory if item['status'] == 'sold' and item.get('selling_price') is not None)
    total_profit = total_revenue - total_cost_sold

    profit_per_item = [
        {
            'id': item['id'],
            'type': item['type'],
            'profit': round(item['selling_price'] - item['cost_price'], 2)
        }
        for item in inventory
        if item['status'] == 'sold' and item.get('selling_price') is not None
    ]

    return {
        'total_cost_all': round(total_cost_all, 2),
        'total_cost_available': round(total_cost_available, 2),
        'total_cost_sold': round(total_cost_sold, 2),
        'total_revenue': round(total_revenue, 2),
        'total_profit': round(total_profit, 2),
        'profit_per_item': profit_per_item
    }

def update_item(inventory, item_id, updated_data):
    for item in inventory:
        if item['id'] == item_id:
            item.update(updated_data)
            return item
    return None

def get_inventory_summary(inventory):
    total_cost = sum(item['cost_price'] for item in inventory)
    total_selling = sum(item['selling_price'] or 0 for item in inventory)
    total_profit = total_selling - total_cost

    return {
        "total_cost": round(total_cost, 2),
        "total_selling": round(total_selling, 2),
        "total_profit": round(total_profit, 2),
    }
