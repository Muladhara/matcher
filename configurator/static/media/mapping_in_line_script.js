/* in line script for mappings */
django.jQuery(document).ready(function() {	
	/* if a parameter type is changed, the respective */
	/* text field is updated with the appropriate placeholder */	
	django.jQuery('[id^="id_mapping"][id$="-fromColumn"]').change(function() { toggleMappingInput(django.jQuery(this)); })
	django.jQuery('[id^="id_mapping"][id$="-toColumn"]').change(function() { toggleMappingInput(django.jQuery(this)); })
	
	/* for initial load */
	django.jQuery('[id^="id_mapping"][id$="-fromColumn"]').each(function() { toggleMappingInput(django.jQuery(this)); })
	django.jQuery('[id^="id_mapping"][id$="-toColumn"]').each(function() { toggleMappingInput(django.jQuery(this)); })
	
	/* alternates if the input in the mapping comes from */
	/* a column in data source 1 or in data source 2 */
	function toggleMappingInput(changedElement) {
		id = changedElement.attr('id');
		/* if the from changed */
		if (id.indexOf("from")!=-1) {
			to_replace_string = "from";
			replace_string = "to";
		} else {
			to_replace_string = "to";
			replace_string = "from";
		}
		
		/* finds the element to disable */
		elementToChange_id = id.replace(to_replace_string, replace_string);
		elementToChange = django.jQuery("#" + elementToChange_id);
		
		/* and, if the selected value is not null */
		/* disables it */	
		if (changedElement.val()!="") {
			elementToChange.attr("disabled","disabled");
		} else
			elementToChange.removeAttr("disabled");
	}
});