#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 22 01:27:37 2020

@author: numata
"""

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.cm import ScalarMappable
import matplotlib.colors as colors
import os

import json

class SurfacePlotter:
    def __init__(self, path=None):

        self.path = path

    def import_config(self):

        if self.path is None:
            config_path = 'config.json'
        else:
            config_path = self.path
        print(config_path)

        with open(config_path) as json_data_file:
            config = json.load(json_data_file)
        return config

    def plot(self, output='output.png', use_image="./macaque_side.png"):


        conf = self.import_config()

        ch_loc = np.array(conf['basic']['coordination'])
        cc = np.random.rand(len(ch_loc))

        cmap = conf['plot_setting']['colormap_type']
        v_range= conf['plot_setting']['scale']
        colorbar = conf['plot_setting']['vis_colorbar']
        interval =conf['plot_setting']['cbar_interval']

        plt.figure(figsize=(10,7))
        plt.rcParams['font.size']=conf['plot_setting']['font_size']

        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        plt.tick_params(labelbottom=False,
                        labelleft=False,
                        labelright=False,
                        labeltop=False,
                        bottom=False,
                        left=False,
                        right=False,
                        top=False)
        img = Image.open(use_image)
        plt.imshow(np.asarray(img))

        if cmap == 'jet':
            norm = colors.Normalize(vmin=v_range[0], vmax=v_range[1])
            mappable = ScalarMappable(cmap='jet',norm=norm)
        elif cmap == 'viridis_r':
            norm = colors.Normalize(vmin=v_range[0], vmax=v_range[1])
            mappable = ScalarMappable(cmap='viridis_r',norm=norm)
        elif cmap == 'Spectral_r':
            norm = colors.Normalize(vmin=v_range[0], vmax=v_range[1])
            mappable = ScalarMappable(cmap='Spectral_r',norm=norm)
        else:
            norm = colors.Normalize(vmin=0, vmax=v_range[1])
            mappable = ScalarMappable(cmap='hot_r',norm=norm)


        for ch in range(ch_loc.shape[0]):
            im=plt.scatter(x=np.reshape(ch_loc[ch,0],-1), y=np.reshape(ch_loc[ch,1],-1),
                           marker = conf['plot_setting']['marker_shape'],
                           s = conf['plot_setting']['marker_size'],
                           c = cc[ch],
                           vmin = v_range[0], vmax = v_range[1],
                           linewidths="3", edgecolors="dimgray", cmap=cmap)

        if colorbar == True:
            colorbar_axes = plt.gcf().add_axes([0.87, 0.3, 0.02, 0.3])
            cbar=plt.colorbar(mappable,cax=colorbar_axes)
            cbar.ax.tick_params(labelsize=20)
            cbar.set_ticks(np.round(np.arange(v_range[0], v_range[1]+interval,interval),1))

        os.makedirs('output',exist_ok=True)
        plt.savefig('output/'+output,
                    bbox_inches="tight",
                    dpi = conf['plot_setting']['dpi'],
                    transparent = conf['plot_setting']['transparent'])
        plt.cla();plt.clf();plt.close()


# conf = SurfacePlotter()
# conf.plot()



