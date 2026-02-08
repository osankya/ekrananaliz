let allData = [], allStocks = [], currentView = 'bist100';

async function init() {
    try {
        const r1 = await fetch('data.json');
        allData = await r1.json();
        const r2 = await fetch('all_stocks.json');
        allStocks = await r2.json();
        renderChart();
    } catch (e) {
        console.error("Dosyalar bulunamadı. Önce Python scriptini çalıştırın.");
    }
}

function renderChart() {
    const displayData = (currentView === 'bist100') ? allData : allStocks;

    const options = {
        series: displayData,
        chart: {
            type: 'treemap',
            height: '100%',
            toolbar: { show: false },
            events: {
                dataPointSelection: (event, chartContext, config) => {
                    const stock = displayData[config.seriesIndex].data[config.dataPointIndex].x;
                    openDetail(stock);
                }
            }
        },
        // İSTEDİĞİN RENK MANTIĞI BURADA
        colors: [function({ value }) {
            if (value >= 3) return '#064e3b';      // Koyu Yeşil
            if (value > 0) return '#10b981';       // Açık Yeşil
            if (value <= -3) return '#7f1d1d';     // Koyu Kırmızı
            if (value < 0) return '#ef4444';       // Açık Kırmızı
            return '#4b5563';                      // Nötr (0)
        }],
        plotOptions: {
            treemap: {
                distributed: true,
                enableShades: false,
                dataLabels: { format: 'scale' }
            }
        },
        dataLabels: {
            enabled: true,
            style: { fontSize: '14px', fontWeight: 'bold' },
            formatter: (text, op) => [text, op.value + "%"]
        },
        tooltip: { theme: 'dark' }
    };

    const chartDiv = document.querySelector("#chart");
    chartDiv.innerHTML = "";
    const chart = new ApexCharts(chartDiv, options);
    chart.render();
}

async function openDetail(stock) {
    document.getElementById('detailTitle').innerText = stock + " Detay Grafiği";
    document.getElementById('detailModal').style.display = 'flex';
    document.getElementById('ov').style.display = 'block';

    const symbol = stock + ".IS";
    // Yahoo Finance CORS hatasını aşmak için (Sadece candlestick verisi için proxy kullanımı)
    // Eğer veri yüklenmiyorsa tarayıcıda geçici olarak CORS izinlerini açmak gerekebilir 
    // veya Python ile bu veriyi önceden çekmek en sağlıklısıdır.
    try {
        const response = await fetch(`https://query1.finance.yahoo.com/v8/finance/chart/${symbol}?range=1d&interval=5m`);
        const data = await response.json();
        const res = data.chart.result[0];
        const seriesData = res.timestamp.map((t, i) => ({
            x: new Date(t * 1000),
            y: [res.indicators.quote[0].open[i], res.indicators.quote[0].high[i], res.indicators.quote[0].low[i], res.indicators.quote[0].close[i]]
        })).filter(d => d.y[3] != null);

        const options = {
            series: [{ data: seriesData }],
            chart: { type: 'candlestick', height: '100%', theme: 'dark' },
            xaxis: { type: 'datetime' }
        };

        const detailDiv = document.querySelector("#detailChart");
        detailDiv.innerHTML = "";
        new ApexCharts(detailDiv, options).render();
    } catch (e) {
        document.getElementById('detailChart').innerHTML = "<p style='text-align:center; padding-top:50px;'>Veri çekilemedi. (Tarayıcı CORS engeli veya Yahoo API kısıtlaması)</p>";
    }
}

function closeDetail() {
    document.getElementById('detailModal').style.display = 'none';
    document.getElementById('ov').style.display = 'none';
}

function changeView(v) {
    currentView = v;
    document.getElementById('btn-bist100').className = v === 'bist100' ? 'active' : '';
    document.getElementById('btn-mine').className = v === 'mine' ? 'active' : '';
    renderChart();
}

init();