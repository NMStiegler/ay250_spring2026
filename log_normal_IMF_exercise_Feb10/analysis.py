"""
Analysis and visualization functions for the IMF bias experiment.
"""
import numpy as np
import matplotlib.pyplot as plt
from imf_core import log_normal_pdf, powerlaw_pdf


def plot_alpha_vs_cutoff_with_errors(results_list, figsize=(12, 8)):
    """
    Plot inferred power-law slope vs observational cutoff with error bars from multiple runs.
    
    Parameters:
    -----------
    results_list : list
        List of results from multiple simulation runs
        Each element is a list of result dictionaries from run_cutoff_study
    figsize : tuple
        Figure size (default: (12, 8))
    
    Returns:
    --------
    fig, ax : matplotlib figure and axis objects
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Get M_obs values from first run
    M_obs_values = [r['M_obs'] for r in results_list[0]]
    n_runs = len(results_list)
    
    # Collect alpha values for each M_obs
    alpha_matrix = []
    n_observable_matrix = []
    
    for run_results in results_list:
        alpha_matrix.append([r['alpha'] for r in run_results])
        n_observable_matrix.append([r['n_observable'] for r in run_results])
    
    alpha_matrix = np.array(alpha_matrix)  # shape: (n_runs, n_M_obs)
    n_observable_matrix = np.array(n_observable_matrix)
    
    # Calculate statistics
    alpha_mean = np.mean(alpha_matrix, axis=0)
    alpha_std = np.std(alpha_matrix, axis=0)
    n_mean = np.mean(n_observable_matrix, axis=0)
    n_std = np.std(n_observable_matrix, axis=0)
    
    # Plot main result with error bars
    line = ax.errorbar(M_obs_values, alpha_mean, yerr=alpha_std, 
                      fmt='bo-', linewidth=2, markersize=8, capsize=5, capthick=2,
                      label='Inferred α (mean ± σ)')
    
    # Add reference lines
    ax.axhline(y=2.35, color='red', linestyle='--', alpha=0.7, label='Salpeter α = 2.35')
    ax.axvline(x=0.20, color='green', linestyle='--', alpha=0.7, label='Characteristic mass m_c = 0.20')
    
    # Add secondary y-axis for number of observable stars (scientific notation)
    ax2 = ax.twinx()
    bars = ax2.bar(M_obs_values, n_mean, alpha=0.3, color='gray', width=0.03, label='N_observable')
    
    # Add error bars to bar chart
    ax2.errorbar(M_obs_values, n_mean, yerr=n_std, fmt='none', color='darkgray', capsize=3, capthick=1)
    
    # Formatting
    ax.set_xlabel('Observational Lower Mass Limit M_obs (M☉)', fontsize=12)
    ax.set_ylabel('Inferred Power-Law Slope α', fontsize=12, color='blue')
    ax2.set_ylabel('Number of Observable Stars', fontsize=12, color='gray')
    ax.set_title(f'Bias in Power-Law IMF Fitting Due to Observational Cutoffs\n({n_runs} Monte Carlo Repetitions, N = 10⁶ per run)', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    # Set y-axis colors
    ax.tick_params(axis='y', labelcolor='blue')
    ax2.tick_params(axis='y', labelcolor='gray')
    
    # Format y-axis for scientific notation
    ax2.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    # Add text annotations with uncertainties
    for i, (M_obs, alpha_mean_val, alpha_std_val, n_mean_val) in enumerate(zip(M_obs_values, alpha_mean, alpha_std, n_mean)):
        ax.annotate(f'{alpha_mean_val:.2f}±{alpha_std_val:.2f}', (M_obs, alpha_mean_val), xytext=(5, 5), 
                   textcoords='offset points', fontsize=9, alpha=0.8)
    
    plt.tight_layout()
    return fig, ax


def plot_alpha_vs_cutoff(results, figsize=(10, 6)):
    """
    Plot inferred power-law slope vs observational cutoff.
    
    Parameters:
    -----------
    results : list
        List of result dictionaries from run_cutoff_study
    figsize : tuple
        Figure size (default: (10, 6))
    
    Returns:
    --------
    fig, ax : matplotlib figure and axis objects
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # Extract data
    M_obs_values = [r['M_obs'] for r in results]
    alpha_values = [r['alpha'] for r in results]
    n_observable = [r['n_observable'] for r in results]
    
    # Plot main result
    line = ax.plot(M_obs_values, alpha_values, 'bo-', linewidth=2, markersize=8, label='Inferred α')
    
    # Add reference lines
    ax.axhline(y=2.35, color='red', linestyle='--', alpha=0.7, label='Salpeter α = 2.35')
    ax.axvline(x=0.20, color='green', linestyle='--', alpha=0.7, label='Characteristic mass m_c = 0.20')
    
    # Add secondary y-axis for number of observable stars
    ax2 = ax.twinx()
    bars = ax2.bar(M_obs_values, n_observable, alpha=0.3, color='gray', width=0.03, label='N_observable')
    
    # Formatting
    ax.set_xlabel('Observational Lower Mass Limit M_obs (M☉)', fontsize=12)
    ax.set_ylabel('Inferred Power-Law Slope α', fontsize=12, color='blue')
    ax2.set_ylabel('Number of Observable Stars', fontsize=12, color='gray')
    ax.set_title('Bias in Power-Law IMF Fitting Due to Observational Cutoffs', fontsize=14)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    
    # Set y-axis colors
    ax.tick_params(axis='y', labelcolor='blue')
    ax2.tick_params(axis='y', labelcolor='gray')
    
    # Format y-axis for scientific notation
    ax2.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
    
    # Add text annotations
    for i, (M_obs, alpha, n_obs) in enumerate(zip(M_obs_values, alpha_values, n_observable)):
        ax.annotate(f'{alpha:.2f}', (M_obs, alpha), xytext=(5, 5), 
                   textcoords='offset points', fontsize=9, alpha=0.8)
    
    plt.tight_layout()
    return fig, ax


