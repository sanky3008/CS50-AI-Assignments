In this assignment, to solve this problem, I first tried out the most basic model architecture, which goes as:
1. Convolution Layer - 32 Filters, 3x3 kernel, activation = relu
2. Max Pooling Layer - Pool size = 2x2
3. Flatten Layer
4. Dense layer for output - 256 units, activation = relu
5. Dense layer for output - NUM_Categories amount of outputs

For the above architecture, the accuracy is = (96.11 + 95.56 + 96.56)/3 = 96.07%

Adding a dropout of 0.5 in the above model between 5 & 6 results in the following model:
1. Convolution Layer - 32 Filters, 3x3 kernel, activation = relu
2. Max Pooling Layer - Pool size = 2x2
3. Flatten Layer
4. Dense layer for output - 256 units, activation = relu
5. Dropout - 0.5
6. Dense layer for output - NUM_Categories amount of outputs

For the above architecture, the accuracy is = (96.35 + 94.84 + 94.37)/3 = 95.18%

=> Adding a dropout decreases the accuracy a bit

Adding another dense layer between 5 & 6, the following architecture results:
1. Convolution Layer - 32 Filters, 3x3 kernel, activation = relu
2. Max Pooling Layer - Pool size = 2x2
3. Flatten Layer
4. Dense layer for output - 256 units, activation = relu
5. Dropout - 0.5
6. Dense layer for output - 256 units, activation = relu
7. Dense layer for output - NUM_Categories amount of outputs

For the above model, the accuracy is = (94.52 + 95.95 + 94.13)/3 = 94.86%

=> Adding another layer doesn't really help the accuracy. In fact, it has reduced a bit now.

Removing the additional dense layer, I'll now try adding another set of convolution and pooling layer - which results in the following architecture:
1. Convolution Layer - 32 Filters, 3x3 kernel, activation = relu
2. Max Pooling Layer - Pool size = 2x2
3. Convolution Layer - 32 Filters, 3x3 kernel, activation = relu
4. Max Pooling Layer - Pool size = 2x2
5. Flatten Layer
6. Dense layer for output - 256 units, activation = relu
7. Dropout - 0.5
8. Dense layer for output - NUM_Categories amount of outputs

Accuracy of the same is = (94.05 + 94.84 + 94.76)/3 = 94.55%

=> Adding another set of convolution + pooling did not help, but rather reduced it a bit.

INFERENCES:
1. Model accuracy is not directly proportional to number of layers, in fact, sometimes adding a layer might reduce the accuracy
2. Just adding more convolution and pooling layer sets does not increase the accuracy that much in all cases
3. Adding dropout slightly reduced the accuracy, which is expected as it is introduced to avoid overfitting