import numpy as np
from ripser import ripser
from scipy.stats import ttest_ind, ks_2samp, wilcoxon
from sklearn.preprocessing import MinMaxScaler
from collections import defaultdict

# Generate point cloud based on framework and complexity
def generate_point_cloud(framework, num_points, dimension, complexity):
    if framework == 'singular':
        # Singular point cloud with perturbations for higher-dimensional singularities
        cloud = np.random.rand(num_points, dimension)
        perturbations = np.random.normal(scale=0.05 * complexity, size=cloud.shape)
        return cloud + perturbations
    elif framework == 'non-smooth':
        # Non-smooth with polyhedral-like irregularities
        cloud = np.random.rand(num_points, dimension)
        cloud[:num_points//2] *= complexity * 0.1  # Irregular scaling
        return cloud
    elif framework == 'fractal':
        # Fractal-like structure, recursive generation with higher-dimensional edge cases
        points = np.random.rand(3, dimension)  # Initial simplex
        for _ in range(complexity):
            new_points = []
            for i in range(len(points)):
                for j in range(i + 1, len(points)):
                    new_points.append((points[i] + points[j]) / 2)
            points = np.vstack([points, new_points])
            points = np.unique(points, axis=0)
        return points[:num_points]  # Truncate to num_points
    elif framework == 'hybrid':
        # Hybrid combining singularities with non-smooth and fractal structures
        cloud_singular = generate_point_cloud('singular', num_points//2, dimension, complexity)
        cloud_fractal = generate_point_cloud('fractal', num_points//2, dimension, complexity)
        return np.vstack((cloud_singular, cloud_fractal))  # Combine singular and fractal clouds
    elif framework == 'curvature':
        # Hybrid framework adding curvature effects to the filtration
        cloud = np.random.rand(num_points, dimension)
        curvature_weight = np.sin(np.linspace(0, np.pi, num_points))  # Simple curvature effect
        return cloud * curvature_weight[:, np.newaxis]  # Scale point cloud by curvature
    elif framework == 'control':
        # Control random point cloud
        return np.random.rand(num_points, dimension)
    else:
        raise ValueError(f"Unknown framework: {framework}")

# Function to run null hypothesis tests
def run_null_hypothesis_tests(singular_stats, control_stats):
    null_tests = {}
    for stat in singular_stats.keys():
        # Perform t-test
        t_stat, t_p_value = ttest_ind(singular_stats[stat], control_stats[stat], nan_policy='omit')

        # Calculate differences for Wilcoxon test
        differences = np.array(singular_stats[stat]) - np.array(control_stats[stat])

        if np.all(differences == 0):
            print(f"All differences for {stat} are zero. Skipping Wilcoxon test.")
            w_stat, w_p_value = np.nan, np.nan
        else:
            # Perform Wilcoxon signed-rank test
            w_stat, w_p_value = wilcoxon(singular_stats[stat], control_stats[stat])

        null_tests[stat] = {'t_stat': t_stat, 't_p_value': t_p_value, 'wilcoxon_stat': w_stat, 'wilcoxon_p_value': w_p_value}
    return null_tests

# Function to compute persistence statistics
def compute_persistence_statistics(diagrams):
    def calculate_statistics(persistence_intervals):
        finite_intervals = persistence_intervals[np.isfinite(persistence_intervals[:, 1])]
        if len(finite_intervals) > 0:
            persistence_lifespans = finite_intervals[:, 1] - finite_intervals[:, 0]
            mean_lifespan = np.mean(persistence_lifespans)
            std_lifespan = np.std(persistence_lifespans)
            max_lifespan = np.max(persistence_lifespans)
            min_lifespan = np.min(persistence_lifespans)
            ks_stat, ks_p = ks_2samp(persistence_lifespans, np.random.normal(mean_lifespan, std_lifespan, len(persistence_lifespans)))
            return {'count': len(finite_intervals), 'mean_lifespan': mean_lifespan, 'std_lifespan': std_lifespan,
                    'max_lifespan': max_lifespan, 'min_lifespan': min_lifespan, 'normality_ks_stat': ks_stat, 'normality_ks_p': ks_p}
        else:
            return {'count': 0, 'mean_lifespan': np.nan, 'std_lifespan': np.nan, 'max_lifespan': np.nan, 'min_lifespan': np.nan,
                    'normality_ks_stat': np.nan, 'normality_ks_p': np.nan}

    h0_diagram = diagrams[0]  # H_0 persistence diagram (connected components)
    h1_diagram = diagrams[1]  # H_1 persistence diagram (loops)

    # Compute statistics for H_0 and H_1
    h0_stats = calculate_statistics(h0_diagram)
    h1_stats = calculate_statistics(h1_diagram)

    return {'H_0': h0_stats, 'H_1': h1_stats}

# Run the final full experiment
def run_ultimate_experiment(num_points=2000, dimension=5, singular_points=5):
    complexities = [1, 2, 3, 4]
    frameworks = ['singular', 'non-smooth', 'fractal', 'hybrid', 'curvature', 'control']

    # Initialize results storage
    all_results = defaultdict(list)

    for complexity in complexities:
        print(f"Running tests for complexity level: {complexity}")
        for framework in frameworks:
            point_cloud = generate_point_cloud(framework, num_points, dimension, complexity)
            # Normalize the data
            scaler = MinMaxScaler()
            normalized_cloud = scaler.fit_transform(point_cloud)

            # Compute persistence diagrams using Ripser
            diagrams = ripser(normalized_cloud)['dgms']

            # Compute statistics for persistence diagrams
            stats = compute_persistence_statistics(diagrams)
            all_results[framework].append(stats)
            print(f"--- Statistical Summary for {framework.capitalize()} Framework (Complexity {complexity}) ---")
            print(f"H_0 (Connected Components): {stats['H_0']}")
            print(f"H_1 (Loops): {stats['H_1']}")

    # Run null hypothesis tests between singular and control
    results_singular = [r for r in all_results['singular']]
    results_control = [r for r in all_results['control']]

    # Collecting statistics for each stat (mean, count, etc.)
    singular_stats = {'mean_lifespan': [res['H_0']['mean_lifespan'] for res in results_singular],
                      'count': [res['H_0']['count'] for res in results_singular],
                      'std_lifespan': [res['H_0']['std_lifespan'] for res in results_singular]}

    control_stats = {'mean_lifespan': [res['H_0']['mean_lifespan'] for res in results_control],
                     'count': [res['H_0']['count'] for res in results_control],
                     'std_lifespan': [res['H_0']['std_lifespan'] for res in results_control]}

    # Run null hypothesis tests on the results
    null_test_results = run_null_hypothesis_tests(singular_stats, control_stats)
    print("\n--- Null Hypothesis Testing Results ---")
    for stat, result in null_test_results.items():
        print(f"\nFor statistic: {stat}")
        print(f"T-test statistic: {result['t_stat']}, P-value: {result['t_p_value']}")
        print(f"Wilcoxon signed-rank statistic: {result['wilcoxon_stat']}, P-value: {result['wilcoxon_p_value']}")

# Execute the final experiment
if __name__ == '__main__':
    run_ultimate_experiment(num_points=2000, dimension=5, singular_points=10)
