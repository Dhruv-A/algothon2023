import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('prices.txt', sep='   ')

days = [i for i in range(1, 501)]
for col in df:
    plt.plot(days, df[col], label=col)
plt.xlabel('Days')
plt.ylabel('Price')
plt.show()