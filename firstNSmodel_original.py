from scipy.optimize import fmin
import pandas as pd
import numpy as np

dd = pd.read_csv('fred_table.csv', index_col=0)
df = dd.copy()

β0 = 0.01
β1 = 0.01
β2 = 0.01
λ = 1.00

# df['NS'] =(β0)+(β1*((1-np.exp(-df['Maturity']/λ))/(df['Maturity']/λ)))+(β2*((((1-np.exp(-df['Maturity']/λ))/(df['Maturity']/λ)))-(np.exp(-df['Maturity']/λ))))

df['Y'] = round(df['Yield']*100,4)
df['NS'] =(β0)+(β1*((1-np.exp(-df['Maturity']/λ))/(df['Maturity']/λ)))+(β2*((((1-np.exp(-df['Maturity']/λ))/(df['Maturity']/λ)))-(np.exp(-df['Maturity']/λ))))
df['N'] = round(df['NS']*100,4)
df['Residual'] =  (df['Yield'] - df['NS'])**2
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
print(df)
