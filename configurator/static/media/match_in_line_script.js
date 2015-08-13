/* match in line script. Also works for mappings */
/* indeed handles all the forms in the Matching page */
django.jQuery(document).ready(function() {
	/* when a data source is changed in the main form */
	/* updates the related columns in the in line form */
	django.jQuery("#id_sourceDs1").change(function() { dataSourceChange(this.value, ".field-fromColumn select", true) } );
	django.jQuery("#id_sourceDs2").change(function() { dataSourceChange(this.value, ".field-toColumn select", true) } );
	/* the same for score column */
	django.jQuery("#id_targetDs").change(function() { dataSourceChange(this.value, ".field-scoreColumn select", true) });
	django.jQuery("#id_targetDs").change(function() { dataSourceChange(this.value, ".field-targetColumn select", true) });
	/* the same for global score */
	django.jQuery("#id_targetDs").change(function() { dataSourceChange(this.value, "#id_global_score_column", true) });
	/* the same for blocking columns */
	django.jQuery("#id_sourceDs1").change(function() { dataSourceChange(this.value, "#id_blocking_column_1", true) } );
	django.jQuery("#id_sourceDs2").change(function() { dataSourceChange(this.value, "#id_blocking_column_2", true) } );
	
	/* when the page is loaded, the initial values */
	/* are kept, but the options are restricted */
	/* calls for initial values */
	dataSourceChange(django.jQuery("#id_sourceDs1").val(),".field-fromColumn select",false);
	dataSourceChange(django.jQuery("#id_sourceDs2").val(),".field-toColumn select",false);
	/* the same for score column */
	dataSourceChange(django.jQuery("#id_targetDs").val(), ".field-scoreColumn select", false);
	dataSourceChange(django.jQuery("#id_targetDs").val(), ".field-targetColumn select", false);
	/* the same for global score */
	dataSourceChange(django.jQuery("#id_targetDs").val(), "#id_global_score_column", false);
	/* the same for block columns */
	dataSourceChange(django.jQuery("#id_sourceDs1").val(),"#id_blocking_column_1",false);
	dataSourceChange(django.jQuery("#id_sourceDs2").val(),"#id_blocking_column_2",false);
	
	/* if a parameter type is changed, the respective */
	/* text field is updated with the appropriate placeholder */	
	django.jQuery('[id$="-type"]').on('change', function() { updateParameterField(django.jQuery(this),true,"match") });
	/* calls for initial values */
	django.jQuery('[id$="-type"]').each(function() { updateParameterField(django.jQuery(this), false,"match") });	
});