import numpy as np
import matplotlib.pyplot as plt

def bezierGenerator(control_points,num_points):
    t=np.linspace(0,1,num_points).reshape(num_points,1)
    all_points=[]
    n=len(control_points)
    first_order=np.zeros((n-1,num_points,2))
    
    for i in range(n-1):
        first_order[i]=(1-t)*control_points[i]+t*control_points[i+1]

    all_points.append(first_order)

    for i in range(1,n-1):
        points=all_points[-1]
        m=len(points)
        internal_points=np.zeros((m-1,num_points,2))
        for j in range(m-1):
            internal_points[j]=(1-t)*points[j]+t*points[j+1]
        all_points.append(internal_points)
    
    drawCurve(control_points,all_points,num_points)

def drawCurve(control_points, all_points,num_points):
    import matplotlib.animation as ani
    fig,ax=plt.subplots()
    n=len(control_points)
    ax.plot(control_points[:,0],control_points[:,1],'o--',color='grey')
    t=[i for i in range(num_points)]
    curve_points=all_points[-1][0]
        
    num=(n-1)*(n-2)//2
    lines=[]
    for i in range(num):
        line, =ax.plot([0,0],[0,0],'o-')
        lines.append(line)
    
    curve, =ax.plot([0,0],[0,0])
    lines.append(curve)
    point, =ax.plot(0,0,'o')

    def animate(i):
        m=0
        for j in range(len(all_points)-1):
            points=all_points[j]
            n=len(points)
            for k in range(n-1):
                lines[m].set_data([points[k][i][0],points[k+1][i][0]],[points[k][i][1],points[k+1][i][1]])
                m+=1
        lines[-1].set_data(curve_points[:i+1,0],curve_points[:i+1,1])
        point.set_data(curve_points[i][0],curve_points[i][1])
        return lines,point

    ani=ani.FuncAnimation(fig,animate,interval=80,blit=False,frames=t)
    ani.save('bezierCurve.gif')
    plt.show()       

control_points=np.array([[0, 0], [2, 3], [4, 3], [5, 0]])    
bezierGenerator(control_points,40)

