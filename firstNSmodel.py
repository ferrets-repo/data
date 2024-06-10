from scipy.optimize import fmin
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dd = pd.read_csv('fred_table.csv')
df = dd.copy()
df.style.format({'Maturity': '{:,.0f}'.format,'Yield': '{:,.2%}'})

sf = df.copy()
sf = sf.dropna()
sf1 = sf.copy()
sf1['Y'] = round(sf['Yield']*1,4)
sf = sf.style.format({'Maturity': '{:,.2f}'.format,'Yield': '{:,.4%}'})

print(sf1)
import matplotlib.pyplot as plt
import matplotlib.markers as mk
import matplotlib.ticker as mtick
fontsize=15
fig = plt.figure(figsize=(13,7))
plt.title("Nelson-Siegel Model - Unfitted Yield Curve",fontsize=fontsize)
ax = plt.axes()
ax.set_facecolor("black")
fig.patch.set_facecolor('white')
X = sf1["Maturity"]
Y = sf1["Y"]
plt.scatter(X, Y, marker="o", c="blue")
plt.xlabel('Time (Months)',fontsize=fontsize)
plt.ylabel('Yield',fontsize=fontsize)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.xaxis.set_ticks(np.arange(0, 360, 12))
ax.yaxis.set_ticks(np.arange(0, 4, 0.5))
ax.legend(loc="lower right", title="Yield")
plt.grid()
plt.show

β0 = 0.01
β1 = 0.01
β2 = 0.01
λ = 1.00

df['NS'] =(β0)+(β1*((1-np.exp(-df['Maturity']/λ))/(df['Maturity']/λ)))+(β2*((((1-np.exp(-df['Maturity']/λ))/(df['Maturity']/λ)))-(np.exp(-df['Maturity']/λ))))
df.style.format({'Maturity': '{:,.0f}'.format,'Yield': '{:,.2%}','NS': '{:,.2%}'})

df1 = df.copy()
df['Y'] = round(df['Yield']*100,4)
df['NS'] =(β0)+(β1*((1-np.exp(-df['Maturity']/λ))/(df['Maturity']/λ)))+(β2*((((1-np.exp(-df['Maturity']/λ))/(df['Maturity']/λ)))-(np.exp(-df['Maturity']/λ))))
df['N'] = round(df['NS']*100,4)
df2 = df.copy()
df2 = df2.style.format({'Maturity': '{:,.2f}'.format,'Y': '{:,.2%}', 'N': '{:,.2%}'})
import matplotlib.pyplot as plt
import matplotlib.markers as mk
import matplotlib.ticker as mtick
fontsize=15
fig = plt.figure(figsize=(13,7))
plt.title("Nelson-Siegel Model - Unfitted Yield Curve",fontsize=fontsize)
ax = plt.axes()
ax.set_facecolor("black")
fig.patch.set_facecolor('white')
X = df["Maturity"]
Y = df["Y"]
x = df["Maturity"]
y = df["N"]
ax.plot(x, y, color="orange", label="NS")
plt.scatter(x, y, marker="o", c="orange")
plt.scatter(X, Y, marker="o", c="blue")
plt.xlabel('Period',fontsize=fontsize)
plt.ylabel('Interest',fontsize=fontsize)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.xaxis.set_ticks(np.arange(0, 30, 5))
ax.yaxis.set_ticks(np.arange(0, 4, 0.5))
ax.legend(loc="lower right", title="Yield")
plt.grid()
plt.show()

df['Residual'] =  (df['Yield'] - df['NS'])**2
df22 = df[['Maturity','Yield','NS','Residual']]  
df22.style.format({'Maturity': '{:,.0f}'.format,'Yield': '{:,.2%}','NS': '{:,.2%}','Residual': '{:,.9f}'})

np.sum(df['Residual'])

def myval(c):
    df = dd.copy()
    df['NS'] =(c[0])+(c[1]*((1-np.exp(-df['Maturity']/c[3]))/(df['Maturity']/c[3])))+(c[2]*((((1-np.exp(-df['Maturity']/c[3]))/(df['Maturity']/c[3])))-(np.exp(-df['Maturity']/c[3]))))
    df['Residual'] =  (df['Yield'] - df['NS'])**2
    val = np.sum(df['Residual'])
    print("[β0, β1, β2, λ]=",c,", SUM:", val)
    return(val)
   
c = fmin(myval, [0.01, 0.00, -0.01, 1.0])

β0 = c[0]
β1 = c[1]
β2 = c[2]
λ = c[3]
print("[β0, β1, β2, λ]=", [c[0].round(4), c[1].round(4), c[2].round(4), c[3].round(4)])

df = df1.copy()
df['NS'] =(β0)+(β1*((1-np.exp(-df['Maturity']/λ))/(df['Maturity']/λ)))+(β2*((((1-np.exp(-df['Maturity']/λ))/(df['Maturity']/λ)))-(np.exp(-df['Maturity']/λ))))
sf4 = df.copy()
sf5 = sf4.copy()
sf5['Y'] = round(sf4['Yield']*100,4)
sf5['N'] = round(sf4['NS']*100,4)
sf4 = sf4.style.format({'Maturity': '{:,.2f}'.format,'Yield': '{:,.2%}', 'NS': '{:,.2%}'})
M0 = 0.00
M1 = 3.50
import matplotlib.pyplot as plt
import matplotlib.markers as mk
import matplotlib.ticker as mtick
fontsize=15
fig = plt.figure(figsize=(13,7))
plt.title("Nelson-Siegel Model - Fitted Yield Curve",fontsize=fontsize)
ax = plt.axes()
ax.set_facecolor("black")
fig.patch.set_facecolor('white')
X = sf5["Maturity"]
Y = sf5["Y"]
x = sf5["Maturity"]
y = sf5["N"]
ax.plot(x, y, color="orange", label="NS")
plt.scatter(x, y, marker="o", c="orange")
plt.scatter(X, Y, marker="o", c="blue")
plt.xlabel('Time (Months)',fontsize=fontsize)
plt.ylabel('Yield',fontsize=fontsize)
ax.yaxis.set_major_formatter(mtick.PercentFormatter())
ax.xaxis.set_ticks(np.arange(0, 372, 12))
ax.yaxis.set_ticks(np.arange(3, 7, 0.5))
ax.legend(loc="lower right", title="Yield")
plt.grid()
plt.show()

df.style.format({'Maturity': '{:,.0f}'.format,'Yield': '{:,.2%}','NS': '{:,.2%}'})