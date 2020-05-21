# Animation for Convolutional layers
## Input Parameters:
```
> ./main.py -h

usage: main.py [-h] [-i INPUT] [-k KERNEL] [-s STRIDE] [-p PADDING]
               [-t {t_conv,conv}]

Generate animation of standard and transposed convolutional layers

optional arguments:
  -h, --help                              show this help message and exit
  -i INPUT, --input INPUT                 input size (default: 3)
  -k KERNEL, --kernel KERNEL              kernel size (default: 3)
  -s STRIDE, --stride STRIDE              stride (default: 2)
  -p PADDING, --padding PADDING           padding (default: 1)
  -t {t_conv,conv}, --type {t_conv,conv}  layer type (default: t_conv)
```

## Results
### Convolution
![](gifs/conv_S1P0.gif)
![](gifs/conv_S1P1.gif)
![](gifs/conv_S2P0.gif)
![](gifs/conv_S2P3.gif)
![](gifs/conv_S3P2.gif)

### Transposed Convolution
![](gifs/transposed_conv_S1P0.gif)
![](gifs/transposed_conv_S1P1.gif)
![](gifs/transposed_conv_S2P0.gif)
![](gifs/transposed_conv_S2P1.gif)
