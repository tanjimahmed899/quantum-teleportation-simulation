import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch

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


# ============================================================
# MAIN LEVELS
# ============================================================

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
# TEXT
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


# ============================================================
# SECTION BOX
# ============================================================

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

            linewidth=1.25,

            linestyle=(0, (6,4)),

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


# ============================================================
# GREEN OPTICAL PATH
# ============================================================

def beam(
    points,
    lw=3.8,
    color=GREEN,
    z=5
):

    p = np.asarray(
        points,
        dtype=float
    )


    ax.plot(
        p[:,0],
        p[:,1],

        color=color,

        linewidth=lw,

        solid_capstyle="round",
        solid_joinstyle="round",

        zorder=z
    )


# ============================================================
# FLOW ARROW
# ============================================================

def arrow(
    p0,
    p1,
    color=GREEN,
    lw=1.0,
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
    size=3.35
):

    # blue square
    ax.add_patch(
        Rectangle(
            (
                x-size/2,
                y-size/2
            ),

            size,
            size,

            facecolor="none",

            edgecolor=BLUE,

            linewidth=1.9,

            zorder=10
        )
    )


    # internal diagonal
    ax.plot(
        [
            x-size*0.35,
            x+size*0.35
        ],

        [
            y-size*0.35,
            y+size*0.35
        ],

        color=BLUE,

        linewidth=1.5,

        zorder=11
    )


    if label:

        offset = size/2 + 1.0

        txt(
            x,

            y+offset if above else y-offset,

            "PBS",

            fs=8.8,
            weight="bold",

            va="bottom" if above else "top"
        )


# ============================================================
# 45 DEGREE MIRROR
# ============================================================

def mirror45(
    x,
    y,
    orientation="/",
    above=True,
    label=True,
    length=4.25
):

    d = length / (
        2*np.sqrt(2)
    )


    if orientation == "/":

        xs = [
            x-d,
            x+d
        ]

        ys = [
            y-d,
            y+d
        ]

    else:

        xs = [
            x-d,
            x+d
        ]

        ys = [
            y+d,
            y-d
        ]


    ax.plot(
        xs,
        ys,

        color="black",

        linewidth=2.2,

        solid_capstyle="butt",

        zorder=12
    )


    if label:

        txt(
            x,

            y+3.15 if above else y-3.15,

            "M",

            fs=8.8,
            weight="bold",

            va="bottom" if above else "top"
        )


# ============================================================
# LASER
# ============================================================

