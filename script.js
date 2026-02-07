let allD = [], sel = JSON.parse(localStorage.getItem('sel')) || ["THYAO", "ASELS", "SASA"], view = 'all';

async function init() {
    try {
        const r = await fetch('data.json');
        allD = await r.json();
        upd();
        list();
    } catch (e) { console.error("Veri yüklenemedi!"); }
}

function upd() {
    let f = view === 'mine' ? 
        allD.map(s => ({name: s.name, data: s.data.filter(h => sel.includes(h.x))})).filter(s => s.data.length > 0) 
        : allD;

    const o = {
        series: f,
        chart: { 
            type: 'treemap', 
            height: '100%', 
            toolbar: { show: false },
            background: 'transparent'
        },
        // Coin360 Tarzı Siyah Kalın Kenarlıklar
        stroke: {
            show: true,
            width: 4,
            colors: ['#0e1013']
        },
        colors: [({ value }) => value > 0 ? '#00c805' : '#ff3b30'],
        plotOptions: {
            treemap: {
                distributed: true,
                enableShades: false,
                dataLabels: { format: 'scale' }
            }
        },
        dataLabels: {
            enabled: true,
            style: { fontSize: '14px', fontWeight: '900' },
            formatter: (text, op) => [text, op.value + "%"]
        },
        theme: { mode: 'dark' },
        tooltip: { theme: 'dark', y: { formatter: v => "% " + v } }
    };

    document.querySelector("#chart").innerHTML = "";
    new ApexCharts(document.querySelector("#chart"), o).render();
}

function openM() { document.getElementById('modal').style.display = 'flex'; document.getElementById('ov').style.display = 'block'; }
function closeM() { document.getElementById('modal').style.display = 'none'; document.getElementById('ov').style.display = 'none'; }

function list() {
    const l = document.getElementById('stock-list');
    const flat = allD.flatMap(s => s.data);
    l.innerHTML = flat.map(h => `
        <div class="stock-row" onclick="toggle('${h.x}')">
            <span style="font-weight:bold">${h.x}</span>
            <input type="checkbox" id="chk-${h.x}" ${sel.includes(h.x)?'checked':''} onclick="event.stopPropagation()">
        </div>
    `).join('');
}

function toggle(id) {
    const c = document.getElementById('chk-'+id);
    c.checked = !c.checked;
}

function fltr() {
    let q = document.getElementById('srch').value.toUpperCase();
    document.querySelectorAll('.stock-row').forEach(i => i.style.display = i.innerText.includes(q) ? 'flex' : 'none');
}

function save() {
    sel = Array.from(document.querySelectorAll('#stock-list input:checked')).map(c => c.id.replace('chk-',''));
    localStorage.setItem('sel', JSON.stringify(sel));
    closeM();
    if(view === 'mine') upd();
}

function changeV(v) {
    view = v;
    document.getElementById('b-all').classList.toggle('active', v==='all');
    document.getElementById('b-mine').classList.toggle('active', v==='mine');
    upd();
}

init();