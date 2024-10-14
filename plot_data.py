import matplotlib.pyplot as plt
import seaborn as sns
import io
from PIL import Image
from load_data import load_config, load_raw_data, load_xy_data, load_position_data, load_distance_data, load_data


#load the cofiguration file
config = load_config('config.yml')

#load the raw data (downlink or uplink) from the .pkl file
raw_data = load_raw_data ('08_08_2024-02_18_27.pkl', config['plot']['type_link'])

#load position data
uex_data, uey_data, bsx_data, bsy_data,uex_off_data, uey_off_data,bs_index_data = load_position_data(config['plot']['n_bs'], config['plot']['n_s'], raw_data)

if config['plot']['x_var'] == 'distance' or config['plot']['y_var']=='distance':
        if config['plot']['x_var']=='distance':
              x_data = load_distance_data(config['plot']['n_bs'], config['plot']['n_s'], raw_data)
              y_data = load_data(config['plot']['y_var'],config['plot']['n_bs'],config['plot']['n_s'], raw_data)
        else:
              y_data = load_distance_data(config['plot']['n_bs'], config['plot']['n_s'], raw_data)
              x_data = load_data(config['plot']['x_var'],config['plot']['n_bs'],config['plot']['n_s'], raw_data)

else:
      x_data, y_data = load_xy_data(config['plot']['x_var'],config['plot']['y_var'],config['plot']['n_bs'],config['plot']['n_s'], raw_data)

#customize the graph
plt.figure(figsize=tuple(config['plot']['figsize']), dpi=config['plot']['resolution'])
plt.title(config['plot']['title'])
plt.xlabel(config['plot']['xlabel'])
plt.ylabel(config['plot']['ylabel'])
match config['plot']['auto_scale']:
    case 'True':
        plt.autoscale()
    case 'False':
        plt.xlim((config['plot']['xlim']))
        plt.ylim(config['plot']['ylim'])
plt.grid(config['plot']['grid'])


#draw the graph
match config['plot']['graph_type']:
    case 'scatter':
         fig =  sns.scatterplot(x=x_data, y=y_data, color='purple', size=y_data, sizes=(1,1), legend=False)
    case 'line':
         fig = sns.lineplot(x=x_data, y=y_data)
    case 'boxplot':
         fig = sns.boxplot(x=x_data, y=y_data)
    case 'bar':
         fig = sns.barplot(x=x_data, y=y_data, ci=None)
    case 'histplot':
         fig = sns.histplot(x_data)
    case _:
         print("Check the 'graph_type' parameter!")

# save the graph
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
plt.close()
imagem1 = Image.open(buf)
imagem1.show()
print('2) Your graph is ready!')
s = input("3) Do you want to save your graph(y/n)?:")
match s:
    case "y":
        imagem1.save(config['plot']['save_as'])
        print("4) Graphic saved as " + str(config['plot']['save_as']) + "!")
    case _:
        print ("4) Make the desired changes to config.yml!")

#customize the map
plt.figure(figsize=tuple(config['plot']['figsize_map']), dpi=config['plot']['resolution_map'])
plt.title(config['plot']['title_map'])
plt.xlabel(config['plot']['xlabel_map'])
plt.ylabel(config['plot']['ylabel_map'])
plt.xlim(config['plot']['xlim_map'])
plt.ylim(config['plot']['ylim_map'])

#draw the map
test = len(uex_off_data)
if  test != 0:
    fig = sns.scatterplot(x=uex_off_data, y=uey_off_data, marker='o',size=10, color='red', legend=False)
else:
    {}
fig = sns.scatterplot(x=uex_data, y=uey_data,hue=bs_index_data, marker='o', palette='colorblind',size=10 ,legend=False)
fig = sns.scatterplot(x=bsx_data, y=bsy_data, hue=bs_index_data, marker='^',size=bs_index_data,sizes=(200,200), palette="colorblind",legend=False)

#save the map
buf = io.BytesIO()
plt.savefig(buf, format='png')
buf.seek(0)
plt.close()
imagem2 = Image.open(buf)
imagem2.show()
print('5) Your map is ready!')

s = input("6) Do you want to save your map(y/n)?:")

match s:
    case "y":
        imagem2.save(config['plot']['save_map_as'])
        print('7) Map saved as ' + str(config['plot']['save_map_as']) + '!')
    case _:
        print ("7) Make the desired changes to config.yml!")


