# **Training your own model!**

I've finally managed to make this guide.

![Example of convolution. Author of gif: Michael Plotke](2D_Convolution_Animation.gif)

Model was created using Convolutional Neural Network algorithm. It was trained on 32x32 grayscale chess tiles. Predicts
chessboards layouts from online chessboard screenshots.

* 5x5x32 Input Convolution layer
* 5x5x64 Convolution layer
* 8x8x1024 Dense Fully Connected layer
* 1024x13 Dropout + softmax Readout layer

