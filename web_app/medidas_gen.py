import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import csv

def get_vectors(file2read):
    rows=[]
    xg=[]
    yg=[]
    zg=[]
    with open(file2read, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)
    for row in rows:
        xg.append(float(row[0]))
        yg.append(float(row[1]))
        zg.append(float(row[2]))
    return xg,yg,zg

def num_derivate_diff(v):
    vp = np.diff(v)
    vp = vp * 9.8/1000
    return vp

def get_rms_simple(v):
    factor = np.sqrt(2)/2
    rms = factor*(abs(max(v))+abs(min(v)))
    return rms

def get_max_absval(v):
    pos = abs(max(v))
    neg = abs(min(v))
    absval = max(pos, neg)
    return absval
#print(get_vectors("/home/pi/servicio/medidas/toma0.txt"))
# xg, yg, zg = get_vectors("/home/pi/servicio/medidas/toma0.txt")

def acc_graph(f00):
    dt=500/1722
    t = np.linspace(0,500,1722)
    win=750
    fig, ax =  plt.subplots()
    ax.plot(t[0:win],f00[0:win], linewidth=0.3)
    ax.axis([t[0],t[win-1],min(f00),max(f00)])
    ax.set_ylabel('g[m/s²] --- original')
    ax.grid(True)
    ax.set_title('Medida en eje X valores, En valores Reales')
    fig.tight_layout()
    plt.show()
    return 0

def antiderivate(xh):
    M=[]
    dt = 500/(len(xh)-1)
    # Lo mejor es hacer la primera itración por fuera del ciclo "seed"
    for i in range(len(xh)-2):
        factor=1
        m=factor*(xh[i+1]-xh[i])
        if i==0:
            M.append(0)
            M.append((0.125)*(m)*(dt)+(factor*xh[i]*dt*0.5))
        else:
            M.append((0.5)*(m)*(dt)+(factor*xh[i]*dt)+M[i-2])
        # x[0] funge como intercepto pues vamos a tratar la fn a pasos
        # Vamos a colocar evaluar en la mitad del periodo
        # la función de la velocidad será entonces :
            M.append((0.125)*(m)*(dt)+(factor*xh[i]*dt*0.5)+M[i-2])
    # Aun no resuelvo por que el AD no me da
    return M
