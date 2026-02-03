#!/usr/bin/env python3
"""
Stellar IMF Monte Carlo Simulation Execution Script
Runs the experimental matrix from the plan
"""

import numpy as np
import pandas as pd
from datetime import datetime
from imf_simulation import StellarIMFSimulation
import argparse


def run_precision_vs_cluster_size(sim, K_sims=1000):
    """Primary experiment: precision vs cluster size"""
    print("=== Running Precision vs Cluster Size Experiment ===")
    
    methods = ['mle', 'ls', 'mcmc']
    all_results = []
    
    alpha_true = sim.config['alpha_true']
    M_min = sim.config['M_min']
    M_max = sim.config['M_max']
    
    for N in sim.config['N_values']:
        print(f"Running N={N} with K={K_sims} simulations...")
        
        results = sim.run_simulation_cluster(N, M_min, M_max, K_sims, methods)
        all_results.append(results)
        
        filename = f"results_N{N}_alpha{alpha_true}_r{int(M_max/M_min)}.csv"
        sim.save_results(results, filename)
        print(f"Saved {len(results)} results to {filename}")
    
    combined_results = pd.concat(all_results, ignore_index=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    combined_filename = f"full_experiment_precision_{timestamp}.csv"
    sim.save_results(combined_results, combined_filename)
    
    print(f"Combined results saved to {combined_filename}")
    return combined_results


def run_mass_ratio_effects(sim, N_clusters=1000):
    """Secondary experiment: mass ratio effects"""
    print("\n=== Running Mass Ratio Effects Experiment ===")
    
    methods = ['mle', 'ls', 'mcmc']
    alpha_true = sim.config['alpha_true']
    
    all_results = []
    
    for r_ratio in sim.config['r_ratios']:
        print(f"Running mass ratio r={r_ratio}...")
        
        M_min = 1.0
        M_max = M_min * r_ratio
        
        results = sim.run_simulation_cluster(N_clusters, M_min, M_max, 500, methods)
        all_results.append(results)
        
        filename = f"results_N{N_clusters}_alpha{alpha_true}_r{r_ratio}.csv"
        sim.save_results(results, filename)
        print(f"Saved {len(results)} results to {filename}")
    
    combined_results = pd.concat(all_results, ignore_index=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    combined_filename = f"full_experiment_massratio_{timestamp}.csv"
    sim.save_results(combined_results, combined_filename)
    
    print(f"Combined results saved to {combined_filename}")
    return combined_results


def run_quick_test(sim):
    """Quick test with small parameters to verify implementation"""
    print("=== Running Quick Test ===")
    
    test_config = {
        'alpha_true': 2.35,
        'M_min': 0.1,
        'M_max': 10.0,
        'N_values': [10, 50],
        'K_simulations': 50,
        'r_ratios': [10, 100],
        'random_seed': 42
    }
    
    test_sim = StellarIMFSimulation(test_config)
    
    for N in test_config['N_values']:
        print(f"Testing N={N}...")
        results = test_sim.run_simulation_cluster(N, 0.1, 10.0, 20, ['mle', 'ls'])
        
        if len(results) > 0:
            analysis = test_sim.analyze_results(results)
            print(f"Results for N={N}:")
            for _, row in analysis.iterrows():
                print(f"  {row['method']}: bias={row['bias']:.3f}, std={row['std_alpha']:.3f}")
        
        filename = f"test_results_N{N}.csv"
        test_sim.save_results(results, filename)
    
    print("Quick test completed successfully!")


def main():
    parser = argparse.ArgumentParser(description='Stellar IMF Monte Carlo Simulation')
    parser.add_argument('--mode', choices=['precision', 'massratio', 'test', 'all'], 
                       default='test', help='Experiment mode to run')
    parser.add_argument('--k-sims', type=int, default=1000, 
                       help='Number of simulations per parameter set')
    parser.add_argument('--quick', action='store_true', 
                       help='Run with reduced parameters for quick testing')
    
    args = parser.parse_args()
    
    if args.quick:
        config = {
            'alpha_true': 2.35,
            'M_min': 0.1,
            'M_max': 100.0,
            'N_values': [10, 50, 100, 500],
            'K_simulations': 100,
            'r_ratios': [10, 100],
            'random_seed': 42
        }
    else:
        config = None
    
    sim = StellarIMFSimulation(config)
    print("Stellar IMF Monte Carlo Simulation")
    print(f"Configuration: {sim.config}")
    
    if args.mode == 'test' or args.mode == 'all':
        run_quick_test(sim)
    
    if args.mode == 'precision' or args.mode == 'all':
        results = run_precision_vs_cluster_size(sim, args.k_sims)
        
        analysis = sim.analyze_results(results)
        analysis_filename = f"analysis_precision_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        sim.save_results(analysis, analysis_filename)
        print(f"Analysis saved to {analysis_filename}")
    
    if args.mode == 'massratio' or args.mode == 'all':
        results = run_mass_ratio_effects(sim)
        
        analysis = sim.analyze_results(results)
        analysis_filename = f"analysis_massratio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        sim.save_results(analysis, analysis_filename)
        print(f"Analysis saved to {analysis_filename}")
    
    print("\nSimulation completed!")


if __name__ == "__main__":
    main()