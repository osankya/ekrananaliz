let allData = []; // API'den gelen ham veri
let selectedStocks = JSON.parse(localStorage.getItem('selectedStocks')) || ["THYAO", "ASELS", "SASA"];
let currentView = 'all';

async function loadData() {
    const res = await fetch('data.json');
    allData = await res.json();
    updateChart();
    renderStockList();
}

function updateChart() {
    let filteredData;
    
    if (currentView === 'mine') {
        // Sadece seçili hisseleri filtrele ama sektörel yapıyı bozma
        filteredData = allData.map(sektor => ({
            name: sektor.name,
            data: sektor.data.filter(hisse => selectedStocks.includes(hisse.x))
        })).filter(sektor => sektor.data.length > 0);
    } else {
        filteredData = allData;
    }

    const options = {
        series: filteredData,
        legend: { show: false },
        chart: { type: 'treemap', height: '100%', toolbar: { show: false } },
        colors: [({ value }) => value > 0 ? '#0ecb81' : '#f6465d'],
        plotOptions: {
            treemap: { distributed: true, enableShades: false }
        },
        tooltip: { theme: 'dark' }
    };

    document.querySelector("#chart").innerHTML = "";
    const chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();
}

// Modal ve Arama İşlemleri
function openModal() {
    document.getElementById('selection-modal').style.display = 'flex';
    document.getElementById('overlay').style.display = 'block';
}

function closeModal() {
    document.getElementById('selection-modal').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}

function renderStockList() {
    const list = document.getElementById('stock-list');
    list.innerHTML = "";
    
    // Tüm hisseleri düz listeye çevir
    const flatStocks = allData.flatMap(s => s.data);

    flatStocks.forEach(stock => {
        const isChecked = selectedStocks.includes(stock.x) ? 'checked' : '';
        const item = document.createElement('div');
        item.className = 'stock-item';
        item.innerHTML = `
            <input type="checkbox" id="check-${stock.x}" ${isChecked} value="${stock.x}">
            <label for="check-${stock.x}">${stock.x}</label>
        `;
        list.appendChild(item);
    });
}

function filterStocks() {
    const query = document.getElementById('stock-search').value.toUpperCase();
    const items = document.querySelectorAll('.stock-item');
    items.forEach(item => {
        const text = item.innerText.toUpperCase();
        item.style.display = text.includes(query) ? 'flex' : 'none';
    });
}

function saveSelection() {
    const checkboxes = document.querySelectorAll('#stock-list input[type="checkbox"]:checked');
    selectedStocks = Array.from(checkboxes).map(cb => cb.value);
    localStorage.setItem('selectedStocks', JSON.stringify(selectedStocks));
    closeModal();
    if(currentView === 'mine') updateChart();
}

function setView(view) {
    currentView = view;
    document.getElementById('btn-all').classList.toggle('active', view === 'all');
    document.getElementById('btn-mine').classList.toggle('active', view === 'mine');
    updateChart();
}

loadData();