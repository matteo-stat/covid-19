
$.getJSON("https://raw.githubusercontent.com/matteo-stat/covid-19/master/py_app/data_out/andamento_nazionale.json", "", function(dati_json){

    //console.log(dati_json.table_summary)
    //console.log(testvarjava);

    // return formatted number
    function getNumberFormatted(mynumber){

		return Number(mynumber).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
    }
    
    // return formatted number
    function getNumberRoundedFormatted(mynumber, decplaces = 2){

		return Number(mynumber).toFixed(decplaces).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
    }
    
    // function for update summary table
    function updateTableSummary(id_div, label, format_number=true) {
        var tag = document.createElement("p");
        if(format_number){
            label = getNumberFormatted(label);
        }        
        var text = document.createTextNode(label);
        tag.appendChild(text);
        var element = document.getElementById(id_div);
        element.appendChild(tag);
    };
    
    // update summary table
    updateTableSummary("table_att_positivi", dati_json.table_summary.att_positivi);
    updateTableSummary("table_tot_casi", dati_json.table_summary.tot_casi);
    updateTableSummary("table_tot_deceduti", dati_json.table_summary.tot_deceduti);
    updateTableSummary("table_tot_dimessi", dati_json.table_summary.tot_dimessi);   
    updateTableSummary("table_popolazione", dati_json.table_summary.popolazione);
    updateTableSummary("table_ult_aggiornamento", dati_json.table_summary.ult_aggiornamento, false);

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
    function getChartOptions(chart_json, perc = false) {

        var options = {
            responsive: true,
            legend: {
                display: false
            },
            tooltips: {
                callbacks: {
                    label: function(tooltipItem) {
                        return getNumberFormatted(tooltipItem.yLabel);
                    }
                }
            },
            scales: {
                    yAxes: [
                        {
                        ticks: {
                            //beginAtZero: false,                            
                            callback: function(value, index, values) {
                                
                                if(perc) {
                                    value = value
                                }
                                
                                else {
                                    value = getNumberFormatted(value)
                                }

                                return  value;
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
           
    // create charts
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

    var chart_att_positivi_reg = new Chart(
        document.getElementById("chart_att_positivi_reg").getContext('2d'), 
        {
            type: 'horizontalBar',
            data: getChartData(dati_json.chart_att_positivi_reg),
            options: {
                legend: {
                   display: false
                },
                maintainAspectRatio: false,
                responsive: true,
                tooltips: {
                   callbacks: {
                      label: function(tooltipItem) {
                         return getNumberFormatted(tooltipItem.xLabel);
                      }
                   }
                },
                scales: {
                    xAxes: [
                        {
                        ticks: {
                            //beginAtZero: false,                            
                            callback: function(value) {                                    
                                value = getNumberFormatted(value)
                                return  value;
                            }
                        }
                    }
                    ]
                }
             }
             //options object ends
            /*
            options: {
                responsive: true,
                maintainAspectRatio: false,
                legend: {
                    display: false
                },
                tooltips: {
                    callbacks: {
                        label: function(tooltipItem) {
                            //value = getNumberRoundedFormatted(tooltipItem.xLabel, 2);
                            value = getNumberFormatted(tooltipItem.yLabel)                    
                        }
                    }
                },
                scales: {
                        xAxes: [
                            {
                            ticks: {
                                //beginAtZero: false,                            
                                callback: function(value, index, values) {                                    
                                    value = getNumberFormatted(value)
                                    return  value;
                                }
                            }
                        }
                    ]
                }
            }                
            */
        }
        
    );    
    chart_att_positivi_reg.canvas.parentNode.style.height = '650px';


});





  