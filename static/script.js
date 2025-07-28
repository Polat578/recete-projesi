import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getFirestore,
  collection,
  getDocs,
  addDoc,
  updateDoc,
  query,
  where,
  doc,
  Timestamp
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

// Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyD4MPM2fvkTXeOWG12g-wV_s3eG4SkBWS0",
  authDomain: "poleroyuncak.firebaseapp.com",
  projectId: "poleroyuncak",
  storageBucket: "poleroyuncak.firebasestorage.app",
  messagingSenderId: "473844630811",
  appId: "1:473844630811:web:bd89bb7d85c7b17ea03fbe",
  measurementId: "G-CV6WKBTJ3V"
};

// Firebase başlat
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// UI elemanları
const overlay = document.getElementById("overlay");
const contextMenu = document.getElementById("context-menu");
const materialList = document.getElementById("materialList");
let selectedMaterial = null;

document.addEventListener("click", () => contextMenu.style.display = "none");

document.addEventListener("contextmenu", (e) => {
  e.preventDefault();
  const target = e.target.closest(".material");
  if (target) {
    selectedMaterial = JSON.parse(target.dataset.raw);
    contextMenu.style.display = "block";
    contextMenu.style.top = `${e.pageY}px`;
    contextMenu.style.left = `${e.pageX}px`;
  } else {
    selectedMaterial = null;
  }
});

document.getElementById("addMaterialBtn").addEventListener("click", () => {
  openModal("modal");
});

document.getElementById("transferBtn").addEventListener("click", () => {
  openModal("transfer-modal");
  populateTransferDropdown();
});

document.getElementById("stockSummaryBtn").addEventListener("click", showStockSummaryForSelected);

document.getElementById("saveMatBtn").addEventListener("click", saveMaterial);
document.getElementById("transferSubmit").addEventListener("click", executeTransfer);

document.getElementById("productSearch").addEventListener("input", (e) => {
  filterProducts(e.target.value);
});

// MODALLAR
function openModal(id) {
  document.getElementById(id).style.display = "block";
  overlay.style.display = "block";
  if (id === "modal") loadWarehouses();
}

function closeAllModals() {
  document.querySelectorAll("#modal, #transfer-modal, #stockSummaryModal").forEach(modal => modal.style.display = "none");
  overlay.style.display = "none";
}

// MATERIAL EKLE
async function saveMaterial() {
  const name = document.getElementById("mat-name").value.trim();
  const code = document.getElementById("mat-code").value.trim();
  const cycle = document.getElementById("mat-cycle").value.trim();
  const warehouse = document.getElementById("mat-warehouse").value;
  const unit = document.getElementById("mat-unit").value;
  const qty = parseFloat(document.getElementById("mat-qty").value);
  const cost = parseFloat(document.getElementById("mat-cost").value);

  if (!name || !code || !warehouse || isNaN(qty)) return alert("Tüm alanları doldurun");

  try {
    await addDoc(collection(db, "materials"), {
      name,
      stock_code: code,
      cycle_time: cycle,
      warehouse,
      unit,
      stock_amount: qty,
      cost,
      created_at: Timestamp.now(),
      updated_at: Timestamp.now()
    });

    alert("Malzeme eklendi");
    closeAllModals();
    loadMaterials();
  } catch (e) {
    console.error(e);
  }
}

// MALZEME LİSTELEME (GRUPLU)
async function loadMaterials() {
  materialList.innerHTML = "⏳ Yükleniyor...";
  const snapshot = await getDocs(collection(db, "materials"));

  const grouped = {};

  snapshot.forEach(doc => {
    const m = doc.data();
    const key = m.name + m.stock_code;
    if (!grouped[key]) grouped[key] = { ...m, total: 0 };
    grouped[key].total += m.stock_amount;
  });

  materialList.innerHTML = "";
  Object.values(grouped).forEach(m => {
    const div = document.createElement("div");
    div.className = "material";
    div.dataset.raw = JSON.stringify(m);
    div.textContent = `🔹 ${m.name} (${m.stock_code}) – ${m.total} ${m.unit}`;
    materialList.appendChild(div);
  });
}

// AMBARLARI YÜKLE
async function loadWarehouses() {
  const select = document.getElementById("mat-warehouse");
  select.innerHTML = "";
  const snapshot = await getDocs(collection(db, "warehouses"));
  snapshot.forEach(doc => {
    const opt = document.createElement("option");
    opt.value = doc.data().name;
    opt.textContent = doc.data().name;
    select.appendChild(opt);
  });
}

// TRANSFER DROPDOWN DOLDUR
let transferMaterials = [];
async function populateTransferDropdown() {
  const dropdown = document.getElementById("transfer-product");
  const toSelect = document.getElementById("transfer-to");
  dropdown.innerHTML = "";
  toSelect.innerHTML = "";

  const snapshot = await getDocs(collection(db, "materials"));
  const map = {};
  snapshot.forEach(doc => {
    const m = doc.data();
    map[m.name + m.stock_code] = m;
  });
  transferMaterials = Object.values(map);

  transferMaterials.forEach(m => {
    const opt = document.createElement("option");
    opt.value = m.name + "|" + m.stock_code;
    opt.textContent = `${m.name} (${m.stock_code})`;
    dropdown.appendChild(opt);
  });

  const warehouses = await getDocs(collection(db, "warehouses"));
  warehouses.forEach(doc => {
    const name = doc.data().name;
    const opt = document.createElement("option");
    opt.value = name;
    opt.textContent = name;
    toSelect.appendChild(opt);
  });
}

// ÜRÜN ARA
function filterProducts(term) {
  const options = document.querySelectorAll("#transfer-product option");
  options.forEach(opt => {
    opt.style.display = opt.textContent.toLowerCase().includes(term.toLowerCase()) ? "block" : "none";
  });
}

// TRANSFER İŞLEMİ
async function executeTransfer() {
  const selected = document.getElementById("transfer-product").value.split("|");
  const productName = selected[0];
  const stockCode = selected[1];
  const qty = parseFloat(document.getElementById("transfer-qty").value);
  const toWarehouse = document.getElementById("transfer-to").value;

  if (!productName || !stockCode || !toWarehouse || isNaN(qty)) return alert("Lütfen tüm alanları doldurun");

  try {
    await addDoc(collection(db, "transfers"), {
      name: productName,
      stock_code: stockCode,
      to: toWarehouse,
      qty,
      created_at: Timestamp.now()
    });

    alert("Transfer kaydedildi (stok değişmedi)");
    closeAllModals();
  } catch (e) {
    console.error("Transfer hatası:", e);
  }
}

// STOK ÖZETİ GÖSTER
async function showStockSummaryForSelected() {
  if (!selectedMaterial) return;

  const snapshot = await getDocs(query(collection(db, "materials"), where("name", "==", selectedMaterial.name)));
  const summary = {};

  snapshot.forEach(doc => {
    const m = doc.data();
    if (!summary[m.warehouse]) summary[m.warehouse] = 0;
    summary[m.warehouse] += m.stock_amount;
  });

  const container = document.getElementById("stockSummaryContent");
  container.innerHTML = "";
  for (const w in summary) {
    const p = document.createElement("p");
    p.textContent = `${w}: ${summary[w]}`;
    container.appendChild(p);
  }

  openModal("stockSummaryModal");
}

loadMaterials();
