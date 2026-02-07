let allD = [], 
    sel = JSON.parse(localStorage.getItem('sel')) || [], 
    view = 'bist100';

async function init() {
    try {
        const r = await fetch('data.json');
        allD = await r.json();
        
        // İlk açılışta varsayılan favoriler
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
        // BIST 100 - Tüm hisseler sektörlere göre
        f = allD;
    } else if (view === 'mine') {
        // Favorilerim - Sadece seçili hisseler
        f = allD.map(s => ({
            name: s.name, 
            data: s.data.filter(h => sel.includes(h.x))
        })).filter(s => s.data.length > 0);
    } else {
        // Tüm Hisseler - Sektör ayrımı olmadan
        const allStocks = allD.flatMap(s => s.data);
        f = [{ name: "TÜM HİSSELER", data: allStocks }];
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
                speed: 600,
                animateGradually: { enabled: true, delay: 150 }
            }
        },
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
            style: { 
                fontSize: '14px', 
                fontWeight: '900',
                fontFamily: 'Inter, sans-serif'
            },
            formatter: (text, op) => [text, op.value + "%"]
        },
        theme: { mode: 'dark' },
        tooltip: { 
            theme: 'dark', 
            y: { formatter: v => "% " + v },
            style: { fontSize: '13px' }
        }
    };

    document.querySelector("#chart").innerHTML = "";
    new ApexCharts(document.querySelector("#chart"), o).render();
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
    
    allD.forEach(sector => {
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
        
        // Sektör başlığını göster/gizle
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
    document.getElementById('b-all').classList.toggle('active', v === 'all');
    upd();
}

init();