import numpy as np
import pickle
import math
import yaml
import os

#load the cofiguration file
def load_config(arquivo_yaml):
    with open(arquivo_yaml, 'r') as file:
        config = yaml.safe_load(file)
    return config

#load the raw data (downlink or uplink) from the .pkl file
def load_raw_data(folder=None,type_link=None):
    with open(folder, 'rb') as f:
        data_dict = pickle.load(f)
        f.close()

    raw_data = data_dict[0][type_link]['raw_data']
    file_name = os.path.basename(folder)
    print('1) The raw data from the ' + file_name + ' has been loaded!')

    return raw_data

#loads data whose lists have the same number of elements
def load_xy_data(x_axis=None, y_axis=None, n_bs=None, n_s=None, raw_data=None, all_bs=None):
     if all_bs == 'True':
        for i in range(0,n_bs):
            x0 = raw_data[i][0][x_axis]
            y0 = raw_data[i][0][y_axis]
            for t in range(1, n_s):
                x1 = raw_data[i][t][x_axis]
                x0 = np.concatenate((x0, x1))
                y1 = raw_data[i][t][y_axis]
                y0 = np.concatenate((y0, y1))
     elif all_bs == 'False':
         x0 = raw_data[n_bs][0][x_axis]
         y0 = raw_data[n_bs][0][x_axis]
         for t in range(1, n_s):
             x1 = raw_data[n_bs][t][x_axis]
             x0 = np.concatenate((x0, x1))
             y1 = raw_data[n_bs][t][y_axis]
             y0 = np.concatenate((y0, y1))
     else:
         print("The variable all_bs just be 'True' or 'False'!")

     x_data = x0.tolist()
     y_data = y0.tolist()
     return x_data, y_data

def load_data(axis=None, n_bs=None, n_s=None, raw_data=None):
     x0 = []
     for i in range(0,n_bs):
         for t in range(0,n_s):
             x1 = raw_data[i][t][axis]
             x0 = np.concatenate((x0,x1))

     x_data = x0.tolist()
     return x_data

def load_distance_data(n_bs=None,n_s=None, raw_data=None):
    distances = []
    distance=[]
    for i in range(0,n_bs):
         distance=[]
         for t in range(0,n_s):
                ue_position = raw_data[i][t]['ue_position']
                ue_dim = len(ue_position)
                for ue in range(0,ue_dim):
                       df = raw_data[i][t]['ue_bs_table']['bs_index']
                       bs_index = df.loc[ue]
                       a=-1
                       if bs_index != a:
                               ue_x = ue_position[ue][0]
                               ue_y = ue_position[ue][1]
                               bs_x = raw_data[i][t]['bs_position'][0][0][bs_index][0]
                               bs_y = raw_data[i][t]['bs_position'][0][0][bs_index][1]
                               distance = ((math.sqrt((bs_x - ue_x) ** 2 + (bs_y - ue_y) ** 2))*30)/1000
                               distances.append(distance)
    return distances

def load_position_data(n_bs=None,n_s=None, raw_data=None):
    uex_data=[]
    uey_data=[]
    bsx_data=[]
    bsy_data=[]
    uex_off_data=[]
    uey_off_data=[]
    bs_index_data=[]
    i = n_bs
    t = n_s
    ue_position = raw_data[i][t]['ue_position']
    ue_dim = len(ue_position)
    for ue in range(0,ue_dim):
            df = raw_data[i][t]['ue_bs_table']['bs_index']
            bs_index = df.loc[ue]
            ue_x = ue_position[ue][0]
            ue_y = ue_position[ue][1]
            bs_x = raw_data[i][t]['bs_position'][0][0][bs_index][0]
            bs_y = raw_data[i][t]['bs_position'][0][0][bs_index][1]
            if bs_index != -1:
                 bs_index_data.append(bs_index)
                 uex_data.append(ue_x)
                 uey_data.append(ue_y)
                 bsx_data.append(bs_x)
                 bsy_data.append(bs_y)
            else:
                 uex_off_data.append(ue_x)
                 uey_off_data.append(ue_y)
                 
    uex_data = (np.array(uex_data)*30)/1000
    uey_data = (np.array(uey_data)*30)/1000
    bsx_data = (np.array(bsx_data)*30)/1000
    bsy_data = (np.array(bsy_data)*30)/1000
    uex_off_data = (np.array(uex_off_data)*30)/1000
    uey_off_data = (np.array(uey_off_data)*30)/1000
                     
    return uex_data, uey_data, bsx_data, bsy_data,uex_off_data, uey_off_data, bs_index_data
