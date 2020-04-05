$.getJSON("https://raw.githubusercontent.com/matteo-stat/covid-19/master/py_app/data_out/ita_regions.geojson", "", function(dati_geojson){

	var map = L.map('map').setView([41.902782, 12.496366], 6);

	L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw', {
		maxZoom: 18,
		attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
			'<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
			'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
		id: 'mapbox/light-v9',
		tileSize: 512,
		zoomOffset: -1
	}).addTo(map);

	// control that shows state info on hover
	var info = L.control();

	info.onAdd = function (map) {
		this._div = L.DomUtil.create('div', 'info');
		this.update();
		return this._div;
	};

	info.update = function (props) {
		this._div.innerHTML = '<h4>COVID-19 Dati Regionali</h4>' +  (props ?
			'<br/><b>' + props.regione + '</b><br/><br/>'
			+'	           Popolazione: ' + getNumberFormatted(props.popolazione) + '<br/>'
			+'	  Attualmente Positivi: ' + getNumberFormatted(props.totale_positivi) + ' (' + getNumberRoundedFormatted(props.totale_positivi_perc, 2) + '%)' + '<br/>'
			+'       Terapia Intensiva: ' + getNumberFormatted(props.terapia_intensiva) + '<br/><br/>'
			+'                 Tamponi: ' + getNumberFormatted(props.tamponi) + '<br/>'
			+'             Totale casi: ' + getNumberFormatted(props.totale_casi) + '<br/>'
			+'                Deceduti: ' + getNumberFormatted(props.deceduti) + ' (' + getNumberRoundedFormatted(props.deceduti/props.totale_casi*100.0, 2) + '%)' + '<br/>'
            +'                 Guariti: ' + getNumberFormatted(props.dimessi_guariti) + ' (' + getNumberRoundedFormatted(props.dimessi_guariti/props.totale_casi*100.0, 2) + '%)' + '<br/>'
			: 'Posizionati sopra una regione');
	};

	info.addTo(map);

	function getNumberFormatted(mynumber){

		return Number(mynumber).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
	}

    // return formatted number
	function getNumberRoundedFormatted(mynumber, decplaces = 2){
		return Number(mynumber).toFixed(decplaces).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
	}

	function style(feature) {
		return {
			weight: 2,
			opacity: 1,
			color: 'white',
			dashArray: '3',
			fillOpacity: 0.7,
			fillColor: feature.properties.hex_color
		};
	}

	function highlightFeature(e) {
		var layer = e.target;

		layer.setStyle({
			weight: 5,
			color: '#666',
			dashArray: '',
			fillOpacity: 0.7
		});

		if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
			layer.bringToFront();
		}

		info.update(layer.feature.properties);
	}

	var geojson;

	function resetHighlight(e) {
		geojson.resetStyle(e.target);
		info.update();
	}

	function zoomToFeature(e) {
		//console.log(e.target.feature.properties.regione);
		map.fitBounds(e.target.getBounds());
	}

	function onEachFeature(feature, layer) {
		layer.on({
			mouseover: highlightFeature,
			mouseout: resetHighlight,
			click: zoomToFeature
		});
	}

	geojson = L.geoJson(dati_geojson, {
		style: style,
		onEachFeature: onEachFeature
	}).addTo(map);

	
	
});    