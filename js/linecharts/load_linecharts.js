
$.getJSON("https://raw.githubusercontent.com/matteo-stat/test/master/andamento_nazionale.json", "", function(dati_json){

    //console.log(dati_json['chart_a'].labels)

    //line
    var ctxL = document.getElementById("chart_a").getContext('2d');
    var myLineChart = new Chart(ctxL, {
    type: 'line',
    data: {
    labels: dati_json.chart_a.labels,
    datasets: [{
    label: dati_json.chart_a.label_first,
    data: dati_json.chart_a.data_first,
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
    }
    });

});


  