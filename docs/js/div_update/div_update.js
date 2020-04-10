// function for updated card header
function cardHeaderUpdate(div_id, header_suffix, sep){

    document.getElementById(div_id).innerHTML = document.getElementById(div_id).innerHTML + sep + header_suffix;
};

// function for update summary table
function updateTableSummary(div_id, label, format_number=true) {
    var tag = document.createElement("p");
    if(format_number){
        label = getNumberFormatted(label);
    }        
    var text = document.createTextNode(label);
    tag.appendChild(text);
    var element = document.getElementById(div_id);
    element.appendChild(tag);
};