def laser(
    x,
    y
):

    ax.add_patch(
        Rectangle(
            (
                x-1.8,
                y-2.4
            ),

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
        y+3.6,

        "Laser",

        fs=8.8,
        weight="bold"
    )


# ============================================================
# SCREEN
# ============================================================

def screen(
    x,
    y
):

    ax.add_patch(
        Rectangle(
            (
                x-0.42,
                y-8.8
            ),

            0.84,
            17.6,

            facecolor="#D8E7F2",

            edgecolor="#8196A5",

            linewidth=1.0,

            zorder=10
        )
    )


    txt(
        x+1.75,
        y-10.4,

        "Screen",

        fs=8.8,
        weight="bold",

        ha="left"
    )


# ============================================================
# SECTION BOXES
# ============================================================

section(
    3,
    42,
    "Preparation",
    PINK
)

section(
    44,
    69,
    "CNOT-1",
    GREY
)

section(
    71,
    104,
    "Coupling",
    COUPLING_EDGE
)

section(
    106,
    131,
    "CNOT-2",
    GREY
)

section(
    133,
    176,
    "Measurement",
    CYAN
)


# ============================================================
# PREPARATION
# ============================================================

laser(
    7.0,
    YM
)


# Laser -> PBS
beam([
    (8.8, YM),
    (22.5, YM)
])


pbs_square(
    22.5,
    YM,

    above=True,

    size=3.35
)


# PBS -> upper path
beam([
    (22.5, YM),
    (22.5, YT)
])


# PBS -> lower path
beam([
    (22.5, YM),
    (22.5, YB)
])


# Mirrors
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


# Upper path
beam([
    (22.5, YT),
    (44.0, YT)
])


# Lower path
beam([
    (22.5, YB),
    (44.0, YB)
])


txt(
    37.0,
    49.1,

    r"Control path  $q_c$",

    fs=8.8,
    weight="bold"
)


txt(
    37.0,
    10.7,

    r"Target path  $q_t$",

    fs=8.8,
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


    # Main rails
    beam([
        (section_left, YT),
        (section_right, YT)
    ])


    beam([
        (section_left, YB),
        (section_right, YB)
    ])


    # PBS
    pbs_square(
        x_left,
        YT,

        above=True,

        size=3.35
    )


    pbs_square(
        x_right,
        YB,

        above=True,

        size=3.35
    )


    # Left side
    beam([
        (x_left, bot_loop),
        (x_left, top_loop)
    ])


    # Top
    beam([
        (x_left, top_loop),
        (x_right, top_loop)
    ])


    # Right side
    beam([
        (x_right, top_loop),
        (x_right, bot_loop)
    ])


    # Bottom
    beam([
        (x_left, bot_loop),
        (x_right, bot_loop)
    ])


    # Mirrors
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


    # Subtle flow arrows
    arrow(
        (x_left+2.0, top_loop),
        (x_right-2.0, top_loop)
    )


    arrow(
        (x_left, YB+3.5),
        (x_left, YT+3.5)
    )


    arrow(
        (x_right, YT-3.5),
        (x_right, YB+3.5)
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
# All paths GREEN
# PBS design SAME as all other PBS
# ============================================================

# subtle panel background
ax.add_patch(
    Rectangle(
        (72.0, 16.3),

        31.0,
        27.4,

        facecolor="#F7F7F7",

        edgecolor="none",

        zorder=0.5
    )
)


p1x = 80.0
p2x = 94.0


# ------------------------------------------------------------
# LEFT INPUT -> PBS1
# ------------------------------------------------------------

beam([
    (71.0, YT),
    (76.0, YT),
    (p1x, YM)
], lw=3.6)


beam([
    (71.0, YB),
    (76.0, YB),
    (p1x, YM)
], lw=3.6)


# ------------------------------------------------------------
# PBS1 -> MIDDLE UPPER / LOWER
# ------------------------------------------------------------

beam([
    (p1x, YM),
    (84.0, YT),
    (89.5, YT)
], lw=3.6)


beam([
    (p1x, YM),
    (84.0, YB),
    (89.5, YB)
], lw=3.6)


# ------------------------------------------------------------
# MIDDLE -> PBS2
# ------------------------------------------------------------

beam([
    (89.5, YT),
    (p2x, YM)
], lw=3.6)


beam([
    (89.5, YB),
    (p2x, YM)
], lw=3.6)


# ------------------------------------------------------------
# PBS2 -> OUTPUT
# ------------------------------------------------------------

beam([
    (p2x, YM),
    (98.0, YT),
    (106.0, YT)
], lw=3.6)


beam([
    (p2x, YM),
    (98.0, YB),
    (106.0, YB)
], lw=3.6)


# ------------------------------------------------------------
# NORMAL PBS — SAME DESIGN AS ALL OTHER PBS
# ------------------------------------------------------------

pbs_square(
    p1x,
    YM,

    above=False,
    label=False,

    size=3.35
)


pbs_square(
    p2x,
    YM,

    above=False,
    label=False,

    size=3.35
)


txt(
    p1x,
    YM-4.5,

    r"PBS$_1$",

    fs=8.6,

    color="#444444"
)


txt(
    p2x,
    YM-4.5,

    r"PBS$_2$",

    fs=8.6,

    color="#444444"
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


# Upper main line
beam([
    (133.0, YT),
    (156.0, YT)
])


# Lower main line
beam([
    (133.0, YB),
    (156.0, YB)
])


# ============================================================
# UPPER PBS
# ============================================================

pbs_square(
    mx,
    YT,

    above=False,

    size=3.5
)


# V branch
beam([
    (mx, YT),
    (mx, 49.0),
    (155.0, 49.0)
])


mirror45(
    mx,
    49.0,

    "/",

    True
)


txt(
    157.0,
    49.0,

    "V",

    fs=9.5,
    weight="bold"
)


txt(
    161.0,
    49.0,

    r"$|10\rangle$",

    fs=9.5,
    ha="left"
)


# H branch
txt(
    157.0,
    YT,

    "H",

    fs=9.5,
    weight="bold"
)


txt(
    161.0,
    YT,

    r"$|00\rangle$",

    fs=9.5,
    ha="left"
)


# ============================================================
# LOWER PBS
# ============================================================

pbs_square(
    mx,
    YB,

    above=True,

    size=3.5
)


# H branch
txt(
    157.0,
    YB,

    "H",

    fs=9.5,
    weight="bold"
)


txt(
    161.0,
    YB,

    r"$|01\rangle$",

    fs=9.5,
    ha="left"
)


# V branch
beam([
    (mx, YB),
    (mx, 11.0),
    (155.0, 11.0)
])


mirror45(
    mx,
    11.0,

    "\\",

    False
)


txt(
    157.0,
    11.0,

    "V",

    fs=9.5,
    weight="bold"
)


txt(
    161.0,
    11.0,

    r"$|11\rangle$",

    fs=9.5,
    ha="left"
)


# ============================================================
# SCREEN
# ============================================================

screen(
    168.5,
    YM
)


# ============================================================
# LEGEND
# ============================================================

txt(
    90.0,
    2.5,

    "PBS = Polarizing Beam Splitter   |   "
    "PBS$_1$, PBS$_2$ = coupling PBSs   |   "
    "M = 45° Mirror   |   "
    "V/H = polarization outputs",

    fs=8.5,

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
# EXPORT
# ============================================================

plt.savefig(
    "optical_quantum_circuit_FINAL.png",

    dpi=600,

    bbox_inches="tight",

    facecolor="white"
)


plt.savefig(
    "optical_quantum_circuit_FINAL.pdf",

    bbox_inches="tight",

    facecolor="white"
)


plt.savefig(
    "optical_quantum_circuit_FINAL.svg",

    bbox_inches="tight",

    facecolor="white"
)


# ============================================================
# SHOW
# ============================================================

plt.show()
