$.getJSON(map_geojson, "", function(dati_geojson){

	var map = L.map('map', {
		zoomSnap: 0.1,
		scrollWheelZoom: false
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
			`<h5 style="text-align:center">` + props.regione + `</h5>
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
						<td style="text-align: right">Attualmente Positivi:</td>
						<td>
							<div>
								<div>` + getNumberFormatted(props.totale_positivi) + ' (' + getNumberRoundedFormatted(props.totale_positivi_perc, 2) + `%)</div>
							</div>
						</td>
					</tr>
					<tr>
						<td style="text-align: right">Terapia Intensiva:</td>
						<td>
							<div>
								<div>` + getNumberFormatted(props.terapia_intensiva) + ' (' + getNumberRoundedFormatted(Number(props.terapia_intensiva)/props.popolazione, 2) + `%)</div>
							</div>
						</td>
					</tr>
					<tr>
						<td>&nbsp;</td>
						<td>&nbsp;</td>
					</tr>
					<tr>
						<td style="text-align: right">Tamponi:</td>
						<td>
							<div>
								<div>` + getNumberFormatted(props.tamponi) + `</div>
							</div>
						</td>
					</tr>
					<tr>
						<td style="text-align: right">Totale Casi:</td>
						<td>
							<div>
								<div>` + getNumberFormatted(props.totale_casi) + `</div>
							</div>
						</td>
					</tr>
					<tr>
						<td style="text-align: right">Decessi:</td>
						<td>
							<div>
								<div>` + getNumberFormatted(props.decessi) + ' (' + getNumberRoundedFormatted(props.decessi/props.totale_casi*100.0, 2) + `%)</div>
							</div>
						</td>
					</tr>
					<tr>
						<td style="text-align: right">Dimessi Guariti:</td>
						<td>
							<div>
								<div>` + getNumberFormatted(props.dimessi_guariti) + ' (' + getNumberRoundedFormatted(props.dimessi_guariti/props.totale_casi*100.0, 2) + `%)</div>
							</div>
						</td>
					</tr>
				</tbody>
			</table>`
			: '<h6 style="text-align:center">Posizionati o clicca sopra una regione</h6>'
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
		var url = "regioni.html?cod_reg=" + encodeURIComponent(e.target.feature.properties.codice_regione);
        window.location.href = url;
		//map.fitBounds(e.target.getBounds());
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
	});
	geojson.addTo(map);	
	map.fitBounds(geojson.getBounds());	
});    