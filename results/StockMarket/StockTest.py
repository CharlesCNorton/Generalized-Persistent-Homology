import numpy as np
import yfinance as yf
from ripser import ripser
from scipy.spatial.distance import pdist, squareform
from itertools import combinations
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from scipy.linalg import svd
from collections import defaultdict
from scipy.optimize import linear_sum_assignment
from scipy.signal import find_peaks
from matplotlib import pyplot as plt
import seaborn as sns
import logging

# Set up logging for detailed debug information
logging.basicConfig(filename='persistent_homology.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# --------------------- STOCK DATA LOADING AND PREPROCESSING --------------------- #

# Enhanced stock data loader with robust error handling and missing data checks
def load_stock_data(symbols, start, end):
    """Load stock data from Yahoo Finance for a list of symbols."""
    data = {}
    for symbol in symbols:
        try:
            logging.info(f"Fetching data for {symbol}...")
            stock_data = yf.download(symbol, start=start, end=end)
            if stock_data.empty:
                logging.warning(f"Warning: No data found for {symbol}. Skipping this symbol.")
                continue
            data[symbol] = stock_data['Adj Close'].values
        except Exception as e:
            logging.error(f"Error fetching data for {symbol}: {e}")
    return data

# Function for time-delay embedding with dimension adjustments based on data length
def time_delay_embedding(data, delay, embedding_dimension):
    """Convert time series to a high-dimensional point cloud using time-delay embedding."""
    logging.info(f"Performing time-delay embedding with dimension {embedding_dimension} and delay {delay}...")

    # Perform time-delay embedding
    embedded_data = np.array([data[i:i + embedding_dimension] for i in range(len(data) - embedding_dimension)])

    # Adjust embedding dimension if necessary
    if len(embedded_data) < 20:
        logging.warning(f"Embedded data has fewer than 20 points. Adjusting embedding dimension.")
        embedding_dimension += 2
        embedded_data = np.array([data[i:i + embedding_dimension] for i in range(len(data) - embedding_dimension)])

    return embedded_data

# Function to normalize and scale the time-delay embedded data
def normalize_time_series(embedded_data):
    """Normalize the time series data to be used in topological computations."""
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(embedded_data)
    logging.info(f"Normalized the embedded time series data with MinMax scaling.")
    return normalized_data

# Visualize stock data for analysis
def plot_stock_data(stock_data):
    """Plot stock data for analysis and visualization."""
    plt.figure(figsize=(10, 6))
    for symbol, data in stock_data.items():
        plt.plot(data, label=symbol)
    plt.title("Stock Prices Over Time")
    plt.xlabel("Time (Days)")
    plt.ylabel("Adjusted Closing Price")
    plt.legend()
    plt.grid(True)
    plt.show()

# --------------------- INTERSECTION HOMOLOGY AND SINGULAR STRATA --------------------- #

# Compute the boundary map for a given simplicial complex and dimension with enhanced validation
def compute_boundary_map(simplices, dimension):
    """Compute the boundary map for simplices of a given dimension with thorough validation."""
    boundary_map = []
    if len(simplices) == 0:
        logging.warning(f"Empty simplices list for dimension {dimension}. Returning empty boundary map.")
        return boundary_map

    for simplex in simplices:
        if len(simplex) == dimension + 1:
            boundary = [simplex[:i] + simplex[i + 1:] for i in range(len(simplex))]
            boundary_map.append(boundary)
        else:
            logging.debug(f"Skipping simplex of incorrect size: {simplex}")

    logging.info(f"Computed boundary map for dimension {dimension} with {len(boundary_map)} simplices.")
    return boundary_map

# Solve homology for a given boundary map using SVD decomposition and validation
def solve_homology(boundary_map):
    """Compute homology by calculating the kernel and image of the boundary map with enhanced SVD handling."""
    if len(boundary_map) == 0:
        logging.warning("Empty boundary map detected, returning zero homology.")
        return 0

    try:
        matrix = np.array(boundary_map, dtype=np.float32)
        if matrix.size == 0:
            logging.warning("Boundary map matrix has invalid dimensions, returning zero homology.")
            return 0

        u, s, vh = svd(matrix, full_matrices=False)
        null_mask = (s <= 1e-10)
        kernel = vh[null_mask]

        image = np.dot(matrix, np.eye(matrix.shape[1])) if matrix.shape[1] > 0 else np.array([])
        homology = max(0, len(kernel) - image.shape[0] if image.size > 0 else len(kernel))
        logging.info(f"Homology computed with kernel size {len(kernel)} and image size {image.shape[0]}")

    except Exception as e:
        logging.error(f"Error in SVD computation: {e}")
        return 0

    return homology

# Function to compute allowable chains for intersection homology with advanced perversity checks
def compute_allowable_chains(boundary_map, strata, perversity):
    """Compute allowable chains in intersection homology based on strata and perversity."""
    logging.info(f"Computing allowable chains with perversity {perversity}...")
    allowable_chains = []
    for chain in boundary_map:
        if satisfies_perversity(chain, strata, perversity):
            allowable_chains.append(chain)
    logging.info(f"Computed {len(allowable_chains)} allowable chains out of {len(boundary_map)} total chains.")
    return allowable_chains

# Function to check if chain satisfies the perversity conditions for intersection homology
def satisfies_perversity(chain, strata, perversity):
    """Check if the chain satisfies intersection homology conditions based on perversity."""
    singular_intersections = count_singular_intersections(chain, strata)
    return singular_intersections <= perversity

# Function to count intersections of chain with singular strata
def count_singular_intersections(chain, strata):
    """Count how many times a chain intersects singular strata."""
    intersections = 0
    for simplex in chain:
        if any(vertex in strata for vertex in simplex):
            intersections += 1
    logging.debug(f"Chain intersects singular strata {intersections} times.")
    return intersections

# Adaptive radius selection for Vietoris-Rips complex based on point cloud density
def adaptive_radius_selection(point_cloud, method='knn', neighbors=5, scale_factor=1.5):
    """
    Determine an adaptive radius for Vietoris-Rips complex based on point cloud density.

    Args:
        point_cloud: Numpy array representing the point cloud.
        method: The method to use for selecting the radius ('knn' or 'density').
        neighbors: Number of neighbors for KNN-based radius calculation.
        scale_factor: Scaling factor for adjusting the radius.

    Returns:
        float: The selected adaptive radius.
    """
    print("Calculating adaptive radius for Vietoris-Rips complex...")

    if method == 'knn':
        # Use K-Nearest Neighbors (KNN) to estimate local point density
        nbrs = NearestNeighbors(n_neighbors=neighbors).fit(point_cloud)
        distances, _ = nbrs.kneighbors(point_cloud)
        avg_distance = np.mean(distances[:, -1])  # Average of the k-th nearest neighbors
        radius = avg_distance * scale_factor
        print(f"Adaptive radius (KNN method): {radius:.4f}")
        return radius

    elif method == 'density':
        # Use pairwise distances to calculate average inter-point distance
        dist_matrix = squareform(pdist(point_cloud))
        avg_distance = np.mean(dist_matrix)
        radius = avg_distance * scale_factor
        print(f"Adaptive radius (Density method): {radius:.4f}")
        return radius

    else:
        raise ValueError("Invalid method for radius selection. Use 'knn' or 'density'.")

# Function to compute intersection homology for singular strata with enhanced degree handling
def compute_intersection_homology(singular_complex, strata, degree, perversity):
    """Compute intersection homology for singular strata with respect to a given perversity."""
    logging.info(f"Computing intersection homology for singular strata with degree {degree} and perversity {perversity}...")
    homology_groups = []
    for dim in range(degree):
        boundary_map = compute_boundary_map(singular_complex, dim)
        allowable_chains = compute_allowable_chains(boundary_map, strata, perversity)
        homology_group = solve_homology(allowable_chains)
        homology_groups.append(homology_group)
    logging.info(f"Intersection homology computed with {len(homology_groups)} groups across {degree} dimensions.")
    return homology_groups

# --------------------- HYBRID FILTRATION SCHEME --------------------- #

# Function to compute Vietoris-Rips filtration for smooth regions with validation
def vietoris_rips(point_cloud, radius):
    """Compute Vietoris-Rips complex for a point cloud with detailed logging and validation."""
    logging.info(f"Building Vietoris-Rips complex with radius: {radius}...")
    distances = squareform(pdist(point_cloud))
    simplicial_complex = []

    # Add 0-simplices (vertices)
    for i in range(len(point_cloud)):
        simplicial_complex.append([i])

    # Add 1-simplices (edges)
    for i, j in combinations(range(len(point_cloud)), 2):
        if distances[i, j] <= radius:
            simplicial_complex.append([i, j])

    # Add 2-simplices (triangles)
    for i, j, k in combinations(range(len(point_cloud)), 3):
        if distances[i, j] <= radius and distances[j, k] <= radius and distances[i, k] <= radius:
            simplicial_complex.append([i, j, k])

    logging.info(f"Vietoris-Rips complex built with {len(simplicial_complex)} simplices.")
    return simplicial_complex, True

# Discrete Morse function for non-smooth regions with comprehensive simplex handling
def discrete_morse_function(simplicial_complex):
    """Assign discrete Morse function values to the simplicial complex with validation."""
    logging.info(f"Assigning discrete Morse function values to simplices.")
    critical_simplices = []

    if len(simplicial_complex) == 0:
        logging.warning("No simplices provided for Morse function. Returning empty critical simplices.")
        return critical_simplices

    for simplex in simplicial_complex:
        if len(simplex) == 1:
            critical_simplices.append((simplex, 0))  # 0-simplices (vertices)
        elif len(simplex) == 2:
            critical_simplices.append((simplex, 1))  # 1-simplices (edges)
        elif len(simplex) == 3:
            critical_simplices.append((simplex, 2))  # 2-simplices (triangles)

    logging.info(f"Assigned Morse function values to {len(critical_simplices)} simplices.")
    return critical_simplices

# Function to apply curvature-weighted filtration to singular regions based on stock price changes
def curvature_weighted_filtration(simplicial_complex, stock_data):
    """Apply curvature-weighted filtration to singular regions with validation."""
    weighted_simplices = []

    if len(simplicial_complex) == 0:
        logging.warning("Empty simplicial complex for curvature-weighted filtration.")
        return weighted_simplices

    for simplex in simplicial_complex:
        birth = stock_data[simplex[0]]
        death = stock_data[simplex[-1]]
        curvature = abs(death - birth)
        weighted_simplices.append((simplex, curvature))

    logging.info(f"Curvature-weighted filtration applied with {len(weighted_simplices)} simplices.")
    return weighted_simplices

# Function to ensure smooth transition across boundaries between regions in hybrid filtration
def apply_boundary_transition(smooth_simplices, non_smooth_simplices, singular_simplices):
    """Smoothly transition across boundaries between regions."""
    transition_simplices = []

    for simplex in smooth_simplices:
        if simplex in non_smooth_simplices or simplex in singular_simplices:
            transition_simplices.append(simplex)

    for simplex in non_smooth_simplices:
        if simplex in smooth_simplices or simplex in singular_simplices:
            transition_simplices.append(simplex)

    for simplex in singular_simplices:
        if simplex in smooth_simplices or simplex in non_smooth_simplices:
            transition_simplices.append(simplex)

    logging.info(f"Found {len(transition_simplices)} transition simplices across boundaries.")
    return transition_simplices

# Main hybrid filtration function combining smooth, non-smooth, and singular regions
def hybrid_filtration(point_cloud, singular_regions, smooth_regions, non_smooth_regions):
    """Compute a hybrid filtration for smooth, non-smooth, and singular regions."""
    logging.info("Applying extended hybrid filtration scheme with enhanced transition rules...")
    hybrid_complex = []

    # Smooth region filtration using Vietoris-Rips
    smooth_simplices, success = vietoris_rips(smooth_regions, adaptive_radius_selection(smooth_regions))
    if success:
        hybrid_complex.extend(smooth_simplices)
    else:
        logging.warning("Insufficient simplices in smooth region.")

    # Non-smooth region filtration using Discrete Morse theory
    non_smooth_simplices = discrete_morse_function(non_smooth_regions)
    hybrid_complex.extend(non_smooth_simplices)

    # Singular region filtration using curvature-weighted filtration
    singular_simplices = curvature_weighted_filtration(singular_regions, singular_regions)
    hybrid_complex.extend(singular_simplices)

    # Apply boundary transition rules between smooth, non-smooth, and singular regions
    logging.info("Ensuring smooth transition between different regions of space...")
    transition_simplices = apply_boundary_transition(smooth_simplices, non_smooth_simplices, singular_simplices)
    hybrid_complex.extend(transition_simplices)

    return hybrid_complex


# --------------------- PERSISTENCE AND STABILITY MEASURES --------------------- #

# Persistent homology computation using Ripser
def compute_persistent_homology(point_cloud):
    """Compute persistent homology using Ripser with enhanced filtration handling."""
    diagrams = ripser(point_cloud)['dgms']
    logging.info(f"Computed persistent homology with {len(diagrams)} diagrams across dimensions.")
    return diagrams

# Filter persistence diagrams to remove short-lived features
def persistence_filtering(persistence_diagrams, threshold=0.01):
    """Filter out persistence intervals with lifespan shorter than threshold."""
    filtered_diagrams = []
    for diagram in persistence_diagrams:
        filtered_diagram = [(b, d) for b, d in diagram if d - b >= threshold]
        filtered_diagrams.append(filtered_diagram)
    logging.info(f"Filtered persistence diagrams to retain features with persistence >= {threshold}.")
    return filtered_diagrams

# Weighted bottleneck distance computation for stability under non-uniform perturbations
def weighted_bottleneck_distance(diagram1, diagram2, weights1, weights2):
    """Compute the weighted bottleneck distance between two persistence diagrams."""
    logging.info("Calculating weighted bottleneck distance under non-uniform perturbations...")
    n = len(diagram1)
    m = len(diagram2)
    cost_matrix = np.zeros((n + m, n + m))

    # Populate cost matrix based on persistence diagrams and weights
    for i, (b_i, d_i) in enumerate(diagram1):
        for j, (b_j, d_j) in enumerate(diagram2):
            cost_matrix[i, j] = np.linalg.norm([b_i - b_j, d_i - d_j], ord=np.inf) * (weights1[i] + weights2[j])

    for i, (b_i, d_i) in enumerate(diagram1):
        cost_matrix[i, n + i] = np.linalg.norm([b_i - d_i, 0], ord=np.inf) * weights1[i]
    for j, (b_j, d_j) in enumerate(diagram2):
        cost_matrix[m + j, j] = np.linalg.norm([b_j - d_j, 0], ord=np.inf) * weights2[j]

    # Solve matching problem using the Hungarian algorithm
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    max_cost = max([cost_matrix[i, j] for i, j in zip(row_ind, col_ind)])

    logging.info(f"Weighted bottleneck distance computed with max cost: {max_cost:.4f}")
    return max_cost


# --------------------- TOPOLOGICAL TRANSITIONS AND ANALYSIS --------------------- #

# Function to detect topological transitions by analyzing persistence diagrams
def detect_topological_transitions(persistence_diagrams, peak_prominence=0.02):
    """Detect topological transitions by analyzing persistence diagrams and identifying peaks."""
    logging.info("Detecting topological transitions in persistence diagrams.")
    transitions = []
    for diagram in persistence_diagrams:
        persistence = [death - birth for birth, death in diagram]
        peaks, _ = find_peaks(persistence, prominence=peak_prominence)
        for peak in peaks:
            transitions.append(diagram[peak])
    logging.info(f"Detected {len(transitions)} topological transitions.")
    return transitions


# --------------------- FINAL STATISTICAL SUMMARY AND ANALYSIS --------------------- #

# Enhanced statistical summary function
def enhanced_statistical_summary(stock_data, persistence_diagrams, topological_transitions, homology_groups, index_names):
    """Produce an enhanced statistical summary of persistent homology and financial metrics."""
    logging.info("Generating enhanced statistical summary for stock data and persistent homology.")
    print("\n--- Enhanced Statistical Summary ---")

    # Stock data summary
    for symbol, data in stock_data.items():
        print(f"\n{symbol} Stock Data Summary:")
        print(f"Mean: {np.mean(data)}")
        print(f"Std Dev: {np.std(data)}")
        print(f"Max Price: {np.max(data)}")
        print(f"Min Price: {np.min(data)}")
        print(f"Price Range: {np.max(data) - np.min(data)}")
        print(f"Average Daily Price Change: {np.mean(np.diff(data))}")

    # Homology group sizes by index
    print("\nHomology Group Sizes by Index:")
    for index, homology_group in zip(index_names, homology_groups):
        print(f"{index} Homology Group Sizes:")
        for dim, group in enumerate(homology_group):
            print(f"Dimension {dim}: {group}")

    # Persistence intervals for topological features
    print("\nPersistence Intervals for Topological Features (across indices):")
    for index, diagrams in zip(index_names, persistence_diagrams):
        print(f"{index} Persistence Intervals:")
        for dim, diagram in enumerate(diagrams):
            for birth, death in diagram:
                print(f"  Birth: {birth:.3f}, Death: {death:.3f}, Persistence: {death - birth:.3f}")

    # Topological transitions detected
    print("\nTopological Transitions Detected (across indices):")
    for index, transitions in zip(index_names, topological_transitions):
        print(f"{index} Transitions:")
        if transitions:
            for transition in transitions:
                print(f"  Birth: {transition[0]:.3f}, Death: {transition[1]:.3f}")
        else:
            print("  No significant transitions detected.")

    # Additional financial statistics
    print("\nAdditional Financial Statistics:")
    for symbol, data in stock_data.items():
        price_diff = np.diff(data)
        print(f"\n{symbol} Additional Statistics:")
        print(f"Max Price Increase: {np.max(price_diff):.3f}")
        print(f"Max Price Decrease: {np.min(price_diff):.3f}")
        print(f"Volatility (Std Dev of Returns): {np.std(price_diff):.3f}")
        print(f"Total Number of Topological Features Detected: {sum(len(diagram) for diagram in persistence_diagrams)}")


# --------------------- MAIN FUNCTION --------------------- #

if __name__ == "__main__":
    indices = ["^GSPC", "^DJI", "^NDX", "^RUT", "XLF", "IYR", "BAC", "JPM", "C", "AIG", "GS", "GLD"]
    stock_data = load_stock_data(indices, "2005-01-01", "2010-12-31")

    persistence_diagrams_all = []
    topological_transitions_all = []
    homology_groups_all = []

    for symbol, data in stock_data.items():
        logging.info(f"Processing {symbol} stock data.")

        # Time-delay embedding and normalization
        embedded_data = time_delay_embedding(data, delay=1, embedding_dimension=5)
        normalized_data = normalize_time_series(embedded_data)

        # Adaptive radius selection
        radius = adaptive_radius_selection(normalized_data)

        # Vietoris-Rips complex
        smooth_simplices, success = vietoris_rips(normalized_data, radius)
        if not success:
            logging.warning(f"Skipping {symbol} due to insufficient simplices.")
            continue

        # Discrete Morse function
        non_smooth_critical_simplices = discrete_morse_function(smooth_simplices)

        # Curvature-weighted filtration
        singular_weighted_simplices = curvature_weighted_filtration(smooth_simplices, data)

        # Boundary map and homology group calculation
        homology_groups = []
        for dim in range(3):
            boundary_map = compute_boundary_map(smooth_simplices, dim)
            homology_group = solve_homology(boundary_map)
            homology_groups.append(homology_group)

        homology_groups_all.append(homology_groups)

        # Persistent homology computation
        persistence_diagrams = compute_persistent_homology(normalized_data)

        # Filter persistence diagrams
        filtered_persistence_diagrams = persistence_filtering(persistence_diagrams)
        persistence_diagrams_all.append(filtered_persistence_diagrams)

        # Detect topological transitions
        topological_transitions = detect_topological_transitions(filtered_persistence_diagrams)
        topological_transitions_all.append(topological_transitions)

    # Final statistical summary
    enhanced_statistical_summary(stock_data, persistence_diagrams_all, topological_transitions_all, homology_groups_all, indices)
