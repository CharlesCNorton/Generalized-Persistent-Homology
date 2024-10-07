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
