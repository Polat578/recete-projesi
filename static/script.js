// script.js

const BASE_URL = "https://recete-backend.onrender.com"; // Kendi Render backend URL'inle değiştir

// Ambarları yükle
async function loadWarehouses() {
  try {
    const res = await fetch(`${BASE_URL}/warehouses`);
    if (!res.ok) throw new Error(`HTTP hata: ${res.status}`);
    const warehouses = await res.json();

    const list = document.getElementById("warehouseList");
    const select = document.getElementById("warehouseSelect");
    if (list) list.innerHTML = '';
    if (select) select.innerHTML = '';

    warehouses.forEach(w => {
      if (list) {
        const row = `<li>${w.name}</li>`;
        list.insertAdjacentHTML("beforeend", row);
      }

      if (select) {
        const option = document.createElement("option");
        option.value = w.id;
        option.textContent = w.name;
        select.appendChild(option);
      }
    });
  } catch (err) {
    console.error("Ambarlar yüklenirken hata:", err);
    alert("Ambar verisi alınamadı.");
  }
}

// Yeni ambar ekle
async function addWarehouse() {
  const nameInput = document.getElementById("warehouseName");
  const name = nameInput?.value.trim();

  if (!name) {
    alert("Lütfen ambar ismi girin.");
    return;
  }

  try {
    const res = await fetch(`${BASE_URL}/warehouses`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name }),
    });

    const result = await res.json();
    if (res.ok) {
      alert("✅ Ambar eklendi.");
      nameInput.value = "";
      loadWarehouses();
    } else {
      alert("❌ Hata: " + result.error);
    }
  } catch (err) {
    console.error("Ambar eklenirken hata:", err);
    alert("Sunucu hatası.");
  }
}

// Malzeme listesini yükle
async function loadMaterials() {
  try {
    const res = await fetch(`${BASE_URL}/materials`);
    if (!res.ok) throw new Error(`HTTP hata: ${res.status}`);
    const materials = await res.json();

    const tbody = document.getElementById("materialsList");
    const materialSelect = document.getElementById("materialSelect");
    if (tbody) tbody.innerHTML = '';
    if (materialSelect) materialSelect.innerHTML = '';

    materials.forEach(m => {
      if (tbody) {
        const row = `<tr><td>${m.name}</td><td>${m.unit}</td><td>${m.stock_amount}</td></tr>`;
        tbody.insertAdjacentHTML("beforeend", row);
      }

      if (materialSelect) {
        const option = document.createElement("option");
        option.value = m.id;
        option.textContent = m.name;
        materialSelect.appendChild(option);
      }
    });
  } catch (err) {
    console.error("Malzeme yüklenirken hata:", err);
    alert("❌ Malzeme verisi alınamadı.");
  }
}

// Sayfa yüklendiğinde otomatik veri çek
document.addEventListener("DOMContentLoaded", () => {
  loadWarehouses();
  loadMaterials();

  const addBtn = document.getElementById("addWarehouseBtn");
  if (addBtn) {
    addBtn.addEventListener("click", addWarehouse);
  }
});
