from pcl.pointcloud import PointCloud
import numpy as np

def print_pcl_info(file_path):
    pcl = PointCloud(file_path)
    n_segms = np.unique(pcl.segm_ixs).shape[0]
    print("General:")
    _, bound_box_str = pcl.bound_box()
    print("    Bounding box: " + bound_box_str)
    mean_vertices = np.mean(pcl.vertices, axis=0)
    center_str = "[" + '{:.6f}'.format(mean_vertices[0]) + ", " + '{:.6f}'.format(mean_vertices[1]) + ", " + '{:.6f}'.format(mean_vertices[1])
    print("    Center: " + center_str)
    print("    Number of faces: " + str(pcl.faces.shape[0]))
    print("    Number of face normals: " + str(pcl.faces_normals.shape[0]))
    print("Segments:")
    print("    Number of segments: " + str(n_segms))
    for i in range(n_segms):
        print("    Segment " + str(i+1) + ":")
        print("        Color (RGB): " + str([0, 0, 0]))
        print("        Number of vertices: " + str(pcl.vertices.shape[0]))
        print("        Number of vertex normals: " + str(pcl.vertices_normals.shape[0]))
