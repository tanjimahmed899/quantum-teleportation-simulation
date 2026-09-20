
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ============================================================
# Micro-polished 3D optical circuit - v13
# Fixes:
# 1) HWP/QWP labels separated more aggressively
# 2) Mirror "M" labels manually offset per mirror
# 3) Screen label moved right/down
# 4) Measurement block widened and elements spaced out
# 5) DRS region enlarged and emphasized
# ============================================================

fig = plt.figure(figsize=(30, 8.8), facecolor="white")
ax = fig.add_axes([0.005, 0.10, 0.99, 0.82], projection="3d")
ax.set_facecolor("white")

# -------------------- helpers --------------------

def cuboid(center, size, facecolor, edgecolor="black", alpha=1.0, lw=0.7, angle=0):
    x, y, z = center
    dx, dy, dz = size
    pts = np.array([
        [-dx/2,-dy/2,-dz/2],[ dx/2,-dy/2,-dz/2],
        [ dx/2, dy/2,-dz/2],[-dx/2, dy/2,-dz/2],
        [-dx/2,-dy/2, dz/2],[ dx/2,-dy/2, dz/2],
        [ dx/2, dy/2, dz/2],[-dx/2, dy/2, dz/2]
    ], dtype=float)

    a = np.deg2rad(angle)
    R = np.array([
        [np.cos(a), -np.sin(a), 0],
        [np.sin(a),  np.cos(a), 0],
        [0, 0, 1]
    ])
    pts = pts @ R.T
    pts += np.array([x, y, z])

    faces_idx = [
        [0,1,2,3],[4,5,6,7],
        [0,1,5,4],[1,2,6,5],
        [2,3,7,6],[3,0,4,7]
    ]
    faces = [[pts[i] for i in f] for f in faces_idx]

    poly = Poly3DCollection(
        faces,
        facecolors=facecolor,
        edgecolors=edgecolor,
        linewidths=lw,
        alpha=alpha
    )
    ax.add_collection3d(poly)

def txt(x, y, z, s, fs=8, weight="normal", white_bg=False):
    bbox = None
    if white_bg:
        bbox = dict(facecolor="white", alpha=0.82, edgecolor="none", pad=0.08)
    ax.text(x, y, z, s, fontsize=fs, fontweight=weight,
            ha="center", va="center", color="black", bbox=bbox)

def line3(points, color="#4fb26c", lw=5.2, alpha=1.0):
    p = np.asarray(points, dtype=float)
    ax.plot(p[:,0], p[:,1], p[:,2], color=color, lw=lw,
            alpha=alpha, solid_capstyle="round")

def path_arrow(p0, p1, color="#4fb26c"):
    p0 = np.asarray(p0, float)
    p1 = np.asarray(p1, float)
    d = p1 - p0
    ax.quiver(p0[0], p0[1], p0[2], d[0], d[1], d[2],
              color=color, linewidth=1.35,
              arrow_length_ratio=0.22, normalize=False)

def frame(x0, x1, z0, z1, title, color, y=1.28, title_z=23.8):
    style = dict(color=color, lw=1.8, linestyle=(0,(5,4)), alpha=0.97)
    ax.plot([x0,x1],[y,y],[z0,z0], **style)
    ax.plot([x1,x1],[y,y],[z0,z1], **style)
    ax.plot([x1,x0],[y,y],[z1,z1], **style)
    ax.plot([x0,x0],[y,y],[z1,z0], **style)
    txt((x0+x1)/2, y, title_z, title, fs=12, weight="bold", white_bg=True)

def mini_mount(x, y, z_bottom, h=0.45):
    cuboid((x, y, z_bottom-h/2), (0.29,0.29,h),
           "#d8dbde", "#93989d", 1.0, 0.30)

def plate(x, z, name, color, y=0.0, h=3.15,
          label_dx=0.0, label_dz=0.0, label_fs=6.7):
    mini_mount(x, y, z-h/2-0.07, 0.45)
    cuboid((x,y,z), (0.78,0.50,h), color, "black", 0.97, 0.58)
    txt(x+label_dx, y, z+h/2+0.62+label_dz,
        name, fs=label_fs, weight="bold", white_bg=True)

def mirror(x, z, y=0.0, tilt=40, show_label=True,
           label_dx=0.0, label_dz=0.0):
    mini_mount(x, y, z-0.80, 0.43)
    cuboid((x,y,z), (1.06,0.23,1.65),
           "#c7ccd2", "#68727c", 0.98, 0.58, tilt)
    if show_label:
        txt(x+label_dx, y, z+1.22+label_dz,
            "M", fs=6.4, weight="bold", white_bg=True)

