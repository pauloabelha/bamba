import numpy as np
import my_linalg
from pcl.pointcloud import PointCloud
from my_linalg import signedpow

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
    return PointCloud(pcl), thetas

def is_a_thin_SQ(lambda_sq):
    # min proportion for considering a SQ thin
    MIN_PROP_THIN_SQ = 0.01
    scale_sort = np.sort(lambda_sq[0:3])
    scale_sort_ixs = np.argsort(lambda_sq[0:3])
    prop_thin = scale_sort[0] / scale_sort[2]
    is_thin_SQ = prop_thin <= MIN_PROP_THIN_SQ
    return is_thin_SQ, scale_sort, scale_sort_ixs, prop_thin

# By Paulo Abelha
#
# Uniformly samples a superellipsoid
# This function will approximate "thin" superellipsoids to be 2D)
# A thin SQ is defined in terms of metric units (m)
# A SQ is thin if its smallest scale over largest is smaller than 0.1
# Inputs:
#   lambda: 1x5 array with the parameters [a1,a2,a3,eps1,eps2]
#   plot_fig: whether to plot
#
# Outputs:
#   pcl: Nx3 array with the uniform point cloud
#   etas: the u parameters for the superparabola
#   omegas: the omega parameters for the superellipse
def sample_superellipsoid(lambda_sq, n_points=2000):
    # max number of points for pcl
    MAX_N_PTS = int(1e7)
    # max number of cross sampling of angles(etas x omegas) - for memory issues
    MAX_N_CROSS_ANGLES = MAX_N_PTS / 2
    # deal with thin SQs
    is_thin_SQ, scale_sort, scale_sort_ixs, _ = is_a_thin_SQ(lambda_sq)



def update_u(b, eps1, u_prev, D):
    return D / np.sqrt(((4*b*b)/(eps1*eps1)) * np.power(u_prev, (4/eps1)-2) + 1.0)

def unif_sample_u(b, eps1, D):
    max_iter = int(1e6)
    us = np.array([0])
    i = 0
    while True:
        if i > max_iter:
            print("First theta sampling reach the maximum number of iterations " + str(max_iter))
            raise 1
        next_u = us[-1] + update_u(b, eps1, us[-1], D)
        if next_u > 1:
            break
        us = np.append(us, [next_u])
        i += 1
    return us

def sample_superparabola( a, b, eps1, D=False):
    if not D:
        D = max(a / b, b / a) / 100.0
    us = unif_sample_u(b, eps1, D)
    X = a * us
    pcl_x = np.hstack((-X[1:][::-1], X))
    Y = b * np.power(np.power(us, 2), 1/eps1)
    pcl_y = np.hstack((Y[1:][::-1], Y))
    pcl = np.transpose(np.vstack((pcl_x, pcl_y)))
    pcl_z = np.zeros((pcl.shape[0], 1))
    pcl = np.hstack((pcl, pcl_z))
    return PointCloud(pcl), us

def get_sq_vol_multiplier(lambda_sq):
    # deal with SQs with a scale number less than 1
    # this is too deal with arbitrarly small SQs and
    # still being able to sample
    vol_mult = 1
    if lambda_sq[0] < 1 or lambda_sq[1] < 1 or lambda_sq[2] < 1:
        vol_mult = 1.0 / np.min(lambda_sq[0:3])
    lambda_sq[0:3] = np.multiply(lambda_sq[0:3], vol_mult)
    return vol_mult, lambda_sq

def sample_superparaboloid(lambda_sq, n_points=5000):
    # max num of samples
    MAX_N_SAMPLES = int(1e4)
    # deal with thin SQs
    vol_mult, lambda_sq = get_sq_vol_multiplier(lambda_sq)
    # get parameters
    a1, a2, a3, eps1, eps2, Kx, Ky, k_bend, eul1, eul2, eul3, posx, posy, poz = lambda_sq
    _, us = sample_superparabola(1, a3, eps1)
    _, omegas = sample_superellipse(a1, a2, eps2)
    us = np.random.choice(us, size=min(us.shape[0], MAX_N_SAMPLES), replace=False)
    us = us.reshape((us.shape[0], 1))
    omegas = np.random.choice(omegas, size=min(omegas.shape[0], MAX_N_SAMPLES), replace=False)
    omegas = omegas.reshape((1, min(omegas.shape[0], MAX_N_SAMPLES)))
    # get vertices
    X = a1 * np.dot(us, signedpow(np.cos(omegas), eps2))
    X = X.reshape((X.shape[0] * X.shape[1], 1))
    Y = a2 * us * signedpow(np.sin(omegas), eps2)
    Y = Y.reshape((Y.shape[0] * Y.shape[1], 1))
    Z = np.dot(2 * a3 * (np.power(np.power(us, 2), (1 / eps1)) - 1 / 2), np.ones((1, omegas.shape[1])))
    Z = Z.reshape((Z.shape[0] * Z.shape[1], 1))
    # create pcl
    pcl_x = np.append(np.append(X, -X), np.append(X, -X))
    pcl_y = np.append(np.append(Y, Y), np.append(-Y, -Y))
    pcl_z = np.append(np.append(Z, Z), np.append(Z, Z))
    pcl = np.transpose(np.vstack((np.vstack((pcl_x, pcl_y)), pcl_z)))
    pcl = pcl[np.random.choice(pcl.shape[0], n_points, replace=False), :]
    # rotate and translate pcl
    rot_mtx = my_linalg.get_eul_rot_mtx(lambda_sq[5:8])
    rot_transl_mtx = my_linalg.get_rot_transl_mtx(rot_mtx, transl_vec=np.reshape(np.transpose(lambda_sq[-3:]), (3, 1)))
    pcl = np.vstack((np.transpose(pcl), np.ones((1, pcl.shape[0]))))
    pcl = np.transpose(np.dot(rot_transl_mtx, pcl))
    pcl = pcl[:, 0:3]
    return PointCloud(pcl)
