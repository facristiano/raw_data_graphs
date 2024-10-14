import matplotlib.pyplot as plt
import seaborn as sns
import io
from PIL import Image
from load_data import load_config, load_raw_data, load_xy_data, load_position_data
from plot_data1 import customize_graph, save_graph, draw_graph, draw_map


#load the cofiguration file
config = load_config('config.yml')

#load the raw data (downlink or uplink) from the .pkl file
raw_data = load_raw_data ('08_08_2024-02_18_27.pkl', config['plot']['type_link'])


if config['plot']['map'] == True:
            if config['plot']['complete'] == True:
                    for t in range (0,config['plot']['n_bs']):
                            for i in range(0,config['plot']['n_s']):
                                    title = config['plot']['title'] +  ' (' + str(t)  + ' BSs, simulation ' + str(i) + ')'
                                    uex_data, uey_data, bsx_data, bsy_data,uex_off_data, uey_off_data,bs_index_data = load_position_data(t, config['plot']['n_s'], raw_data)
                                    draw_map(uex_data, uey_data, bsx_data, bsy_data,uex_off_data, uey_off_data, bs_index_data, title,config['plot']['xlabel'], config['plot']['ylabel'], config['plot']['auto_scale'], config['plot']['xlim'], config['plot']['ylim'], config['plot']['figsize'], config['plot']['resolution'], config['plot']['save_as'], config['plot']['complete'],config['plot']['grid'] )
            else:
                            uex_data, uey_data, bsx_data, bsy_data,uex_off_data, uey_off_data,bs_index_data = load_position_data(config['plot']['n_bs'], config['plot']['n_s'], raw_data)
                            draw_map(uex_data, uey_data, bsx_data, bsy_data,uex_off_data, uey_off_data, bs_index_data, config['plot']['title'],config['plot']['xlabel'], config['plot']['ylabel'], config['plot']['auto_scale'], config['plot']['xlim'], config['plot']['ylim'], config['plot']['figsize'], config['plot']['resolution'], config['plot']['save_as'], config['plot']['complete'],config['plot']['grid'])
else:
            {}
