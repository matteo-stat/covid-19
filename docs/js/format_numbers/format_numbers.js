// return formatted number
function getNumberFormatted(mynumber){
	return Number(mynumber).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
}

// return formatted number
function getNumberRoundedFormatted(mynumber, decplaces = 2){
	return Number(mynumber).toFixed(decplaces).toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,');
}