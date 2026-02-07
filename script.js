let allData = [], selectedStocks = JSON.parse(localStorage.getItem('selectedStocks')) || [], currentView = 'all';

async function init() {
    const res = await fetch('data.json');
    allData = await res.json();
    renderChart();
    renderStockList();
    updateCount();
}

function renderChart() {
    // Sektörler arası siyah kalın çizgiler için stroke ayarı
    let filtered = currentView === 'mine' ? 
        allData.map(s => ({name: s.name, data: s.data.filter(h => selectedStocks.includes(h.x))})).filter(s => s.data.length > 0) 
        : allData;

    const options = {
        series: filtered,
        chart: { type: 'treemap', height: '100%', toolbar: { show: false }, background: 'transparent' },
        stroke: { show: true, width: 4, colors: ['#0a0b0d'] }, // COIN360 TARZI SİYAH BÖLMELER
        colors: [({ value }) => value > 0 ? '#00c805' : '#ff3b30'],
        plotOptions: {
            treemap: { distributed: true, enableShades: false }
        },
        dataLabels: {
            enabled: true,
            style: { fontSize: '15px', fontWeight: '900' },
            formatter: (text, op) => [text, op.value + "%"]
        },
        tooltip: { theme: 'dark', y: { formatter: v => "% " + v } },
        theme: { mode: 'dark' }
    };

    document.querySelector("#chart").innerHTML = "";
    new ApexCharts(document.querySelector("#chart"), options).render();
}

// LİSTELEME VE FİLTRELEME SİSTEMİ
function renderStockList() {
    const list = document.getElementById('stock-list');
    list.innerHTML = "";
    
    allData.forEach(sector => {
        sector.data.forEach(stock => {
            const isSel = selectedStocks.includes(stock.x);
            const row = document.createElement('div');
            row.className = `stock-row ${isSel ? 'selected' : ''}`;
            row.id = `row-${stock.x}`;
            row.onclick = () => toggleStock(stock.x);
            row.innerHTML = `
                <div class="stock-info">
                    <span class="stock-symbol">${stock.x}</span>
                    <span class="stock-sector">${sector.name}</span>
                </div>
                <div class="checkbox-custom"></div>
            `;
            list.appendChild(row);
        });
    });
}

function filterStocks() {
    const q = document.getElementById('searchBox').value.toUpperCase();
    const rows = document.querySelectorAll('.stock-row');
    rows.forEach(row => {
        const text = row.innerText.toUpperCase();
        row.style.display = text.includes(q) ? 'flex' : 'none';
    });
}

function toggleStock(id) {
    if (selectedStocks.includes(id)) {
        selectedStocks = selectedStocks.filter(s => s !== id);
        document.getElementById(`row-${id}`).classList.remove('selected');
    } else {
        selectedStocks.push(id);
        document.getElementById(`row-${id}`).classList.add('selected');
    }
    updateCount();
}

function updateCount() {
    document.getElementById('selected-count').innerText = `${selectedStocks.length} Hisse Seçildi`;
}

function saveSelection() {
    localStorage.setItem('selectedStocks', JSON.stringify(selectedStocks));
    closeModal();
    if (currentView === 'mine') renderChart();
}

// GÖRÜNÜM DEĞİŞTİRME
function setView(v) {
    currentView = v;
    document.getElementById('btn-all').classList.toggle('active', v === 'all');
    document.getElementById('btn-mine').classList.toggle('active', v === 'mine');
    renderChart();
}

function openModal() { document.getElementById('modal').style.display = 'flex'; document.getElementById('overlay').style.display = 'block'; }
function closeModal() { document.getElementById('modal').style.display = 'none'; document.getElementById('overlay').style.display = 'none'; }

init();