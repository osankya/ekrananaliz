let allData = [], fearScore = 50;

async function init() {
    try {
        const r1 = await fetch('data.json');
        allData = await r1.json();
        const r2 = await fetch('fear_index.json');
        const f = await r2.json();
        fearScore = f.score;
        renderChart();
    } catch (e) {
        console.error("Veri yükleme hatası!");
    }
}

function renderChart() {
    const processedData = allData.map(sector => ({
        name: sector.name,
        data: sector.data.map(s => {
            // RENK MANTIĞI: ASLA ŞAŞMAZ
            let c = '#4b5563'; // Nötr
            if (s.y >= 3) c = '#064e3b';        // KOYU YEŞİL
            else if (s.y > 0) c = '#10b981';    // AÇIK YEŞİL
            else if (s.y <= -3) c = '#7f1d1d';  // KOYU KIRMIZI
            else if (s.y < 0) c = '#ef4444';    // AÇIK KIRMIZI
            
            return { x: s.x, y: s.y, fillColor: c };
        })
    }));

    const options = {
        series: processedData,
        chart: {
            type: 'treemap',
            height: '100%',
            toolbar: { show: false },
            events: {
                dataPointSelection: (e, chart, config) => {
                    const stock = processedData[config.seriesIndex].data[config.dataPointIndex].x;
                    openDetail(stock);
                }
            }
        },
        plotOptions: { treemap: { distributed: true, enableShades: false } },
        dataLabels: {
            enabled: true,
            formatter: (text, op) => [text, op.value + "%"],
            style: { fontSize: '12px' }
        }
    };

    const container = document.querySelector("#chart");
    container.innerHTML = "";
    new ApexCharts(container, options).render();
}

async function openDetail(s) {
    const modal = document.getElementById('detailModal');
    modal.style.display = 'flex';
    document.getElementById('modalTitle').innerText = s;
    const dChart = document.getElementById('detailChart');
    dChart.innerHTML = "Yükleniyor...";

    try {
        // AllOrigins Proxy kullanarak Yahoo CORS engelini aşma
        const resp = await fetch(`https://api.allorigins.win/raw?url=${encodeURIComponent(`https://query1.finance.yahoo.com/v8/finance/chart/${s}.IS?range=1d&interval=5m`)}`);
        const data = await resp.json();
        const res = data.chart.result[0];
        const seriesData = res.timestamp.map((t, i) => ({
            x: new Date(t * 1000),
            y: [res.indicators.quote[0].open[i], res.indicators.quote[0].high[i], res.indicators.quote[0].low[i], res.indicators.quote[0].close[i]]
        })).filter(d => d.y[0] != null);

        dChart.innerHTML = "";
        new ApexCharts(dChart, {
            series: [{ data: seriesData }],
            chart: { type: 'candlestick', height: '100%', theme: 'dark' },
            xaxis: { type: 'datetime' }
        }).render();
    } catch (e) { dChart.innerHTML = "Veri çekilemedi."; }
}

function openFear() {
    const m = document.getElementById('fearModal');
    m.style.display = 'flex';
    new ApexCharts(document.getElementById('fearGauge'), {
        series: [fearScore],
        chart: { type: 'radialBar', height: 300 },
        plotOptions: { radialBar: { startAngle: -135, endAngle: 135, dataLabels: { name: { show: false }, value: { fontSize: '30px', color: '#fff' } } } },
        fill: { colors: [fearScore > 50 ? '#10b981' : '#ef4444'] },
        labels: ['Korku Endeksi']
    }).render();
}

function closeModal(id) { document.getElementById(id).style.display = 'none'; }

init();