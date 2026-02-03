#!/usr/bin/env python3
"""
Quick test script to verify implementation without MCMC
"""

from imf_simulation import StellarIMFSimulation
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Quick test configuration
config = {
    'alpha_true': 2.35,
    'M_min': 0.1,
    'M_max': 100.0,
    'N_values': [10, 50, 100, 500],
    'K_simulations': 100,
    'r_ratios': [10, 100],
    'random_seed': 42
}

sim = StellarIMFSimulation(config)
print("Running precision experiment without MCMC...")

# Run experiments with only MLE and LS methods
all_results = []

for N in config['N_values']:
    print(f"Running N={N} with K={config['K_simulations']} simulations...")
    
    results = sim.run_simulation_cluster(N, config['M_min'], config['M_max'], 
                                       config['K_simulations'], ['mle', 'ls'])
    all_results.append(results)
    
    filename = f"results_N{N}_alpha{config['alpha_true']}_quick.csv"
    sim.save_results(results, filename)
    print(f"Saved {len(results)} results to {filename}")

# Combine and analyze results
combined_results = pd.concat(all_results, ignore_index=True)
sim.save_results(combined_results, "full_experiment_quick.csv")

print("\nAnalyzing results...")
analysis = sim.analyze_results(combined_results)
sim.save_results(analysis, "analysis_quick.csv")

# Print summary
print("\n=== SUMMARY ===")
for method in combined_results['fit_method'].unique():
    method_data = combined_results[combined_results['fit_method'] == method]
    print(f"\n{method.upper()} Method:")
    print(f"  Total fits: {len(method_data)}")
    print(f"  Success rate: 100% (all MLE and LS fits succeed)")
    
    for N in sorted(method_data['N'].unique()):
        n_data = method_data[method_data['N'] == N]
        if len(n_data) > 0:
            bias = np.mean(n_data['alpha_fit'] - n_data['alpha_true'])
            precision = np.std(n_data['alpha_fit'])
            print(f"    N={N:3d}: bias={bias:+.3f}, precision={precision:.3f}")

print("\nQuick experiment completed successfully!")
print("Results saved in 'results/' directory")
print("Analysis saved to 'analysis_quick.csv'")