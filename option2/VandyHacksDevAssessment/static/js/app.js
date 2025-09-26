// SwagTrackr Frontend JavaScript

let currentItems = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadInventory();
    
    // Set up form event listeners
    document.getElementById('addItemForm').addEventListener('submit', function(e) {
        e.preventDefault();
        addItem();
    });
    
    document.getElementById('checkoutForm').addEventListener('submit', function(e) {
        e.preventDefault();
        checkoutItem();
    });
    
    document.getElementById('editQuantityForm').addEventListener('submit', function(e) {
        e.preventDefault();
        updateQuantity();
    });
});

// Load inventory from API
async function loadInventory() {
    try {
        const response = await fetch('/api/items');
        if (!response.ok) {
            throw new Error('Failed to load inventory');
        }
        
        currentItems = await response.json();
        renderInventoryTable();
        updateStats();
    } catch (error) {
        showToast('Error loading inventory: ' + error.message, 'error');
    }
}

// Render the inventory table
function renderInventoryTable() {
    const tbody = document.getElementById('inventoryTableBody');
    tbody.innerHTML = '';
    
    if (currentItems.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="4" class="text-center text-muted py-4">
                    <i class="fas fa-box-open fa-2x mb-2"></i><br>
                    No items in inventory. Add your first item to get started!
                </td>
            </tr>
        `;
        return;
    }
    
    currentItems.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>
                <strong>${escapeHtml(item.name)}</strong>
            </td>
            <td>
                <span class="badge bg-secondary fs-6">${item.quantity}</span>
            </td>
            <td>
                ${getStatusBadge(item.quantity)}
            </td>
            <td>
                <div class="btn-group" role="group">
                    <button class="btn btn-outline-primary btn-sm" onclick="openCheckoutModal('${escapeHtml(item.name)}', ${item.quantity})" title="Checkout">
                        <i class="fas fa-shopping-cart"></i>
                    </button>
                    <button class="btn btn-outline-warning btn-sm" onclick="openEditModal('${escapeHtml(item.name)}', ${item.quantity})" title="Edit Quantity">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-outline-danger btn-sm" onclick="deleteItem(${item.id}, '${escapeHtml(item.name)}')" title="Delete">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Get status badge based on quantity
function getStatusBadge(quantity) {
    if (quantity === 0) {
        return '<span class="status-badge status-out-of-stock">Out of Stock</span>';
    } else if (quantity <= 10) {
        return '<span class="status-badge status-low-stock">Low Stock</span>';
    } else {
        return '<span class="status-badge status-in-stock">In Stock</span>';
    }
}

// Update statistics cards
function updateStats() {
    const totalItems = currentItems.length;
    const totalQuantity = currentItems.reduce((sum, item) => sum + item.quantity, 0);
    const lowStockItems = currentItems.filter(item => item.quantity > 0 && item.quantity <= 10).length;
    const outOfStockItems = currentItems.filter(item => item.quantity === 0).length;
    
    document.getElementById('totalItems').textContent = totalItems;
    document.getElementById('totalQuantity').textContent = totalQuantity;
    document.getElementById('lowStockItems').textContent = lowStockItems;
    document.getElementById('outOfStockItems').textContent = outOfStockItems;
}

// Add new item
async function addItem() {
    const name = document.getElementById('itemName').value.trim();
    const quantity = parseInt(document.getElementById('itemQuantity').value);
    
    if (!name) {
        showToast('Please enter an item name', 'error');
        return;
    }
    
    if (isNaN(quantity) || quantity < 0) {
        showToast('Please enter a valid quantity', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/items', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, quantity })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to add item');
        }
        
        const newItem = await response.json();
        showToast(`Successfully added ${newItem.quantity} of ${newItem.name}`, 'success');
        
        // Close modal and reset form
        bootstrap.Modal.getInstance(document.getElementById('addItemModal')).hide();
        document.getElementById('addItemForm').reset();
        
        // Reload inventory
        await loadInventory();
    } catch (error) {
        showToast('Error adding item: ' + error.message, 'error');
    }
}

// Open checkout modal
function openCheckoutModal(name, currentQuantity) {
    document.getElementById('checkoutItemName').value = name;
    document.getElementById('checkoutAmount').max = currentQuantity;
    document.getElementById('checkoutAmount').value = '';
    document.getElementById('checkoutRecipient').value = '';
    
    new bootstrap.Modal(document.getElementById('checkoutModal')).show();
}

// Checkout items
async function checkoutItem() {
    const name = document.getElementById('checkoutItemName').value;
    const amount = parseInt(document.getElementById('checkoutAmount').value);
    const recipient = document.getElementById('checkoutRecipient').value.trim() || null;
    
    if (!name || isNaN(amount) || amount <= 0) {
        showToast('Please enter a valid amount', 'error');
        return;
    }
    
    try {
        const response = await fetch('/api/checkout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name, amount, recipient })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to checkout items');
        }
        
        const result = await response.json();
        showToast(`Successfully checked out ${result.checked_out} of ${result.name}. Remaining: ${result.quantity}`, 'success');
        
        // Close modal and reset form
        bootstrap.Modal.getInstance(document.getElementById('checkoutModal')).hide();
        document.getElementById('checkoutForm').reset();
        
        // Reload inventory
        await loadInventory();
    } catch (error) {
        showToast('Error checking out items: ' + error.message, 'error');
    }
}

// Open edit quantity modal
function openEditModal(name, currentQuantity) {
    document.getElementById('editItemName').value = name;
    document.getElementById('editQuantity').value = currentQuantity;
    
    new bootstrap.Modal(document.getElementById('editQuantityModal')).show();
}

// Update item quantity
async function updateQuantity() {
    const name = document.getElementById('editItemName').value;
    const quantity = parseInt(document.getElementById('editQuantity').value);
    
    if (!name || isNaN(quantity) || quantity < 0) {
        showToast('Please enter a valid quantity', 'error');
        return;
    }
    
    // Find the item ID
    const item = currentItems.find(item => item.name === name);
    if (!item) {
        showToast('Item not found', 'error');
        return;
    }
    
    try {
        const response = await fetch(`/api/items/${item.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ quantity })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to update quantity');
        }
        
        const updatedItem = await response.json();
        showToast(`Successfully updated ${updatedItem.name} quantity to ${updatedItem.quantity}`, 'success');
        
        // Close modal and reset form
        bootstrap.Modal.getInstance(document.getElementById('editQuantityModal')).hide();
        document.getElementById('editQuantityForm').reset();
        
        // Reload inventory
        await loadInventory();
    } catch (error) {
        showToast('Error updating quantity: ' + error.message, 'error');
    }
}

// Delete item
async function deleteItem(itemId, itemName) {
    if (!confirm(`Are you sure you want to delete "${itemName}"? This action cannot be undone.`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/items/${itemId}`, {
            method: 'DELETE'
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to delete item');
        }
        
        showToast(`Successfully deleted ${itemName}`, 'success');
        
        // Reload inventory
        await loadInventory();
    } catch (error) {
        showToast('Error deleting item: ' + error.message, 'error');
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    const toastBody = document.getElementById('toastBody');
    const toastHeader = toast.querySelector('.toast-header');
    
    // Set message
    toastBody.textContent = message;
    
    // Set icon and color based on type
    const icon = toastHeader.querySelector('i');
    icon.className = 'fas me-2';
    
    switch (type) {
        case 'success':
            icon.classList.add('fa-check-circle', 'text-success');
            break;
        case 'error':
            icon.classList.add('fa-exclamation-circle', 'text-danger');
            break;
        case 'warning':
            icon.classList.add('fa-exclamation-triangle', 'text-warning');
            break;
        default:
            icon.classList.add('fa-info-circle', 'text-primary');
    }
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast);
    bsToast.show();
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
