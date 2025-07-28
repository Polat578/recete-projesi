// 🔥 Firebase modülleri
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getFirestore,
  collection,
  addDoc,
  getDocs
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

// ✅ Firebase yapılandırması (senin config)
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

// HTML elementlerini al
const nameInput = document.getElementById("warehouseName");
const addBtn = document.getElementById("addWarehouseBtn");
const listEl = document.getElementById("warehouseList");

// 🔁 Listeleme fonksiyonu
async function getWarehouses() {
  listEl.innerHTML = "";
  try {
    const snapshot = await getDocs(collection(db, "warehouses"));
    snapshot.forEach((doc) => {
      const li = document.createElement("li");
      li.textContent = doc.data().name;
      listEl.appendChild(li);
    });
  } catch (e) {
    console.error("Listeleme hatası:", e);
  }
}

// ➕ Ekleme fonksiyonu
async function addWarehouse() {
  const name = nameInput.value.trim();
  if (!name) {
    alert("Ambar adı boş olamaz!");
    return;
  }

  try {
    await addDoc(collection(db, "warehouses"), { name });
    nameInput.value = "";
    getWarehouses();
  } catch (e) {
    console.error("Ekleme hatası:", e);
  }
}

// Başlat
addBtn.addEventListener("click", addWarehouse);
getWarehouses();
// 📦 Malzeme Ekleme Fonksiyonu
async function addMaterial() {
  const name = document.getElementById("mat-name").value.trim();
  const code = document.getElementById("mat-code").value.trim();
  const cycle = document.getElementById("mat-cycle").value.trim();

  if (!name || !code || !cycle) {
    alert("Lütfen tüm alanları doldurun!");
    return;
  }

  try {
    await addDoc(collection(db, "materials"), {
      name,
      code,
      cycleTime: cycle
    });

    alert("Malzeme başarıyla eklendi!");
    closeModal();
    document.getElementById("mat-name").value = "";
    document.getElementById("mat-code").value = "";
    document.getElementById("mat-cycle").value = "";

    // Gerekirse buraya listeyi yenile fonksiyonu da eklenebilir
  } catch (e) {
    console.error("Malzeme eklenemedi:", e);
  }
}

