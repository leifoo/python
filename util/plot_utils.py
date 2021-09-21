import numpy as np
import matplotlib.pyplot as plt

def plot(y, x=None, figsize=[16, 10], title='', color=None, labels=[], legendout=False, 
         show=True, save=False):    
    '''
    Plot y versus x as lines and/or markers.
    
    Parameters
    ----------
    y : 1D or 2D array of shape [n_samples] or [n_components, n_samples]
        The input y
    x : 1D array or None, default=None
        The x axis, if x == None, plot the index starting from zero
    figsize : tuple or list of float, default=[16, 10] instead of [6.4, 4.8] 
        The width, height of the figure in inches
    title : str, default=''
        The title to the figure.
    color : str or list of str, default=None,
        The line color 
    labels : list of str, default=[]
        The labels of the components of input y
    legendout : bool, default=False
        Whether to put legend outside of the plot
    show : bool, default=True
        Whether to display figure.
    save : bool, default=False
        Whether to save figure

    Return:
        c:  corr
    '''
    
    fig, ax = plt.subplots(1, 1, figsize=figsize)
    fig.suptitle(title, fontsize=16)

    if x is None:
        x = np.arange(0, y.shape[-1])

    if not color:
        color = plt.rcParams['axes.prop_cycle'].by_key()['color']

    dim = len(y.shape)

    if dim == 1:
        ax.plot(x, y, color[0], label=labels)
    else:
        if not labels:
            labels = ['y_'+str(i) for i in range(y.shape[0])]
        for i in range(y.shape[0]):
            ax.plot(x, y[i], color[i], label=labels[i])

        # Add legend
        ax.legend(loc="upper right", fontsize=14)
        if legendout:
            # Shrink current axis by 20%
            box = ax.get_position()
            ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])

            ax.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., ncol=1, fontsize=14)

    if show:
        plt.show()

    if save:
        fname = ''
        fname if title else 'y'
        plt.imsave(f"{fname}.png")


# def subplot(data, nrows=1, ncols=1, figsize=(16, 10), title='', subtitle=[],):    
#     fig, ax = plt.subplots(nrows, ncols, figsize=figsize)
#     fig.suptitle(title)

#     for i in range(nrows):
#         for j in range(ncols):
#             ax[i, j].plot(x, data[0], label='Gas', marker='o')

#             if title:
#                 ax[i, j].set_title(title[i*ncols+j], fontsize=16)
#     ax.set_xlabel(x_label, fontsize=16)
#     ax.set_xticks(np.arange(len(x)))
#     ax.set_xticklabels(labels)
#     ax.tick_params(axis="x", labelsize=14, labelrotation=90)
#     # ax.set_ylabel(f"{metric}", fontsize=16)
#     ax.set_ylabel(f"Metric", fontsize=16)
#     # ax.set_yticks(np.arange(0, 81, 10))
#     ax.tick_params(axis="y", labelsize=14)
#     ax.legend(loc="upper left", fontsize=14)
#     ax.legend(bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0., ncol=1, fontsize=14)
    
#     plt.imsave(f"{title}.png")

#     plt.show()

if __name__ == "__main__":
    # example data
    x = np.arange(0.1, 4, 0.1)
    y1 = np.exp(-1.0 * x)
    y2 = np.exp(-0.5 * x)

    print(f'len(y1.shape) = {len(y1.shape)}')
    plot(y1, title='y1', show=False)
    plot(y2, x, title='y2', show=False)
    plot(np.stack((y1, y2), axis=0), x, title='y', color=['k', 'r', 'b'], legendout=True)