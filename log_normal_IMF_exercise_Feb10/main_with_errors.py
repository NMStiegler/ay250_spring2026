"""
Main script for the IMF bias simulation with multiple runs for error estimation.
"""
import numpy as np
import matplotlib.pyplot as plt
from monte_carlo import run_cutoff_study
from analysis import plot_alpha_vs_cutoff_with_errors, print_summary_statistics


def run_multiple_simulations(n_runs=10):
    """Run multiple simulations to estimate uncertainties."""
    
    # Parameters
    M_obs_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]  # Solar masses
    N = 10**6  # Number of stars per run
    M_max = 0.8  # Maximum observable mass
    m_c = 0.20  # Characteristic mass for log-normal IMF
    sigma = 0.69  # Width parameter for log-normal IMF
    
    print(f"Running {n_runs} Monte Carlo simulations...")
    print("="*60)
    print(f"Parameters:")
    print(f"  - True IMF: Log-normal with m_c = {m_c} M☉, σ = {sigma}")
    print(f"  - Sample size: N = {N:,} stars per run")
    print(f"  - Observable range: [M_obs, {M_max}] M☉")
    print(f"  - Testing M_obs values: {M_obs_values}")
    print()
    
    # Run multiple simulations
    all_results = []
    
    for run in range(n_runs):
        print(f"Run {run + 1}/{n_runs}...")
        
        # Use different seed for each run
        seed = 42 + run
        
        results = run_cutoff_study(
            M_obs_values=M_obs_values,
            N=N,
            M_max=M_max,
            m_c=m_c,
            sigma=sigma,
            random_seed=seed
        )
        
        all_results.append(results)
        
        # Print brief results for this run
        alpha_values = [r['alpha'] for r in results]
        print(f"  α values: {[f'{α:.2f}' for α in alpha_values]}")
    
    print()
    
    # Calculate and print statistics
    print("Monte Carlo Statistics:")
    print("="*60)
    
    for i, M_obs in enumerate(M_obs_values):
        alpha_values = [all_results[run][i]['alpha'] for run in range(n_runs)]
        n_values = [all_results[run][i]['n_observable'] for run in range(n_runs)]
        
        alpha_mean = np.mean(alpha_values)
        alpha_std = np.std(alpha_values)
        n_mean = np.mean(n_values)
        n_std = np.std(n_values)
        
        print(f"M_obs = {M_obs:.1f}: α = {alpha_mean:.3f} ± {alpha_std:.3f}, N_obs = {n_mean:.0f} ± {n_std:.0f}")
    
    print()
    
    # Create the main plot with error bars
    print("Creating visualization with error bars...")
    fig, ax = plot_alpha_vs_cutoff_with_errors(all_results)
    plt.savefig('alpha_vs_cutoff_with_errors.png', dpi=150, bbox_inches='tight')
    print("Saved main plot: alpha_vs_cutoff_with_errors.png")
    
    plt.show()
    
    return all_results


def main():
    """Run the complete IMF bias simulation with multiple runs."""
    
    # Run multiple simulations for error estimation
    results_list = run_multiple_simulations(n_runs=10)
    
    return results_list


if __name__ == "__main__":
    results = main()