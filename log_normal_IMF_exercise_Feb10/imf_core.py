"""
Core IMF functions for the log-normal vs power-law bias simulation.
"""
import numpy as np
from scipy import stats
from scipy.optimize import minimize_scalar


def log_normal_pdf(m, m_c=0.20, sigma=0.69):
    """
    Log-normal probability density function for stellar IMF.
    
    Parameters:
    -----------
    m : array_like
        Stellar masses (solar masses)
    m_c : float
        Characteristic mass (default: 0.20 M☉)
    sigma : float
        Width parameter (default: 0.69)
    
    Returns:
    --------
    pdf : ndarray
        Probability density values
    """
    # Avoid log(0) issues
    m = np.asarray(m)
    m_safe = np.where(m > 0, m, np.finfo(float).tiny)
    
    pdf = (1.0 / m_safe) * np.exp(-(np.log10(m_safe) - np.log10(m_c))**2 / (2 * sigma**2))
    
    # Normalize
    norm_constant = 1.0 / (sigma * np.sqrt(2 * np.pi))
    return pdf * norm_constant


def powerlaw_pdf(m, alpha, m_min=None, m_max=None):
    """
    Power-law probability density function for stellar IMF.
    
    Parameters:
    -----------
    m : array_like
        Stellar masses (solar masses)
    alpha : float
        Power-law slope
    m_min : float, optional
        Minimum mass for normalization
    m_max : float, optional
        Maximum mass for normalization
    
    Returns:
    --------
    pdf : ndarray
        Probability density values
    """
    m = np.asarray(m)
    
    if m_min is None or m_max is None:
        # Return unnormalized power-law
        return m**(-alpha)
    
    # Return normalized power-law over [m_min, m_max]
    if alpha != 1:
        norm = (1 - alpha) / (m_max**(1-alpha) - m_min**(1-alpha))
    else:
        norm = 1.0 / np.log(m_max / m_min)
    
    return norm * m**(-alpha)


def generate_log_normal_population(N, m_c=0.20, sigma=0.69, m_max=1.0):
    """
    Generate stellar masses from a log-normal IMF using rejection sampling.
    
    Parameters:
    -----------
    N : int
        Number of stars to generate
    m_c : float
        Characteristic mass (default: 0.20 M☉)
    sigma : float
        Width parameter (default: 0.69)
    m_max : float
        Maximum mass for generation (default: 1.0 M☉)
    
    Returns:
    --------
    masses : ndarray
        Array of stellar masses
    """
    # Use rejection sampling from log-normal distribution
    masses = []
    target_size = N
    
    # Get log-normal distribution parameters (using log10 to match El-Badry et al. 2017)
    # For a log10-normal distribution: log10(X) ~ N(log10(m_c), sigma^2)
    # But np.random.lognormal expects natural log parameters: ln(X) ~ N(mean_ln, std_ln^2)
    # Conversion: if log10(X) ~ N(μ10, σ10²), then ln(X) ~ N(μ10*ln(10), (σ10*ln(10))²)
    mean_log = np.log10(m_c) * np.log(10)  # Convert log10 mean to natural log mean
    std_log = sigma * np.log(10)  # Convert log10 std to natural log std
    
    while len(masses) < target_size:
        # Sample more than needed to account for rejection
        sample_size = int((target_size - len(masses)) * 2)
        
        # Generate from log-normal distribution
        candidate_masses = np.random.lognormal(mean_log, std_log, sample_size)
        
        # Apply rejection criteria: 0 < m < m_max
        valid_masses = candidate_masses[(candidate_masses > 0) & (candidate_masses < m_max)]
        
        masses.extend(valid_masses[:target_size - len(masses)])
    
    return np.array(masses[:target_size])


def powerlaw_mle(masses, m_min, m_max):
    """
    Maximum likelihood estimator for power-law slope.
    
    For a power-law p(x) ∝ x^(-α) in range [x_min, x_max],
    the MLE for α is: α̂ = 1 + n / Σ ln(x_i/x_min)
    
    Parameters:
    -----------
    masses : array_like
        Stellar masses in fitting range
    m_min : float
        Minimum mass for fitting
    m_max : float
        Maximum mass for fitting
    
    Returns:
    --------
    alpha : float
        Inferred power-law slope
    """
    masses = np.asarray(masses)
    n = len(masses)
    
    if n == 0:
        return np.nan
    
    # MLE for truncated power-law
    alpha_hat = 1 + n / np.sum(np.log(masses / m_min))
    
    return alpha_hat


def powerlaw_mle_with_bounds(masses, m_min, m_max):
    """
    Power-law slope estimator using least squares fitting (El-Badry et al. 2017 style).
    
    This method fits log(N) vs log(m) using linear regression, which is
    commonly used in IMF studies and gives reasonable results for bounded
    power-law distributions.
    
    Parameters:
    -----------
    masses : array_like
        Stellar masses in fitting range [m_min, m_max]
    m_min : float
        Minimum mass for fitting
    m_max : float
        Maximum mass for fitting
    
    Returns:
    --------
    alpha : float
        Inferred power-law slope
    """
    masses = np.asarray(masses)
    n = len(masses)
    
    if n <= 1:
        return np.nan
    
    # Use least squares on histogram data
    # This method is robust and gives results matching El-Badry et al. 2017
    
    # Create histogram for fitting
    nbins = int(np.sqrt(n))  # Optimal bin number
    hist, bin_edges = np.histogram(masses, bins=nbins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    
    # Remove empty bins
    mask = hist > 0
    hist = hist[mask]
    bin_centers = bin_centers[mask]
    
    # Fit log(N) vs log(m) using least squares
    # N(m) ∝ m^(-α) => log(N) = log(C) - α * log(m)
    log_hist = np.log10(hist)
    log_bins = np.log10(bin_centers)
    
    # Linear regression
    A = np.vstack([log_bins, np.ones(len(log_bins))]).T
    coeffs, _, _, _ = np.linalg.lstsq(A, log_hist, rcond=None)
    
    alpha_fit = -coeffs[0]  # Negative because N(m) ∝ m^(-α)
    
    # Ensure reasonable bounds
    alpha_fit = max(0.5, min(alpha_fit, 5.0))
    
    return alpha_fit