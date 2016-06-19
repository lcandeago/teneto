#Main function to draw a slice_graph
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math
def plot_circle(vlabs,ax,edgeIndex=0,linestyle='k-',nodesize=1000):
#Plots a circle connectivity figure
    n = len(vlabs)
    #Get positions of node on unit circle
    posx=[math.cos((2*math.pi*i)/n) for i in range(0,n)]
    posy=[math.sin((2*math.pi*i)/n) for i in range(0,n)]
    #Get Bezier lines in a circle
    for edge in edgeIndex:
        bvx,bvy=bezier_circle((posx[edge[0]],posy[edge[0]]),(posx[edge[1]],posy[edge[1]]),20)
        ax.plot(bvx,bvy,linestyle)
    ax.scatter(posx,posy,s=nodesize,c=range(0,n))
    #Remove things that make plot unpretty
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.set_frame_on(False)
    #make plot a square
    x0,x1 = ax.get_xlim()
    y0,y1 = ax.get_ylim()
    ax.set_aspect((x1-x0)/(y1-y0))
    return ax

def plot_slice(vlabs,dlabs,ax,edgeIndex=0,linestyle='k-',nodesize=100):
# Functoins draws and saves a "slice graph"
# dLabs = labels of dimension Graph is expressed across. List of strings
# vlabs = nodes labels. List of strings
# edgeIndex = tupes of connections to draw. If 0, all connections are drawn.
# ax = axis handles to output too
    timeNum=len(dlabs)
    nodeNum=len(vlabs)
    G=nx.Graph()
    pos=[]
    posy = np.tile(list(range(0,nodeNum)),timeNum)
    posx = np.repeat(list(range(0,timeNum)),nodeNum)
    G.add_nodes_from(range(0,nodeNum*timeNum))
    #Generate edgeindex for all edges, or add edgeList
    if edgeIndex==0:
        nodeNumind=0
        for timeNumind in range(0,timeNum):
            #option if edges are missing to add all possible edges
            triInd = np.triu_indices(nodeNum,k=1)
            x,y=np.meshgrid(np.array([range(nodeNumind,nodeNumind+nodeNum)]),np.array([range(nodeNumind,nodeNumind+nodeNum)]),sparse=False,indexing='xy')
            edgeIndex=list(zip(x[triInd], y[triInd]))
            G.add_edges_from(edgeIndex)
            nodeNumind = nodeNumind + nodeNum
    else:
        G.add_edges_from(edgeIndex)

    #plt.plot(points)
    #Draw Bezier vectors around egde positions
    for edge in G.edges():
        bvx,bvy=bezier_points((posx[edge[0]],posy[edge[0]]),(posx[edge[1]],posy[edge[1]]),nodeNum,20)
        ax.plot(bvx,bvy,linestyle)
    ax.scatter(posx,posy,s=nodesize,c=posy)
    ax.set_yticks(range(0,len(vlabs)))
    ax.set_xticks(range(0,len(dlabs)))
    ax.set_yticklabels(vlabs)
    ax.set_xticklabels(dlabs)
    ax.grid()
    ax.set_frame_on(False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    return ax


def edgeListFromMatrix(A,gtth=0):
# creates a tuple list of connections. The input shoud be v*v*d where v=number of nodes and d=dimension (e.g. time)
# At the moment only binary connections are created. Anything greater threshold (gtth) is counted as 1.
    edg=np.where(A>gtth)
    edg=edg[0:2]+edg[-1]*A.shape[0]
    edgeList = [tuple(i) for i in edg.T]
    return edgeList




#Following 3 Function that draw vertical curved lines from around points.
#p1 nad p2 are start and end trupes (x,y coords) and pointN is the resolution of the points
#negxLim tries to restrain how far back along the x axis the bend can go.
def bezier_points(p1,p2,negxLim,pointN):
    ts = [t/pointN for t in range(pointN+1)]
    d=p1[0]-(max(p1[1],p2[1])-min(p1[1],p2[1]))/negxLim
    bezier=make_bezier([p1,(d,p1[1]),(d,p2[1]),p2])
    points = bezier(ts)
    bvx=[i[0] for i in points]
    bvy=[i[1] for i in points]
    return bvx, bvy

#Adapaption of bezier_points but for going towards a circle
def bezier_circle(p1,p2,pointN):
    ts = [t/pointN for t in range(pointN+1)]
#    d=p1[0]-(max(p1[1],p2[1])-min(p1[1],p2[1]))/negxLim
    bezier=make_bezier([p1,(0,0),p2])
    points = bezier(ts)
    bvx=[i[0] for i in points]
    bvy=[i[1] for i in points]
    return bvx, bvy

#These two functions originated from the plot.ly's documentation for python API.
#They create points along a curve.
def make_bezier(xys):
    # xys should be a sequence of 2-tuples (Bezier control points)
    n = len(xys)
    combinations = pascal_row(n-1)
    def bezier(ts):
        # This uses the generalized formula for bezier curves
        # http://en.wikipedia.org/wiki/B%C3%A9zier_curve#Generalization
        result = []
        for t in ts:
            tpowers = (t**i for i in range(n))
            upowers = reversed([(1-t)**i for i in range(n)])
            coefs = [c*a*b for c, a, b in zip(combinations, tpowers, upowers)]
            result.append(
                tuple(sum([coef*p for coef, p in zip(coefs, ps)]) for ps in zip(*xys)))
        return result
    return bezier
def pascal_row(n):
    # This returns the nth row of Pascal's Triangle
    result = [1]
    x, numerator = 1, n
    for denominator in range(1, n//2+1):
        # print(numerator,denominator,x)
        x *= numerator
        x /= denominator
        result.append(x)
        numerator -= 1
    if n&1 == 0:
        # n is even
        result.extend(reversed(result[:-1]))
    else:
        result.extend(reversed(result))
    return result
