import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap


height, width = 200, 200

def initial_state():
    pUrban = 0.09 / 1000
    pRural = 1.0 - pUrban
    temp = np.random.choice((0,1), size=(height, width), p=(pRural, pUrban))
    
    # Establecer algunas celdas iniciales como no habitables
    temp[20:50, 20:60] = 3
    temp[130:160,:150] = 3
    temp[60:90,150:180] = 3

    return temp

def transition(C, N):
    q = C
    
    # Regla: Si ya estoy muy urbanizado, creo ruta de acceso
    if N.count(1) > 4:
        q = 0
        
    # Regla: Si tengo 4 vecinos, me vuelvo zona productiva
    elif C == 1 and N.count(1) == 4:
        q = 2
    
    # Regla: Si tengo al menos 1 vecino urbanizado, me urbanizo
    elif C == 0 and N.count(1) == 1:
        q = 1
    
    return q

def apply_rules():
    temp = np.zeros((height, width), dtype=int)

    for i in range(height):
        for j in range(width):
            # Frontera Periodica
            # Vecindad
            # U|A|V
            # L|C|R 
            # W|B|X
            
            # Estado actual de la celda central
            C = G[i, j] 
            
            L = 0 if j == 0 else G[i, j - 1]
            R = 0 if j == (width - 1) else G[i, j+1]
            A = 0 if i == 0 else G[i - 1, j]
            B = 0 if i == (height - 1) else G[i + 1, j]
            U = 0 if i == 0 or j == 0 else G[i - 1, j - 1]
            V = 0 if i == 0 or j == (width - 1) else G[i - 1, j + 1]
            W = 0 if i == (width - 1) or j == 0 else G[i + 1, j - 1]
            X = 0 if i == (width - 1) or j == (height - 1) else G[i + 1, j + 1]
            
            # Estado de todos los vecinos  
            # Moore
            N = [L, R, A, B, U, V, W, X]
            
            # Función de transición para determinar el nuevo estado de la celda
            q = transition(C, N)
            temp[i, j] = q
    
    return temp

def animate(frame):
    global G
    im.set_data(G)
    G = apply_rules()

    return im


G = initial_state()

fig_animation = plt.figure(figsize = (8, 8), dpi = 100)
plt.title('Expansión Urbana')
# Colors: 
    # Amarillo: No urbano
    # Naranja: Urbano
    # Azul: Productivo
    # Verde: Inhabitable
cmap_animation = ListedColormap([(1,1,0.75), (1,0.5,0.49), (0.45,0.7,1), (0.6,0.98,0.6)])
im = plt.imshow(G, cmap = cmap_animation)
plt.xticks([]) 
plt.yticks([])

anim = FuncAnimation(fig_animation, func = animate, interval = 100, frames = 200)
anim.save('simulacion1.gif', writer = 'ffmpeg', fps = 10)

plt.show()
