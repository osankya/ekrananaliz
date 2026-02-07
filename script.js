let allData = [];
let currentView = 'bist100';

async function init() {
    const res = await fetch('data.json');
    allData = await res.json();
    renderTreemap(allData);
}

function renderTreemap(data) {
    // Sektörlere göre gruplama yapıyoruz
    const options = {
        series: [{ data: data }],
        chart: { type: 'treemap', height: '100%', toolbar: {show:false} },
        colors: [({ value }) => value > 0 ? '#0ecb81' : '#f6465d'],
        plotOptions: {
            treemap: {
                distributed: true,
                enableShades: false
            }
        },
        tooltip: {
            custom: function({ series, seriesIndex, dataPointIndex, w }) {
                const item = w.config.series[seriesIndex].data[dataPointIndex];
                return `<div style="padding:10px; background:#1c1f26;">
                    <b>${item.x}</b> <br>
                    Sektör: ${item.s} <br>
                    Değişim: %${item.y}
                </div>`;
            }
        }
    };
    
    document.querySelector("#chart").innerHTML = "";
    const chart = new ApexCharts(document.querySelector("#chart"), options);
    chart.render();
}

function showMyPage() {
    const myStocks = localStorage.getItem('myStocks')?.split(',') || [];
    const filtered = allData.filter(d => myStocks.includes(d.x));
    renderTreemap(filtered);
}

function saveMyStocks() {
    const input = document.getElementById('my-stocks-input').value.toUpperCase().replace(/\s/g, '');
    localStorage.setItem('myStocks', input);
    document.getElementById('settings-modal').style.display = 'none';
    showMyPage();
}

init();