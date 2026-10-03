import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch, Polygon

# ============================================================
# FINAL POLISHED OPTICAL QUANTUM CIRCUIT
# ============================================================

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

fig, ax = plt.subplots(figsize=(20, 7.2))
ax.set_xlim(0, 180)
ax.set_ylim(0, 62)
ax.axis("off")

# ============================================================
# COLORS
# ============================================================

GREEN = "#58B96E"
DARK = "#202020"
GREY = "#666666"

PINK = "#F25AB4"
CYAN = "#22C6D4"
BLUE = "#314CFF"

COUPLING_EDGE = "#7E92A6"

WG = "#B9B9B9"
WG_DARK = "#6F7F90"

PBS_FACE = "#B8CDE7"
PBS_SIDE = "#93A9C3"
PBS_HILITE = "#DEE8F5"

YT = 43
YM = 30
YB = 17

# ============================================================
# OUTER PANEL
# ============================================================

ax.add_patch(
    Rectangle(
        (1.5, 4),
        177,
        54,
        facecolor="white",
        edgecolor="#D7D7D7",
        linewidth=0.9,
        zorder=0
    )
)

# ============================================================
# HELPERS
# ============================================================

def txt(
    x,
    y,
    s,
    fs=9,
    weight="normal",
    ha="center",
    va="center",
    color=DARK,
    z=30
):
    ax.text(
        x,
        y,
        s,
        fontsize=fs,
        fontweight=weight,
        ha=ha,
        va=va,
        color=color,
        zorder=z
    )

def section(
    x0,
    x1,
    title,
    color
):
    ax.add_patch(
        FancyBboxPatch(
            (x0, 7.2),
            x1-x0,
            46.3,
            boxstyle="round,pad=0.02,rounding_size=0.6",
            fill=False,
            edgecolor=color,
            linewidth=1.35,
            linestyle=(0, (6, 4)),
            zorder=1
        )
    )

    txt(
        (x0+x1)/2,
        56.8,
        title,
        fs=10,
        weight="bold"
    )

def beam(
    points,
    lw=4.0,
    color=GREEN,
    z=5
):
    p = np.asarray(points, float)

    ax.plot(
        p[:, 0],
        p[:, 1],
        color=color,
        linewidth=lw,
        solid_capstyle="round",
        solid_joinstyle="round",
        zorder=z
    )

def waveguide(
    points,
    lw=1.75
):
    p = np.asarray(points, float)

    ax.plot(
        p[:, 0],
        p[:, 1],
        color=WG,
        linewidth=lw,
        solid_capstyle="butt",
        solid_joinstyle="miter",
        zorder=3
    )

def arrow(
    p0,
    p1,
    color=GREEN,
    lw=1.05,
    ms=8.5,
    z=20
):
    ax.annotate(
        "",
        xy=p1,
        xytext=p0,
        arrowprops=dict(
            arrowstyle="-|>",
            color=color,
            linewidth=lw,
            mutation_scale=ms,
            shrinkA=0,
            shrinkB=0
        ),
        zorder=z
    )

# ============================================================
# STANDARD PBS
# ============================================================

def pbs_square(
    x,
    y,
    above=True,
    label=True,
    size=3.3
):
    ax.add_patch(
        Rectangle(
            (x-size/2, y-size/2),
            size,
            size,
            facecolor="none",
            edgecolor=BLUE,
            linewidth=2.0,
            zorder=10
        )
    )

    ax.plot(
        [x-size*0.35, x+size*0.35],
        [y-size*0.35, y+size*0.35],
        color=BLUE,
        linewidth=1.6,
        zorder=11
    )

    if label:
        off = size/2 + 0.95

        txt(
            x,
            y+off if above else y-off,
            "PBS",
            fs=8.7,
            weight="bold",
            va="bottom" if above else "top"
        )

# ============================================================
# 3D-LIKE COUPLING PBS
# ============================================================

def pbs_coupler_3d(
    x,
    y,
    label
):
    dx = 0.55
    dy = 0.40

    # narrower + taller
    w = 2.15
    h = 3.75

    # back diamond
    back = np.array([
        [x+dx,   y+h+dy],
        [x+w+dx, y+dy],
        [x+dx,   y-h+dy],
        [x-w+dx, y+dy]
    ])

    ax.add_patch(
        Polygon(
            back,
            closed=True,
            facecolor=PBS_SIDE,
            edgecolor=WG_DARK,
            linewidth=0.9,
            zorder=8
        )
    )

    # front diamond
    front = np.array([
        [x,   y+h],
        [x+w, y],
        [x,   y-h],
        [x-w, y]
    ])

    ax.add_patch(
        Polygon(
            front,
            closed=True,
            facecolor=PBS_FACE,
            edgecolor=WG_DARK,
            linewidth=1.1,
            zorder=10
        )
    )

    # top facet
    ax.add_patch(
        Polygon(
            [front[0], front[1], back[1], back[0]],
            closed=True,
            facecolor=PBS_HILITE,
            edgecolor=WG_DARK,
            linewidth=0.6,
            alpha=0.9,
            zorder=9
        )
    )

    # side facet
    ax.add_patch(
        Polygon(
            [front[1], front[2], back[2], back[1]],
            closed=True,
            facecolor=PBS_SIDE,
            edgecolor=WG_DARK,
            linewidth=0.6,
            alpha=0.9,
            zorder=9
        )
    )

    # inner crossed planes
    ax.plot(
        [x-1.55, x+1.55],
        [y+2.65, y-2.65],
        color=WG_DARK,
        lw=0.85,
        zorder=12
    )

    ax.plot(
        [x-1.55, x+1.55],
        [y-2.65, y+2.65],
        color=WG_DARK,
        lw=0.85,
        zorder=12
    )

    ax.plot(
        [x-0.65, x+0.65],
        [y+3.0, y-3.0],
        color="#7186A0",
        lw=0.55,
        zorder=12
    )

    ax.plot(
        [x-0.65, x+0.65],
        [y-3.0, y+3.0],
        color="#7186A0",
        lw=0.55,
        zorder=12
    )

    txt(
        x+0.1,
        y-4.8,
        label,
        fs=8.7,
        color="#404040"
    )

