/* disables in lines to force to fill in the parent */
django.jQuery(document).ready(function() {
	/* when a data source is changed in the main form */
	/* updates the related columns in the in line form */
	django.jQuery("#id_sourceDs").change(function() { dataSourceChange(this.value, ".field-fromColumn select", true) } );
	django.jQuery("#id_targetDs").change(function() { dataSourceChange(this.value, ".field-toColumn select", true) } );
	
	/* when the page is loaded, the initial values */
	/* are kept, but the options are restricted */
	/* calls for initial values */
	dataSourceChange(django.jQuery("#id_sourceDs").val(),".field-fromColumn select",false);
	dataSourceChange(django.jQuery("#id_targetDs").val(),".field-toColumn select",false);
	
	/* if a parameter type is changed, the respective */
	/* text field is updated with the appropriate placeholder */	
	django.jQuery('[id$="-type"]').on('change', function() { updateParameterField(django.jQuery(this),true,"clean") });
	/* calls for initial values */
	django.jQuery('[id$="-type"]').each(function() { updateParameterField(django.jQuery(this), false,"clean") });	
});