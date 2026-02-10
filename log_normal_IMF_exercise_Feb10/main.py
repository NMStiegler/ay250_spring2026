"""
Main script for the IMF bias simulation experiment.
"""
import numpy as np
import matplotlib.pyplot as plt
from monte_carlo import run_cutoff_study
from analysis import plot_alpha_vs_cutoff, plot_imf_comparison, print_summary_statistics


def main():
    """Run the complete IMF bias simulation."""
    
    print("Starting IMF Bias Simulation...")
    print("="*50)
    
    # Parameters
    M_obs_values = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]  # Solar masses
    N = 10**6  # Number of stars
    M_max = 0.8  # Maximum observable mass
    m_c = 0.20  # Characteristic mass for log-normal IMF
    sigma = 0.69  # Width parameter for log-normal IMF
    
    print(f"Parameters:")
    print(f"  - True IMF: Log-normal with m_c = {m_c} M☉, σ = {sigma}")
    print(f"  - Sample size: N = {N:,} stars")
    print(f"  - Observable range: [M_obs, {M_max}] M☉")
    print(f"  - Testing M_obs values: {M_obs_values}")
    print()
    
    # Run the cutoff study
    print("Running simulations...")
    results = run_cutoff_study(
        M_obs_values=M_obs_values,
        N=N,
        M_max=M_max,
        m_c=m_c,
        sigma=sigma,
        random_seed=42  # For reproducibility
    )
    
    # Print summary statistics
    print_summary_statistics(results)
    
    # Create the main plot
    print("Creating visualization...")
    fig1, ax1 = plot_alpha_vs_cutoff(results)
    plt.savefig('alpha_vs_cutoff.png', dpi=150, bbox_inches='tight')
    print("Saved main plot: alpha_vs_cutoff.png")
    
    # Create detailed comparison for one case (middle cutoff)
    middle_idx = len(M_obs_values) // 2
    M_obs_example = M_obs_values[middle_idx]
    result_example = results[middle_idx]
    
    print(f"\nCreating detailed comparison for M_obs = {M_obs_example} M☉...")
    
    # Generate fresh data for the detailed plot
    from monte_carlo import apply_observation_cutoff
    from imf_core import generate_log_normal_population
    
    np.random.seed(42 + middle_idx)
    masses_full = generate_log_normal_population(N, m_c, sigma)
    masses_obs = apply_observation_cutoff(masses_full, M_obs_example, M_max)
    
    fig2, axes2 = plot_imf_comparison(
        masses_obs, 
        result_example['alpha'], 
        M_obs_example,
        M_max,
        m_c,
        sigma
    )
    plt.savefig(f'imf_comparison_Mobs_{M_obs_example:.1f}.png', dpi=150, bbox_inches='tight')
    print(f"Saved detailed comparison: imf_comparison_Mobs_{M_obs_example:.1f}.png")
    
    plt.show()
    
    return results


def run_simple_tests():
    """Run basic sanity tests without pytest."""
    print("Running basic sanity tests...")
    
    try:
        # Test imports
        from imf_core import log_normal_pdf, generate_log_normal_population, powerlaw_mle_with_bounds
        from monte_carlo import apply_observation_cutoff, run_single_simulation
        print("✓ All imports successful")
        
        # Test basic functionality
        np.random.seed(42)
        
        # Test population generation
        masses = generate_log_normal_population(1000)
        assert len(masses) == 1000
        assert np.all(masses >= 0)
        print("✓ Population generation works")
        
        # Test cutoff
        masses_cut = apply_observation_cutoff(masses, 0.3, 0.8)
        assert np.all(masses_cut >= 0.3)
        assert np.all(masses_cut <= 0.8)
        print("✓ Cutoff function works")
        
        # Test single simulation
        result = run_single_simulation(0.3, 1000, random_seed=42)
        assert 'alpha' in result
        assert 'n_observable' in result
        print("✓ Single simulation works")
        
        # Test MLE
        if len(masses_cut) > 1:
            alpha = powerlaw_mle_with_bounds(masses_cut, 0.3, 0.8)
            assert np.isfinite(alpha)
            print("✓ Power-law MLE works")
        
        print("All basic tests passed!\n")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False


if __name__ == "__main__":
    # Run basic tests first
    if run_simple_tests():
        # Run the main simulation
        results = main()
    else:
        print("Tests failed. Please fix issues before running main simulation.")