def pbs(x, z, y=0.0, s=2.00, label_dx=0.0, label_dz=0.0):
    mini_mount(x, y, z-s/2-0.05, 0.43)
    cuboid((x,y,z), (s,s,s),
           "#78bdff", "#1848ff", 0.30, 1.0)
    ax.plot([x-s*0.36,x+s*0.36],
            [y-s*0.36,y+s*0.36],
            [z,z], color="#1848ff", lw=1.45)
    txt(x+label_dx, y, z+s/2+0.64+label_dz,
        "PBS", fs=6.7, weight="bold", white_bg=True)

def drs(x, z, y=0.0):
    # larger and darker than previous version
    verts = np.array([
        [x, y, z+1.55],
        [x+1.35, y, z],
        [x, y, z-1.55],
        [x-1.35, y, z],
        [x, y+1.00, z],
        [x, y-1.00, z]
    ])
    faces = [
        [verts[i] for i in [0,1,4]],[verts[i] for i in [0,4,3]],
        [verts[i] for i in [0,3,5]],[verts[i] for i in [0,5,1]],
        [verts[i] for i in [2,4,1]],[verts[i] for i in [2,3,4]],
        [verts[i] for i in [2,5,3]],[verts[i] for i in [2,1,5]]
    ]
    poly = Poly3DCollection(
        faces,
        facecolors="#9fb3c7",
        edgecolors="#5f7387",
        linewidths=0.9,
        alpha=0.88
    )
    ax.add_collection3d(poly)
    txt(x, y, z-2.15, "DRS₁", fs=7.0, weight="bold", white_bg=True)

def screen(x, z_center, y=0.0):
    cuboid((x,y,z_center), (0.56,0.82,15.8),
           "#d8dfe5", "#73808d", 0.98, 0.72)

# -------------------- constants --------------------

Y  = 0.0
ZM = 11.8
ZT = 18.4
ZB = 5.4
GREEN = "#56b874"

# background
cuboid((61.0,1.42,12.0), (120.0,0.022,22.5),
       "#f2f2f2","#d5d5d5",0.13,0.38)

# frames
frame(8.0,38.5,2.0,22.0,"Preparation","#ff4db2",1.30,23.8)
frame(39.0,59.5,1.5,22.5,"CNOT","#4b4b4b",1.30,24.1)
frame(83.0,105.0,1.5,22.5,"CNOT","#4b4b4b",1.30,24.1)
frame(105.5,132.5,1.0,22.5,"Measurement","#11c7d5",1.30,24.1)

# -------------------- input --------------------

cuboid((4.5,Y,ZM),(4.0,1.90,2.65),
       "#d9332e","#8e1815",1.0,0.75)
txt(4.5,Y,ZM+2.00,"Laser",fs=9.2,weight="bold",white_bg=True)

plate(11.5,ZM,"NF","#666666",Y,3.25,label_fs=6.6)
plate(17.0,ZM,"HWP","#f28e2b",Y,3.25,label_fs=6.6)
pbs(23.0,ZM,Y,2.05)

# preparation upper/lower
mirror(27.0,ZT+0.55,Y,40,True,-0.40,0.10)
plate(31.4,ZT,"QWP","#ff35d3",Y,3.35,-0.80,+0.55,6.6)
plate(35.0,ZT,"HWP","#f28e2b",Y,3.35,+0.80,-0.18,6.6)

mirror(27.0,ZB-0.55,Y,-40,True,-0.40,-0.10)
plate(31.4,ZB,"QWP","#ff35d3",Y,3.35,-0.80,+0.55,6.6)
plate(35.0,ZB,"HWP","#f28e2b",Y,3.35,+0.80,-0.18,6.6)

# CNOT 1
plate(41.6,ZT,"HWP","#f28e2b",Y,3.25,-0.30,+0.20,6.6)
pbs(46.2,ZT,Y,2.05)
mirror(49.5,21.0,Y,40,True,-0.45,+0.10)
mirror(54.5,21.0,Y,-40,True,+0.45,+0.10)

plate(41.6,ZB,"HWP","#f28e2b",Y,3.25,-0.30,+0.20,6.6)
pbs(46.2,ZB,Y,2.05)
mirror(49.5,2.8,Y,-40,True,-0.45,-0.10)
mirror(54.5,2.8,Y,40,True,+0.45,-0.10)

# DRS region, stronger
drs(65.5,ZM,Y)
drs(75.5,ZM,Y)
txt(70.5,Y,ZM+3.8,"Coupling region",fs=6.1,weight="bold",white_bg=True)

