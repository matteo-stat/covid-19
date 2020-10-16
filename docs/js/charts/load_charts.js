
$.getJSON(chart_json, "", function(dati_json){
   
    // update card header
    cardHeaderUpdate("card_table_summary", dati_json.area.suffix, " - ");
       
    cardHeaderUpdate("card_nuovi_positivi", dati_json.area.suffix, " - ");    
    modalHeaderUpdate("modalheader_nuovi_positivi", dati_json.area.suffix, " - ");
    cardHeaderUpdate("card_att_positivi", dati_json.area.suffix, " - ");
    modalHeaderUpdate("modalheader_att_positivi", dati_json.area.suffix, " - ");

    cardHeaderUpdate("card_nuovi_tamponi", dati_json.area.suffix, " - ");
    modalHeaderUpdate("modalheader_nuovi_tamponi", dati_json.area.suffix, " - ");
    cardHeaderUpdate("card_var_att_positivi", dati_json.area.suffix, " - ");
    modalHeaderUpdate("modalheader_var_att_positivi", dati_json.area.suffix, " - ");

    cardHeaderUpdate("card_perc_tamponi_positivi", dati_json.area.suffix, " - ");
    modalHeaderUpdate("modalheader_perc_tamponi_positivi", dati_json.area.suffix, " - ");

    cardHeaderUpdate("card_decessi", dati_json.area.suffix, " - ");
    modalHeaderUpdate("modalheader_decessi", dati_json.area.suffix, " - ");
    cardHeaderUpdate("card_ter_intensiva", dati_json.area.suffix, " - ");
    modalHeaderUpdate("modalheader_ter_intensiva", dati_json.area.suffix, " - ");

    cardHeaderUpdate("card_dimessi", dati_json.area.suffix, " - ");
    modalHeaderUpdate("modalheader_dimessi", dati_json.area.suffix, " - ");
    cardHeaderUpdate("card_ospedalizzati", dati_json.area.suffix, " - ");
    modalHeaderUpdate("modalheader_ospedalizzati", dati_json.area.suffix, " - ");

    // update summary table
    updateTableSummary("table_att_positivi", dati_json.table_summary.att_positivi);
    updateTableSummary("table_tot_casi", dati_json.table_summary.tot_casi);
    updateTableSummary("table_tot_decessi", dati_json.table_summary.tot_decessi);
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

                        if(perc) {
                            value = getNumberRoundedFormatted(tooltipItem.yLabel, 2) + "%"
                        }                                            

                        else {
                            value = getNumberFormatted(tooltipItem.yLabel)
                        }
                        return value;
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
                                    value = getNumberRoundedFormatted(value, 2) + "%"
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

    var chartmodal_nuovi_positivi = new Chart(
        document.getElementById("chartmodal_nuovi_positivi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_nuovi_positivi),
            options: getChartOptions(dati_json.chart_nuovi_positivi)
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

    var chartmodal_att_positivi = new Chart(
        document.getElementById("chartmodal_att_positivi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_att_positivi),
            options: getChartOptions(dati_json.chart_att_positivi)
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

    var chartmodal_nuovi_tamponi = new Chart(
        document.getElementById("chartmodal_nuovi_tamponi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_nuovi_tamponi),
            options: getChartOptions(dati_json.chart_nuovi_tamponi)
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

    var charmodal_var_att_positivi = new Chart(
        document.getElementById("chartmodal_var_att_positivi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_var_att_positivi),
            options: getChartOptions(dati_json.chart_var_att_positivi)
        }
    );
           
    var chart_perc_tamponi_positivi = new Chart(
        document.getElementById("chart_perc_tamponi_positivi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_perc_tamponi_positivi),
            options: getChartOptions(dati_json.chart_perc_tamponi_positivi, perc = true)
        }
    );

    var chartmodal_perc_tamponi_positivi = new Chart(
        document.getElementById("chartmodal_perc_tamponi_positivi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_perc_tamponi_positivi),
            options: getChartOptions(dati_json.chart_perc_tamponi_positivi, perc = true)
        }
    ); 

    var chart_decessi = new Chart(
        document.getElementById("chart_decessi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_decessi),
            options: getChartOptions(dati_json.chart_decessi)
        }
    );

    var chart_decessi = new Chart(
        document.getElementById("chartmodal_decessi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_decessi),
            options: getChartOptions(dati_json.chart_decessi)
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
    
    var chart_ter_intensiva = new Chart(
        document.getElementById("chartmodal_ter_intensiva").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_ter_intensiva),
            options: getChartOptions(dati_json.chart_ter_intensiva)
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

    var chart_dimessi = new Chart(
        document.getElementById("chartmodal_dimessi").getContext('2d'), 
        {
            type: 'bar',
            data: getChartData(dati_json.chart_dimessi),
            options: getChartOptions(dati_json.chart_dimessi)
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

    var chart_ospedalizzati = new Chart(
        document.getElementById("chartmodal_ospedalizzati").getContext('2d'), 
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
        }
        
    );    
    chart_att_positivi_reg.canvas.parentNode.style.height = '665px';

});





  