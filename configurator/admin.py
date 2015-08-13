from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from configurator.models import DataSource
from configurator.models import Cleaning
from configurator.models import Column
from configurator.models import Blocking
from configurator.models import Matching
from configurator.models import Match
from configurator.models import CleaningStep
from configurator.models import Mapping

from django import forms

# to require at least one in line
class AtLeastOneRequiredInlineFormSet(BaseInlineFormSet):
	def clean(self):
		"""Check that at least one service has been entered."""
		super(AtLeastOneRequiredInlineFormSet, self).clean()
		if any(self.errors):
			return    
		if not any(cleaned_data and not cleaned_data.get('DELETE', False)
			for cleaned_data in self.cleaned_data):
			raise forms.ValidationError('At least one item required.')

class MatchValidationInlineFormSet(AtLeastOneRequiredInlineFormSet):
	def clean(self):
		"""Performs al the validation checks"""
		"""and the AtLeastOneRequiredInLineFormSet"""
		# cleaned_data: {'is_blocking_pair': False, 'fromColumn': <Column: COL_2>, 'parameter': u'', 'columns_to_keep': u'1', u'id': None, 'toColumn': <Column: COL_A>, 'position': 0, 'type': <MatchType: weighted jaccard>, 'matching': <Matching: test_matching>, u'DELETE': False}

		super(MatchValidationInlineFormSet, self).clean()
		if any(self.errors):
			return
		
		# to save in the matching the score columns
		self.instance.__score_columns__ = []
		
		# each score column can be used only once
		score_cols = []
		for match in self.cleaned_data:
			if 'scoreColumn' in match and not match.get('DELETE', False):
				score_col_name = match['scoreColumn'].name
				if score_col_name not in score_cols:
					score_cols.append(score_col_name)
					# saves in the Matching the used score columns
					self.instance.__score_columns__.append(score_col_name)
				else:
					raise forms.ValidationError('A score column can be used only once.')
		
		# checks that score and target columns are disjoint
		if self.instance.__dict__.get('__score_columns__',None) is not None and self.instance.__dict__.get("__target_columns__",None):
			if len(set(self.instance.__score_columns__) & set(self.instance.__target_columns__))>0:
				raise forms.ValidationError('There are overlappings between score and target columns.')
		# compatibility with global score
		if len(set(self.instance.__score_columns__) & set([self.instance.global_score_column.name]))>0:
			raise forms.ValidationError('There are overlappings between score and global score columns.')
			
class MappingValidationInlineFormSet(AtLeastOneRequiredInlineFormSet):
	def clean(self):
		"""Performs al the validation checks"""
		"""and the AtLeastOneRequiredInLineFormSet"""
		super(MappingValidationInlineFormSet, self).clean()
		if any(self.errors):
			return
				
		# for each mapping either the column from data source 1
		# or the column from data source 2 is specified
		for mapp in self.cleaned_data:
			if 'fromColumn' in mapp and 'toColumn' in mapp and not mapp.get('DELETE', False):
				if (mapp['fromColumn'] is None and mapp['toColumn'] is None) or (mapp['fromColumn'] is not None and mapp['toColumn'] is not None):
					raise forms.ValidationError('Exactly one column is required for each mapping.')
		
		# to save in the matching the target columns
		self.instance.__target_columns__ = []
		
		# each target column can be used only once
		target_cols = []
		for mapp in self.cleaned_data:
			if 'targetColumn' in mapp and not mapp.get('DELETE', False):
				target_col_name = mapp['targetColumn'].name
				if target_col_name not in target_cols:
					target_cols.append(target_col_name)
					self.instance.__target_columns__.append(target_col_name)
				else:
					raise forms.ValidationError('A target column can be used only once.')
		
		# checks that score and target columns are disjoint
		if self.instance.__dict__.get('__score_columns__',None) is not None and self.instance.__dict__.get("__target_columns__",None):
			if len(set(self.instance.__score_columns__) & set(self.instance.__target_columns__))>0:
				raise forms.ValidationError('There are overlappings between score and target columns.')
		# compatibility with global score
		if len(set(self.instance.__target_columns__) & set([self.instance.global_score_column.name]))>0:
			raise forms.ValidationError('There are overlappings between target and global score columns.')
		
class MatchInLine(admin.TabularInline):
	model = Match
	odering = ['position']
	formset = MatchValidationInlineFormSet	

	class Media:
		js = ("media/update_parameters.js", "media/update_columns.js", "media/match_in_line_script.js",)

class MappingInLine(admin.TabularInline):
	model = Mapping
	formset = MappingValidationInlineFormSet

	class Media: 
		js = ("media/mapping_in_line_script.js",)

class BlockingInLine(admin.TabularInline):
	model = Blocking

class MatchingAdmin(admin.ModelAdmin):
	inlines = [
		MatchInLine, MappingInLine
	]

class CleaningStepInlineFormSet(AtLeastOneRequiredInlineFormSet):
	def clean(self):
		"""Performs al the validation checks"""
		"""and the AtLeastOneRequiredInLineFormSet"""
		super(CleaningStepInlineFormSet, self).clean()
		if any(self.errors):
			return
		# checks that no output column is used twice 
		# with different input columns.
		# Conversely, the same pair can be repeated if
		# more than one cleaning is needed on the input column.
		stg = dict()
		for clean_step in self.cleaned_data:
			if 'fromColumn' in clean_step and 'toColumn' in clean_step and not clean_step.get('DELETE', False):
				fromColumn = clean_step['fromColumn']
				toColumn = clean_step['toColumn']
				if toColumn not in stg:
					stg[toColumn] = fromColumn
				elif stg[toColumn] != fromColumn:
					raise forms.ValidationError("An output column cannot be used for different input columns.")

class CleaningStepInLine(admin.TabularInline):
	model = CleaningStep
	ordering = ['position']
	formset = CleaningStepInlineFormSet

	class Media:
		js = ("media/update_parameters.js", "media/update_columns.js", "media/cleaning_step_in_line_script.js",)

class CleaningAdmin(admin.ModelAdmin):
	inlines = [
		CleaningStepInLine,
    ]

class ColumnInLine(admin.TabularInline):
	model = Column
	formset = AtLeastOneRequiredInlineFormSet

class DataSourceAdmin(admin.ModelAdmin):
	inlines = [
		ColumnInLine,
	]

# Register your models here.
admin.site.register(DataSource, DataSourceAdmin)
admin.site.register(Cleaning, CleaningAdmin)
admin.site.register(Matching, MatchingAdmin)
admin.site.register(Blocking)