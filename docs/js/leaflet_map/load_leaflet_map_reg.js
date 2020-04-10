$.getJSON(map_geojson, "", function(dati_geojson){

	var map = L.map('map', {
		zoomSnap: 0.1
	});
	var map = map.setView([41.902782, 12.496366], 1);	

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
		this._div.innerHTML = (props ? 
			`<h5 style="text-align:center">` + props.provincia + `</h5>
			<table>
				<tbody>
					<tr>
						<td style="text-align: right">Popolazione:</td>
						<td>
							<div>
								<div>` + getNumberFormatted(props.popolazione) + `</div>
							</div>
						</td>
					</tr>					
					<tr>
						<td style="text-align: right">Totale Casi:</td>
						<td>
							<div>
								<div>` + getNumberFormatted(props.totale_casi) + ' (' + getNumberRoundedFormatted(props.totale_casi/props.popolazione*100.0, 2) + `%)</div>
							</div>
						</td>
					</tr>
				</tbody>
			</table>`
			: '<h6 style="text-align:center">Posizionati sopra una provincia</h6>'
		);
	};

	info.addTo(map);

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
		//var url = "regioni.html?cod_reg=" + encodeURIComponent(e.target.feature.properties.regione);
        //window.location.href = url;
		map.fitBounds(e.target.getBounds());
	}

	function onEachFeature(feature, layer) {
		layer.on({
			mouseover: highlightFeature,
			mouseout: resetHighlight,
			//click: zoomToFeature
		});
	}

	geojson = L.geoJson(dati_geojson, {
		style: style,
		onEachFeature: onEachFeature
	});
	geojson.addTo(map);	
	map.fitBounds(geojson.getBounds());
	map.setZoom(map.getZoom() - 0.1);
});    