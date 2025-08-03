from sklearn.ensemble import IsolationForest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


normal_data = pd.DataFrame({
    "Hours": np.random.normal(loc=10,scale=2,size=100),
    "Location": np.zeros(100),
    "Size": np.random.normal(loc=5,scale=2,size=100)
})

anamoly = pd.DataFrame({
    "Hours": [1,24],
    "Location": [1,1],
    "Size": [200,400]
})

data = pd.concat([normal_data,anamoly],ignore_index=True)

model = IsolationForest(contamination=0.2,random_state=42)
model.fit(data)

data['prediction'] = model.predict(data)
colors = ['red' if val == -1 else 'green' for val in data["prediction"]]
plt.scatter(data['Hours'],data['Size'],c=colors)
plt.xlabel("Hours")
plt.ylabel("Size")
plt.show()