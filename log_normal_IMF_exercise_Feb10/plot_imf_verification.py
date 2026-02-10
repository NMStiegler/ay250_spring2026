"""
Script to generate and verify the log-normal IMF distribution.
"""
import numpy as np
import matplotlib.pyplot as plt
from imf_core import generate_log_normal_population, log_normal_pdf


def plot_imf_distribution():
    """Plot the generated log-normal IMF distribution."""
    
    # Parameters
    N = 10**6
    m_c = 0.20  # Characteristic mass
    sigma = 0.69  # Width parameter
    
    print("Generating log-normal IMF sample...")
    np.random.seed(42)
    masses = generate_log_normal_population(N, m_c, sigma)
    
    # Create histogram
    bins = np.arange(0, 1.05, 0.05)  # 0.05 solar mass bins
    hist, edges = np.histogram(masses, bins=bins, density=True)
    
    # Plot setup
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Plot histogram (use log-scale for x-axis)
    bin_centers = (edges[:-1] + edges[1:]) / 2
    mask = bin_centers > 0  # Remove zero for log scale
    ax.bar(bin_centers[mask], hist[mask], width=0.04, alpha=0.7, 
           color='skyblue', edgecolor='black', label='Generated Sample')
    
    # Overlay theoretical log-normal PDF
    m_theory = np.linspace(0.01, 1.0, 1000)
    pdf_theory = log_normal_pdf(m_theory, m_c, sigma)
    ax.plot(m_theory, pdf_theory, 'r-', linewidth=2, label='Theoretical Log-Normal')
    
    # Formatting
    ax.set_xlabel('Mass (M☉)', fontsize=12)
    ax.set_ylabel('Normalized Frequency', fontsize=12)
    ax.set_title('Generated Log-Normal IMF Distribution\n(N = 10⁶, m_c = 0.20 M☉, σ = 0.69)', fontsize=14)
    ax.set_xscale('log')
    ax.grid(True, alpha=0.3)
    ax.legend()
    
    # Add statistics text
    mean_mass = np.mean(masses)
    median_mass = np.median(masses)
    std_mass = np.std(masses)
    
    stats_text = f'Sample Statistics:\nMean: {mean_mass:.3f} M☉\nMedian: {median_mass:.3f} M☉\nStd: {std_mass:.3f} M☉'
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('imf_distribution_verification.png', dpi=150, bbox_inches='tight')
    print("Saved: imf_distribution_verification.png")
    
    # Print some basic checks
    print(f"\nVerification:")
    print(f"Generated N = {len(masses):,} stars")
    print(f"Mass range: {np.min(masses):.3f} - {np.max(masses):.3f} M☉")
    print(f"Fraction in [0.1, 0.8] M☉: {np.sum((masses >= 0.1) & (masses <= 0.8)) / N:.3f}")
    print(f"Theoretical peak at m_c = {m_c} M☉")
    print(f"Sample peak at {bin_centers[np.argmax(hist)]:.3f} M☉")
    
    return masses


if __name__ == "__main__":
    masses = plot_imf_distribution()
    plt.show()