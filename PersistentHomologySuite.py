import gudhi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Test 1: Sierpiński Gasket ---
def sierpinski_gasket_test(depth):
    print("Running Sierpiński Gasket Test...")

    # Function to generate points in the Sierpiński gasket
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

    # Generate points for a depth-6 Sierpiński gasket
    points = sierpinski_gasket(depth)

    # Construct a Rips complex from the points
    rips_complex = gudhi.RipsComplex(points=points, max_edge_length=0.2)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)

    # Compute the persistence of the simplicial complex
    diag = simplex_tree.persistence()

    # Gather the persistence data for statistical summary
    persistence_data = []
    for birth_death in diag:
        dim, (birth, death) = birth_death
        if death == float('inf'):
            death = np.nan  # Replace infinite death with NaN for easier statistics
        lifespan = death - birth if not np.isnan(death) else np.nan
        persistence_data.append([dim, birth, death, lifespan])

    # Create a DataFrame for statistical analysis
    df = pd.DataFrame(persistence_data, columns=['Dimension', 'Birth', 'Death', 'Lifespan'])

    # Summary statistics for each dimension
    summary_stats = df.groupby('Dimension').agg(
        count=('Lifespan', 'size'),
        avg_birth=('Birth', 'mean'),
        avg_death=('Death', 'mean'),
        avg_lifespan=('Lifespan', 'mean'),
        std_lifespan=('Lifespan', 'std'),
        max_lifespan=('Lifespan', 'max'),
        min_lifespan=('Lifespan', 'min')
    )

    # Display summary statistics
    print("Sierpiński Gasket Persistence Summary:")
    print(summary_stats)

    # Plot persistence lifespan histograms
    for dim in df['Dimension'].unique():
        dim_df = df[df['Dimension'] == dim]
        plt.hist(dim_df['Lifespan'].dropna(), bins=20, alpha=0.7, label=f'Dimension {dim}')
        plt.title(f'Sierpiński Gasket: Lifespan Histogram for Dimension {dim}')
        plt.xlabel('Lifespan')
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

    return df

# --- Test 2: Triangulated Cube ---
def triangulated_cube_test():
    print("Running Triangulated Cube Test...")

    # Vertices of a cube in 3D space
    vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],
                         [1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1]])

    # Create a Rips complex for the triangulated cube
    rips_complex = gudhi.RipsComplex(points=vertices, max_edge_length=2.0)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=3)

    # Compute persistence of the complex
    diag = simplex_tree.persistence()

    # Gather persistence data
    persistence_data = []
    for birth_death in diag:
        dim, (birth, death) = birth_death
        if death == float('inf'):
            death = np.nan  # Replace infinite death with NaN for easier statistics
        lifespan = death - birth if not np.isnan(death) else np.nan
        persistence_data.append([dim, birth, death, lifespan])

    # Create a DataFrame for statistical analysis
    df = pd.DataFrame(persistence_data, columns=['Dimension', 'Birth', 'Death', 'Lifespan'])

    # Summary statistics for each dimension
    summary_stats = df.groupby('Dimension').agg(
        count=('Lifespan', 'size'),
        avg_birth=('Birth', 'mean'),
        avg_death=('Death', 'mean'),
        avg_lifespan=('Lifespan', 'mean'),
        std_lifespan=('Lifespan', 'std'),
        max_lifespan=('Lifespan', 'max'),
        min_lifespan=('Lifespan', 'min')
    )

    # Display summary statistics
    print("Triangulated Cube Persistence Summary:")
    print(summary_stats)

    # Plot persistence lifespan histograms
    for dim in df['Dimension'].unique():
        dim_df = df[df['Dimension'] == dim]
        plt.hist(dim_df['Lifespan'].dropna(), bins=20, alpha=0.7, label=f'Dimension {dim}')
        plt.title(f'Triangulated Cube: Lifespan Histogram for Dimension {dim}')
        plt.xlabel('Lifespan')
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

    return df

# --- Test 3: Whitney Umbrella Approximation ---
def whitney_umbrella_test(num_points):
    print("Running Whitney Umbrella Approximation Test...")

    # Generate points approximating a Whitney Umbrella-like structure
    def whitney_umbrella(num_points):
        points = []
        for _ in range(num_points):
            x = np.random.uniform(-1, 1)
            y = x * np.random.uniform(-1, 1)  # Singular line at y = 0
            z = y ** 2
            points.append([x, y, z])
        return np.array(points)

    # Generate points
    points = whitney_umbrella(num_points)

    # Create a Rips complex from the points
    rips_complex = gudhi.RipsComplex(points=points, max_edge_length=0.5)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=2)

    # Compute persistence of the complex
    diag = simplex_tree.persistence()

    # Gather persistence data
    persistence_data = []
    for birth_death in diag:
        dim, (birth, death) = birth_death
        if death == float('inf'):
            death = np.nan  # Replace infinite death with NaN for easier statistics
        lifespan = death - birth if not np.isnan(death) else np.nan
        persistence_data.append([dim, birth, death, lifespan])

    # Create a DataFrame for statistical analysis
    df = pd.DataFrame(persistence_data, columns=['Dimension', 'Birth', 'Death', 'Lifespan'])

    # Summary statistics for each dimension
    summary_stats = df.groupby('Dimension').agg(
        count=('Lifespan', 'size'),
        avg_birth=('Birth', 'mean'),
        avg_death=('Death', 'mean'),
        avg_lifespan=('Lifespan', 'mean'),
        std_lifespan=('Lifespan', 'std'),
        max_lifespan=('Lifespan', 'max'),
        min_lifespan=('Lifespan', 'min')
    )

    # Display summary statistics
    print("Whitney Umbrella Approximation Persistence Summary:")
    print(summary_stats)

    # Plot persistence lifespan histograms
    for dim in df['Dimension'].unique():
        dim_df = df[df['Dimension'] == dim]
        plt.hist(dim_df['Lifespan'].dropna(), bins=20, alpha=0.7, label=f'Dimension {dim}')
        plt.title(f'Whitney Umbrella: Lifespan Histogram for Dimension {dim}')
        plt.xlabel('Lifespan')
        plt.ylabel('Frequency')
        plt.legend()
        plt.show()

    return df

# --- Run All Tests in the Unified Suite ---
def run_unified_test_suite():
    print("Running Unified Persistent Homology Test Suite...\n")

    # Run Sierpiński Gasket Test
    sierpinski_gasket_test(depth=6)

    # Run Triangulated Cube Test
    triangulated_cube_test()

    # Run Whitney Umbrella Approximation Test
    whitney_umbrella_test(num_points=500)

# Execute the unified test suite
if __name__ == "__main__":
    run_unified_test_suite()
