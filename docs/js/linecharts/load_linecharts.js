
$.getJSON("https://raw.githubusercontent.com/matteo-stat/covid-19/master/py_app/data_out/andamento_nazionale.json", "", function(dati_json){

    // chart_a
    var ctxL = document.getElementById("chart_a").getContext('2d');
    var chart_a = new Chart(ctxL, {
    type: 'bar',
    data: {
    labels: dati_json.chart_a.labels,
    datasets: [{
    label: dati_json.chart_a.label_first,
    data: dati_json.chart_a.data_first,
    backgroundColor: [
    'rgba(105, 0, 132, .65)',
    ],
    borderColor: [
    'rgba(200, 99, 132, .95)',
    ],
    borderWidth: 2
    }
    ]
    },
    options: {
    responsive: true
    ,legend: {display: false}
    ,scales: {
        yAxes: [{
        ticks: {
        beginAtZero: false
        }
        }]
        }
    }
    });

    // chart_b
    var ctxL = document.getElementById("chart_b").getContext('2d');
    var chart_b = new Chart(ctxL, {
    type: 'line',
    data: {
    labels: dati_json.chart_b.labels,
    datasets: [{
    label: dati_json.chart_b.label_first,
    data: dati_json.chart_b.data_first,
    backgroundColor: [
    'rgba(105, 0, 132, .2)',
    ],
    borderColor: [
    'rgba(200, 99, 132, .7)',
    ],
    borderWidth: 2
    }
    ]
    },
    options: {
    responsive: true
    ,legend: {display: false}
    }
    });


    // chart_c
    var ctxL = document.getElementById("chart_c").getContext('2d');
    var chart_c = new Chart(ctxL, {
    type: 'line',
    data: {
    labels: dati_json.chart_c.labels,
    datasets: [{
    label: dati_json.chart_c.label_first,
    data: dati_json.chart_c.data_first,
    backgroundColor: [
    'rgba(105, 0, 132, .2)',
    ],
    borderColor: [
    'rgba(200, 99, 132, .7)',
    ],
    borderWidth: 2
    }
    ]
    },
    options: {
    responsive: true
    ,legend: {display: false}
    }
    });
        

    // chart_d
    var ctxL = document.getElementById("chart_d").getContext('2d');
    var chart_d = new Chart(ctxL, {
    type: 'line',
    data: {
    labels: dati_json.chart_d.labels,
    datasets: [{
    label: dati_json.chart_d.label_first,
    data: dati_json.chart_d.data_first,
    backgroundColor: [
    'rgba(105, 0, 132, .2)',
    ],
    borderColor: [
    'rgba(200, 99, 132, .7)',
    ],
    borderWidth: 2
    }
    ]
    },
    options: {
    responsive: true
    ,legend: {display: false}
    }
    });    

});


  