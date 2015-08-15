from django.db import models
from django.core.exceptions import ValidationError

class DataSource(models.Model):
	name = models.CharField(max_length=100, unique=True)
	host = models.CharField(max_length=100)
	port = models.IntegerField(default=0)
	user = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	db_name = models.CharField(max_length=100)
	table = models.CharField(max_length=100)
	
	def get_columns_as_list(self):
		# returns the ordered list of columns
		name_f = lambda x : x.name
		col_list = map(name_f,self.column.all().order_by("id"))
		return col_list
	
	def get_column_pos(self, column_name):
		# returns the position of a column in the data source given its name
		try:
			return self.get_columns_as_list().index(column_name)
		except ValueError:
			return -1
		
	def __str__(self):
		return self.name

class Cleaning(models.Model):
	name = models.CharField(max_length=100, unique=True)
	sourceDs = models.ForeignKey(DataSource, verbose_name="input data source", related_name = "cleaning_source")
	targetDs = models.ForeignKey(DataSource, verbose_name="target data source", related_name = "cleaning_target")
	
	def __str__(self):
		return self.name
	
	def get_list_repr(self):
		# returns the list representation of this cleaning
		return [x.get_list_repr() for x in self.cleaning_step.all().order_by("position")]
		
	def clean(self):
		# checks that source and target data source are distinct
		if (self.sourceDs == self.targetDs):
			raise ValidationError("Source and target data source must be distinct.")
	
class Column(models.Model):
	name = models.CharField(max_length=100)
	dataSource = models.ForeignKey(DataSource, related_name = "column")

	def get_my_pos(self):
		# returns the position of this column in its data source
		return self.dataSource.get_column_pos(self.name)

	def __str__(self):
		return self.name
	
class Blocking(models.Model):
	class Meta:
		verbose_name_plural = "Blocking criteria"
		
	criterion = models.CharField(verbose_name="criterion name", max_length=100)
	threshold = models.FloatField(default=0)
	search_discard_words = models.CharField(verbose_name="words to discard in search", default="['SPA','SRL','SCRL','SOCIETA','ARL','E','LIMITATA','DI','COOPERATIVA', 'SOCIALE','CONSORZIO']", max_length=2000)
	
	def __str__(self):
		return self.criterion + "_" + str(self.id)
	
class Matching(models.Model):
	name = models.CharField(max_length=100, unique=True)
	sourceDs1 = models.ForeignKey(DataSource, verbose_name="input data source 1", related_name = "matching_ds1")
	sourceDs2 = models.ForeignKey(DataSource, verbose_name="input data source 2", related_name = "matching_ds2")
	targetDs = models.ForeignKey(DataSource, verbose_name="target data source", related_name = "matching_target_ds")
	global_score_column = models.ForeignKey(Column, related_name = "matching_global_score")
	blocking = models.ForeignKey(Blocking, verbose_name="blocking criterion", related_name = "matching_blocking")
	blocking_column_1 = models.ForeignKey(Column, related_name = "matching_blocking_1")
	blocking_column_2 = models.ForeignKey(Column, related_name = "matching_blocking_2")
	
	def __str__(self):
		return self.name
	
	def get_list_repr(self):
		# returns the list representation of this matching
		return [x.get_list_repr() for x in self.match.all().order_by("position")]
	
	def get_mapping_list_db1(self):
		# returns the mapping list of all columns from dataSource1
		return [(x.fromColumn.get_my_pos(), x.targetColumn.get_my_pos()) for x in self.mapping.all().order_by("id").exclude(fromColumn__isnull=True)]
	
	def get_mapping_list_db2(self):
		# returns the mapping list of all columns from dataSource2
		return [(x.toColumn.get_my_pos(), x.targetColumn.get_my_pos()) for x in self.mapping.all().order_by("id").exclude(toColumn__isnull=True)]
	
	def get_match_score_column_list(self):
		# returns the ordered list of scoreColumn
		return [x.scoreColumn.get_my_pos() for x in self.match.all().order_by("id")]
	
	def clean(self):
		# checks that source and target data source are distinct
		if (self.sourceDs1 == self.targetDs) or (self.sourceDs2 == self.targetDs):
			raise ValidationError("Source and target data source must be distinct.")

