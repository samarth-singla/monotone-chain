import numpy as np
from sklearn.datasets import make_blobs, make_moons, make_circles

def save_points(points, filename):
    """Saves an (n, 2) numpy array to a text file."""
    # We use a space delimiter, which is easy for C (scanf) to read.
    np.savetxt(filename, points, fmt='%.8f', delimiter=' ')
    print(f"Generated: {filename} ({len(points)} points)")

def gen_case_collinear_vertical(n=50):
    """Case: All points on a perfect vertical line."""
    x = np.ones(n)
    y = np.linspace(0, 10, n)
    # Shuffle y to test the initial sort
    np.random.shuffle(y)
    points = np.stack([x, y], axis=1)
    save_points(points, "case_vertical_line.txt")

def gen_case_collinear_horizontal(n=50):
    """Case: All points on a perfect horizontal line."""
    x = np.linspace(0, 10, n)
    y = np.ones(n)
    points = np.stack([x, y], axis=1)
    save_points(points, "case_horizontal_line.txt")

def gen_case_gaussian_blob(n=100):
    """Case: Standard "best case" cloud of points."""
    points, _ = make_blobs(n_samples=n, centers=1, cluster_std=2.5, random_state=42)
    save_points(points, "case_gaussian_blob.txt")

def gen_case_circle(n=100):
    """Case: Points on a circle. (Most points are on the hull)"""
    points, _ = make_circles(n_samples=n, factor=0.8, noise=0.05, random_state=7)
    save_points(points, "case_circle.txt")

def gen_case_u_shape(n=100):
    """Case: "U" shape (tests lower hull logic)"""
    points, _ = make_moons(n_samples=n, noise=0.05, random_state=6)
    save_points(points, "case_u_shape.txt")

def gen_case_rectangle(n=100):
    """Case: Points in a rectangle. (Tests 4 corners)"""
    # 4 corners
    corners = np.array([
        [0, 0], [10, 0], [10, 5], [0, 5]
    ])
    # n-4 interior points
    interior = np.random.rand(n - 4, 2)
    interior[:, 0] *= 9.8    # Scale to 0-9.8
    interior[:, 1] *= 4.8    # Scale to 0-4.8
    interior += 0.1          # Shift to 0.1-9.9 / 0.1-4.9
    
    points = np.concatenate([corners, interior])
    save_points(points, "case_rectangle.txt")
    
def gen_case_duplicates(n=50):
    """Case: Only a few unique points, repeated many times."""
    base_points = np.array([
        [0, 0], [5, 2], [1, 7], [8, 8]
    ])
    # Pick n times from the 4 base points
    indices = np.random.randint(0, 4, size=n)
    points = base_points[indices]
    # Add tiny noise so they aren't *identical* but are clustered
    points = points + np.random.randn(n, 2) * 1e-5
    save_points(points, "case_duplicates.txt")

if __name__ == "__main__":
    print("--- Generating Test Datasets for Convex Hull ---")
    
    gen_case_collinear_vertical(50)
    gen_case_collinear_horizontal(50)
    gen_case_gaussian_blob(200)
    gen_case_circle(100)
    gen_case_u_shape(100)
    gen_case_rectangle(150)
    gen_case_duplicates(100)
    save_points(np.array([[5.0, 5.0]]), "case_single_point.txt")
    save_points(np.array([]).reshape(0, 2), "case_empty_set.txt")
    
    print("--- All datasets generated. ---")