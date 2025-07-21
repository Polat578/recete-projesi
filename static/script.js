// script.js

async function loadMaterials() {
  const res = await fetch('/materials');
  const materials = await res.json();
  const tbody = document.getElementById('materialsList');
  const materialSelect = document.getElementById('materialSelect');
  tbody.innerHTML = '';
  materialSelect.innerHTML = '';
  materials.forEach(m => {
    const row = `<tr><td>${m.name}</td><td>${m.unit}</td><td>${m.stock_amount}</td></tr>`;
    tbody.insertAdjacentHTML('beforeend', row);

    const option = document.createElement('option');
    option.value = m.id;
    option.textContent = m.name;
    materialSelect.appendChild(option);
  });
}

async function loadProducts() {
  const res = await fetch('/products');
  const products = await res.json();
  const tbody = document.getElementById('productsList');
  const productSelect = document.getElementById('productSelect');
  const orderProductSelect = document.getElementById('orderProductSelect');
  tbody.innerHTML = '';
  productSelect.innerHTML = '';
  orderProductSelect.innerHTML = '';
  products.forEach(p => {
    const row = `<tr><td>${p.name}</td></tr>`;
    tbody.insertAdjacentHTML('beforeend', row);

    const option1 = new Option(p.name, p.id);
    const option2 = new Option(p.name, p.id);
    productSelect.appendChild(option1);
    orderProductSelect.appendChild(option2);
  });
  loadRecipe(); // Varsayılan ürün reçetesi yüklensin
}

async function loadRecipe() {
  const productId = document.getElementById('productSelect').value;
  if (!productId) return;
  const res = await fetch(`/recipes/${productId}`);
  const data = await res.json();
  const tbody = document.getElementById('recipeList');
  tbody.innerHTML = '';
  data.forEach(item => {
    const row = `<tr><td>${item.material}</td><td>${item.quantity}</td><td>${item.unit}</td></tr>`;
    tbody.insertAdjacentHTML('beforeend', row);
  });
}

document.getElementById('materialForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const name = document.getElementById('name').value;
  const unit = document.getElementById('unit').value;
  const stock = parseFloat(document.getElementById('stock').value) || 0;
  await fetch('/materials', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, unit, stock_amount: stock })
  });
  this.reset();
  loadMaterials();
});

document.getElementById('productForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const name = document.getElementById('productName').value;
  await fetch('/products', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  });
  this.reset();
  loadProducts();
});

document.getElementById('recipeForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const productId = document.getElementById('productSelect').value;
  const materialId = document.getElementById('materialSelect').value;
  const quantity = parseFloat(document.getElementById('quantity').value);
  await fetch('/recipes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id: productId, material_id: materialId, quantity })
  });
  this.reset();
  loadRecipe();
});

document.getElementById('productSelect').addEventListener('change', loadRecipe);

document.getElementById('orderForm').addEventListener('submit', async function (e) {
  e.preventDefault();
  const product_id = document.getElementById('orderProductSelect').value;
  const quantity = parseInt(document.getElementById('orderQuantity').value);
  await fetch('/orders', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ product_id, quantity })
  });
  this.reset();
  loadOrders();
});

async function loadOrders() {
  const res = await fetch('/orders');
  const orders = await res.json();
  const tbody = document.getElementById('ordersList');
  tbody.innerHTML = '';
  orders.forEach(o => {
    const row = document.createElement('tr');
    row.innerHTML = `
      <td>${o.product}</td>
      <td>${o.quantity}</td>
      <td>${o.status}</td>
      <td>
        ${o.status === 'Üretimde' ? `<button class="btn btn-sm btn-primary" onclick="completeOrder(${o.id})">Üretimi Bitir</button>` : ''}
      </td>
    `;
    tbody.appendChild(row);
  });
}

async function completeOrder(id) {
  await fetch(`/orders/${id}/complete`, { method: 'POST' });
  loadMaterials();
  loadOrders();
}

loadMaterials();
loadProducts();
loadOrders();