def plot_imf_comparison(masses, fit_alpha, M_obs, M_max=0.8, m_c=0.20, sigma=0.69, figsize=(12, 8)):
    """
    Plot comparison between true log-normal IMF and fitted power-law.
    
    Parameters:
    -----------
    masses : array_like
        Observable stellar masses
    fit_alpha : float
        Fitted power-law slope
    M_obs : float
        Observational lower mass cutoff
    M_max : float
        Maximum observable mass (default: 0.8)
    m_c : float
        Characteristic mass for log-normal (default: 0.20)
    sigma : float
        Width parameter for log-normal (default: 0.69)
    figsize : tuple
        Figure size (default: (12, 8))
    
    Returns:
    --------
    fig, axes : matplotlib figure and axis objects
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)
    
    # Mass range for plotting
    m_plot = np.linspace(0.01, 1.0, 1000)
    
# Top left: PDF comparison
    ax1 = axes[0, 0]
    lognormal_vals = log_normal_pdf(m_plot, m_c, sigma)
    # Normalize log-normal over the fitting range for fair comparison
    mask = (m_plot >= M_obs) & (m_plot <= M_max)
    lognormal_integral = np.trapz(lognormal_vals[mask], m_plot[mask])
    lognormal_normalized = lognormal_vals / lognormal_integral
    
    powerlaw_vals = powerlaw_pdf(m_plot, fit_alpha, M_obs, M_max)  # Use normalized power-law
    ax1.axvspan(M_obs, M_max, alpha=0.2, color='yellow', label='Observable Range')
    ax1.set_xlabel('Mass (M☉)')
    ax1.set_ylabel('PDF')
    ax1.set_title('PDF Comparison (Log-Log Scale)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Top right: Histogram with fitted distributions
    ax2 = axes[0, 1]
    # Create histogram with log-log scale
    ax2.hist(masses, bins=30, density=True, alpha=0.7, color='skyblue', edgecolor='black', label='Data')
    ax2.loglog(m_plot, lognormal_normalized, 'b-', label='True Log-Normal (normalized)', linewidth=2)
    ax2.loglog(m_plot, powerlaw_vals, 'r--', label=f'Fitted Power-Law (α={fit_alpha:.2f})', linewidth=2)
    ax2.set_xlabel('Mass (M☉)')
    ax2.set_ylabel('Normalized Frequency')
    ax2.set_title('Histogram with Fitted Models (Log-Log Scale)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim([M_obs - 0.05, M_max + 0.05])
    
    # Bottom left: Log-log plot
    ax3 = axes[1, 0]
    mask = (m_plot >= M_obs) & (m_plot <= M_max)
    ax3.loglog(m_plot[mask], lognormal_normalized[mask], 'b-', label='True Log-Normal (normalized)', linewidth=2)
    ax3.loglog(m_plot[mask], powerlaw_vals[mask], 'r--', label=f'Fitted Power-Law (α={fit_alpha:.2f})', linewidth=2)
    ax3.set_xlabel('Mass (M☉)')
    ax3.set_ylabel('PDF')
    ax3.set_title('Log-Log Plot (Observable Range)')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Bottom right: Residuals
    ax4 = axes[1, 1]
    lognormal_interp = np.interp(m_plot[mask], m_plot[mask], lognormal_normalized[mask])
    powerlaw_interp = np.interp(m_plot[mask], m_plot[mask], powerlaw_vals[mask])
    residuals = (powerlaw_interp - lognormal_interp) / lognormal_interp * 100
    
    ax4.plot(m_plot[mask], residuals, 'g-', linewidth=2)
    ax4.axhline(y=0, color='black', linestyle='--', alpha=0.5)
    ax4.set_xlabel('Mass (M☉)')
    ax4.set_ylabel('Residual (%)')
    ax4.set_title('Power-Law Minus Log-Normal (%)')
    ax4.grid(True, alpha=0.3)
    
    plt.suptitle(f'IMF Fitting Analysis (M_obs = {M_obs:.2f}, N = {len(masses)})', fontsize=14)
    plt.tight_layout()
    
    return fig, axes


def print_summary_statistics(results):
    """
    Print summary statistics for the cutoff study.
    
    Parameters:
    -----------
    results : list
        List of result dictionaries from run_cutoff_study
    """
    print("\n" + "="*60)
    print("IMF BIAS STUDY SUMMARY")
    print("="*60)
    
    print(f"True underlying IMF: Log-normal with m_c = 0.20 M☉, σ = 0.69")
    print(f"Observational range: [M_obs, 0.8] M☉")
    print(f"Generated N = 10^6 stars for each cutoff")
    print("-"*60)
    
    print(f"{'M_obs (M☉)':<12} {'α (slope)':<10} {'N_obs':<10} {'% observed':<12}")
    print("-"*60)
    
    for r in results:
        print(f"{r['M_obs']:<12.2f} {r['alpha']:<10.3f} {r['n_observable']:<10d} {r['fraction_observed']*100:<12.1f}")
    
    print("-"*60)
    
    # Calculate some statistics
    valid_alphas = [r['alpha'] for r in results if not np.isnan(r['alpha'])]
    if valid_alphas:
        print(f"α range: {min(valid_alphas):.3f} - {max(valid_alphas):.3f}")
        print(f"α mean: {np.mean(valid_alphas):.3f} ± {np.std(valid_alphas):.3f}")
    
    print("="*60 + "\n")