// script.js

// Malzeme listesini yükler
async function loadMaterials() {
  try {
    const res = await fetch('/materials');
    if (!res.ok) {
      throw new Error(`HTTP hata: ${res.status}`);
    }

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
  } catch (err) {
    console.error('Malzeme yüklenirken hata oluştu:', err);
    alert('❌ Malzeme verisi alınamadı. Lütfen sunucunun çalıştığından ve "/materials" adresinin geçerli olduğundan emin olun.');
  }
}

// Ürün listesini yükler
async function loadProducts() {
  try {
    const res = await fetch('/products');
    if (!res.ok) {
      throw new Error(`HTTP hata: ${res.status}`);
    }

    const products = await res.json();
    const tbody = document.getElementById('productsList');
    const productSelect = document.getElementById('productSelect');
    const orderProductSelect = document.getElementById('orderProductSelect');
    tbody.innerHTML = '';
    productSelect.innerHTML = '';
    orderProductSelect.innerHTML = '';

    products.forEach(p => {
      const row = `<tr><td>${p.name}</td><td>${p.unit}</td><td>${p.stock_amount}</td></tr>`;
      tbody.insertAdjacentHTML('beforeend', row);

      const option1 = document.createElement('option');
      option1.value = p.id;
      option1.textContent = p.name;
      productSelect.appendChild(option1);

      const option2 = document.createElement('option');
      option2.value = p.id;
      option2.textContent = p.name;
      orderProductSelect.appendChild(option2);
    });
  } catch (err) {
    console.error('Ürün yüklenirken hata oluştu:', err);
    alert('❌ Ürün verisi alınamadı.');
  }
}
