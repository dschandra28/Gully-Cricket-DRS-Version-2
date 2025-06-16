import numpy as np
from scipy.optimize import curve_fit

def predict_trajectory(points):
    if len(points) < 5:
        raise ValueError("Not enough data points for trajectory prediction.")

    points = np.array(points)
    x = points[:, 0]
    y = points[:, 1]

    def poly2(x, a, b, c):
        return a * x**2 + b * x + c

    try:
        params, _ = curve_fit(poly2, x, y)
    except Exception as e:
        print(f"Curve fitting failed: {e}")
        raise e

    return params

