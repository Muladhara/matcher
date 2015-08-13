import json

from django.http import HttpResponse
from configurator.models import Column
from configurator.models import CleaningParameter
from configurator.models import MatchParameter
from django.core import serializers
from django.template import Context, Template
from django.template.loader import *

# returns all the columns for a given data source
def columnsByDs(request, ds=-1):
	columns = Column.objects.filter(dataSource=ds)
	response_data = {}
	response_data['columns']=serializers.serialize('json', columns)
	return HttpResponse(json.dumps(response_data), content_type="application/json")
	
# returns the parameter by cleaning type
def cleaningParameterByType(request, ct=-1):
	par = CleaningParameter.objects.filter(cleaning_type=ct)
	response_data = {}
	response_data['parameter']=serializers.serialize('json', par)
	return HttpResponse(json.dumps(response_data), content_type="application/json")
	
# returns the parameter by match type
def matchParameterByType(request, mt=-1):
    par = MatchParameter.objects.filter(matchType=mt)
    response_data = {}
    response_data['parameter']=serializers.serialize('json', par)
    return HttpResponse(json.dumps(response_data), content_type="application/json")

# default view
def welcome(request):
    html = "<html><body>Welcome to Glimpse</body></html>"
    c = Context()
    t = get_template('glimpse/index.html')
    return HttpResponse(t.render(c))