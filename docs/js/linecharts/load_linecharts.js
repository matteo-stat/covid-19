
$.getJSON("https://raw.githubusercontent.com/matteo-stat/covid-19/master/py_app/data_out/andamento_nazionale.json", "", function(dati_json){


    //console.log(dati_json.chart_nuovi_positivi)

    // chart_nuovi_positivi
    var ctxL = document.getElementById("chart_nuovi_positivi").getContext('2d');

    var data = {
        labels: dati_json.chart_nuovi_positivi.labels,
        datasets: [
            {
            label: dati_json.chart_nuovi_positivi.label_first,
            data: dati_json.chart_nuovi_positivi.data_first,
            backgroundColor: dati_json.chart_nuovi_positivi.backgroundcolor_first,
            borderColor: dati_json.chart_nuovi_positivi.bordercolor_first,
            borderWidth: 1
            }
        ]
        }

    var options = {
        responsive: true,
        legend: {
            display: false
        },
        tooltips: {
            callbacks: {
                label: function(tooltipItem) {
                    return Number(tooltipItem.yLabel).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,') + " and so worth it !";
                }
            }
        },
        scales: {
                yAxes: [
                    {
                    ticks: {
                        beginAtZero: false
                    }
                }
            ]
        },
        /*
        title: {
            display: true,
            text: 'Ice Cream Truck',
            position: 'top'
        }
        */
    }

    var chart_nuovi_positivi = new Chart(ctxL, 
        {
            type: 'bar',
            data: data,
            options: options
        }
    );
   
    
	// chart_tot_positivi
    var ctxL = document.getElementById("chart_tot_positivi").getContext('2d');
    var chart_tot_positivi = new Chart(ctxL, 
            {
                type: 'bar',
                    data: {
                    labels: dati_json.chart_tot_positivi.labels,
                    datasets: [
                        {
                        label: dati_json.chart_tot_positivi.label_first,
                        data: dati_json.chart_tot_positivi.data_first,
                        backgroundColor: dati_json.chart_tot_positivi.backgroundcolor_first,
                        borderColor: dati_json.chart_tot_positivi.bordercolor_first,
                        borderWidth: 1
                        }
                    ]
                    },
                options: {
                    responsive: true
                    ,legend: {
                        display: false
                    }
                    ,scales: {
                            yAxes: [
                                {
                                ticks: {
                                    beginAtZero: false
                                }
                            }
                        ]
                    }
                }
        }
    );
    
    
    // chart_deceduti
    var ctxL = document.getElementById("chart_deceduti").getContext('2d');
    var chart_deceduti = new Chart(ctxL, 
            {
                type: 'bar',
                    data: {
                    labels: dati_json.chart_deceduti.labels,
                    datasets: [
                        {
                        label: dati_json.chart_deceduti.label_first,
                        data: dati_json.chart_deceduti.data_first,
                        backgroundColor: dati_json.chart_deceduti.backgroundcolor_first,
                        borderColor: dati_json.chart_deceduti.bordercolor_first,
                        borderWidth: 1
                        }
                    ]
                    },
                options: {
                    responsive: true
                    ,legend: {
                        display: false
                    }
                    ,scales: {
                            yAxes: [
                                {
                                ticks: {
                                    beginAtZero: false
                                }
                            }
                        ]
                    }
                }
        }
    );
    
    
    // chart_guariti
    var ctxL = document.getElementById("chart_guariti").getContext('2d');
    var chart_guariti = new Chart(ctxL, 
            {
                type: 'bar',
                    data: {
                    labels: dati_json.chart_guariti.labels,
                    datasets: [
                        {
                        label: dati_json.chart_guariti.label_first,
                        data: dati_json.chart_guariti.data_first,
                        backgroundColor: dati_json.chart_guariti.backgroundcolor_first,
                        borderColor: dati_json.chart_guariti.bordercolor_first,
                        borderWidth: 1
                        }
                    ]
                    },
                options: {
                    responsive: true
                    ,legend: {
                        display: false
                    }
                    ,scales: {
                            yAxes: [
                                {
                                ticks: {
                                    beginAtZero: false
                                }
                            }
                        ]
                    }
                }
        }
    );
        
        
        
});





  