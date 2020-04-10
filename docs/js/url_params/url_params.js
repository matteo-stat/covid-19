var queryparams = new Array();
var cod_reg_valid = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20];
var pagename = window.location.pathname.split("/").pop();

var defaultpage = 'https://matteo-stat.github.io/covid-19/'

// dev
//var defaultrepo = 'https://raw.githubusercontent.com/matteo-stat/covid-19/master/docs/json/';

// prod
var defaultrepo = 'json/';

chart_json = defaultrepo + 'italia/charts_ita.json';
map_geojson = defaultrepo + 'italia/map_ita.geojson';


if (pagename.includes('regioni.html')){
                
    if (window.location.search.split('?').length > 1) {
        
        var params = window.location.search.split('?')[1].split('&');
        
        for (var i = 0; i < params.length; i++) {

            var key = params[i].split('=')[0];

            var value = decodeURIComponent(params[i].split('=')[1]);

            queryparams[key] = value;

        }
    }        
        
    if ('cod_reg' in queryparams){
        
        if (cod_reg_valid.includes(Number(queryparams.cod_reg)))
        {
            chart_json = defaultrepo + 'regioni/' + queryparams.cod_reg + '.json';
        
            map_geojson = defaultrepo + 'regioni/' + queryparams.cod_reg + '.geojson';
        }

        else {

            window.location.href = defaultpage;

        }
        
    }    
    else {

        window.location.href = defaultpage;

    }      

}