# middle QWP/HWP labels even more separated
plate(79.7,ZT,"QWP","#ff35d3",Y,3.35,-1.35,+0.75,6.2)
plate(83.0,ZT,"HWP","#f28e2b",Y,3.35,-0.55,-0.10,6.2)

plate(79.7,ZB,"QWP","#ff35d3",Y,3.35,-1.35,+0.75,6.2)
plate(83.0,ZB,"HWP","#f28e2b",Y,3.35,-0.55,-0.10,6.2)

# CNOT 2
plate(89.5,ZT,"HWP","#f28e2b",Y,3.25,+0.80,+0.48,6.2)
pbs(94.0,ZT,Y,2.05)
mirror(97.1,21.0,Y,40,True,-0.45,+0.10)
mirror(102.1,21.0,Y,-40,True,+0.45,+0.10)

plate(89.5,ZB,"HWP","#f28e2b",Y,3.25,+0.80,+0.48,6.2)
pbs(94.0,ZB,Y,2.05)
mirror(97.1,2.8,Y,-40,True,-0.45,-0.10)
mirror(102.1,2.8,Y,40,True,+0.45,-0.10)

# Measurement widened and spaced
pbs(110.0,ZT,Y,2.05)
pbs(110.0,ZB,Y,2.05)
mirror(115.2,20.8,Y,40,True,-0.25,+0.12)
mirror(115.2,3.1,Y,-40,True,-0.25,-0.12)
screen(130.5,ZM,Y)

# grey center guide
ax.plot([59.5,62.8,65.0],[0.10]*3,[ZT,ZT,ZM+1.0],color="#b0b0b0",lw=1.5)
ax.plot([59.5,62.8,65.0],[0.10]*3,[ZB,ZB,ZM-1.0],color="#b0b0b0",lw=1.5)
ax.plot([76.0,78.0,79.4],[0.10]*3,[ZM+1.0,ZT,ZT],color="#b0b0b0",lw=1.5)
ax.plot([76.0,78.0,79.4],[0.10]*3,[ZM-1.0,ZB,ZB],color="#b0b0b0",lw=1.5)

# -------------------- green paths --------------------

# input
line3([(6.5,Y,ZM),(11.0,Y,ZM)],GREEN)
line3([(12.0,Y,ZM),(16.4,Y,ZM)],GREEN)
line3([(17.6,Y,ZM),(21.8,Y,ZM)],GREEN)

# preparation
line3([(24.0,Y,ZM),(27.0,Y,ZM),(27.0,Y,ZT)],GREEN,5.4)
line3([(27.5,Y,ZT),(30.6,Y,ZT)],GREEN)
line3([(35.6,Y,ZT),(39.0,Y,ZT)],GREEN)

line3([(24.0,Y,ZM),(27.0,Y,ZM),(27.0,Y,ZB)],GREEN,5.4)
line3([(27.5,Y,ZB),(30.6,Y,ZB)],GREEN)
line3([(35.6,Y,ZB),(39.0,Y,ZB)],GREEN)

# CNOT 1
line3([(42.2,Y,ZT),(45.0,Y,ZT)],GREEN)
line3([(47.3,Y,ZT),(49.5,Y,ZT),(49.5,Y,19.9)],GREEN)
line3([(50.1,Y,19.9),(54.5,Y,19.9)],GREEN)
line3([(54.5,Y,19.9),(54.5,Y,ZT),(59.5,Y,ZT)],GREEN)

line3([(42.2,Y,ZB),(45.0,Y,ZB)],GREEN)
line3([(47.3,Y,ZB),(49.5,Y,ZB),(49.5,Y,4.0)],GREEN)
line3([(50.1,Y,4.0),(54.5,Y,4.0)],GREEN)
line3([(54.5,Y,4.0),(54.5,Y,ZB),(59.5,Y,ZB)],GREEN)

# center
line3([(59.5,Y,ZT),(63.5,Y,ZT),(65.5,Y,ZM)],GREEN,5.9)
line3([(59.5,Y,ZB),(63.5,Y,ZB),(65.5,Y,ZM)],GREEN,5.9)
line3([(66.9,Y,ZM),(74.1,Y,ZM)],color="#6f7f89",lw=2.6)
line3([(75.5,Y,ZM),(79.4,Y,ZT)],GREEN,5.9)
line3([(75.5,Y,ZM),(79.4,Y,ZB)],GREEN,5.9)

# middle plates
line3([(79.4,Y,ZT),(79.25,Y,ZT)],GREEN)
line3([(83.45,Y,ZT),(88.85,Y,ZT)],GREEN)
line3([(79.4,Y,ZB),(79.25,Y,ZB)],GREEN)
line3([(83.45,Y,ZB),(88.85,Y,ZB)],GREEN)

