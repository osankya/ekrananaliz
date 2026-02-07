async function veriyiGetir() {
    try {
        // data.json dosyasını oku
        const response = await fetch('data.json');
        
        if (!response.ok) {
            throw new Error('Veri dosyası (data.json) bulunamadı!');
        }

        const borsaVerisi = await response.json();
        
        // ApexCharts ile Treemap (Kutu) grafiğini oluştur
        var options = {
            series: [{
                data: borsaVerisi
            }],
            legend: {
                show: false
            },
            chart: {
                height: '100%',
                type: 'treemap',
                toolbar: { show: false }
            },
            title: {
                text: 'BIST 100 ISI HARİTASI',
                align: 'center',
                style: { color: '#fff', fontSize: '20px' }
            },
            theme: {
                mode: 'dark'
            },
            plotOptions: {
                treemap: {
                    distributed: true,
                    enableShades: false
                }
            }
        };

        var chart = new ApexCharts(document.querySelector("#chart"), options);
        chart.render();
        console.log("Grafik başarıyla yüklendi.");

    } catch (error) {
        console.error("Hata detayı:", error);
        document.body.innerHTML += `<h2 style="color:red; text-align:center;">Bir hata oluştu: ${error.message}</h2>`;
    }
}

// Fonksiyonu çalıştır
veriyiGetir();