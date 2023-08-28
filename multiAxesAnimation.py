import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as ani
from matplotlib.patches import ConnectionPatch

fig,(axl,axr)=plt.subplots(
    ncols=2,
    sharey=True,
    figsize=(6,2),
    gridspec_kw=dict(width_ratios=[1,3],wspace=0))

axl.set_aspect(1)
axr.set_box_aspect(1/3)
axr.yaxis.set_visible(False)
axr.xaxis.set_ticks([0,np.pi,2*np.pi],["0",r"$\pi$",r"$2\pi$"])

x=np.linspace(0,2*np.pi,50)
print(x)
axl.plot(np.cos(x),np.sin(x),"k",lw=0.3)
point, =axl.plot(0,0,'o')
sine, =axr.plot(x,np.sin(x))


con=ConnectionPatch(
    (1,0),
    (0,0),
    'data',
    'data',
    axesA=axl,
    axesB=axr,
    color='C0',
    ls='dotted'
)
fig.add_artist(con)

def animate(i):
    print(i)
    x=np.linspace(0,i,int(i*25/np.pi))
    sine.set_data(x,np.sin(x))
    x,y=np.cos(i),np.sin(i)
    point.set_data([x],[y])
    con.xy1=x,y
    con.xy2=i,y
    return point,sine,con

ani=ani.FuncAnimation(fig,animate,interval=50,blit=False,frames=x,repeat_delay=100)
plt.show()