# ============================================================
# MIRROR
# ============================================================

def mirror45(
    x,
    y,
    orientation="/",
    above=True,
    label=True,
    length=4.2
):
    d = length / (2*np.sqrt(2))

    if orientation == "/":
        xs = [x-d, x+d]
        ys = [y-d, y+d]
    else:
        xs = [x-d, x+d]
        ys = [y+d, y-d]

    ax.plot(
        xs,
        ys,
        color="black",
        linewidth=2.35,
        solid_capstyle="butt",
        zorder=12
    )

    if label:
        txt(
            x,
            y+3.15 if above else y-3.15,
            "M",
            fs=8.7,
            weight="bold",
            va="bottom" if above else "top"
        )

# ============================================================
# LASER / SCREEN
# ============================================================

def laser(
    x,
    y
):
    ax.add_patch(
        Rectangle(
            (x-1.8, y-2.4),
            3.6,
            4.8,
            facecolor="#D9483E",
            edgecolor="#93231D",
            linewidth=0.9,
            zorder=10
        )
    )

    txt(
        x,
        y+3.4,
        "Laser",
        fs=8.7,
        weight="bold"
    )

def screen(
    x,
    y
):
    ax.add_patch(
        Rectangle(
            (x-0.45, y-9.6),
            0.9,
            19.2,
            facecolor="#D8E7F2",
            edgecolor="#8196A5",
            linewidth=1.0,
            zorder=10
        )
    )

    txt(
        x+1.8,
        y-10.9,
        "Screen",
        fs=8.7,
        weight="bold",
        ha="left"
    )

# ============================================================
# SECTIONS
# ============================================================

section(3, 42, "Preparation", PINK)
section(44, 69, "CNOT-1", GREY)
section(71, 104, "Coupling", COUPLING_EDGE)
section(106, 131, "CNOT-2", GREY)
section(133, 176, "Measurement", CYAN)

# ============================================================
# PREPARATION
# ============================================================

laser(7.0, YM)

beam([
    (8.8, YM),
    (22.5, YM)
])

pbs_square(
    22.5,
    YM,
    above=True,
    size=3.3
)

beam([
    (22.5, YM),
    (22.5, YT)
])

beam([
    (22.5, YM),
    (22.5, YB)
])

mirror45(
    22.5,
    YT,
    "/",
    True
)

mirror45(
    22.5,
    YB,
    "\\",
    False
)

beam([
    (22.5, YT),
    (44.0, YT)
])

beam([
    (22.5, YB),
    (44.0, YB)
])

txt(
    37.0,
    49.0,
    r"Control path  $q_c$",
    fs=8.7,
    weight="bold"
)

txt(
    37.0,
    10.8,
    r"Target path  $q_t$",
    fs=8.7,
    weight="bold"
)

# ============================================================
# CNOT MODULE
# ============================================================

def draw_cnot(
    x_left,
    x_right,
    section_left,
    section_right
):
    top_loop = 49.0
    bot_loop = 11.0

    # direct upper rail
    beam([
        (section_left, YT),
        (section_right, YT)
    ])

    # direct lower rail
    beam([
        (section_left, YB),
        (section_right, YB)
    ])

    # PBS positions
    pbs_square(
        x_left,
        YT,
        above=True,
        size=3.3
    )

    pbs_square(
        x_right,
        YB,
        above=True,
        size=3.3
    )

    # left full vertical
    beam([
        (x_left, bot_loop),
        (x_left, top_loop)
    ])

    # top loop
    beam([
        (x_left, top_loop),
        (x_right, top_loop)
    ])

    # right full vertical
    beam([
        (x_right, top_loop),
        (x_right, bot_loop)
    ])

    # bottom loop
    beam([
        (x_left, bot_loop),
        (x_right, bot_loop)
    ])

    # mirrors
    mirror45(
        x_left,
        top_loop,
        "/",
        True
    )

    mirror45(
        x_right,
        top_loop,
        "\\",
        True
    )

    mirror45(
        x_left,
        bot_loop,
        "\\",
        False
    )

    mirror45(
        x_right,
        bot_loop,
        "/",
        False
    )

    # subtle flow arrows
    arrow(
        (x_left+2.0, top_loop),
        (x_right-2.0, top_loop)
    )

    arrow(
        (x_left, YB+4.0),
        (x_left, YT+2.0)
    )

    arrow(
        (x_right, YT-2.0),
        (x_right, YB+4.0)
    )

    arrow(
        (x_right-2.0, bot_loop),
        (x_left+2.0, bot_loop)
    )

