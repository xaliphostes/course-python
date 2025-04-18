import numpy as np
import matplotlib.pyplot as plt
import mplstereonet
from mplstereonet import stereonet_math
import os

def load(name):
    """Read data from a text file on disk."""
    # Get the data file relative to this file's location...
    datadir = os.path.dirname(__file__)
    filename = os.path.join(datadir, name)

    data = []
    with open(filename, 'r') as infile:
        for line in infile:
            # Skip comments
            if line.startswith('#'):
                continue

            # First column: strike, second: dip, third: rake.
            strike, dip, rake = line.strip().split()

            if rake[-1].isalpha():
                # If there's a directional letter on the rake column, parse it
                # normally.
                strike, dip, rake = mplstereonet.parse_rake(strike, dip, rake)
            else:
                # Otherwise, it's actually an azimuthal measurement of the
                # slickenslide directions, so we need to convert it to a rake.
                strike, dip = mplstereonet.parse_strike_dip(strike, dip)
                azimuth = float(rake)
                rake = mplstereonet.azimuth2rake(strike, dip, azimuth)

            data.append([strike, dip, rake])

    # Separate the columns back out
    strike, dip, rake = zip(*data)
    return strike, dip, rake

strikes, dips, rakes = load('angelier-data.txt')
n_data = len(strikes)

# 2. Créer le stéréonet
fig = plt.figure(figsize=(10, 10))
ax = fig.add_subplot(111, projection='stereonet')

# 3. Tracer toutes les mesures
for i in range(n_data):
    ax.plane(strikes[i], dips[i], 'b-', linewidth=0.5, alpha=0.3)
    ax.pole(strikes[i], dips[i], 'bo', markersize=4, alpha=0.5)
    
# 4. Calculer la densité des pôles pour identifier les clusters
cax = ax.density_contourf(strikes, dips, measurement='poles', cmap='Reds', 
                         method='kamb', sigma=3, alpha=0.8)
fig.colorbar(cax)

# 5. Identifier les orientations principales (directions préférentielles)
# Pour cela, on peut utiliser des méthodes comme l'analyse en composantes principales
# ou des algorithmes de clustering, mais voici une méthode simplifiée:

# Convertir les données en vecteurs cartésiens
lon, lat = stereonet_math.pole(strikes, dips)
x, y, z = stereonet_math.sph2cart(lon, lat)
vectors = np.column_stack((x, y, z))

# Calculer le tenseur d'orientation 
orientation_tensor = np.zeros((3, 3))
for v in vectors:
    orientation_tensor += np.outer(v, v)
orientation_tensor /= len(vectors)

# Calculer les vecteurs et valeurs propres du tenseur
eigenvalues, eigenvectors = np.linalg.eigh(orientation_tensor)

# Les vecteurs propres correspondent aux axes principaux de contrainte (sigma1, sigma2, sigma3)
# sigma1 (compression max) = eigenvector avec la plus grande valeur propre
# sigma3 (extension max) = eigenvector avec la plus petite valeur propre
idx = np.argsort(eigenvalues)
sigma3 = eigenvectors[:, idx[0]]  # Contrainte minimale (extension)
sigma2 = eigenvectors[:, idx[1]]  # Contrainte intermédiaire
sigma1 = eigenvectors[:, idx[2]]  # Contrainte maximale (compression)

# Convertir en coordonnées sphériques pour le traçage
lon1, lat1 = stereonet_math.cart2sph(*sigma1)
lon2, lat2 = stereonet_math.cart2sph(*sigma2)
lon3, lat3 = stereonet_math.cart2sph(*sigma3)

# 6. Tracer les axes principaux de contrainte
ax.line(lon1, lat1, 'r*', markersize=20, label='σ1 (compression max)')
ax.line(lon2, lat2, 'g*', markersize=20, label='σ2 (intermédiaire)')
ax.line(lon3, lat3, 'b*', markersize=20, label='σ3 (extension max)')

ax.grid(True)
plt.legend(loc='upper left', bbox_to_anchor=(1.1, 1.0))
plt.title('Analyse des contraintes principales (n=' + str(n_data) + ' mesures)')

plt.tight_layout()
plt.show()
