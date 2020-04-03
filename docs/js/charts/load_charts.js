
$.getJSON("https://raw.githubusercontent.com/matteo-stat/covid-19/master/py_app/data_out/andamento_nazionale.json", "", function(dati_json){


    //console.log(dati_json.table_summary)

    updateTableSummary("table_att_positivi", dati_json.table_summary.att_positivi);
    updateTableSummary("table_tot_casi", dati_json.table_summary.tot_casi);
    updateTableSummary("table_tot_deceduti", dati_json.table_summary.tot_deceduti);
    updateTableSummary("table_tot_dimessi", dati_json.table_summary.tot_dimessi);

    function updateTableSummary(id_div, label) {
        var tag = document.createElement("p");
        label = Number(label).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
        var text = document.createTextNode(label);
        tag.appendChild(text);
        var element = document.getElementById(id_div);
        element.appendChild(tag);
    };

    var chart_nuovi_positivi = new Chart(
        document.getElementById("chart_nuovi_positivi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_nuovi_positivi),
            options: getChartOptions(dati_json.chart_nuovi_positivi)
        }
    );
   
    var chart_nuovi_tamponi = new Chart(
        document.getElementById("chart_nuovi_tamponi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_nuovi_tamponi),
            options: getChartOptions(dati_json.chart_nuovi_tamponi)
        }
    );

    var chart_att_positivi = new Chart(
        document.getElementById("chart_att_positivi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_att_positivi),
            options: getChartOptions(dati_json.chart_att_positivi)
        }
    );
    
    var chart_var_att_positivi = new Chart(
        document.getElementById("chart_var_att_positivi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_var_att_positivi),
            options: getChartOptions(dati_json.chart_var_att_positivi)
        }
    );
    /*
    var chart_reg_att_positivi = new Chart(
        document.getElementById("chart_reg_att_positivi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_reg_att_positivi),
            options: getChartOptions(dati_json.chart_reg_att_positivi)
        }
    );
    */
    var chart_deceduti = new Chart(
        document.getElementById("chart_deceduti").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_deceduti),
            options: getChartOptions(dati_json.chart_deceduti)
        }
    );
    
    var chart_dimessi = new Chart(
        document.getElementById("chart_dimessi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_dimessi),
            options: getChartOptions(dati_json.chart_dimessi)
        }
    );
    
    var chart_ter_intensiva = new Chart(
        document.getElementById("chart_ter_intensiva").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_ter_intensiva),
            options: getChartOptions(dati_json.chart_ter_intensiva)
        }
    );
    
    var chart_ospedalizzati = new Chart(
        document.getElementById("chart_ospedalizzati").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_ospedalizzati),
            options: getChartOptions(dati_json.chart_ospedalizzati)
        }
    );

    // return data for chart
    function getChartData(chart_json) {

        var data = {
            labels: chart_json.labels,
            datasets: [
                {
                label: chart_json.label_first,
                data: chart_json.data_first,
                backgroundColor: chart_json.backgroundcolor_first,
                borderColor: chart_json.bordercolor_first,
                borderWidth: 1
                }
            ]
            }

        return(data)

    }
    
    // return options for chart
    function getChartOptions(chart_json) {

        var options = {
            responsive: true,
            legend: {
                display: false
            },
            tooltips: {
                callbacks: {
                    label: function(tooltipItem) {
                        return Number(tooltipItem.yLabel).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
                    }
                }
            },
            scales: {
                    yAxes: [
                        {
                        ticks: {
                            //beginAtZero: false,                            
                            callback: function(value, index, values) {
                                return Number(value).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
                            }
                        }
                    }
                ]
            },
            /*
            title: {
                display: true,
                text: 'my title',
                position: 'top'
            }
            */
        } 

        return(options)
    }                
        
    
});





  