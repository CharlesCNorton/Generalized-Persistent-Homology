import gudhi as gd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as stats
import time
from sklearn.neighbors import NearestNeighbors

plt.rcParams['text.usetex'] = False

# A function to calculate curvature combining local point density and local angles
def refined_curvature_measure(points, n_neighbors=10):
    # Calculate local point density using nearest neighbors
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm='ball_tree').fit(points)
    distances, indices = nbrs.kneighbors(points)
    avg_density_distance = np.mean(distances[:, 1:], axis=1)  # Average of nearest neighbors (excluding self)

    # Calculate local curvature using angles between neighbors
    angles = []
    for idx, point_indices in enumerate(indices):
        current_point = points[idx]
        neighbor_points = points[point_indices[1:]]  # Skip the point itself
        vectors = neighbor_points - current_point
        num_neighbors = vectors.shape[0]

        # Calculate pairwise angles between neighbor vectors
        angle_sum = 0
        count = 0
        for i in range(num_neighbors):
            for j in range(i + 1, num_neighbors):
                vec1 = vectors[i]
                vec2 = vectors[j]
                dot_product = np.dot(vec1, vec2)
                norm_product = np.linalg.norm(vec1) * np.linalg.norm(vec2)
                if norm_product > 0:
                    angle_sum += np.arccos(dot_product / norm_product)
                    count += 1
        avg_angle = angle_sum / count if count > 0 else 0
        angles.append(avg_angle)

    avg_angles = np.array(angles)

    # Combine density and angle information
    # The lower the distance and the larger the angles, the higher the curvature proxy
    curvature_combined = (1 / avg_density_distance) * avg_angles
    return curvature_combined

# Define a more complex random point cloud in 5 dimensions
np.random.seed(42)  # Ensure reproducibility

# Create 150 points in 5 dimensions to simulate a higher-dimensional structure with some complexity
points = np.random.uniform(-1, 1, size=(150, 5))  # Random points within a unit hypercube in 5D

# Calculate refined curvature for each point
refined_curvatures = refined_curvature_measure(points)

# Define a refined curvature threshold for the filtration
refined_curvature_threshold = np.percentile(refined_curvatures, 50)  # Use the median as a threshold

# Create a filtration based on refined curvature (curvature-weighted filtration)
filtered_points = points[refined_curvatures <= refined_curvature_threshold]

# Plot the original shape (in 2D projection) and filtered points for visualization
plt.figure(figsize=(10, 5))
plt.scatter(points[:, 0], points[:, 1], color='b', alpha=0.5, label='Original Shape (2D Projection)')
plt.scatter(filtered_points[:, 0], filtered_points[:, 1], color='r', alpha=0.5, label='Filtered Points (2D Projection)')
plt.legend()
plt.title("Refined Curvature-Weighted Filtration (150 points, 5D, 2D Projection)")
plt.show()

# --- Higher-Dimensional Complex Analysis ---

# Build a Rips complex on the filtered points
rips_complex = gd.RipsComplex(points=filtered_points, max_edge_length=2.0)  # Adjust max edge length for higher dimensionality
simplex_tree = rips_complex.create_simplex_tree(max_dimension=5)  # Increase max dimension to 5 for deeper analysis

# Compute persistent homology for the refined curvature-weighted filtration
start_time = time.time()
diag_refined_curvature_weighted = simplex_tree.persistence()
end_time = time.time()
print(f"Time to compute persistence (Refined Curvature-Weighted Filtration): {end_time - start_time:.2f} seconds")

# Plot persistence diagram for the refined curvature-weighted filtration
gd.plot_persistence_diagram(diag_refined_curvature_weighted)
plt.title("Persistence Diagram (Refined Curvature-Weighted Filtration)")
plt.show()

# --- Parallel Test: Using Standard Filtration ---

# Build a Rips complex on the original points without curvature-based filtration
rips_complex_standard = gd.RipsComplex(points=points, max_edge_length=2.0)
simplex_tree_standard = rips_complex_standard.create_simplex_tree(max_dimension=5)

