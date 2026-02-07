let allData = [], selectedStocks = JSON.parse(localStorage.getItem('selectedStocks')) || [];
let currentView = 'all';

async function init() {
    try {
        const res = await fetch('data.json');
        allData = await res.json();
        renderChart();
        // Arama kutusu dışına tıklayınca listeyi kapat
        document.addEventListener('click', (e) => {
            if (!e.target.closest('.search-wrapper')) document.getElementById('search-results').style.display = 'none';
        });
    } catch (e) {
        console.error("Veri hatası:", e);
        document.getElementById('chart').innerHTML = "<h2 style='text-align:center; margin-top:50px;'>Hata: data.json dosyası bulunamadı!</h2>";
    }
}

function filterAndShow() {
    const q = document.getElementById('mainSearch').value.toUpperCase();
    const resDiv = document.getElementById('search-results');
    
    if (q.length < 1) { resDiv.style.display = 'none'; return; }
    
    const flat = allData.flatMap(s => s.data.map(d => ({...d, sector: s.name})));
    const filtered = flat.filter(h => h.x.includes(q) || h.sector.includes(q));
    
    resDiv.innerHTML = filtered.map(h => {
        const isSel = selectedStocks.includes(h.x);
        return `
            <div class="result-item ${isSel ? 'selected' : ''}" onclick="toggleStock('${h.x}')">
                <div><b>${h.x}</b> <br> <span>${h.sector}</span></div>
                <div style="font-size:18px">${isSel ? '✅' : '+'}</div>
            </div>
        `;
    }).join('');
    resDiv.style.display = 'block';
}

function toggleStock(id) {
    if (selectedStocks.includes(id)) {
        selectedStocks = selectedStocks.filter(s => s !== id);
    } else {
        selectedStocks.push(id);
    }
    localStorage.setItem('selectedStocks', JSON.stringify(selectedStocks));
    filterAndShow(); 
    renderChart();
}

function renderChart() {
    let filtered = currentView === 'mine' ? 
        allData.map(s => ({
            name: s.name, 
            data: s.data.filter(h => selectedStocks.includes(h.x))
        })).filter(s => s.data.length > 0) 
        : allData;

    const options = {
        series: filtered,
        chart: { 
            type: 'treemap', 
            height: '100%', 
            toolbar: { show: false },
            background: '#0a0b0d'
        },
        // SEKTÖR ARALARI SİYAH BOŞLUK (COIN360 TARZI)
        stroke: { show: true, width: 4, colors: ['#0a0b0d'] },
        colors: [({ value, seriesIndex, dataPointIndex, w }) => {
            const stock = w.config.series[seriesIndex].data[dataPointIndex];
            return stock.c > 0 ? '#00c805' : '#ff3b30';
        }],
        plotOptions: {
            treemap: { distributed: true, enableShades: false }
        },
        dataLabels: {
            enabled: true,
            style: { fontSize: '14px', fontWeight: '900' },
            formatter: (text, op) => {
                const stock = op.w.config.series[op.seriesIndex].data[op.dataPointIndex];
                return [text, stock.c + "%"];
            }
        },
        theme: { mode: 'dark' },
        tooltip: {
            theme: 'dark',
            custom: function({ series, seriesIndex, dataPointIndex, w }) {
                const item = w.config.series[seriesIndex].data[dataPointIndex];
                return `<div style="padding:10px; background:#1b1e23; border:1px solid #2d2e33;">
                    <b style="font-size:16px">${item.x}</b><br>
                    Değişim: <span style="color:${item.c > 0 ? '#00c805':'#ff3b30'}">%${item.c}</span><br>
                    Ağırlık: Piyasa Değeri Odaklı
                </div>`;
            }
        }
    };

    const container = document.querySelector("#chart");
    container.innerHTML = "";
    new ApexCharts(container, options).render();
}

function setView(v) {
    currentView = v;
    document.getElementById('btn-all').classList.toggle('active', v === 'all');
    document.getElementById('btn-mine').classList.toggle('active', v === 'mine');
    renderChart();
}

init();