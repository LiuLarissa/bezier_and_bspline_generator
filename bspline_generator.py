import numpy as np
import matplotlib.pyplot as plt

def generateBspline(controlPoints,k,num=100):
    n=len(controlPoints)
    # knot vector
    v0=np.linspace(0,0,k+1)
    v1=np.linspace(1,n-k-1,n-k-1)
    v2=np.linspace(n-k,n-k,k+1)
    knot=np.concatenate((v0,v1,v2))
    # knot=[0,0,0,0,0.5,2,3,3,3,3]
    
    t=np.linspace(0,n-k,num)

    # order 0
    BF=np.zeros((knot.size-1,num))
    for i in range(knot.size-1):
        if knot[i]!=knot[i+1]:
            for j in range(num):
                time=t[j]
                if i==knot.size-k-2:
                    if knot[i]<=time<=knot[i+1]:BF[i][j]=1
                else:
                    if knot[i]<=time<knot[i+1]:BF[i][j]=1
    
    # order recurison
    for order in range(1,k+1):
        tmp=np.zeros((knot.size-1-order,num))
        for i in range(knot.size-1-order):
            for j in range(num):
                time=t[j]
                if knot[i+order]!=knot[i]:
                    tmp[i][j]+=(time-knot[i])*BF[i][j]/(knot[i+order]-knot[i])
                if knot[i+order+1]!=knot[i+1]:
                    tmp[i][j]+=(knot[i+order+1]-time)*BF[i+1][j]/(knot[i+order+1]-knot[i+1])
        BF=tmp
    
    points=np.zeros((num,2))
    for i in range(num):
        for p in range(n):
            point=controlPoints[p]
            points[i]+=BF[p][i]*point
    return points
    
def drawBspline(points,controlPoints):
    fig,ax=plt.subplots()
    ax.plot(points[:,0],points[:,1])
    ax.plot(controlPoints[:,0],controlPoints[:,1],'o--')
    plt.show()

# control points S0-S4
controlPoints=np.array([[0, 0], [2, 3], [6, 3], [9, 0],[10,3]])
points=generateBspline(controlPoints,3)
drawBspline(points,controlPoints)