// 🔥 Firebase modülleri
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getFirestore,
  collection,
  addDoc,
  getDocs,
  Timestamp
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

// ✅ Firebase yapılandırması
const firebaseConfig = {
  apiKey: "AIzaSyD4MPM2fvkTXeOWG12g-wV_s3eG4SkBWS0",
  authDomain: "poleroyuncak.firebaseapp.com",
  projectId: "poleroyuncak",
  storageBucket: "poleroyuncak.firebasestorage.app",
  messagingSenderId: "473844630811",
  appId: "1:473844630811:web:bd89bb7d85c7b17ea03fbe",
  measurementId: "G-CV6WKBTJ3V"
};

// 🔗 Firebase başlat
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

// HTML referansları
const list = document.getElementById("materialList");
const overlay = document.getElementById("overlay");

// Modal kontrolü
function openModal() {
  document.getElementById("modal").style.display = "block";
  overlay.style.display = "block";
}

function closeModal() {
  document.getElementById("modal").style.display = "none";
  overlay.style.display = "none";
}

// 📦 Malzeme ekle
async function addMaterial() {
  const name = document.getElementById("mat-name").value.trim();
  const code = document.getElementById("mat-code").value.trim();
  const cycle = document.getElementById("mat-cycle").value.trim();
  const warehouse = document.getElementById("mat-warehouse").value.trim();
  const unit = document.getElementById("mat-unit").value;
  const qty = parseFloat(document.getElementById("mat-qty").value);
  const cost = parseFloat(document.getElementById("mat-cost").value);

  if (!name || !code || !warehouse || isNaN(qty)) {
    alert("Lütfen gerekli alanları eksiksiz doldurun.");
    return;
  }

  const data = {
    name,
    stock_code: code,
    cycle_time: cycle,
    warehouse,
    unit,
    stock_amount: qty,
    cost,
    created_at: Timestamp.now(),
    updated_at: Timestamp.now()
  };

  try {
    await addDoc(collection(db, "materials"), data);
    alert("✅ Malzeme eklendi.");
    closeModal();
    clearForm();
    loadMaterials();
  } catch (err) {
    console.error("Malzeme ekleme hatası:", err);
  }
}

// 🔁 Malzeme listele
async function loadMaterials() {
  list.innerHTML = "⏳ Yükleniyor...";
  try {
    const snapshot = await getDocs(collection(db, "materials"));
    list.innerHTML = "";
    snapshot.forEach(doc => {
      const m = doc.data();
      const div = document.createElement("div");
      div.className = "material";
      div.textContent = `🔹 ${m.name} (${m.stock_code}) – ${m.stock_amount} ${m.unit}`;
      list.appendChild(div);
      list.appendChild(document.createElement("hr"));
    });
  } catch (err) {
    console.error("Listeleme hatası:", err);
    list.innerHTML = "❌ Listeleme başarısız.";
  }
}

// 🧼 Formu temizle
function clearForm() {
  document.getElementById("mat-name").value = "";
  document.getElementById("mat-code").value = "";
  document.getElementById("mat-cycle").value = "";
  document.getElementById("mat-warehouse").value = "";
  document.getElementById("mat-unit").value = "adet";
  document.getElementById("mat-qty").value = "";
  document.getElementById("mat-cost").value = "";
}

// 🏭 Ambarları yükle (dropdownda göster)
async function loadWarehouses() {
  const select = document.getElementById("mat-warehouse");
  const snapshot = await getDocs(collection(db, "warehouses"));
  select.innerHTML = "<option value=''>Ambar Seç</option>";
  snapshot.forEach(doc => {
    const name = doc.data().name;
    const opt = document.createElement("option");
    opt.value = name;
    opt.textContent = name;
    select.appendChild(opt);
  });
}

// Sağ tık menüsü
const menu = document.getElementById("context-menu");
document.addEventListener("click", () => menu.style.display = "none");
document.addEventListener("contextmenu", (e) => {
  e.preventDefault();
  menu.style.display = "block";
  menu.style.top = `${e.pageY}px`;
  menu.style.left = `${e.pageX}px`;
});

// Başlangıç
loadMaterials();
loadWarehouses();

// Global erişim için fonksiyonları pencerede tut
window.openModal = openModal;
window.closeModal = closeModal;
window.saveMaterial = addMaterial;
