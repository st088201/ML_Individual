import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from math import exp
from random import random

X = np.array([i for i in range(1, 10000)]).reshape(-1, 1)
Y = np.array([i*(1+0.3*random())*exp(i**(1/3)) for i in range(1, 10000)]).reshape(-1, 1)

# Linear Regression
reg_linear = LinearRegression()
reg_linear.fit(X, Y)
Y_linear = reg_linear.predict(X)

# Polynomial Regression
preprocess_polynomial = PolynomialFeatures(degree=4)
reg_polynomial = LinearRegression()
X_poly = preprocess_polynomial.fit_transform(X)
reg_polynomial.fit(X_poly, Y)
Y_polynomial = reg_polynomial.predict(X_poly)

# Exponential Regression
expo = np.polyfit(X[:, 0], np.log(Y[:, 0]), 1, w=np.sqrt(Y[:, 0]))
Y_exponential = np.array([])
for x1 in X:
    y = exp(expo[1] + expo[0] * x1[0])
    Y_exponential = np.append(Y_exponential, [y], axis=0)

print('!!!!!')
print(Y_exponential[:3])
plt.figure(figsize=(10, 5))
plt.scatter(X, Y, s=1, c='blue')
plt.plot(X, Y_linear, c='red')
plt.plot(X, Y_polynomial, c='green')
plt.plot(X[:len(X)-1], Y_exponential[:len(Y_exponential)-1], c='pink')
print(Y)
print(Y_polynomial)
print(Y_exponential)
plt.title('Regression types comparison')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()
