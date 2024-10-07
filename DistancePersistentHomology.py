import gudhi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import gudhi.wasserstein as wasserstein
import gudhi.bottleneck as bottleneck

# --- Test 1: Sierpinski Gasket ---
def sierpinski_gasket_test(depth):
    print("Running Sierpinski Gasket Test...")

    def sierpinski_gasket(depth):
        points = np.array([[0, 0], [1, 0], [0.5, np.sqrt(3)/2]])  # Initial triangle
        for _ in range(depth):
            new_points = []
            for i in range(len(points)):
                for j in range(i + 1, len(points)):
                    new_points.append((points[i] + points[j]) / 2)
            points = np.vstack([points, new_points])
            points = np.unique(points, axis=0)
        return points

    points = sierpinski_gasket(depth)
    rips_complex = gudhi.RipsComplex(points=points, max_edge_length=0.2)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=4)
    diag = simplex_tree.persistence()

    # Extract the persistence diagram for comparison
    diag_np = np.array([pair[1] for pair in diag])

    # Gather persistence data
    persistence_data = []
    for birth_death in diag:
        dim, (birth, death) = birth_death
        if death == float('inf'):
            death = np.nan  # Replace infinite death with NaN for easier statistics
        lifespan = death - birth if not np.isnan(death) else np.nan
        persistence_data.append([dim, birth, death, lifespan])

    df = pd.DataFrame(persistence_data, columns=['Dimension', 'Birth', 'Death', 'Lifespan'])

    summary_stats = df.groupby('Dimension').agg(
        count=('Lifespan', 'size'),
        avg_birth=('Birth', 'mean'),
        avg_death=('Death', 'mean'),
        avg_lifespan=('Lifespan', 'mean'),
        std_lifespan=('Lifespan', 'std'),
        max_lifespan=('Lifespan', 'max'),
        min_lifespan=('Lifespan', 'min')
    )

    print("Sierpinski Gasket Persistence Summary:")
    print(summary_stats)
    return diag_np, df

# --- Test 2: Triangulated Cube ---
def triangulated_cube_test():
    print("Running Triangulated Cube Test...")

    vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
                         [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]])

    rips_complex = gudhi.RipsComplex(points=vertices, max_edge_length=2.0)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=4)
    diag = simplex_tree.persistence()

    diag_np = np.array([pair[1] for pair in diag])

    persistence_data = []
    for birth_death in diag:
        dim, (birth, death) = birth_death
        if death == float('inf'):
            death = np.nan
        lifespan = death - birth if not np.isnan(death) else np.nan
        persistence_data.append([dim, birth, death, lifespan])

    df = pd.DataFrame(persistence_data, columns=['Dimension', 'Birth', 'Death', 'Lifespan'])

    summary_stats = df.groupby('Dimension').agg(
        count=('Lifespan', 'size'),
        avg_birth=('Birth', 'mean'),
        avg_death=('Death', 'mean'),
        avg_lifespan=('Lifespan', 'mean'),
        std_lifespan=('Lifespan', 'std'),
        max_lifespan=('Lifespan', 'max'),
        min_lifespan=('Lifespan', 'min')
    )

    print("Triangulated Cube Persistence Summary:")
    print(summary_stats)
    return diag_np, df

# --- Test 3: Whitney Umbrella Approximation ---
def whitney_umbrella_test(num_points):
    print("Running Whitney Umbrella Approximation Test...")

    def whitney_umbrella(num_points):
        points = []
        for _ in range(num_points):
            x = np.random.uniform(-1, 1)
            y = x * np.random.uniform(-1, 1)
            z = y ** 2
            points.append([x, y, z])
        return np.array(points)

    points = whitney_umbrella(num_points)
    rips_complex = gudhi.RipsComplex(points=points, max_edge_length=0.5)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=4)
    diag = simplex_tree.persistence()

    diag_np = np.array([pair[1] for pair in diag])

    persistence_data = []
    for birth_death in diag:
        dim, (birth, death) = birth_death
        if death == float('inf'):
            death = np.nan
        lifespan = death - birth if not np.isnan(death) else np.nan
        persistence_data.append([dim, birth, death, lifespan])

    df = pd.DataFrame(persistence_data, columns=['Dimension', 'Birth', 'Death', 'Lifespan'])

    summary_stats = df.groupby('Dimension').agg(
        count=('Lifespan', 'size'),
        avg_birth=('Birth', 'mean'),
        avg_death=('Death', 'mean'),
        avg_lifespan=('Lifespan', 'mean'),
        std_lifespan=('Lifespan', 'std'),
        max_lifespan=('Lifespan', 'max'),
        min_lifespan=('Lifespan', 'min')
    )

    print("Whitney Umbrella Approximation Persistence Summary:")
    print(summary_stats)
    return diag_np, df

# --- Distance Calculation ---
def compute_distances(diag1, diag2):
    print("Calculating Bottleneck and Wasserstein distances between diagrams...")

    bottleneck_dist = bottleneck.bottleneck_distance(diag1, diag2)
    print(f"Bottleneck Distance: {bottleneck_dist}")

    wasserstein_dist = wasserstein.wasserstein_distance(diag1, diag2)
    print(f"Wasserstein Distance: {wasserstein_dist}")

    return bottleneck_dist, wasserstein_dist

# --- Unified Test Suite ---
def run_unified_test_suite_with_distances():
    print("Running Unified Persistent Homology Test Suite with Distance Calculations...\n")

    diag1, df1 = sierpinski_gasket_test(depth=6)
    diag2, df2 = triangulated_cube_test()
    diag3, df3 = whitney_umbrella_test(num_points=500)

    print("\nSierpinski Gasket Persistence Data:\n", df1)
    print("\nTriangulated Cube Persistence Data:\n", df2)
    print("\nWhitney Umbrella Persistence Data:\n", df3)

    print("\nComparing Sierpinski Gasket and Triangulated Cube:")
    compute_distances(diag1, diag2)

    print("\nComparing Triangulated Cube and Whitney Umbrella:")
    compute_distances(diag2, diag3)

    print("\nComparing Sierpinski Gasket and Whitney Umbrella:")
    compute_distances(diag1, diag3)

# Run the test suite
if __name__ == "__main__":
    run_unified_test_suite_with_distances()
