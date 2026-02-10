"""
Monte Carlo simulation functions for the IMF bias experiment.
"""
import numpy as np
from imf_core import generate_log_normal_population, powerlaw_mle_with_bounds


def apply_observation_cutoff(masses, M_obs, M_max=0.8):
    """
    Apply observational cutoff to stellar masses.
    
    Parameters:
    -----------
    masses : array_like
        Original stellar masses
    M_obs : float
        Observable minimum mass (lower cutoff)
    M_max : float
        Maximum mass for observation (upper cutoff)
    
    Returns:
    --------
    observable_masses : ndarray
        Masses in range [M_obs, M_max]
    """
    masses = np.asarray(masses)
    
    # Apply double truncation: [M_obs, M_max]
    observable_masses = masses[(masses >= M_obs) & (masses <= M_max)]
    
    return observable_masses


def run_single_simulation(M_obs, N=10**6, M_max=0.8, m_c=0.20, sigma=0.69, m_max_gen=1.0, random_seed=None):
    """
    Run a single simulation experiment for a given observational cutoff.
    
    Parameters:
    -----------
    M_obs : float
        Observable minimum mass
    N : int
        Number of stars to generate (default: 10^6)
    M_max : float
        Maximum observable mass (default: 0.8)
    m_c : float
        Characteristic mass for log-normal IMF (default: 0.20)
    sigma : float
        Width parameter for log-normal IMF (default: 0.69)
    m_max_gen : float
        Maximum mass for generation (default: 1.0)
    random_seed : int, optional
        Random seed for reproducibility
    
    Returns:
    --------
    results : dict
        Dictionary containing:
        - 'M_obs': observational cutoff
        - 'alpha': inferred power-law slope
        - 'n_observable': number of observable stars
        - 'n_generated': total number generated
        - 'fraction_observed': fraction of stars observable
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    # Generate population from log-normal IMF
    masses = generate_log_normal_population(N, m_c, sigma, m_max_gen)
    
    # Apply observational cutoff
    observable_masses = apply_observation_cutoff(masses, M_obs, M_max)
    
    # Fit power-law to observable sample
    if len(observable_masses) > 1:
        alpha = powerlaw_mle_with_bounds(observable_masses, M_obs, M_max)
    else:
        alpha = np.nan
    
    # Compile results
    results = {
        'M_obs': M_obs,
        'alpha': alpha,
        'n_observable': len(observable_masses),
        'n_generated': N,
        'fraction_observed': len(observable_masses) / N
    }
    
    return results


def run_cutoff_study(M_obs_values, N=10**6, M_max=0.8, m_c=0.20, sigma=0.69, m_max_gen=1.0, random_seed=None):
    """
    Run the complete cutoff study for multiple observational limits.
    
    Parameters:
    -----------
    M_obs_values : array_like
        Array of observational cutoff values to test
    N : int
        Number of stars to generate for each cutoff (default: 10^6)
    M_max : float
        Maximum observable mass (default: 0.8)
    m_c : float
        Characteristic mass for log-normal IMF (default: 0.20)
    sigma : float
        Width parameter for log-normal IMF (default: 0.69)
    m_max_gen : float
        Maximum mass for generation (default: 1.0)
    random_seed : int, optional
        Random seed for reproducibility
    
    Returns:
    --------
    results : list
        List of result dictionaries for each M_obs value
    """
    if random_seed is not None:
        np.random.seed(random_seed)
    
    results = []
    
    for i, M_obs in enumerate(M_obs_values):
        # Use different seed for each cutoff to avoid correlations
        seed = None if random_seed is None else random_seed + i
        
        result = run_single_simulation(
            M_obs=M_obs, 
            N=N, 
            M_max=M_max, 
            m_c=m_c, 
            sigma=sigma, 
            m_max_gen=m_max_gen,
            random_seed=seed
        )
        
        results.append(result)
        
        # Print progress
        print(f"M_obs = {M_obs:.2f}: α = {result['alpha']:.3f}, N_obs = {result['n_observable']}")
    
    return results