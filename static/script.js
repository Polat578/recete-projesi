// Firebase modülleri (CDN üzerinden)
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js";
import {
  getFirestore,
  collection,
  addDoc,
  getDocs
} from "https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js";

// Firebase yapılandırma — senin verdiğin config
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

// HTML öğeleri
const nameInput = document.getElementById("warehouseName");
const warehouseList = document.getElementById("warehouseList");

// 🔁 Listeleme fonksiyonu
async function getWarehouses() {
  warehouseList.innerHTML = "";
  const snapshot = await getDocs(collection(db, "warehouses"));
  snapshot.forEach((doc) => {
    const li = document.createElement("li");
    li.textContent = doc.data().name;
    warehouseList.appendChild(li);
  });
}

// ➕ Ekleme fonksiyonu
async function addWarehouse() {
  const name = nameInput.value.trim();
  if (!name) {
    alert("Ambar adı boş olamaz");
    return;
  }

  await addDoc(collection(db, "warehouses"), { name });
  nameInput.value = "";
  getWarehouses();
}

// Sayfa yüklenince listele
getWarehouses();
