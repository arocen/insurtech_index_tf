# visualize computed index
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # use Chinese font

def drawCurves(indices:pd.DataFrame):
    '''draw curves of indices'''
    # draw curves with method of pandas
    plot = indices.plot(title="保险科技指标")
    plt.show()
    return

