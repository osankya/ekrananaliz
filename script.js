let allD = [],           
    allStocks = [],      
    sel = JSON.parse(localStorage.getItem('sel')) || [], 
    view = 'bist100',
    currentStock = null,
    currentTime = '1d',
    detailChartObj = null,
    fearData = null;

async function init() {
    try {
        const r1 = await fetch('data.json');
        allD = await r1.json();
        
        const r2 = await fetch('all_stocks.json');
        allStocks = await r2.json();
        
        const r3 = await fetch('fear_index.json');
        fearData = await r3.json();
        
        if (sel.length === 0) {
            sel = ["THYAO", "ASELS", "SASA", "AKBNK", "GARAN"];
            localStorage.setItem('sel', JSON.stringify(sel));
        }
        
        upd();
        list();
    } catch (e) { 
        console.error("Veri yüklenemedi!", e); 
    }
}

function upd() {
    let f;
    
    if (view === 'bist100') {
        f = allD;
    } else {
        f = allStocks.map(s => ({
            name: s.name, 
            data: s.data.filter(h => sel.includes(h.x))
        })).filter(s => s.data.length > 0);
    }

    const o = {
        series: f,
        chart: { 
            type: 'treemap', 
            height: '100%', 
            toolbar: { show: false },
            background: 'transparent',
            animations: {
                enabled: true,
                speed: 600
            },
            events: {
                dataPointSelection: function(event, chartContext, config) {
                    const seriesIndex = config.seriesIndex;
                    const dataPointIndex = config.dataPointIndex;
                    const stock = f[seriesIndex].data[dataPointIndex].x;
                    openDetail(stock);
                }
            }
        },
        stroke: {
            show: true,
            width: 5,
            colors: ['#0a0e27']
        },
        // YENİ RENK SİSTEMİ:
        // 0 ila 3: Açık Yeşil
        // 3+: Koyu Yeşil
        // 0 ila -3: Açık Kırmızı
        // -3 ve altı: Koyu Kırmızı
        colors: [({ value }) => {
            if (value >= 3) return '#16c784';        // Koyu Yeşil (3%+)
            if (value > 0) return '#7fd4a8';         // Açık Yeşil (0-3%)
            if (value === 0) return '#6b7280';       // Gri (0%)
            if (value > -3) return '#f58a8f';        // Açık Kırmızı (0 ila -3%)
            return '#ea3943';                         // Koyu Kırmızı (-3% altı)
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
            style: { 
                fontSize: '22px',  // Daha büyük
                fontWeight: '900',
                fontFamily: 'Inter, sans-serif',
                colors: ['#ffffff']
            },
            formatter: (text, op) => [text, op.value + "%"]
        },
        theme: { mode: 'dark' },
        tooltip: { 
            enabled: false
        }
    };

    document.querySelector("#chart").innerHTML = "";
    new ApexCharts(document.querySelector("#chart"), o).render();
}

// Korku Endeksi Sayfası
function showFearIndex() {
    document.getElementById('chart').style.display = 'none';
    document.getElementById('fearPage').style.display = 'block';
    
    if (!fearData) return;
    
    // Skor göster
    document.getElementById('fearScoreNum').textContent = fearData.score;
    document.getElementById('fearScoreText').textContent = fearData.status;
    
    // Renk ayarla
    const scoreEl = document.querySelector('.fear-score-number');
    if (fearData.score >= 75) scoreEl.style.color = '#16c784';
    else if (fearData.score >= 55) scoreEl.style.color = '#7fd4a8';
    else if (fearData.score >= 45) scoreEl.style.color = '#6b7280';
    else if (fearData.score >= 25) scoreEl.style.color = '#f58a8f';
    else scoreEl.style.color = '#ea3943';
    
    // Bileşenler
    const components = fearData.components;
    document.getElementById('fearComponents').innerHTML = `
        <div class="component-card">
            <h3>Momentum</h3>
            <div class="value" style="color: ${getColorForScore(components.momentum)}">${components.momentum}</div>
        </div>
        <div class="component-card">
            <h3>Volatilite</h3>
            <div class="value" style="color: ${getColorForScore(components.volatility)}">${components.volatility}</div>
        </div>
        <div class="component-card">
            <h3>Hacim</h3>
            <div class="value" style="color: ${getColorForScore(components.volume)}">${components.volume}</div>
        </div>
        <div class="component-card">
            <h3>Piyasa Genişliği</h3>
            <div class="value" style="color: ${getColorForScore(components.breadth)}">${components.breadth}</div>
        </div>
    `;
    
    // Tarihsel grafik
    const dates = fearData.data.map(d => d.date);
    const scores = fearData.data.map(d => d.score);
    
    const chartOptions = {
        series: [{
            name: 'Korku & Açgözlülük',
            data: scores
        }],
        chart: {
            type: 'area',
            height: 300,
            background: 'transparent',
            toolbar: { show: false }
        },
        stroke: {
            curve: 'smooth',
            width: 3
        },
        fill: {
            type: 'gradient',
            gradient: {
                shadeIntensity: 1,
                opacityFrom: 0.7,
                opacityTo: 0.2,
            }
        },
        colors: ['#16c784'],
        xaxis: {
            categories: dates,
            labels: { 
                style: { colors: '#9ca3af' },
                rotate: -45
            }
        },
        yaxis: {
            min: 0,
            max: 100,
            labels: { style: { colors: '#9ca3af' } }
        },
        grid: {
            borderColor: '#1e2639'
        },
        title: {
            text: 'Son 30 Gün',
            style: {
                color: '#fff',
                fontSize: '18px',
                fontWeight: 700
            }
        },
        theme: { mode: 'dark' }
    };
    
    document.getElementById('fearHistoryChart').innerHTML = '';
    new ApexCharts(document.querySelector("#fearHistoryChart"), chartOptions).render();
}

function getColorForScore(score) {
    if (score >= 75) return '#16c784';
    if (score >= 55) return '#7fd4a8';
    if (score >= 45) return '#6b7280';
    if (score >= 25) return '#f58a8f';
    return '#ea3943';
}

function showHeatmap() {
    document.getElementById('chart').style.display = 'block';
    document.getElementById('fearPage').style.display = 'none';
}

// Detay sayfası
async function openDetail(stock) {
    currentStock = stock;
    document.getElementById('detailTitle').textContent = stock;
    document.getElementById('detailModal').style.display = 'flex';
    document.getElementById('detailOv').style.display = 'block';
    
    await loadDetailChart();
}

function closeDetail() {
    document.getElementById('detailModal').style.display = 'none';
    document.getElementById('detailOv').style.display = 'none';
}

async function changeTime(period) {
    currentTime = period;
    
    ['1d', '5d', '1mo', '3mo', '6mo', '1y', '5y'].forEach(p => {
        const btn = document.getElementById('t-' + p);
        if (btn) btn.classList.toggle('active', p === period);
    });
    
    await loadDetailChart();
}

async function loadDetailChart() {
    const loadingHTML = '<div style="text-align:center; padding:100px; color:#9ca3af;"><div style="font-size:24px; margin-bottom:10px;">⏳</div><div>Grafik yükleniyor...</div></div>';
    document.getElementById('detailChart').innerHTML = loadingHTML;
    
    try {
        const symbol = currentStock + ".IS";
        
        // İnterval ayarla
        let interval = '1d';
        if (currentTime === '1d') interval = '5m';
        else if (currentTime === '5d') interval = '15m';
        else if (currentTime === '1mo') interval = '1h';
        
        const url = `https://query1.finance.yahoo.com/v8/finance/chart/${symbol}?range=${currentTime}&interval=${interval}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (!data.chart || !data.chart.result || !data.chart.result[0]) {
            throw new Error('Veri bulunamadı');
        }
        
        const result = data.chart.result[0];
        const timestamps = result.timestamp;
        const prices = result.indicators.quote[0];
        
        if (!timestamps || !prices) {
            throw new Error('Fiyat verisi yok');
        }
        
        const series = timestamps.map((t, i) => {
            const open = prices.open[i];
            const high = prices.high[i];
            const low = prices.low[i];
            const close = prices.close[i];
            
            // Null değerleri filtrele
            if (open === null || high === null || low === null || close === null) {
                return null;
            }
            
            return {
                x: new Date(t * 1000),
                y: [open, high, low, close]
            };
        }).filter(s => s !== null);
        
        if (series.length === 0) {
            throw new Error('Geçerli veri yok');
        }
        
        const options = {
            series: [{
                name: currentStock,
                data: series
            }],
            chart: {
                type: 'candlestick',
                height: 500,
                background: 'transparent',
                toolbar: { 
                    show: true,
                    tools: {
                        download: true,
                        zoom: true,
                        zoomin: true,
                        zoomout: true,
                        pan: true,
                        reset: true
                    }
                }
            },
            plotOptions: {
                candlestick: {
                    colors: {
                        upward: '#16c784',
                        downward: '#ea3943'
                    },
                    wick: {
                        useFillColor: true
                    }
                }
            },
            xaxis: {
                type: 'datetime',
                labels: { 
                    style: { colors: '#9ca3af' },
                    datetimeFormatter: {
                        year: 'yyyy',
                        month: 'MMM yyyy',
                        day: 'dd MMM',
                        hour: 'HH:mm'
                    }
                }
            },
            yaxis: {
                tooltip: { enabled: true },
                labels: { 
                    style: { colors: '#9ca3af' },
                    formatter: (val) => val ? val.toFixed(2) + ' ₺' : ''
                }
            },
            grid: {
                borderColor: '#1e2639'
            },
            tooltip: {
                theme: 'dark',
                x: {
                    format: 'dd MMM yyyy HH:mm'
                }
            },
            theme: { mode: 'dark' }
        };
        
        document.getElementById('detailChart').innerHTML = '';
        detailChartObj = new ApexCharts(document.querySelector("#detailChart"), options);
        await detailChartObj.render();
        
    } catch (e) {
        console.error("Grafik hatası:", e);
        document.getElementById('detailChart').innerHTML = `
            <div style="text-align:center; padding:100px; color:#ea3943;">
                <div style="font-size:48px; margin-bottom:20px;">⚠️</div>
                <div style="font-size:20px; font-weight:700; margin-bottom:10px;">Grafik Yüklenemedi</div>
                <div style="color:#9ca3af;">${e.message || 'Bir hata oluştu'}</div>
                <button onclick="loadDetailChart()" style="margin-top:20px; padding:12px 24px; background:#16c784; border:none; border-radius:8px; color:#000; font-weight:700; cursor:pointer;">Tekrar Dene</button>
            </div>
        `;
    }
}

function openM() { 
    document.getElementById('modal').style.display = 'flex'; 
    document.getElementById('ov').style.display = 'block'; 
}

function closeM() { 
    document.getElementById('modal').style.display = 'none'; 
    document.getElementById('ov').style.display = 'none'; 
}

function list() {
    const l = document.getElementById('stock-list');
    let html = '';
    
    allStocks.forEach(sector => {
        html += `<div class="sector-group">`;
        html += `<div class="sector-title">${sector.name}</div>`;
        
        sector.data.forEach(h => {
            html += `
                <div class="stock-row" onclick="toggle('${h.x}')">
                    <div class="stock-info">
                        <span class="stock-code">${h.x}</span>
                        <span class="stock-sector">${sector.name}</span>
                    </div>
                    <input type="checkbox" 
                           id="chk-${h.x}" 
                           data-sector="${sector.name}"
                           ${sel.includes(h.x) ? 'checked' : ''} 
                           onclick="event.stopPropagation()">
                </div>
            `;
        });
        
        html += `</div>`;
    });
    
    l.innerHTML = html;
}

function toggle(id) {
    const c = document.getElementById('chk-' + id);
    c.checked = !c.checked;
}

function fltr() {
    let q = document.getElementById('srch').value.toUpperCase();
    
    document.querySelectorAll('.sector-group').forEach(group => {
        let hasVisibleStock = false;
        
        group.querySelectorAll('.stock-row').forEach(row => {
            const code = row.querySelector('.stock-code').textContent;
            const sector = row.querySelector('.stock-sector').textContent;
            const matches = code.includes(q) || sector.toUpperCase().includes(q);
            
            row.style.display = matches ? 'flex' : 'none';
            if (matches) hasVisibleStock = true;
        });
        
        group.style.display = hasVisibleStock ? 'block' : 'none';
    });
}

function save() {
    sel = Array.from(document.querySelectorAll('#stock-list input:checked'))
           .map(c => c.id.replace('chk-', ''));
    localStorage.setItem('sel', JSON.stringify(sel));
    closeM();
    if (view === 'mine') upd();
}

function changeV(v) {
    view = v;
    document.getElementById('b-bist100').classList.toggle('active', v === 'bist100');
    document.getElementById('b-mine').classList.toggle('active', v === 'mine');
    upd();
}

init();