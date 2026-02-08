let allD = [], allStocks = [], sel = JSON.parse(localStorage.getItem('sel')) || [], 
    view = 'bist100', currentStock = null, currentTime = '1d', detailChartObj = null, fearData = null;

async function init() {
    try {
        allD = await (await fetch('data.json')).json();
        allStocks = await (await fetch('all_stocks.json')).json();
        fearData = await (await fetch('fear_index.json')).json();
        if (sel.length === 0) sel = ["THYAO", "ASELS", "AKBNK"];
        upd(); list();
    } catch (e) { console.error(e); }
}

function getColor(val) {
    // TAM DÜZGÜN RENK SİSTEMİ
    const value = parseFloat(val);
    if (isNaN(value)) return '#6b7280';
    if (value === 0) return '#6b7280';                    // 0% = GRİ
    if (value > 0 && value <= 3) return '#7fd4a8';       // 0-3% = AÇIK YEŞİL
    if (value > 3) return '#16c784';                      // 3%+ = KOYU YEŞİL
    if (value < 0 && value >= -3) return '#f58a8f';      // 0 ila -3% = AÇIK KIRMIZI
    if (value < -3) return '#ea3943';                     // -3% ALTI = KOYU KIRMIZI
    return '#6b7280';
}

function upd() {
    let f = view === 'bist100' ? allD : allStocks.map(s => ({
        name: s.name, data: s.data.filter(h => sel.includes(h.x))
    })).filter(s => s.data.length > 0);

    const o = {
        series: f,
        chart: { 
            type: 'treemap', 
            height: '100%', 
            toolbar: { show: false },
            background: 'transparent',
            events: {
                dataPointSelection: (e, ctx, cfg) => openDetail(f[cfg.seriesIndex].data[cfg.dataPointIndex].x)
            }
        },
        stroke: { show: true, width: 6, colors: ['#0a0e27'] },
        colors: [({ value }) => getColor(value)],
        plotOptions: { treemap: { distributed: true, enableShades: false } },
        dataLabels: {
            enabled: true,
            style: { fontSize: '24px', fontWeight: '900', colors: ['#fff'] },
            formatter: (text, op) => [text, op.value + "%"]
        },
        tooltip: { enabled: false },
        theme: { mode: 'dark' }
    };
    document.querySelector("#chart").innerHTML = "";
    new ApexCharts(document.querySelector("#chart"), o).render();
}

function showFearIndex() {
    document.getElementById('chart').style.display = 'none';
    document.getElementById('fearPage').style.display = 'block';
    if (!fearData) return;
    
    document.getElementById('fearScoreNum').textContent = fearData.score;
    document.getElementById('fearScoreText').textContent = fearData.status;
    document.querySelector('.fear-score-number').style.color = getColor(fearData.score - 50);
    
    const c = fearData.components;
    document.getElementById('fearComponents').innerHTML = `
        <div class="component-card"><h3>Momentum</h3><div class="value" style="color:${getColor(c.momentum-50)}">${c.momentum}</div></div>
        <div class="component-card"><h3>Volatilite</h3><div class="value" style="color:${getColor(c.volatility-50)}">${c.volatility}</div></div>
        <div class="component-card"><h3>Hacim</h3><div class="value" style="color:${getColor(c.volume-50)}">${c.volume}</div></div>
        <div class="component-card"><h3>Genişlik</h3><div class="value" style="color:${getColor(c.breadth-50)}">${c.breadth}</div></div>`;
    
    document.getElementById('fearHistoryChart').innerHTML = '';
    new ApexCharts(document.querySelector("#fearHistoryChart"), {
        series: [{name: 'Endeks', data: fearData.data.map(d => d.score)}],
        chart: {type: 'area', height: 300, background: 'transparent', toolbar: {show: false}},
        stroke: {curve: 'smooth', width: 3},
        fill: {type: 'gradient', gradient: {opacityFrom: 0.7, opacityTo: 0.2}},
        colors: ['#16c784'],
        xaxis: {categories: fearData.data.map(d => d.date), labels: {style: {colors: '#9ca3af'}, rotate: -45}},
        yaxis: {min: 0, max: 100, labels: {style: {colors: '#9ca3af'}}},
        grid: {borderColor: '#1e2639'},
        title: {text: 'Son 30 Gün', style: {color: '#fff', fontSize: '18px', fontWeight: 700}},
        theme: {mode: 'dark'}
    }).render();
}

function showHeatmap() {
    document.getElementById('chart').style.display = 'block';
    document.getElementById('fearPage').style.display = 'none';
}

async function openDetail(stock) {
    currentStock = stock;
    document.getElementById('detailTitle').textContent = stock;
    document.getElementById('detailModal').style.display = 'flex';
    document.getElementById('detailOv').style.display = 'block';
    loadDetailChart();
}

function closeDetail() {
    document.getElementById('detailModal').style.display = 'none';
    document.getElementById('detailOv').style.display = 'none';
}

async function changeTime(p) {
    currentTime = p;
    ['1d','5d','1mo','3mo','6mo','1y','5y'].forEach(t => {
        const b = document.getElementById('t-'+t);
        if(b) b.classList.toggle('active', t===p);
    });
    loadDetailChart();
}

async function loadDetailChart() {
    document.getElementById('detailChart').innerHTML = '<div style="text-align:center;padding:100px;color:#9ca3af;">⏳ Yükleniyor...</div>';
    
    // PYTHON'DAN VERİ ÇEKELİM - BROWSER'DA ÇALIŞMAZ
    document.getElementById('detailChart').innerHTML = `
        <div style="text-align:center;padding:100px;">
            <div style="font-size:48px;margin-bottom:20px;">📊</div>
            <div style="font-size:20px;font-weight:700;margin-bottom:10px;">${currentStock}</div>
            <div style="color:#9ca3af;margin-bottom:30px;">Grafik verisi sunucudan çekilemedi</div>
            <div style="color:#9ca3af;font-size:14px;">Python backend gerekiyor - şu an sadece heatmap aktif</div>
        </div>`;
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
    let html = '';
    allStocks.forEach(s => {
        html += `<div class="sector-group"><div class="sector-title">${s.name}</div>`;
        s.data.forEach(h => {
            html += `<div class="stock-row" onclick="toggle('${h.x}')">
                <div class="stock-info">
                    <span class="stock-code">${h.x}</span>
                    <span class="stock-sector">${s.name}</span>
                </div>
                <input type="checkbox" id="chk-${h.x}" ${sel.includes(h.x)?'checked':''} onclick="event.stopPropagation()">
            </div>`;
        });
        html += `</div>`;
    });
    document.getElementById('stock-list').innerHTML = html;
}

function toggle(id) { document.getElementById('chk-'+id).checked = !document.getElementById('chk-'+id).checked; }

function fltr() {
    let q = document.getElementById('srch').value.toUpperCase();
    document.querySelectorAll('.sector-group').forEach(g => {
        let vis = false;
        g.querySelectorAll('.stock-row').forEach(r => {
            const m = r.innerText.toUpperCase().includes(q);
            r.style.display = m ? 'flex' : 'none';
            if(m) vis = true;
        });
        g.style.display = vis ? 'block' : 'none';
    });
}

function save() {
    sel = Array.from(document.querySelectorAll('#stock-list input:checked')).map(c => c.id.replace('chk-',''));
    localStorage.setItem('sel', JSON.stringify(sel));
    closeM();
    if(view === 'mine') upd();
}

function changeV(v) {
    view = v;
    document.getElementById('b-bist100').classList.toggle('active', v==='bist100');
    document.getElementById('b-mine').classList.toggle('active', v==='mine');
    upd();
}

init();