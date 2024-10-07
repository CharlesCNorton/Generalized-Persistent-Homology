## Algorithm 1: Spectral Sequence and Handling Singular Strata

Input: X (topological space), Σ (singular points), Filtration { X_t }
Output: Persistent homology near singularities

1. Initialize:
   For each singular point p ∈ Σ:
      Construct link L(p), capturing local topological structure near p.

2. First Page of Spectral Sequence:
   Compute E1^p,q, where p is filtration degree and q is dimension of homology.
   Populate the first page with H_q(L(p)): E1^p,q = H_q(L(p))

3. Successive Pages:
   For each subsequent page r > 1:
      Compute differentials: d_r: E_r^p,q → E_r^p+r, q-r+1
      Track evolution of homology classes.
      Homology classes that vanish under action of d_r are considered "killed."

4. Convergence:
   The spectral sequence converges to persistent homology near p: E_infinity^p,q → PH_q(X_t)

5. Output persistence intervals for homology classes near Σ.

import numpy as np
from itertools import combinations

class ChainComplex:
    def __init__(self, simplices, dimension):
        self.simplices = simplices
        self.dimension = dimension

    def boundary_map(self):
        # Compute boundary map for each simplex in the complex
        boundary_matrix = []
        for simplex in self.simplices:
            if len(simplex) == self.dimension + 1:
                boundary = []
                for i in range(len(simplex)):
                    boundary.append(simplex[:i] + simplex[i+1:])
                boundary_matrix.append(boundary)
        return np.array(boundary_matrix)

class SpectralSequenceSingularStrata:
    def __init__(self, space, singular_strata):
        self.space = space  # Full space X
        self.singular_strata = singular_strata  # Singular part Σ
        self.smooth_part = list(set(space) - set(singular_strata))  # X - Σ
        self.homology_groups = {}  # Store homology groups per stage

    def initialize_filtration(self):
        # Initialize filtration over smooth and singular parts
        filtration = [self.smooth_part]
        for t in range(1, 100):  # Detailed iteration over scales
            filtration.append(self.apply_filtration_step(t))
        return filtration

    def apply_filtration_step(self, t):
        # Build filtration for time-step t, gradually including singular strata
        smooth = self.inflate(self.smooth_part, t)
        singular = self.inflate(self.singular_strata, t)
        return smooth + singular

    def inflate(self, simplices, scale):
        # Inflate simplices based on scale (imagine expanding boundaries)
        return [tuple(np.array(s) * scale) for s in simplices]

    def compute_spectral_sequence(self):
        filtration = self.initialize_filtration()
        spectral_sequence = {}
        # Iterate over filtration to compute homology groups for each layer
        for i, step in enumerate(filtration):
            homology_at_step = self.compute_homology(step, i)
            spectral_sequence[i] = homology_at_step
        return spectral_sequence

    def compute_homology(self, step, step_index):
        homology = {}
        for k in range(0, 3):  # Compute H_0, H_1, H_2
            chain_complex = ChainComplex(self.get_k_simplices(step, k), k)
            boundary_map = chain_complex.boundary_map()
            homology[k] = self.solve_homology(boundary_map)
        return homology

    def get_k_simplices(self, space, k):
        return [simplex for simplex in combinations(space, k+1)]

    def solve_homology(self, boundary_map):
        # Compute kernel and image of boundary operator, H_k = ker(∂k) / im(∂k+1)
        kernel = self.compute_kernel(boundary_map)
        image = self.compute_image(boundary_map)
        homology = len(kernel) - len(image)
        return homology

    def compute_kernel(self, boundary_map):
        # Null space of the boundary map
        u, s, vh = np.linalg.svd(boundary_map)
        null_mask = (s <= 1e-10)
        kernel = np.compress(null_mask, vh, axis=0)
        return kernel

    def compute_image(self, boundary_map):
        # Image of the boundary map
        return np.dot(boundary_map, np.eye(boundary_map.shape[1]))

# Example usage:
space = [(0,), (1,), (2,), (0, 1), (1, 2), (0, 2), (0, 1, 2)]  # Simplicial complex example
singular_strata = [(0, 1, 2)]  # Singular region Σ
spectral_sequence_solver = SpectralSequenceSingularStrata(space, singular_strata)
spectral_sequence = spectral_sequence_solver.compute_spectral_sequence()

## Algorithm 2: Hybrid Filtration Scheme for Smooth, Non-Smooth, and Singular Transitions

Input: X (stratified space with smooth, non-smooth, and singular regions)
Output: Hybrid filtration { X_t } that transitions between regions

1. Smooth Region Filtration:
   Apply classical filtration (Vietoris-Rips or alpha complex) to smooth regions X_smooth.
   Construct nested subspaces { X_t^smooth }.

