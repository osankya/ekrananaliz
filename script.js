let allData = [], selectedStocks = JSON.parse(localStorage.getItem('selectedStocks')) || [];
let currentView = 'all';

async function init() {
    const res = await fetch('data.json');
    allData = await res.json();
    renderChart();
}

// Arama ve Filtreleme Mantığı
function filterAndShow() {
    const q = document.getElementById('mainSearch').value.toUpperCase();
    const resDiv = document.getElementById('search-results');
    
    if(q.length < 1) { resDiv.style.display = 'none'; return; }
    
    const flat = allData.flatMap(s => s.data);
    const filtered = flat.filter(h => h.x.includes(q));
    
    resDiv.innerHTML = filtered.map(h => `
        <div class="result-item ${selectedStocks.includes(h.x) ? 'selected' : ''}" onclick="toggleStock('${h.x}')">
            <span>${h.x}</span>
            <span>${selectedStocks.includes(h.x) ? '✅' : '+'}</span>
        </div>
    `).join('');
    resDiv.style.display = 'block';
}

function toggleStock(id) {
    if(selectedStocks.includes(id)) {
        selectedStocks = selectedStocks.filter(s => s !== id);
    } else {
        selectedStocks.push(id);
    }
    localStorage.setItem('selectedStocks', JSON.stringify(selectedStocks));
    filterAndShow(); // Listeyi güncelle
    if(currentView === 'mine') renderChart();
}

function renderChart() {
    let filtered = currentView === 'mine' ? 
        allData.map(s => ({name: s.name, data: s.data.filter(h => selectedStocks.includes(h.x))})).filter(s => s.data.length > 0) 
        : allData;

    const options = {
        series: filtered,
        chart: { type: 'treemap', height: '100%', toolbar: {show: false} },
        stroke: { show: true, width: 4, colors: ['#0a0b0d'] }, // Sektör araları siyah boşluk
        colors: [({ value, seriesIndex, dataPointIndex, w }) => {
            const c = w.config.series[seriesIndex].data[dataPointIndex].c;
            return c > 0 ? '#00c805' : '#ff3b30';
        }],
        plotOptions: {
            treemap: { distributed: true, enableShades: false }
        },
        dataLabels: {
            enabled: true,
            formatter: (text, op) => {
                const c = op.w.config.series[op.seriesIndex].data[op.dataPointIndex].c;
                return [text, c + "%"];
            }
        }
    };
    document.querySelector("#chart").innerHTML = "";
    new ApexCharts(document.querySelector("#chart"), options).render();
}