class MatchType(models.Model):
	name = models.CharField(max_length=100)
	
	def get_encoded_name(self):
		return self.name.replace(" ","_")
	
	def __str__(self):
		return self.name.replace("_"," ")
	
class CleaningType(models.Model):
	name = models.CharField(max_length=100)
	
	def get_encoded_name(self):
		return self.name.replace(" ","_")
	
	def __str__(self):
		return self.name.replace("_"," ")

class MatchParameter(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=250)
	matchType = models.ForeignKey(MatchType, related_name = "match_parameter")

class Match(models.Model):
	class Meta:
		verbose_name_plural = "matches"

	position = models.IntegerField(default=0)
	matching = models.ForeignKey(Matching, related_name = "match")	
	fromColumn = models.ForeignKey(Column, verbose_name="source column 1", related_name = "match_from")
	toColumn = models.ForeignKey(Column, verbose_name="source column 2", related_name = "match_to")
	scoreColumn = models.ForeignKey(Column, verbose_name="score column", related_name = "match_score")
	type = models.ForeignKey(MatchType, verbose_name="match type", related_name = "type_match")
	parameter = models.CharField(null = True, blank = True, verbose_name="extra parameters", max_length=100)
	
	def get_list_repr(self):
		# returns the list representation of this cleaning step
		rep = [self.fromColumn.get_my_pos(),self.toColumn.get_my_pos(),self.type.get_encoded_name()]
		if self.parameter is not None and len(self.parameter)>0:
			rep.append(self.parameter)
		return rep
	
	def clean(self):
		# checks if a parameter is needed
		is_parameter_needed = len(MatchParameter.objects.filter(matchType=self.type))>0
		if is_parameter_needed and (self.parameter is None or len(self.parameter)==0):
				raise ValidationError({'parameter' : ["Parameter needed"]})
		
	def __str__(self):
		return "match #" + str(self.position)
		
class Mapping(models.Model):
	matching = models.ForeignKey(Matching, related_name = "mapping")	
	fromColumn = models.ForeignKey(Column, verbose_name="column from data source 1", related_name = "mapping_from",null=True, blank=True)
	toColumn = models.ForeignKey(Column, verbose_name="column from data source 2", related_name = "mapping_to",null=True, blank=True)
	targetColumn = models.ForeignKey(Column, verbose_name="target column", related_name = "mapping_target")
	
	def __str__(self):
		return "mapping #" + str(self.id)

class CleaningParameter(models.Model):
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=250)
	cleaning_type = models.ForeignKey(CleaningType, related_name = "cleaning_parameter")
	
class CleaningStep(models.Model):
	position = models.IntegerField(verbose_name="execution order", default=0)
	fromColumn = models.ForeignKey(Column, verbose_name="input column", related_name = "cleaning_step_from")
	toColumn = models.ForeignKey(Column, verbose_name="output column", related_name = "cleaning_step_to")
	type = models.ForeignKey(CleaningType, verbose_name="cleaning type", related_name = "type_cleaning")
	cleaning = models.ForeignKey(Cleaning, related_name = "cleaning_step")
	parameter = models.CharField(null=True, blank=True, verbose_name="extra parameters", max_length=100)
	
	def clean(self):
		# checks if a parameter is needed
		is_parameter_needed = len(CleaningParameter.objects.filter(cleaning_type=self.type))>0
		if is_parameter_needed and (self.parameter is None or len(self.parameter)==0):
				raise ValidationError({'parameter' : ["Parameter needed"]})

	def get_list_repr(self):
		# returns the list representation of this cleaning step
		rep = [self.fromColumn.get_my_pos(),self.toColumn.get_my_pos(),self.type.get_encoded_name()]
		if self.parameter is not None and len(self.parameter)>0:
			rep.append(self.parameter)
		return rep
	
			
	def __str__(self):
		return "cleaning step #" + str(self.position)

# molti a molti tra match e valori per i parametri ridondante
# molti a molti tra cleaning e valori per i parametri ridondante