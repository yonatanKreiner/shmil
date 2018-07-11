import kdtree

def get_nearest_point(point, points):
    emptyTree = kdtree.create(dimensions=2)
    tree = kdtree.create(points)
    return tree.search_nn(point).data