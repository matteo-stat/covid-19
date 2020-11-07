// function for update card header
function cardHeaderUpdate(div_id, header_suffix, sep){

    document.getElementById(div_id).innerHTML = document.getElementById(div_id).innerHTML + sep + header_suffix;
};

// function for update modal header
function modalHeaderUpdate(div_id, header_suffix, sep){

    document.getElementById(div_id).innerHTML = document.getElementById(div_id).innerHTML.replace("###", sep + header_suffix);
};

// function for update summary table
function updateTableSummary(div_id, label, delta_label="", delta_invert=false, format_number=true, format_perc=false) {
    var tag = document.createElement("p");
    var tag_span = document.createElement("span");

    if(format_number && format_perc){
        label = getNumberRoundedFormatted(label, 2)+ "%"; 
        delta_label_new = getNumberRoundedFormatted(delta_label, 2) + "%"; 
    }
    if(format_number && format_perc==false){
        label = getNumberFormatted(label, 2); 
        delta_label_new = getNumberFormatted(delta_label, 2); 
    }

    text_tag = "<p>" + label + "</p>";        

    delta_color = "#000000";
    delta_symbol = "";

    delta_invert_factor = 1;    
    if(delta_invert){
        delta_invert_factor = -1;
    }

    if(delta_label!=""){        
        if(Number(delta_label)*delta_invert_factor > 0){
            delta_color = "#990000";
        }
        if(Number(delta_label)*delta_invert_factor < 0) {
            delta_color = "#009900";
        }    
        if(Number(delta_label) > 0){  
            delta_symbol = "+";     
        }
        if(Number(delta_label) < 0) {
            delta_symbol = "";
        }              
        text_tag = "<p>" + label + " <span style='color:" + delta_color + "'>(" + delta_symbol + delta_label_new + ")</span></p>";        
    }

    document.getElementById(div_id).innerHTML = text_tag;    
};