import matplotlib.pyplot as plt

# rectangle de largeur 4 et hauteur 2
rect = plt.Rectangle((0, 0), 4, 2, facecolor='skyblue', edgecolor='navy')

fig, ax = plt.subplots()
ax.add_patch(rect)
ax.set_xlim(-1, 6)
ax.set_ylim(-1, 4)
plt.show()