# CNOT 2
line3([(89.95,Y,ZT),(92.85,Y,ZT)],GREEN)
line3([(95.05,Y,ZT),(97.1,Y,ZT),(97.1,Y,19.9)],GREEN)
line3([(97.7,Y,19.9),(102.1,Y,19.9)],GREEN)
line3([(102.1,Y,19.9),(102.1,Y,ZT),(105.0,Y,ZT)],GREEN)

line3([(89.95,Y,ZB),(92.85,Y,ZB)],GREEN)
line3([(95.05,Y,ZB),(97.1,Y,ZB),(97.1,Y,4.0)],GREEN)
line3([(97.7,Y,4.0),(102.1,Y,4.0)],GREEN)
line3([(102.1,Y,4.0),(102.1,Y,ZB),(105.0,Y,ZB)],GREEN)

# Measurement
line3([(111.2,Y,ZT),(118.2,Y,ZT)],GREEN)
line3([(110.0,Y,ZT),(115.2,Y,ZT),(115.2,Y,19.0)],GREEN)
line3([(115.7,Y,19.0),(124.2,Y,19.0)],GREEN)

line3([(111.2,Y,ZB),(118.2,Y,ZB)],GREEN)
line3([(110.0,Y,ZB),(115.2,Y,ZB),(115.2,Y,4.8)],GREEN)
line3([(115.7,Y,4.8),(124.2,Y,4.8)],GREEN)

# arrows, consistent and sparse
path_arrow((7.5,Y,ZM),(9.3,Y,ZM),GREEN)
path_arrow((27.0,Y,14.0),(27.0,Y,16.4),GREEN)
path_arrow((27.0,Y,9.5),(27.0,Y,7.3),GREEN)
path_arrow((51.0,Y,19.9),(53.0,Y,19.9),GREEN)
path_arrow((53.0,Y,4.0),(51.0,Y,4.0),GREEN)
path_arrow((62.0,Y,ZT),(64.1,Y,15.7),GREEN)
path_arrow((64.1,Y,7.8),(62.0,Y,ZB),GREEN)
path_arrow((76.2,Y,13.0),(78.0,Y,16.2),GREEN)
path_arrow((78.0,Y,7.8),(76.2,Y,10.8),GREEN)
path_arrow((98.3,Y,19.9),(100.1,Y,19.9),GREEN)
path_arrow((100.1,Y,4.0),(98.3,Y,4.0),GREEN)
path_arrow((112.4,Y,ZT),(114.7,Y,ZT),GREEN)
path_arrow((116.7,Y,19.0),(119.7,Y,19.0),GREEN)
path_arrow((112.4,Y,ZB),(114.7,Y,ZB),GREEN)
path_arrow((116.7,Y,4.8),(119.7,Y,4.8),GREEN)

# -------------------- output grid --------------------

# direct output column
txt(119.2,Y,ZT,"|00⟩",fs=9.4,weight="bold",white_bg=True)
txt(119.2,Y,ZB,"|01⟩",fs=9.4,weight="bold",white_bg=True)

# reflected output column
txt(125.2,Y,19.0,"|10⟩",fs=9.4,weight="bold",white_bg=True)
txt(125.2,Y,4.8,"|11⟩",fs=9.4,weight="bold",white_bg=True)

# fixed screen label further right and lower
txt(130.5,Y,1.15,"Screen",fs=8.8,weight="bold",white_bg=True)

# -------------------- final view --------------------

ax.set_xlim(1.0,134.0)
ax.set_ylim(-1.7,1.8)
ax.set_zlim(0.8,24.8)

try:
    ax.set_proj_type("ortho")
except Exception:
    pass

ax.view_init(elev=8.0, azim=-86.0)
ax.set_box_aspect((5.9,0.42,2.95))
ax.set_axis_off()

fig.suptitle(
    "3D Reconstruction of the Optical CNOT / Measurement Circuit",
    fontsize=16,
    y=0.965
)

fig.text(
    0.5, 0.028,
    "NF = Neutral Filter  |  HWP = Half-Wave Plate  |  QWP = Quarter-Wave Plate  |  PBS = Polarizing Beam Splitter  |  M = Mirror  |  DRS₁ = Coupling Region",
    ha="center", va="center", fontsize=10
)

plt.savefig(
    "optical_circuit_3D_targeted_fix_v15.png",
    dpi=350,
    bbox_inches="tight",
    facecolor="white"
)
plt.show()
