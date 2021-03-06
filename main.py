#!/usr/bin/env python

# Author: aqeelanwar
# Created: 6 March,2020, 11:29 AM
# Email: aqeel.anwar@gatech.edu

import argparse
from PIL import Image
import numpy as np
import imageio
import time
import seaborn as sns
import matplotlib.pylab as plt
from matplotlib.colors import ListedColormap


def fig2img(fig):
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    buffer = np.frombuffer(fig.canvas.tostring_argb(), dtype=np.uint8)
    buffer.shape = (w, h, 4)
    buffer = np.roll(buffer, 3, axis=2)
    w, h, d = buffer.shape
    return Image.frombytes("RGBA", (w, h), buffer.tostring())


def run_animation(output_sz, input_sz, new_input_sz, duration, layer_type, padding_sz, actual_padding_sz, stride, actual_stride, kernel_sz, kernel, fig, axes, padded_input, gif_name):
    annot = False
    if output_sz == int(output_sz):
        output_sz = int(output_sz)
        y = np.ones(shape=(output_sz, output_sz))
        img = []

        for i in range(output_sz):
            for j in range(output_sz):
                plt.pause(1e-17)
                time.sleep(duration)
                axes[0].clear()
                axes[1].clear()
                plt.suptitle(f"Stride {actual_stride}, Padding {actual_padding_sz}", fontsize=10)
                # Input and Kernel
                array_cmap = np.asarray(["#DD8047", "#CD8B67", "#A6A6A6", "#6abcff"])
                cmap_indices = np.asarray(np.sort(list(set(np.unique(kernel + padded_input)))) + 2)
                cmap_val = array_cmap[cmap_indices]
                cmap = ListedColormap(cmap_val)

                plot_vals = kernel + padded_input
                if set(np.unique(kernel + padded_input)) == set([-2, 0, 1]):
                    plot_vals = np.sign(plot_vals)

                sns.heatmap(plot_vals, yticklabels=False, xticklabels=False, ax=axes[0], annot=annot, cbar=False, linewidth=0.5, cmap=cmap)

                axes[0].set_xlabel(f"Input ({input_sz},{input_sz})", fontdict={"fontsize": 10})
                # Output
                y[i, j] = 0
                sns.heatmap(np.sign(y), yticklabels=False, xticklabels=False, ax=axes[1], annot=annot, cbar=False, linewidth=0.5, cmap=ListedColormap(["#A5Ab81", "#DBDDCD"]))

                axes[1].set_xlabel(f"Output ({output_sz},{output_sz})", fontdict={"fontsize": 10})
                img.append(fig2img(fig))
                shift_num = stride
                if (j * (stride) + kernel_sz) >= (new_input_sz + 2 * padding_sz):
                    shift_num = kernel_sz + (stride - 1) * (new_input_sz + 2 * padding_sz)
                kernel = np.roll(kernel, shift_num)

        kargs = {"duration": duration}
        imageio.mimsave(gif_name, img, **kargs)
    else:
        print("Set the parameters")


def main():
    my_parser = argparse.ArgumentParser(
        description="Generate animation of standard and transposed convolutional layers", formatter_class=lambda prog: argparse.HelpFormatter(prog, max_help_position=50)
    )
    my_parser.add_argument("-i", "--input", action="store", type=int, help="input size (default: 3)", default=3)
    my_parser.add_argument("-k", "--kernel", action="store", type=int, help="kernel size (default: 3)", default=3)
    my_parser.add_argument("-s", "--stride", action="store", type=int, help="stride (default: 2)", default=2)
    my_parser.add_argument("-p", "--padding", action="store", type=int, help="padding (default: 1)", default=1)
    my_parser.add_argument("-t", "--type", action="store", help="layer type (default: t_conv)", default="t_conv", choices=["t_conv", "conv"])
    args = my_parser.parse_args()

    layer_type = args.type
    print(f"Layer Type: {layer_type}")
    input_sz = args.input
    print(f"Input Size: {input_sz}")
    kernel_sz = args.kernel
    print(f"Kernel Size: {kernel_sz}")
    stride = args.stride
    print(f"Stride: {stride}")
    padding_sz = args.padding
    print(f"Padding: {padding_sz}")
    duration = 0.3

    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(5, 2.5))

    gif_name = layer_type + "_K" + str(kernel_sz) + "S" + str(stride) + "P" + str(padding_sz) + ".gif"
    actual_stride = stride
    actual_padding_sz = padding_sz

    x = np.ones(shape=(input_sz, input_sz), dtype=int)

    if layer_type == "conv":
        output_sz = (input_sz + 2 * padding_sz - kernel_sz) / stride + 1
        new_input = x

    elif layer_type == "t_conv":
        stride = 1
        output_sz = (input_sz - 1) * actual_stride + kernel_sz - 2 * padding_sz

        padding_sz = kernel_sz - padding_sz - 1
        zero_insertion = actual_stride - 1

        pos = np.arange(1, input_sz)
        pos = np.repeat(pos, zero_insertion)
        zero_inserted_input = np.insert(x, pos, 0, axis=1)
        zero_inserted_input = np.insert(zero_inserted_input, pos, 0, axis=0)

        new_input = zero_inserted_input

    p1 = np.zeros(shape=(padding_sz, 2 * padding_sz + new_input.shape[0]), dtype=int)
    p21 = np.zeros(shape=(new_input.shape[0], padding_sz), dtype=int)
    padded_input = np.block([[p1], [p21, new_input, p21], [p1]])

    k11 = np.ones(shape=(kernel_sz, kernel_sz), dtype=int)
    k12 = np.zeros(shape=(kernel_sz, new_input.shape[0] + 2 * padding_sz - kernel_sz), dtype=int)
    k2 = np.zeros(shape=(new_input.shape[0] + 2 * padding_sz - kernel_sz, 2 * padding_sz + new_input.shape[0]), dtype=int)

    kernel = -2 * np.block([[k11, k12], [k2]])

    run_animation(output_sz, input_sz, new_input.shape[0], duration, layer_type, padding_sz, actual_padding_sz, stride, actual_stride, kernel_sz, kernel, fig, axes, padded_input, gif_name)


if __name__ == "__main__":
    main()
