import pandas as pd
from bokeh.charts import VBar, output_file, show
from bokeh.models.glyphs import VBar
from bokeh.models import FuncTickFormatter

x = ['cheese making', 'squanching', 'leaving harsh criticisms']
y = [25, 40, 1]
df = pd.DataFrame({'skill': x, 'pct jobs with skill': y})
p = VBar(df, 'index', values='pct jobs with skill', legend=False)
label_dict = {}
for i, s in enumerate(x):
    label_dict[i] = s

p.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict)
show(p)
p.xaxis.formatter = FuncTickFormatter(code="""
    var labels = %s;
    return labels[tick];
""" % label_dict)
show(p)

output_file("bar.html")