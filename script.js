let allData = [];
let selectedStocks = JSON.parse(localStorage.getItem('selectedStocks')) || [];
let currentView = 'all';

async function init() {
    const chartDiv = document.querySelector("#chart");
    try {
        const res = await fetch('data.json');
        allData = await res.json();
        if (allData.length > 0) renderChart();
        else chartDiv.innerHTML = "Veri boş. Lütfen data_fetcher.py çalıştırın.";
    } catch (e) {
        chartDiv.innerHTML = "data.json bulunamadı! Lütfen veriyi yükleyin.";
    }
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
        chart: { type: 'treemap', height: '100%', toolbar: {show: false}, background: '#0a0b0d' },
        stroke: { show: true, width: 3, colors: ['#000'] }, // Sektör ayırıcı siyahlar
        colors: [({ value, seriesIndex, dataPointIndex, w }) => {
            const stock = w.config.series[seriesIndex].data[dataPointIndex];
            return stock.c > 0 ? '#00c805' : '#ff3b30';
        }],
        plotOptions: { treemap: { distributed: true, enableShades: false } },
        dataLabels: {
            enabled: true,
            formatter: (text, op) => [text, op.w.config.series[op.seriesIndex].data[op.dataPointIndex].c + "%"]
        },
        theme: { mode: 'dark' }
    };

    document.querySelector("#chart").innerHTML = "";
    new ApexCharts(document.querySelector("#chart"), options).render();
}

function setView(v) {
    currentView = v;
    document.getElementById('btn-all').className = v === 'all' ? 'active' : '';
    document.getElementById('btn-mine').className = v === 'mine' ? 'active' : '';
    renderChart();
}

init();