# Compute persistent homology for the standard filtration
start_time = time.time()
diag_standard = simplex_tree_standard.persistence()
end_time = time.time()
print(f"Time to compute persistence (Standard Filtration): {end_time - start_time:.2f} seconds")

# Plot persistence diagram for standard filtration
gd.plot_persistence_diagram(diag_standard)
plt.title("Persistence Diagram (Standard Filtration)")
plt.show()

# --- Comparison Test ---

# Compare persistence intervals between refined curvature-weighted and standard filtration
longer_persistence_curvature = 0
shorter_persistence_curvature = 0
same_persistence = 0

for i, (interval_curvature, interval_standard) in enumerate(zip(diag_refined_curvature_weighted, diag_standard)):
    dim_curvature, (birth_curvature, death_curvature) = interval_curvature
    dim_standard, (birth_standard, death_standard) = interval_standard

    if dim_curvature == dim_standard:
        # Compare the persistence intervals
        if np.isinf(death_curvature) or np.isinf(death_standard):
            continue  # Skip comparisons involving infinite persistence values

        if death_curvature > death_standard:
            longer_persistence_curvature += 1
        elif death_curvature < death_standard:
            shorter_persistence_curvature += 1
        else:
            same_persistence += 1

print(f"Number of intervals where refined curvature-weighted filtration had longer persistence: {longer_persistence_curvature}")
print(f"Number of intervals where refined curvature-weighted filtration had shorter persistence: {shorter_persistence_curvature}")
print(f"Number of intervals with the same persistence in both filtrations: {same_persistence}")

# --- Statistical Suite for Full Comparison ---

# Convert persistence diagrams to dataframes for analysis
def diag_to_dataframe(diag, label):
    data = []
    for dim, (birth, death) in diag:
        if not np.isinf(birth) and not np.isinf(death):  # Filter out infinite persistence values
            data.append({'Dimension': dim, 'Birth': birth, 'Death': death, 'Persistence': death - birth, 'Label': label})
    return pd.DataFrame(data)

df_refined_curvature_weighted = diag_to_dataframe(diag_refined_curvature_weighted, label='Refined Curvature-Weighted')
df_standard = diag_to_dataframe(diag_standard, label='Standard')

# Combine dataframes for comparison
df_combined = pd.concat([df_refined_curvature_weighted, df_standard], ignore_index=True)

# Summary statistics for persistence intervals by filtration type
summary_stats = df_combined.groupby(['Label', 'Dimension'])['Persistence'].describe()
print("Summary Statistics for Persistence Intervals:\n", summary_stats)

# Statistical tests to compare persistence intervals
for dim in df_combined['Dimension'].unique():
    df_dim = df_combined[df_combined['Dimension'] == dim]
    persistence_curvature = df_dim[df_dim['Label'] == 'Refined Curvature-Weighted']['Persistence']
    persistence_standard = df_dim[df_dim['Label'] == 'Standard']['Persistence']

    # Perform t-test to check for significant difference in persistence between the two filtrations
    if len(persistence_curvature) > 1 and len(persistence_standard) > 1:
        t_stat, p_value = stats.ttest_ind(persistence_curvature, persistence_standard, equal_var=False)
        print(f"Dimension {dim} - T-test results: t-statistic = {t_stat}, p-value = {p_value}")

        # Effect size (Cohen's d) to quantify the difference
        mean_diff = np.abs(np.mean(persistence_curvature) - np.mean(persistence_standard))
        pooled_std = np.sqrt((np.std(persistence_curvature, ddof=1) ** 2 + np.std(persistence_standard, ddof=1) ** 2) / 2)
        cohens_d = mean_diff / pooled_std
        print(f"Dimension {dim} - Cohen's d = {cohens_d}")

print("\nDeep Comparison of Filtrations:")
print(df_combined)
