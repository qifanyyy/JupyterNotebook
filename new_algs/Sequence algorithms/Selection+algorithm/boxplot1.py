from pylab import plot, show, savefig, xlim, figure, \
                hold, ylim, legend, boxplot, setp, axes

# function for setting the colors of the box plots pairs
def setBoxColors(bp):
    setp(bp['boxes'][0], color='black')
    setp(bp['caps'][0], color='black')
    setp(bp['caps'][1], color='black')
    setp(bp['whiskers'][0], color='black')
    setp(bp['whiskers'][1], color='black')
    setp(bp['fliers'][0], color='black')
    setp(bp['medians'][0], color='black')

    setp(bp['boxes'][1], color='black')
    setp(bp['caps'][2], color='black')
    setp(bp['caps'][3], color='black')
    setp(bp['whiskers'][2], color='black')
    setp(bp['whiskers'][3], color='black')
    setp(bp['fliers'][1], color='black')
    setp(bp['medians'][1], color='black')

    setp(bp['boxes'][2], color='black')
    setp(bp['caps'][4], color='black')
    setp(bp['caps'][5], color='black')
    setp(bp['whiskers'][4], color='black')
    setp(bp['whiskers'][5], color='black')
    setp(bp['fliers'][2], color='black')
    setp(bp['medians'][2], color='black')

    '''setp(bp['boxes'][3], color='black')
    setp(bp['caps'][6], color='black')
    setp(bp['caps'][7], color='black')
    setp(bp['whiskers'][6], color='black')
    setp(bp['whiskers'][7], color='black')
    setp(bp['fliers'][3], color='black')
    setp(bp['medians'][3], color='black')

    setp(bp['boxes'][4], color='black')
    setp(bp['caps'][8], color='black')
    setp(bp['caps'][9], color='black')
    setp(bp['whiskers'][8], color='black')
    setp(bp['whiskers'][9], color='black')
    setp(bp['fliers'][4], color='black')
    setp(bp['medians'][4], color='black')

    setp(bp['boxes'][5], color='black')
    setp(bp['caps'][10], color='black')
    setp(bp['caps'][11], color='black')
    setp(bp['whiskers'][10], color='black')
    setp(bp['whiskers'][11], color='black')
    setp(bp['fliers'][5], color='black')
    setp(bp['medians'][5], color='black')

    setp(bp['boxes'][6], color='black')
    setp(bp['caps'][11], color='black')
    setp(bp['caps'][12], color='black')
    setp(bp['whiskers'][11], color='black')
    setp(bp['whiskers'][12], color='black')
    setp(bp['fliers'][6], color='black')
    setp(bp['medians'][6], color='black')'''
# [[ASA],[HSS]]
ds = [
        [1.000000,0.559245,0.995154,1.000000,0.005632,-0.000121,0.023012,0.000413,0.976747,1.000000,0.985885,0.003153,0.001841,0.015633,-0.000729,0.022233,0.921403,-0.000077,0.007589,-0.002516,-0.002888,-0.000550,-0.000121,1.000000,0.003141,0.010189,0.921403,0.012505,-0.005065,0.005749,-0.005874,-0.002250,0.001560],
		[1.000000,0.010189,0.003153,-0.000550,0.012505,-0.005065,0.005632,-0.002250,0.001841,-0.005874,0.001560,0.005749,-0.002888,-0.002516,0.559245,-0.000121,-0.000077],
        [-0.005874,0.921403,0.005632,0.001560,-0.000121,0.012505]
        ]


fig = figure(figsize=(5, 3))
fig.suptitle('spiral')
ax = axes()
hold(True)

bp = boxplot(ds, widths = .25)
setBoxColors(bp)


# set axes limits and labels
'''xlim(0,20.3)
ylim(-0.1,1.3)
ax.set_xticks([1.1, 3.1])'''
ax.set_xticklabels(['$\Pi_C$','ASA', 'HSS'])#, rotation=25)

#ax.set_xlabel('Dataset')
ax.set_ylabel('Adjusted Rand Index')

# draw temporary black and black lines and use them to create a legend
'''hB, = plot([1,1],'b-')
hR, = plot([1,1],'r-')
hG, = plot([1,1],'g-')
#legend((hB, hR, hG),('ASA', 'HSS', 'SR'))
hB.set_visible(False)
hR.set_visible(False)
'''
savefig('boxcompare.png')
show()