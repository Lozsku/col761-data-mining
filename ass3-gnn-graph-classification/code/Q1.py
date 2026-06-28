import numpy as np
import random
from matplotlib import pyplot as plt

np.set_printoptions(precision = 5)
d_values = [1, 2, 4, 8, 16, 32, 64]
num_points = 1000000

l1_y1, l2_y1, linf_y1 = [], [], []
l1_y2, l2_y2, linf_y2 = [], [], []
for d in d_values:
    points = np.random.rand(num_points, d)
    near_l1_sum, near_l2_sum, near_linf_sum = 0, 0, 0
    far_l1_sum, far_l2_sum, far_linf_sum = 0, 0, 0
    for i in range(100):
        idx = random.randint(0, num_points - 1)
        diff = points - points[idx]

        l1_norm = np.linalg.norm(diff, ord = 1, axis = 1)
        l2_norm = np.linalg.norm(diff, ord = 2, axis = 1)
        linf_norm = np.linalg.norm(diff, ord = np.inf, axis = 1)

        l1_sort = np.sort(l1_norm)
        l2_sort = np.sort(l2_norm)
        linf_sort = np.sort(linf_norm)

        near_l1_dist = l1_sort[0] if l1_sort[0] != 0 else l1_sort[1]
        near_l2_dist = l2_sort[0] if l2_sort[0] != 0 else l2_sort[1]
        near_linf_dist = linf_sort[0] if linf_sort[0] != 0 else linf_sort[1]

        far_l1_dist = l1_norm[num_points - 1]
        far_l2_dist = l2_norm[num_points - 1]
        far_linf_dist = linf_norm[num_points - 1]
        
        near_l1_sum += near_l1_dist
        near_l2_sum += near_l2_dist
        near_linf_sum += near_linf_dist

        far_l1_sum += far_l1_dist
        far_l2_sum += far_l2_dist
        far_linf_sum += far_linf_dist

    l1_y1.append(near_l1_sum/100)
    l1_y2.append(far_l1_sum/100)

    l2_y1.append(near_l2_sum/100)
    l2_y2.append(far_l2_sum/100)

    linf_y1.append(near_linf_sum/100)
    linf_y2.append(far_linf_sum/100)

plt.plot(d_values, l1_y1, label = 'Nearest Distance')
plt.plot(d_values, l1_y2, label = 'Farthest Distance')
plt.xlabel('d')
plt.ylabel('L1 - Distance')
plt.title('Variation of Nearest and Farthest distance vs d')
plt.legend()
plt.savefig('l1_fig.png')

plt.clf()
plt.plot(d_values, l2_y1, label = 'Nearest Distance')
plt.plot(d_values, l2_y2, label = 'Farthest Distance')
plt.xlabel('d')
plt.ylabel('L2 - Distance')
plt.title('Variation of Nearest and Farthest distance vs d')
plt.legend()
plt.savefig('l2_fig.png')

plt.clf()
plt.plot(d_values, linf_y1, label = 'Nearest Distance')
plt.plot(d_values, linf_y2, label = 'Farthest Distance')
plt.xlabel('d')
plt.ylabel('Linf - Distance')
plt.title('Variation of Nearest and Farthest distance vs d')
plt.legend()
plt.savefig('linf_fig.png')
