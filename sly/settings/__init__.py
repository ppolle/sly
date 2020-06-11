import sys

if 'runserver' or 'collecstatic' in sys.argv:
	from sly.settings.local import *
else:
	from sly.settings.prod import *