import matplotlib as mpl
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from medidas_gen import *

def components(xr, yr, zr):
    fpy = 1/max(xr,yr,zr)
    rms = np.sqrt(xr**2+yr**2+zr**2)
    xpy = xr*fpy
    ypy = yr*fpy
    zpy = zr*fpy
    print(fpy)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    z = [0,0]
    z1 = [0,0]
    z2 = [0,1]
    zm = [0, zpy]

    x = [0,1]
    x1 = [0,0]
    x2 = [0,0]
    xm = [0, xpy]

    y = [0,0]
    y1 = [0,1]
    y2 = [0,0]
    ym = [0, ypy]

    # Ejes
    ax.plot(x, y, z, linewidth=0.3, color='black')
    ax.plot(x1, y1, z1, linewidth=0.3, color='black')
    ax.plot(x1, y2, z2, linewidth=0.3, color='black')
    ax.quiver([0,0,0.9],[0,0.9,0],[0.9,0,0],[0,0,1],[0,1,0],[1,0,0], length=0.1, color='black', linewidth=0.4)

    # Proyeción obre los ejes
    ax.plot([0, xpy],[0, 0],[0, 0], linewidth=1, color='blue')
    ax.quiver([0,0.85*xpy],[0,0],[0,0],[0,xpy],[0,0],[0,0], length=0.15, color='blue')
    ax.plot([0, 0],[0, ypy],[0, 0], linewidth=1, color='blue')
    ax.quiver([0,0],[0,0.85*ypy],[0,0],[0,0],[0,ypy],[0,0], length=0.15, color='blue')
    ax.plot([0, 0],[0, 0],[0, zpy], linewidth=1, color='blue')
    ax.quiver([0,0],[0,0],[0,0.85*zpy],[0,0],[0,0],[0,zpy], length=0.15, color='blue')

    # Vector resultante
    ax.plot(xm, ym, zm, linewidth=1, color='red', label='RMS = '+ str(rms))
    ax.quiver([0,0.85*xpy],[0,0.85*ypy],[0,0.85*zpy],[0,xpy],[0,ypy],[0,zpy], length=0.15, color='red')

    # Proyecciones
    ax.plot([0,0],[0,ypy],[0,zpy], linewidth=0.3, color='black', ls='--')
    ax.plot([0,xpy],[0,0],[0,zpy], linewidth=0.3, color='black', ls='--')
    ax.plot([0,xpy],[0,ypy],[0,0], linewidth=0.3, color='black', ls='--')

    # Vamos con las marcas con los textos
    ax.text(0,0,1, 'Z')
    ax.text(0,1,0, 'Y')
    ax.text(1,0,0, 'X')
    ax.text(0,0,0.3, str(round(zr,5)), zdir='z', fontsize=8 )
    ax.text(0,0.5,0, str(round(yr,5)), zdir='y', fontsize=8 )
    ax.text(0.5,0,0, str(round(xr,5)), zdir='x', fontsize=8 )

    ax.grid(False)
#    ax.legend(loc='lower center')
#    ax.set_title('Componetes Normales de la medida')
    ax.axis(False)
    fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
    ax.view_init(24,62)

    plt.show()

xg,yg,zg = get_vectors('/home/pi/servicio/medidas/toma0.txt')

xp = num_derivate_diff(xg)
yp = num_derivate_diff(yg)
zp = num_derivate_diff(zg)
# Generamos los vectores de velocidad
xv = antiderivate(xp)
yv = antiderivate(yp)
zv = antiderivate(zp)
# Encontremos los RMS
xr = get_rms_simple(xv)
yr = get_rms_simple(yv)
zr = get_rms_simple(zv)

# evolution2(zg,zp,zv)
components(xr,yr,zr)

