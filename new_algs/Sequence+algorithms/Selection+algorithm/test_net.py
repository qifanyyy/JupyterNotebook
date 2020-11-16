import numpy as np
import matplotlib.pyplot as plt
from dataloader import parse_dataset
from genetic import EPOCHS
from net import NeuralNetwork

model = NeuralNetwork(input_size=13, hidden_size=5, output_size=3)
X_train, Y_train, X_test, Y_test = parse_dataset()
losses = 0
losses_hist= []
accuracy = []
for epoch in range(EPOCHS):
    model.train(X_train, Y_train)


    output = model.predict(X_test)
    loss = np.square(np.argmax(output, axis=1) - Y_test).mean()
    acc = len(np.where(np.argmax(output, axis=1) == Y_test)[0]) / len(Y_test)
    losses_hist.append(loss)
    accuracy.append(acc)

plt.plot([i for i in range(EPOCHS)],losses_hist )
plt.title("Loss using all input dimensions")
plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.show()