2. Non-Smooth Region Filtration:
   Use discrete Morse theory in non-smooth regions X_non-smooth.
   Assign critical simplices to track topological features.
   Construct { X_t^non-smooth } based on critical simplices.

3. Singular Region Filtration:
   Introduce curvature-weighted filtration for singular regions Σ ⊆ X.
   Include regions based on local curvature: X_t^Σ = { x ∈ X | κ(x) ≤ t }

4. Boundary Transitions:
   Ensure smooth transition between regions, define boundary transition rules:
   X_t^smooth ∩ X_t^non-smooth = X_t^boundary.

5. Combine results into hybrid filtration: 
   X_t = X_t^smooth ∪ X_t^non-smooth ∪ X_t^Σ.

6. Compute persistent homology using the hybrid filtration.

import numpy as np
import itertools
from scipy.spatial import Delaunay

# Class definition for a simplicial complex.
class SimplicialComplex:
    def __init__(self):
        self.vertices = set()
        self.simplices = set()

    def add_simplex(self, simplex):
        self.simplices.add(tuple(sorted(simplex)))
        self.vertices.update(simplex)

    def get_simplices(self, dim):
        return [s for s in self.simplices if len(s) == dim + 1]

# Function to compute the Vietoris-Rips complex for a point cloud.
def vietoris_rips(points, radius):
    n = len(points)
    simplicial_complex = SimplicialComplex()

    # 0-simplices (vertices)
    for i in range(n):
        simplicial_complex.add_simplex([i])

    # 1-simplices (edges)
    for i, j in itertools.combinations(range(n), 2):
        if np.linalg.norm(points[i] - points[j]) <= radius:
            simplicial_complex.add_simplex([i, j])

    # 2-simplices (triangles)
    for i, j, k in itertools.combinations(range(n), 3):
        if np.linalg.norm(points[i] - points[j]) <= radius and np.linalg.norm(points[j] - points[k]) <= radius and np.linalg.norm(points[i] - points[k]) <= radius:
            simplicial_complex.add_simplex([i, j, k])

    return simplicial_complex

# Function to compute the discrete Morse function for non-smooth regions.
def discrete_morse_function(simplicial_complex):
    critical_simplices = []

    # Assigning a discrete Morse function value to each simplex.
    for simplex in simplicial_complex.simplices:
        if len(simplex) == 1:
            # Vertices are critical 0-simplices.
            critical_simplices.append((simplex, 0))
        elif len(simplex) == 2:
            # Edges are critical 1-simplices.
            critical_simplices.append((simplex, 1))
        elif len(simplex) == 3:
            # Triangles are critical 2-simplices.
            critical_simplices.append((simplex, 2))

    return critical_simplices

# Function to compute the spectral sequence filtration for singular regions.
def spectral_sequence_filtration(simplicial_complex, singular_points, max_dim):
    filtration = {}
    for d in range(max_dim + 1):
        filtration[d] = []

    for simplex in simplicial_complex.simplices:
        if any(v in singular_points for v in simplex):
            filtration[len(simplex) - 1].append(simplex)

    return filtration

# Main function to run the hybrid filtration.
def hybrid_filtration(points, radius, singular_points):
    smooth_complex = vietoris_rips(points, radius)
    morse_critical = discrete_morse_function(smooth_complex)
    max_dim = max(len(s) for s in smooth_complex.simplices) - 1
    spectral_filtration = spectral_sequence_filtration(smooth_complex, singular_points, max_dim)

    # Construct the hybrid filtration by integrating all three.
    hybrid_complex = {}
    for d in range(max_dim + 1):
        hybrid_complex[d] = {
            'smooth': smooth_complex.get_simplices(d),
            'morse': [s for s, dim in morse_critical if dim == d],
            'singular': spectral_filtration[d]
        }

    return hybrid_complex

# Example usage.
if __name__ == "__main__":
    # Sample point cloud for testing.
    points = np.array([
        [0.1, 0.2],
        [0.4, 0.5],
        [0.6, 0.7],
        [0.9, 0.1],
        [0.3, 0.8]
    ])
    
    # Define singular points.
    singular_points = [2, 4]  # Points 2 and 4 are assumed to be in singular regions.
    
    # Define radius for the Vietoris-Rips complex.
    radius = 0.5
    
    # Run the hybrid filtration.
    hybrid_complex = hybrid_filtration(points, radius, singular_points)
    
    # Print results.
    for d in hybrid_complex:
        print(f"Dimension {d}:")
        print(f"  Smooth: {hybrid_complex[d]['smooth']}")
        print(f"  Morse Critical: {hybrid_complex[d]['morse']}")
        print(f"  Singular Filtration: {hybrid_complex[d]['singular']}")

## Algorithm 3: Weighted Bottleneck Distance under Non-Uniform Perturbations

Input: Persistence diagrams D1, D2, Weight function w(x)
Output: Weighted bottleneck distance d_B^w(D1, D2)

