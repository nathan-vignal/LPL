from bokeh.io import show
from bokeh.layouts import column
from bokeh.models import Button, CustomJS
from bokeh.plotting import figure


s = 'r\xc3\xa9veiller'
print(s.encode().decode('string_escape'))
print("éé")