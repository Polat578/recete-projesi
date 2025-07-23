function getWarehouses() {
    fetch('https://recete-projesi.onrender.com/warehouses')
        .then(response => response.json())
        .then(data => {
            const warehouseSelect = document.getElementById("warehouse");
            warehouseSelect.innerHTML = "";
            data.forEach(warehouse => {
                const option = document.createElement("option");
                option.value = warehouse.name;
                option.text = warehouse.name;
                warehouseSelect.appendChild(option);
            });
        });
}

function addWarehouse() {
    const name = document.getElementById("warehouseName").value;
    fetch('https://recete-projesi.onrender.com/warehouses', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ name })
    })
    .then(response => response.json())
    .then(data => {
        alert("Ambar eklendi!");
        getWarehouses();
    });
}

function addMaterial() {
    const name = document.getElementById("name").value;
    const unit = document.getElementById("unit").value;
    const stock_amount = document.getElementById("stock_amount").value;
    const cycle_time = document.getElementById("cycle_time").value;
    const type = document.getElementById("type").value;
    const warehouse = document.getElementById("warehouse").value;
    const stock_code = document.getElementById("stock_code").value;

    fetch('https://recete-projesi.onrender.com/materials', {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name,
            unit,
            stock_amount,
            cycle_time,
            type,
            warehouse,
            stock_code
        })
    })
    .then(response => response.json())
    .then(data => {
        alert("Malzeme eklendi!");
        loadMaterials();
    });
}

function loadMaterials() {
    fetch('https://recete-projesi.onrender.com/materials')
        .then(response => response.json())
        .then(data => {
            const table = document.getElementById("materialTable");
            table.innerHTML = "<tr><th>Ad</th><th>Birim</th><th>Stok</th><th>Çevrim Süresi</th><th>Tip</th><th>Ambar</th><th>Stok Kodu</th></tr>";
            data.forEach(material => {
                const row = document.createElement("tr");
                row.innerHTML = `
                    <td>${material.name}</td>
                    <td>${material.unit}</td>
                    <td>${material.stock_amount}</td>
                    <td>${material.cycle_time}</td>
                    <td>${material.type}</td>
                    <td>${material.warehouse}</td>
                    <td>${material.stock_code}</td>
                `;
                table.appendChild(row);
            });
        });
}

window.onload = function () {
    getWarehouses();
    loadMaterials();
};
