import math
import matplotlib.pyplot as plt

Vector = tuple[float, float]
Stress = tuple[Vector, Vector]

Angle = float


def normalAndShear(S: Stress, theta: Angle) -> Vector:
    a = math.radians(theta)
    sxx = S[0][0]
    syy = S[1][1]
    sxy = S[0][1]
    cos = math.cos(2 * a)
    sin = math.sin(2 * a)
    n = 0.5 * (sxx + syy) + 0.5 * (sxx - syy) * cos + sxy * sin
    s = 0.5 * (syy - sxx) * sin + sxy * cos
    return n, s


def simplePlots(S: Stress):
    """
    For a given stress, varies the normal of a plane and compute
    the normal and shear stress magnitude.
    :param S: The stress
    """
    x = []
    yN = []
    yS = []

    font = {'family': 'serif',
            'color': 'darkred',
            'weight': 'normal',
            'size': 16,
            }

    for theta in range(0, 91):
        x.append(theta)
        ns = normalAndShear(S, theta)
        yN.append(ns[0])
        yS.append(ns[1])

    fig, ax = plt.subplots()
    ax.plot(x, yN, label='Normal stress')
    ax.plot(x, yS, label='Shear stress')
    ax.legend()

    plt.title('Normal and shear stress on a plane', fontdict=font)
    plt.xlabel('$\Theta$', fontdict=font)
    plt.ylabel('Magnitude', fontdict=font)

    ax.axvline(x=45, ymax=0.5, linewidth=1, color='black', linestyle=(0, (5, 5)))

    ax.set_xlim(0, 90)
    ax.set_ylim(0, 1)
    plt.show()


# ---------------------------------------------

"""
The following stress is 
  |0 0|
  |0 1|
i.e., only with the vertical component
"""
stress = ((0, 0), (0, 1))
simplePlots(stress)
