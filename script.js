let allD = [],           
    allStocks = [],      
    sel = JSON.parse(localStorage.getItem('sel')) || [], 
    view = 'bist100',
    currentStock = null,
    currentTime = '1d',
    detailChartObj = null;

async function init() {
    try {
        const r1 = await fetch('data.json');
        allD = await r1.json();
        
        const r2 = await fetch('all_stocks.json');
        allStocks = await r2.json();
        
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
        // DÜZELTME: 0 = Gri, Pozitif = Yeşil, Negatif = Kırmızı
        colors: [({ value }) => {
            if (value === 0) return '#6b7280';      // Gri (nötr)
            if (value > 0) return '#16c784';        // Yeşil (pozitif)
            return '#ea3943';                        // Kırmızı (negatif)
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
                fontSize: '20px',  // Daha büyük yazı
                fontWeight: '900',
                fontFamily: 'Inter, sans-serif',
                colors: ['#ffffff']
            },
            formatter: (text, op) => [text, op.value + "%"]
        },
        theme: { mode: 'dark' },
        tooltip: { 
            enabled: false  // TOOLTIP KAPALI
        }
    };

    document.querySelector("#chart").innerHTML = "";
    new ApexCharts(document.querySelector("#chart"), o).render();
}

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
    
    ['1d', '1mo', '6mo', '1y', '5y'].forEach(p => {
        document.getElementById('t-' + p).classList.toggle('active', p === period);
    });
    
    await loadDetailChart();
}

async function loadDetailChart() {
    try {
        const symbol = currentStock + ".IS";
        const response = await fetch(`https://query1.finance.yahoo.com/v8/finance/chart/${symbol}?range=${currentTime}&interval=${currentTime === '1d' ? '5m' : '1d'}`);
        const data = await response.json();
        
        if (!data.chart || !data.chart.result || !data.chart.result[0]) {
            throw new Error('Veri yok');
        }
        
        const timestamps = data.chart.result[0].timestamp;
        const prices = data.chart.result[0].indicators.quote[0];
        
        const series = timestamps.map((t, i) => ({
            x: new Date(t * 1000),
            y: [prices.open[i], prices.high[i], prices.low[i], prices.close[i]]
        })).filter(s => s.y.every(v => v !== null && v !== undefined));
        
        const options = {
            series: [{
                name: currentStock,
                data: series
            }],
            chart: {
                type: 'candlestick',
                height: 500,
                background: 'transparent',
                toolbar: { show: true }
            },
            plotOptions: {
                candlestick: {
                    colors: {
                        upward: '#16c784',
                        downward: '#ea3943'
                    }
                }
            },
            xaxis: {
                type: 'datetime',
                labels: { style: { colors: '#9ca3af' } }
            },
            yaxis: {
                tooltip: { enabled: true },
                labels: { 
                    style: { colors: '#9ca3af' },
                    formatter: (val) => val.toFixed(2)
                }
            },
            grid: {
                borderColor: '#1e2639'
            },
            theme: { mode: 'dark' }
        };
        
        document.getElementById('detailChart').innerHTML = '';
        detailChartObj = new ApexCharts(document.querySelector("#detailChart"), options);
        detailChartObj.render();
        
    } catch (e) {
        console.error("Grafik yüklenemedi:", e);
        document.getElementById('detailChart').innerHTML = '<p style="text-align:center; padding:50px; color:#9ca3af;">Veri yüklenemedi. Lütfen tekrar deneyin.</p>';
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