import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results_of_algorithms.csv")

plt.figure(figsize = (20,10))
plt.plot(df["Index"], df["Grade School Algorithm"], label = "Grade School Algorithm")
plt.plot(df["Index"], df["Divide And Conquer Algorithm"], label = "Divide And Conquer Algorithm")
plt.plot(df["Index"], df["Karatsuba Algorithm"], label = "Karatsuba Algorithm")
plt.legend()
plt.xlabel("Number")
plt.ylabel("Time")
plt.show()
plt.savefig("")