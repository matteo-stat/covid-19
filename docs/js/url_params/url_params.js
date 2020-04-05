var queryString = new Array();


if (queryString.length == 0) {

    if (window.location.search.split('?').length > 1) {

        var params = window.location.search.split('?')[1].split('&');

        for (var i = 0; i < params.length; i++) {

            var key = params[i].split('=')[0];

            var value = decodeURIComponent(params[i].split('=')[1]);

            queryString[key] = value;

        }
    }

}


/*
if (queryString["name"] != null && queryString["technology"] != null) {
        var data = "<u>Values from QueryString</u><br /><br />";
    data += "<b>Name:</b> " + queryString["name"] + " <b>Technology:</b> " + queryString["technology"];
    document.getElementById("lblData").innerHTML = data;
}
*/

//console.log(queryString.cod_reg == null);