# ============================================================
# CNOT-1
# ============================================================

draw_cnot(
    53.0,
    63.0,
    44.0,
    71.0
)

# ============================================================
# COUPLING
# ============================================================

ax.add_patch(
    Rectangle(
        (72.0, 16.2),
        31.0,
        27.6,
        facecolor="#F5F5F5",
        edgecolor="none",
        zorder=0.5
    )
)

p1x = 80.0
p2x = 94.0

# left rails -> PBS1
waveguide([
    (71.0, YT),
    (76.0, YT),
    (p1x, YM)
])

waveguide([
    (71.0, YB),
    (76.0, YB),
    (p1x, YM)
])

# PBS1 -> middle rails
waveguide([
    (p1x, YM),
    (84.0, YT),
    (89.5, YT)
])

waveguide([
    (p1x, YM),
    (84.0, YB),
    (89.5, YB)
])

# middle rails -> PBS2
waveguide([
    (89.5, YT),
    (p2x, YM)
])

waveguide([
    (89.5, YB),
    (p2x, YM)
])

# PBS2 -> output rails
waveguide([
    (p2x, YM),
    (98.0, YT),
    (106.0, YT)
])

waveguide([
    (p2x, YM),
    (98.0, YB),
    (106.0, YB)
])

# 3D coupling PBS
pbs_coupler_3d(
    p1x,
    YM,
    r"PBS$_1$"
)

pbs_coupler_3d(
    p2x,
    YM,
    r"PBS$_2$"
)

# ============================================================
# CNOT-2
# ============================================================

draw_cnot(
    115.0,
    125.0,
    106.0,
    133.0
)

# ============================================================
# MEASUREMENT
# ============================================================

mx = 148.0

# main upper/lower rails
beam([
    (133.0, YT),
    (154.0, YT)
])

beam([
    (133.0, YB),
    (154.0, YB)
])

# ------------------------------------------------------------
# Upper PBS
# ------------------------------------------------------------

pbs_square(
    mx,
    YT,
    above=False,
    size=3.5
)

beam([
    (mx, YT),
    (mx, 49.0),
    (154.0, 49.0)
])

mirror45(
    mx,
    49.0,
    "/",
    True
)

txt(
    156.0,
    49.0,
    "V",
    fs=9.5,
    weight="bold"
)

txt(
    160.0,
    49.0,
    r"$|10\rangle$",
    fs=9.5,
    ha="left"
)

txt(
    156.0,
    YT,
    "H",
    fs=9.5,
    weight="bold"
)

txt(
    160.0,
    YT,
    r"$|00\rangle$",
    fs=9.5,
    ha="left"
)

# ------------------------------------------------------------
# Lower PBS
# ------------------------------------------------------------

pbs_square(
    mx,
    YB,
    above=True,
    size=3.5
)

txt(
    156.0,
    YB,
    "H",
    fs=9.5,
    weight="bold"
)

txt(
    160.0,
    YB,
    r"$|01\rangle$",
    fs=9.5,
    ha="left"
)

beam([
    (mx, YB),
    (mx, 11.0),
    (154.0, 11.0)
])

mirror45(
    mx,
    11.0,
    "\\",
    False
)

txt(
    156.0,
    11.0,
    "V",
    fs=9.5,
    weight="bold"
)

txt(
    160.0,
    11.0,
    r"$|11\rangle$",
    fs=9.5,
    ha="left"
)

# Screen slightly closer
screen(
    167.0,
    YM
)

# ============================================================
# LEGEND
# ============================================================

txt(
    90.0,
    2.6,
    "PBS = Polarizing Beam Splitter   |   "
    "PBS$_1$, PBS$_2$ = 3D coupling PBSs   |   "
    "M = 45° Mirror   |   "
    "V/H = polarization outputs",
    fs=8.4,
    color="#4E565C"
)

# ============================================================
# FINAL LAYOUT
# ============================================================

fig.subplots_adjust(
    left=0.01,
    right=0.995,
    top=0.96,
    bottom=0.08
)

# ============================================================
# SAVE
# ============================================================

plt.savefig(
    "optical_quantum_circuit_final_polished.png",
    dpi=600,
    bbox_inches="tight",
    facecolor="white"
)

plt.savefig(
    "optical_quantum_circuit_final_polished.pdf",
    bbox_inches="tight",
    facecolor="white"
)

plt.savefig(
    "optical_quantum_circuit_final_polished.svg",
    bbox_inches="tight",
    facecolor="white"
)

plt.show()
