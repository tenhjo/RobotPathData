import numpy as np

from wzk import sql2, trajectory

import matplotlib.pyplot as plt

file = "/Users/jote/Documents/code/python/misc2/RobotPathData/data/SingleSphere02.db"  # download from cloud, update path
sql2.summary(file=file)

n_voxels = 64
voxel_size = 10 / 64     # in m
extent = [0, 10, 0, 10]  # in m
n_waypoints = 20  # start + 20 inner points + end
n_dim = 2
n_dof = 2
n_paths = sql2.get_n_rows(file=file, table="paths")
n_worlds = sql2.get_n_rows(file=file, table="worlds")


worlds = sql2.get_values(file=file, table="worlds", columns="img_cmp")
worlds = sql2.compressed2img(img_cmp=worlds, shape=(n_voxels, n_voxels), dtype=bool)

i_world, q = sql2.get_values(file=file, table="paths", rows=-1, columns=["world_i32", "q_f32"])
q = q.reshape(-1, n_waypoints, n_dof)


i = 2017
path_img_cmp = sql2.get_values(file=file, table="paths", rows=i, columns="path_img_cmp")
path_img = sql2.compressed2img(img_cmp=path_img_cmp, shape=(n_voxels, n_voxels), n_dim=2, dtype=bool)

q_n32 = trajectory.get_path_adjusted(q[i], n=32)

fig, ax = plt.subplots()
ax.imshow(worlds[i_world[i], :, :].T, origin="lower", extent=extent, cmap="Greys", alpha=0.5)  # world
ax.imshow(path_img.T, origin="lower", extent=extent, cmap="Reds", alpha=0.5)  # world
ax.plot(*q_n32.T, marker="o", color="blue", alpha=0.3, label="n_wp=32")
ax.plot(*q[i].T, marker="o", color="red", alpha=0.3, label="n_wp=20")
ax.legend()


# generate path_img data
# from mopla.world import swept_volume
# r = 0.1
# path_img_cmp = np.zeros(len(q), dtype=object)
# for i in range(len(q)):
#     printing.progress_bar(i, len(q), eta=True)
#     path_img = swept_volume.sphere2img_path(x=q[i], r=r, shape=(n_voxels, n_voxels), limits=np.array([[0, 10],
#                                                                                                       [0, 10]]))
#     path_img_cmp[i] = sql2.img2compressed(img=path_img, n_dim=2)
#
#
# sql2.add_column(file=file, table="paths", column="path_img_cmp", dtype=sql2.TYPE_BLOB)
# sql2.set_values(file=file, table="paths", rows=-1, columns=("path_img_cmp",), values=(path_img_cmp,))

