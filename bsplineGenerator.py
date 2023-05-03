import numpy as np
import matplotlib.pyplot as plt

def bsplineGenerator(control_points,num_points, degree):
    m,k=len(control_points),degree
    knot_vector=[0]*(m+k+1)
    for i in range(4,m+k+1):
        if i<m:knot_vector[i]=i-k
        else:knot_vector[i]=m-k
    
    t=np.linspace(0,m-k,num_points)
    # base of order 0
    base=np.zeros((m+k,num_points))
    for i in range(m+k):
        for j in range(num_points):
            if knot_vector[i]!=knot_vector[i+1]:
                time=t[j]
                if knot_vector[i]<=time<=knot_vector[i+1]:
                    base[i][j]=1
    
    # base of order k
    for order in range(1,k+1):
        baseOrder=np.zeros((m+k-order,num_points))
        for i in range(m+k-order):
            for j in range(num_points):
                time=t[j]
                coef=[0,0]
                if knot_vector[i+order]!=knot_vector[i]:
                    coef[0]=(time-knot_vector[i])/(knot_vector[i+order]-knot_vector[i])
                if knot_vector[i+order+1]!=knot_vector[i+1]:
                    coef[1]=(knot_vector[i+order+1]-time)/(knot_vector[i+order+1]-knot_vector[i+1])
                baseOrder[i][j]=coef[0]*base[i][j]+coef[1]*base[i+1][j]
        base=baseOrder
    
    curve_points=np.zeros((num_points,2))
    for i in range(num_points):
        array=[0]*m
        for j in range(m):
            array[j]=base[j][i]
        curve_points[i]=np.dot(array,control_points)
    drawBspline(control_points,curve_points)
    
def drawBspline(control_points,curve_points):
    fig,ax=plt.subplots()
    ax.plot(control_points[:,0],control_points[:,1],'o--',color='grey')
    ax.plot(curve_points[:,0],curve_points[:,1])
    plt.show()

control_points=np.array([[0, 0], [2, 3], [4, 4], [6, 4],[7,0]])
bsplineGenerator(control_points,40,3)

    
    