1. Initialization:
   For each point x ∈ D1 and D2, define weight w(x) based on the intensity of local perturbations (e.g., noise or variability specific to the region of the space).

2. Matching Persistence Diagrams:
   Identify matching φ between points in D1 and D2, where φ(x) is a mapping between corresponding points from D1 to D2. Optionally, allow points to map to the diagonal, representing feature disappearance.

3. Weighted Distance Calculation:
   For each matched pair (x, φ(x)):
      If x maps to a point in D2 (i.e., φ(x) ≠ diagonal):
         Compute the weighted distance as: d(x, φ(x)) = w(x) * |birth(x) - birth(φ(x))| + |death(x) - death(φ(x))|
      If x maps to the diagonal (i.e., φ(x) = diagonal):
         Compute the weighted persistence as: d(x, diagonal) = w(x) * persistence(x), where persistence(x) = death(x) - birth(x).

4. Supremum of Weighted Distances:
   Calculate the weighted bottleneck distance by taking the supremum (maximum) of all computed distances over the matching φ:
   d_B^w(D1, D2) = inf_φ sup_x∈D1 { w(x) * |birth(x) - birth(φ(x))| + |death(x) - death(φ(x))| }

5. Optimization:
   Minimize the supremum by adjusting the matching φ to find the optimal correspondence between points in D1 and D2 (or their mapping to the diagonal).

6. Return the final weighted bottleneck distance d_B^w(D1, D2).

import numpy as np
from scipy.optimize import linear_sum_assignment

# Function to compute the bottleneck distance between two persistence diagrams with weights
def weighted_bottleneck_distance(diagram1, diagram2, weights1, weights2):
    """
    Compute the weighted bottleneck distance between two persistence diagrams.
    
    Args:
        diagram1: List of tuples representing birth and death times in the first persistence diagram [(b_i, d_i), ...].
        diagram2: List of tuples representing birth and death times in the second persistence diagram [(b_j, d_j), ...].
        weights1: List of weights associated with each point in diagram1.
        weights2: List of weights associated with each point in diagram2.
    
    Returns:
        The weighted bottleneck distance between the two diagrams.
    """
    
    n = len(diagram1)
    m = len(diagram2)
    
    # Cost matrix for pairwise distances between points in diagram1 and diagram2.
    cost_matrix = np.zeros((n + m, n + m))
    
    # Fill the cost matrix for distances between points in diagram1 and diagram2.
    for i, (b_i, d_i) in enumerate(diagram1):
        for j, (b_j, d_j) in enumerate(diagram2):
            cost_matrix[i, j] = np.linalg.norm([b_i - b_j, d_i - d_j], ord=np.inf) * (weights1[i] + weights2[j])
    
    # Add diagonal elements for persistence points being matched to the diagonal (death = birth)
    for i, (b_i, d_i) in enumerate(diagram1):
        cost_matrix[i, n + i] = np.linalg.norm([b_i - d_i, 0], ord=np.inf) * weights1[i]  # matched to diagonal
    for j, (b_j, d_j) in enumerate(diagram2):
        cost_matrix[m + j, j] = np.linalg.norm([b_j - d_j, 0], ord=np.inf) * weights2[j]  # matched to diagonal
    
    # Solving the assignment problem using linear_sum_assignment to minimize the total cost
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    # Maximum cost in the optimal matching represents the weighted bottleneck distance
    max_cost = max([cost_matrix[i, j] for i, j in zip(row_ind, col_ind)])
    
    return max_cost

# Example function to generate persistence diagrams (mock data for testing)
def generate_mock_persistence_diagram(num_points, max_value=1.0):
    """
    Generate a mock persistence diagram with a specified number of points.
    
    Args:
        num_points: Number of points in the diagram.
        max_value: Maximum birth or death value.
    
    Returns:
        A list of persistence intervals and their associated weights.
    """
    persistence_diagram = []
    weights = []
    for _ in range(num_points):
        birth = np.random.uniform(0, max_value)
        death = np.random.uniform(birth, max_value)
        persistence_diagram.append((birth, death))
        weights.append(np.random.uniform(0.5, 1.5))  # Assign random weights between 0.5 and 1.5
    return persistence_diagram, weights

# Main function for testing the weighted bottleneck distance
if __name__ == "__main__":
    # Generate two mock persistence diagrams with associated weights
    diagram1, weights1 = generate_mock_persistence_diagram(5)
    diagram2, weights2 = generate_mock_persistence_diagram(5)
    
    # Compute the weighted bottleneck distance
    distance = weighted_bottleneck_distance(diagram1, diagram2, weights1, weights2)
    
    # Print results
    print("Persistence Diagram 1:", diagram1)
    print("Weights 1:", weights1)
    print("Persistence Diagram 2:", diagram2)
    print("Weights 2:", weights2)
    print("Weighted Bottleneck Distance:", distance)

