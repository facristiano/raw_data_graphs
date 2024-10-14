import matplotlib.pyplot as plt
import seaborn as sns
import io
from PIL import Image


#customize the graph
def customize_graph (title=None, xlabel=None, ylabel=None, auto_scale=True, xlim=None, ylim=None, figsize=None,resolution=None, grid=None):
        plt.figure(figsize=figsize, dpi=resolution)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        match auto_scale:
            case 'True':
                plt.autoscale()
            case 'False':
                plt.xlim(xlim)
                plt.ylim(ylim)
        plt.grid(grid)
        
        return ()


#save the graph       
def save_graph (complete=None, save_as=None):
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        plt.close()
        imagem = Image.open(buf)
        if complete == False:
                imagem.show()
                print('2) Your graph is ready!')
                s = input("3) Do you want to save(y/n)?:")
                match s:
                        case "y":
                             imagem.save(save_as)
                        case _:
                             print ("4) Make the desired changes to config.yml!")
        else:
                imagem.save(save_as)
                
        return ()
      

# draw the graph               
def draw_graph (x_var=None, y_var=None, n_bs=None, n_s=None, figsize=None, resolution=None, title=None, xlabel=None, ylabel=None, auto_scale=True, xlim=None, ylim=None, grid=None, raw_data=None):
        if x_var == 'distance' or y_var == 'distance':
              if x_var == 'distance':
                     x_data = load_distance_data(n_bs, n_s, raw_data)
                     y_data = load_data(y_var,n_bs,n_s, raw_data)
              else:
                     y_data = load_distance_data(n_bs,n_s,raw_data)
                     x_data = load_data(x_var,n_bs,n_s,raw_data)

        else:
           x_data, y_data = load_xy_data(x_var,y_var,n_bs,n_s, raw_data)

        #customize the graph
        customize_graph (title, xlabel, ylabel, auto_scale=True, xlim=None, ylim=None)

        #draw the graph
        match graph_type:
            case 'scatter':
                fig =  sns.scatterplot(x=x_data, y=y_data,size=1)
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
        save_graph(False, save_as)
        
        return ()


def draw_map (uex_data, uey_data, bsx_data, bsy_data,uex_off_data, uey_off_data, bs_index_data, title, xlabel, ylabel, auto_scale=True, xlim=None, ylim=None,figsize=None,resolution=None, save_as=None, complete=False, grid=None ):
                sns.scatterplot(x=uex_off_data, y=uey_off_data, marker='o',size=10, color='red', legend=False)
                sns.scatterplot(x=bsx_data, y=bsy_data, hue=bs_index_data, marker='^', palette="colorblind", size=1,legend=False) 
                sns.scatterplot(x=uex_data, y=uey_data,hue=bs_index_data, marker='o', palette='colorblind',size=10,legend=False)
                customize_graph (title, xlabel, ylabel, auto_scale=True, xlim=None, ylim=None,figsize=None,resolution=None, grid=None)
                save_graph(complete)
                
                return ()










