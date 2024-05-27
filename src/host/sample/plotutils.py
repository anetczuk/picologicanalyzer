#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

from matplotlib import pyplot


# 'plot_data - list of pairs of values
def image_xyplot(plot_data, plot_config=None, out_path=None, show=False):
    if plot_config is None:
        plot_config = {}

    title = plot_config.pop("title", None)
    xlabel = plot_config.pop("xlabel", None)
    ylabel = plot_config.pop("ylabel", None)
    legend_pos = plot_config.pop("legendpos", "upper left")
    labels = plot_config.pop("labels", None)

    xvalues, yvalues = zip(*plot_data)
    lines_list = pyplot.plot(xvalues, yvalues, **plot_config)

    pyplot.title(title)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)

    if labels:
        for index, plot_line in enumerate(lines_list):
            plot_label = labels[index]
            plot_line.set_label(plot_label)
        pyplot.legend(loc=legend_pos)

    if out_path:
        pyplot.savefig(out_path)
    if show:
        pyplot.show()


# 'plot_data - list of pairs of values
def image_points(plot_data, plot_config=None, out_path=None, show=False):
    if plot_config is None:
        plot_config = {}

    title = plot_config.pop("title", None)
    xlabel = plot_config.pop("xlabel", None)
    ylabel = plot_config.pop("ylabel", None)
    legend_pos = plot_config.pop("legendpos", "upper left")
    labels = plot_config.pop("labels", None)

    xvalues, yvalues = zip(*plot_data)
    lines_list = pyplot.scatter(xvalues, yvalues, s=1)

    pyplot.title(title)
    pyplot.xlabel(xlabel)
    pyplot.ylabel(ylabel)

    if labels:
        for index, plot_line in enumerate(lines_list):
            plot_label = labels[index]
            plot_line.set_label(plot_label)
        pyplot.legend(loc=legend_pos)

    if out_path:
        pyplot.savefig(out_path)
    if show:
        pyplot.show()


# 'plot_data - list of values
def image_hist(plot_data, out_path=None, show=False):
    pyplot.hist(plot_data)
    if out_path:
        pyplot.savefig(out_path)
    if show:
        pyplot.show()
