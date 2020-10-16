// function for update card header
function cardHeaderUpdate(div_id, header_suffix, sep){

    document.getElementById(div_id).innerHTML = document.getElementById(div_id).innerHTML + sep + header_suffix;
};

// function for update modal header
function modalHeaderUpdate(div_id, header_suffix, sep){

    document.getElementById(div_id).innerHTML = document.getElementById(div_id).innerHTML.replace("###", sep + header_suffix);
};

// function for update summary table
function updateTableSummary(div_id, label, delta_label="", format_number=true) {
    var tag = document.createElement("p");
    var tag_span = document.createElement("span");

    if(format_number){
        label = getNumberFormatted(label);    
    }

    text_tag = "<p>" + label + "</p>";        

    delta_color = "#000000";
    delta_symbol = "";

    if(delta_label!=""){        
        if(Number(delta_label > 0)){
            delta_color = "#990000";   
            delta_symbol = "+";     
        }
        if(Number(delta_label < 0)) {
            delta_color = "#009900";
            delta_symbol = "-";
        }        
        text_tag = "<p>" + label + " <span style='color:" + delta_color + "'>(" + delta_symbol + getNumberFormatted(delta_label) + ")</span></p>";        
    }

    document.getElementById(div_id).innerHTML = text_tag;    
};