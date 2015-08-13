/* if a parameter text is changed, updates with */
/* the placeholder the corresponding text field */
/* updateParameter the jQuery object that has been modified/loaded */
/* isChange : true if it is an actual change, false if a simple load */
/* matchOrClean : match to update match parameters, clean for cleaning step parameters */
function updateParameterField(updatedParameter, isChange, matchOrClean) {
	selected_type = updatedParameter.val();
	to_change = updatedParameter;
	
	/* the fields to update */
	siblings = to_change.parent().siblings().filter('[class="field-parameter"]').children();
	
	/* if it is an actual change, clears the text */
	if (isChange) {
		siblings.val("");
		siblings.removeAttr("placeholder");
	}
	
	/* chooses the right dao */
	if (matchOrClean=="match")
		requestUri = "/dao/matchParameterByType/" + selected_type + "/";
	else
		requestUri = "/dao/cleaningParameterByType/" + selected_type + "/";
	
	django.jQuery.ajax({ url: requestUri , success: function(data)
	{
		obj = eval(data);
		obj = eval(obj["parameter"]);
		obj = eval(obj[0]);
		if (obj!=null) {
			obj = eval(obj["fields"]);
			name = obj["name"];
			description = obj["description"];
			template = name + " (" + description + ")";				
		} else {
			template = "";
		}
		
		/* updates with the placeholder */
		
		siblings.each(function () { 
			if (template!="") {
				siblings.removeAttr("disabled");
				siblings.attr("placeholder",template);	
			} else {
				siblings.prop("disabled",true);
			}
		
		});
	}, async: false });			
}