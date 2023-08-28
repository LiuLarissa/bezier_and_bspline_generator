import numpy as np
import matplotlib.pyplot as plt

def generateBspline(control_points,order,num_points):
    n=len(control_points)

    # knot vector
    V=[0 for i in range(n+1+order)]
    k=1
    for i in range(order+1,len(V),1):
        V[i]=k
        if k!=n-order:k+=1

    t=np.linspace(0,n-order,num_points)
    coeff=np.zeros((len(V)-1,num_points))

    # order 0
    for i in range(len(V)-1):
        for j in range(num_points):
            time=t[j]
            if i==len(V)-order-2:
                if V[i]<=time<=V[i+1]:coeff[i][j]=1
            else:
                if V[i]<=time<V[i+1]: coeff[i][j]=1
    
    # order recursion
    for k in range(1,order+1):
        l=len(coeff)
        _coeff=np.zeros((l-1,num_points))
        for i in range(l-1):
            for j in range(num_points):
                time=t[j]
                if V[i+k]!=V[i]:_coeff[i][j]+=(time-V[i])*coeff[i][j]/(V[i+k]-V[i])
                if V[i+k+1]!=V[i+1]:_coeff[i][j]+=(V[i+k+1]-time)*coeff[i+1][j]/(V[i+k+1]-V[i+1])
        coeff=_coeff

    x=[0 for i in range(num_points)]
    y=[0 for i in range(num_points)]

    for i in range(num_points):
        for p in range(n):
            point=control_points[p]
            x[i]+=coeff[p][i]*point[0]
            y[i]+=coeff[p][i]*point[1]
    
    fig,ax=plt.subplots()
    ax.plot(control_points[:,0],control_points[:,1],'o--',color='grey')
    ax.plot(x,y)
    plt.show()

control_points=np.array([[0, 0], [2, 3], [4, 4], [6, 4],[7,0],[10,5],[15,0]])
generateBspline(control_points,3,100)