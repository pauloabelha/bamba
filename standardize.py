import numpy as np
from pcl.pointcloud import PointCloud


def centroid(pcl):
    if pcl.vertices.shape[0] == 0:
        raise BaseException('Cannot calculate point cloud centroid it has no vertices.')
    return np.mean(pcl.vertices, axis=0)


def _centralize(pcl):
    if pcl.vertices.shape[0] == 0:
        raise BaseException('Cannot centralize point cloud because it has no vertices.')
    pcl.vertices = np.subtract(pcl.vertices, centroid(pcl))


def _run_pca(pcl):
    if pcl.vertices.shape[0] == 0:
        raise BaseException('Cannot standardize point cloud because it has no vertices.')
    u, s, v = np.linalg.svd(pcl.vertices, full_matrices=False)
    pcl.vertices = np.dot(pcl.vertices, v.T)


def standardize(pcl):
    _run_pca(pcl)
    _centralize(pcl)


def action_standardize(input_file_path, output_file_path, verbose=False):
    """Standardizes a point cloud for repeatable orientation and position
       This involves running PCA and centralizing on the point cloud's centroid
    """

    if verbose:
        print('Reading point cloud...')
    pcl = PointCloud.from_file(input_file_path)
    if verbose:
        print('Finished reading point cloud.')
    if verbose:
        print('Standardizing point cloud...')
    standardize(pcl)
    if verbose:
        print('Finished standardizing point cloud.')
    if verbose:
        print('Writing point cloud...')
    pcl.write(output_file_path)
    if verbose:
        print('Finished writing point cloud.')