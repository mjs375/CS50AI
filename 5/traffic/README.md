## PROJECT: TRAFFIC
*a Python program that creates a neural network model trained on images of 43 types of traffic signs that can classify  images of unknown signs. Uses TensorFlow.*

### Trial & Error
- My first **get_model()** function was modeled on the settings from the *handwriting.py* program. However, these results only achieved a 0.0559 accuracy(!), so some tinkering was necessary. Available to change were number of layers (convolution, pooling, hidden), as well as numerical values such as convolution kernel size, max-pooling size, hidden layer nodes, and dropout rate.
- It seemed pretty obvious early on that a 2nd Convolution layer was key to achieving a very high accuracy. I tried to fiddle with other settings in addition to keeping that 2nd conv2D layer, but this tended to drop the accuracy a few percentage points. However, one run with x2 Convolution layers and Dropout at 0.33 scored the highest, at 0.9658%.
- Surprisingly, more Hidden layers/neurons didn't seem to help. Research on line suggested most practical problems only needed a single hidden layer, and two at the very most (for the vast majority of problems). Additionally, one should pseudo-randomly test number of units/neurons per hidden layer, for example testing 8, 16, 32, 64, 128... and seeing how it works.
- In the end my chosen settings were x2 convolution layers (32, (3,3)), dropout at 0.33, x1 hidden layer (128 nodes), and x1 max-pooling layer (2x2). This achieved an Accuracy score of 0.9683 and Loss of 0.1584.



#### TRIAL 1
- Settings:
  - Convolution:
    - x1 layer, "relu", 3x3 kernel
  - Pooling:
    - Max-Pooling, 2x2
  - Hidden Layers:
    - x1, 128 nodes
  - Dropout:
    - 0.5 rate
- Accuracy: 0.0559 after 10 Epochs
- Loss: 3.4995

#### TRIAL 2
- Settings:
  - Convolution: x2 layer, "relu", 3x3
  - Pooling: Max-Pooling, 2x2
  - Hidden Layers: x1, 254 nodes
  - Dropout: 0.5
- Accuracy: 0.9619
- Loss: 0.1977

#### TRIAL 3
- Settings:
  - Convolution: x2 layers, 3x3
  - Pooling: Max-Pooling, 2x2
  - Hidden Layers: x1, 128 nodes
  - Dropout: 0.25
- Accuracy: 0.9624
- Loss: 0.1985

### TRIAL 4
- Settings:
  - Convolution: x2 layers, 3x3
    - 2nd layer, 4x4 kernel size
  - Pooling: Max-Pooling, 2x2
  - Hidden Layers: x1, 128 nodes
  - Dropout: 0.5
- Accuracy: 0.9384
- Loss: 0.2555

### TRIAL 5
- Settings:
  - Convolution: x2 layers, 3x3
  - Pooling: 2x2 max-pooling
  - Hidden: x1, 128 nodes
  - Dropout: 0.5
- Accuracy: 0.9630
- Loss: 0.1636

### TRIAL 6
- Settings:
  - Convolution: x2 layers, 3x3
  - Pooling: 2x2 max
  - Hidden: x2, 128/64 nodes
  - Dropout: 0.5
- Accuracy: 0.9499
- Loss: 0.2220

### TRIAL 7 & 7.1
- Settings:
  - Convolution: x2 layers, 3x3
  - Pooling: 2x2, max
  - Hidden: x1, 128 nodes
  - Dropout: 0.33
- Accuracy: 0.9658 / 0.9467
- Loss: 0.1857 / 0.2621


### TRIAL 8
- Settings:
  - Convolution: x2, 3x3
  - Pooling: 2x2, max
  - Hidden: x1, 42 nodes/neurons
  - Dropout: 0.33
- Accuracy: 0.0546
- Loss: 3.5090
