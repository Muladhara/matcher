/* reacts to a change of data source */
/* selectedDs is the new data source */
/* whichColumns = the id of the in line related item */
/* isRealChange = true if it is a real change happening, false if the first load */
function dataSourceChange(selectedDs, whichColumns, isRealChange) {
		cols = {}
		queryUrl = "/dao/columnsByDs/";
		/* if it is a real change, resets the selected field */
		if(isRealChange)
			django.jQuery(whichColumns+' option[value=""]').attr("selected", true);
		
		/* calls the update function */		
		django.jQuery.ajax({ url: queryUrl + selectedDs + "/" , success: function (data) { updateColumns(data, whichColumns); }, async: false });
};

/* runs through the found columns */
/* and updates the html removing them */
function updateColumns(data, inLineFieldName) {
	obj = eval(data);
	obj = eval(obj["columns"]);
	
	// hides all the options (except for the blank default)
	django.jQuery(inLineFieldName+' option[value!=""]').attr('disabled', 'disabled');
	
	// re-enables only the appropriate ones
	for(var i=0;i<obj.length;i++) {
       	var obj2 = obj[i];
       	for(var key in obj2) {
           	var attrName = key;
           	var attrValue = obj2[key];
           	if (attrName=='pk') {
           		pk = attrValue;
           		django.jQuery(inLineFieldName+" option[value="+pk+"]").removeAttr("disabled");
           	} 
       	} 
   	}
}