import math
import matplotlib.pyplot as plt


def deg2rad(a):
    return a * math.pi / 180


def normalize(n):
    l = math.sqrt(n[0] ** 2 + n[1] ** 2)
    if l != 0:
        return [n[0] / l, n[1] / l]
    else:
        return n


def dot(n1, n2):
    return n1[0] * n2[0] + n1[1] * n2[1]


def principalDirections(theta, k):
    a = deg2rad(theta)
    c, s = math.cos(a), math.sin(a)
    xx, xy, yy = k * s * s, k * c * s, k * c * c
    trace = xx + yy
    discri = math.sqrt(trace * trace - 4 * (xx * yy - xy * xy))
    # Decreasing order according to the eigen values
    S1 = normalize([xy, (trace + discri) / 2 - xx])
    S3 = normalize([xy, (trace - discri) / 2 - xx])
    return [S1, S3]


def costJoint(n, r):
    return 1.0 - math.fabs(dot(n, r[1]))


def costStylo(n, r):
    return 1.0 - math.fabs(dot(n, r[0]))


def plotRotateS3():
    x = []
    yj = []
    ys = []

    font = {'family': 'serif',
            'color': 'darkred',
            'weight': 'normal',
            'size': 16,
            }

    for angle in range(0, 91, 1):
        x.append(angle)
        dirs = principalDirections(angle, 1)
        yj.append(costJoint([0, 1], dirs))
        ys.append(costStylo([0, 1], dirs))

    fig, ax = plt.subplots()
    ax.plot(x, yj, label='Joint')
    ax.plot(x, ys, label='Stylolite')
    ax.legend()
    px = 1 - math.sqrt(2) / 2
    ax.axvline(x=45, linewidth=1, color='black', linestyle=(0, (5, 5)))
    ax.axhline(xmax=45, y=px, linewidth=1, color='black', linestyle=(0, (5, 5)))
    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1)
    # ---
    plt.title('Cost functions for a vertical fracture', fontdict=font)
    plt.xlabel('$\sigma_3$ orientation', fontdict=font)
    plt.ylabel('Cost', fontdict=font)
    # ---
    plt.show()


def readData(filename):
    f = open(filename, "r")
    for line in f:
        tokens = line.split(' ')  # c'est un tableau de str
        nx = float(tokens[0])
        ny = float(tokens[1])
        print(nx, ny)


readData("matelles-joints.txt")
readData("matelles-stylolites.txt")

