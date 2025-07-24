function getWarehouses() {
    fetch('/warehouses')
        .then(response => response.json())
        .then(data => {
            const warehouseSelect = document.getElementById("warehouse");
            const warehouseList = document.getElementById("warehouse-list");

            if (warehouseSelect) {
                warehouseSelect.innerHTML = "";
                data.forEach(warehouse => {
                    const option = document.createElement("option");
                    option.value = warehouse.name;
                    option.text = warehouse.name;
                    warehouseSelect.appendChild(option);
                });
            }

            if (warehouseList) {
                warehouseList.innerHTML = "";
                data.forEach(warehouse => {
                    const li = document.createElement("li");
                    li.textContent = warehouse.name;
                    warehouseList.appendChild(li);
                });
            }
        });
}

function addWarehouse() {
    const name = document.getElementById("warehouseName").value;
    fetch('/warehouses', {
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

window.onload = () => {
    getWarehouses();
};
