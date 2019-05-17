import pandas as pd
label = pd.Series(['a','a','a','a', 'b','b', 'c', 'c'])
x = pd.Series([0,0,0,0,1,1,2,2])
y = pd.Series([0,0,0,0,1,1,2,2])
test = pd.DataFrame({ 'x': x, 'y': y,'label':label })


print( [0,1,2,3][-1])