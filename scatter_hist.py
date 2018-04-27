import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter

def scatterHist(x, y, title, figSave, slopeAt=56,
                deg=3, xbinwidth=0.25, ybinwidth=1000):
    
    nullfmt = NullFormatter()         # no labels
    
    x, y = x.align(y, join='inner')

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left + width + 0.1

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]

    # start with a rectangular Figure
    plt.figure(1, figsize=(8, 8))

    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)

    # no labels
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)

    # the scatter plot:
    
    # function for poly fit
    def regLine(x, y, deg, slopeAt):
        fitted = np.zeros(len(y))
        slope = 0
        fit = np.polyfit(x, y, deg=deg)
        x_sorted = x.copy().sort_values()

        for i in np.arange(0, deg):
            slope += (deg - i) * fit[i] * np.power(slopeAt, deg - 1 - i)
        print('\nSlope of cubic at empl =', slopeAt, '%:', slope)
        
        for i in np.arange(0, (deg + 1)):
            fitted += fit[i] * np.power(x_sorted, deg - i)
        return fitted

    axScatter.plot(x.sort_values(), regLine(x,y, deg, slopeAt), color='red')
    axScatter.plot(x, y, 'o', alpha=0.5)
    axScatter.set(xlabel= "Skill's weighted 'employment rate'",
                  ylabel="Skill's weighted GDP pc 2016 PPP",
                  title=title)
    
    # now determine nice limits by hand:
    xmax = np.max(x)
    xmin = np.min(x)
    ymax = np.max(y)
    ymin = np.min(y)
    
    axScatter.set_xlim((xmin, xmax))
    axScatter.set_ylim((ymin, ymax))
    
    xbins = np.arange(xmin, xmax + xbinwidth, xbinwidth)
    ybins = np.arange(ymin, ymax + ybinwidth, ybinwidth)
    axHistx.hist(x, bins=xbins)
    axHisty.hist(y, orientation='horizontal', bins=ybins)
    
    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())
    
    plt.savefig(figSave, bbox_inches='tight')

    plt.show()
    


def doubleScatterHist(x, y, 
                      x2, y2,
                      title, figSave, slopeAt=56,
                      deg=3, xbinwidth=0.25, ybinwidth=1000):
    
    nullfmt = NullFormatter()         # no labels
    
    x, y = x.align(y, join='inner')
    x2, y2 = x2.align(y2, join='inner')

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left + width + 0.1

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]

    # start with a rectangular Figure
    plt.figure(1, figsize=(8, 8))

    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)

    # no labels
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)

    # the scatter plot:
    
    # function for poly fit
    def regLine(x, y, deg, slopeAt):
        fitted = np.zeros(len(y))
        slope = 0
        fit = np.polyfit(x, y, deg=deg)
        x_sorted = x.copy().sort_values()

        for i in np.arange(0, deg):
            slope += (deg - i) * fit[i] * np.power(slopeAt, deg - 1 - i)
        print('\nSlope of cubic at empl =', slopeAt, '%:', slope)
        
        for i in np.arange(0, (deg + 1)):
            fitted += fit[i] * np.power(x_sorted, deg - i)
        return fitted

    axScatter.plot(x.sort_values(), regLine(x,y, deg, slopeAt), color='grey')
    axScatter.plot(x, y, 'o', alpha=0.25)
    axScatter.plot(x2.sort_values(), regLine(x2,y2, deg, slopeAt), color='red')
    axScatter.plot(x2, y2, 'o', color='green', alpha=0.5)
    axScatter.set(xlabel= "Skill's weighted 'employment rate'",
                  ylabel="Skill's weighted GDP pc 2016 PPP",
                  title=title)
    
    # now determine nice limits by hand:
    xmax = np.max(x)
    xmin = np.min(x)
    ymax = np.max(y)
    ymin = np.min(y)
    
    axScatter.set_xlim((xmin, xmax))
    axScatter.set_ylim((ymin, ymax))
    
    xbins = np.arange(xmin, xmax + xbinwidth, xbinwidth)
    ybins = np.arange(ymin, ymax + ybinwidth, ybinwidth)
    axHistx.hist(x, bins=xbins, alpha=0.25)
    axHisty.hist(y, orientation='horizontal', bins=ybins, alpha=0.25)
    axHistx.hist(x2, bins=xbins, color='green')
    axHisty.hist(y2, orientation='horizontal', bins=ybins, color='green')
    
    axHistx.set_xlim(axScatter.get_xlim())
    axHisty.set_ylim(axScatter.get_ylim())
    
    plt.savefig(figSave, bbox_inches='tight')

    plt.show()
    
