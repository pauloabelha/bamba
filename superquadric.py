import numpy as np
import my_linalg
from pcl.pointcloud import PointCloud

# Based on [PiluFisher95] Pilu, Maurizio, and Robert B. Fisher.
# �Equal-distance sampling of superellipse models.� DAI RESEARCH PAPER (1995)
# Update u based on the combinations of models in the paper
def update_theta( a1, a2, eps1, theta_prev, D ):
    theta_eps = 1e-2
    if theta_prev <= theta_eps:
        # equation(8)
        theta_next = np.power(np.abs((D / a2) + np.power(theta_prev, eps1)), 1 / eps1) - theta_prev
    else:
        if np.pi / 2 - theta_prev < theta_eps:
            # equation(9)
            theta_next = np.power((D / a1) + np.power(np.pi / 2 - theta_prev, eps1), 1 / eps1) - (np.pi / 2 - theta_prev)
        else:
            # equation(5)
            theta_next = (D / eps1) * np.cos(theta_prev) * np.sin(theta_prev)\
                         * np.sqrt(1 / (np.power(a1, 2) * np.power(np.cos(theta_prev), 2 * eps1)
                                        * np.power(np.sin(theta_prev), 4.) + np.power(a2, 2)
                                        * np.power(np.sin(theta_prev), 2 * eps1)
                                        * np.power(np.cos(theta_prev), 4.)))
    return theta_next


def unif_sample_theta(a, b, eps1, D):
    max_iter = int(1e6)
    thetas1 = np.array([0])
    i = 0
    while True:
        if i > max_iter:
            print("First theta sampling reach the maximum number of iterations " + str(max_iter))
            raise 1
        theta_next = update_theta(a, b, eps1, thetas1[-1], D)
        new_theta = thetas1[-1] + theta_next
        if new_theta > np.pi / 4:
            break
        thetas1 = np.append(thetas1, [new_theta])
        i += 1
    thetas = np.append(thetas1, -thetas1 + np.pi/2)
    return thetas

def sample_superellipse(a, b, eps1, D=False):
    if not D:
        D = max(a / b, b / a) / 100.0
    rot = np.identity(2)
    if a > b:
        aux = a
        a = b
        b = aux
        rot = my_linalg.rot_mtx_2D(np.pi / 2)
    thetas = unif_sample_theta(a, b, eps1, D)
    X = np.multiply(a, my_linalg.signedpow(np.cos(thetas), eps1))
    Y = np.multiply(b, my_linalg.signedpow(np.sin(thetas), eps1))
    pcl_x = np.append(np.append(X, -X), np.append(X, -X))
    pcl_y = np.append(np.append(Y, Y), np.append(-Y, -Y))
    pcl = np.transpose(np.vstack((pcl_x, pcl_y)))
    pcl = np.dot(pcl, rot)
    pcl_z = np.zeros((pcl.shape[0], 1))
    pcl = np.hstack((pcl, pcl_z))
    return PointCloud(pcl)


