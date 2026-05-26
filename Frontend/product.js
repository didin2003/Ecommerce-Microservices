const PRODUCT_API = 'https://products.didin.in/api/products/';
const CART_API = 'https://cart.didin.in/api/cart';

function getToken() {
    return localStorage.getItem('access_token');
}

async function addToCart(productId) {
    try {
        const res = await fetch(`${CART_API}/add/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getToken()}`
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: 1
            })
        });

        if (!res.ok) throw new Error();

        alert('✅ Added to cart');

    } catch (err) {
        console.error('Add to cart error:', err);
        alert('❌ Failed to add');
    }
}

async function loadProducts() {
    try {
        const res = await fetch(PRODUCT_API);
        const data = await res.json();

        const container = document.getElementById('products');
        container.innerHTML = '';

        data.forEach(p => {
            container.innerHTML += `
                <div class="col-md-4 mb-4">
                    <div class="card h-100 shadow-sm">
                        <img src="${p.image || 'https://via.placeholder.com/200'}" 
                             class="card-img-top" style="height:200px; object-fit:cover;">
                        <div class="card-body">
                            <h5>${p.name}</h5>
                            <p>${p.description}</p>
                            <h6>₹${p.price}</h6>

                            <button class="btn btn-primary w-100 mt-2"
                                onclick="addToCart(${p.id})">
                                🛒 Add to Cart
                            </button>
                        </div>
                    </div>
                </div>
            `;
        });

    } catch (err) {
        console.error('❌ Product load error:', err);
    }
}

document.addEventListener('DOMContentLoaded', loadProducts);