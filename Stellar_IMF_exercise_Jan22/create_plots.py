#!/usr/bin/env python3
"""
Create visualizations of IMF simulation results
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load results
df = pd.read_csv('results/full_experiment_quick.csv')

# Create analysis
analysis = []
for method in df['fit_method'].unique():
    method_data = df[df['fit_method'] == method]
    for N in sorted(method_data['N'].unique()):
        n_data = method_data[method_data['N'] == N]
        if len(n_data) > 0:
            analysis.append({
                'method': method,
                'N': N,
                'mean_alpha': np.mean(n_data['alpha_fit']),
                'std_alpha': np.std(n_data['alpha_fit']),
                'bias': np.mean(n_data['alpha_fit'] - n_data['alpha_true']),
                'count': len(n_data)
            })

analysis_df = pd.DataFrame(analysis)

# Create plots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

# Precision vs N
for method in analysis_df['method'].unique():
    method_data = analysis_df[analysis_df['method'] == method]
    ax1.loglog(method_data['N'], method_data['std_alpha'], 'o-', 
              label=f'{method.upper()}', markersize=6, linewidth=2)

# Theoretical scaling
N_theory = np.logspace(1, 3, 100)
sigma_theory = 0.5 / np.sqrt(N_theory)
ax1.loglog(N_theory, sigma_theory, 'k--', alpha=0.5, label=r'$\propto N^{-1/2}$')
ax1.set_xlabel('Cluster Size N')
ax1.set_ylabel('Precision $\sigma_\\alpha$')
ax1.set_title('Recovery Precision vs Cluster Size')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Bias vs N
for method in analysis_df['method'].unique():
    method_data = analysis_df[analysis_df['method'] == method]
    ax2.semilogx(method_data['N'], method_data['bias'], 'o-', 
                 label=f'{method.upper()}', markersize=6, linewidth=2)

ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
ax2.set_xlabel('Cluster Size N')
ax2.set_ylabel('Bias $\\langle\\alpha_{fit}\\rangle - \\alpha_{true}$')
ax2.set_title('Recovery Bias vs Cluster Size')
ax2.legend()
ax2.grid(True, alpha=0.3)

# Method comparison at N=500
n500_data = analysis_df[analysis_df['N'] == 500]
ax3.bar(n500_data['method'], n500_data['std_alpha'])
ax3.set_ylabel('Precision $\sigma_\\alpha$')
ax3.set_title('Precision Comparison (N=500)')
ax3.tick_params(axis='x', rotation=45)

# Bias comparison at N=500
ax4.bar(n500_data['method'], np.abs(n500_data['bias']))
ax4.set_ylabel('|Bias|')
ax4.set_title('Bias Comparison (N=500)')
ax4.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('results/imf_analysis_quick.png', dpi=300, bbox_inches='tight')
print('Analysis plot saved to results/imf_analysis_quick.png')
plt.show()

# Print summary statistics
print('\n=== DETAILED ANALYSIS ===')
for method in analysis_df['method'].unique():
    method_data = analysis_df[analysis_df['method'] == method]
    print(f'\n{method.upper()} Method:')
    
    # Calculate scaling
    if len(method_data) > 2:
        logN = np.log10(method_data['N'])
        logp = np.log10(method_data['std_alpha'])
        slope, intercept, r_value, p_value, std_err = stats.linregress(logN, logp)
        print(f'  Precision scaling: σ ∝ N^{slope:.2f} (expected: -0.50)')
        print(f'  Scaling R² = {r_value**2:.3f}')
    
    # Show convergence to true value
    bias_at_10 = method_data[method_data['N'] == 10]['bias'].iloc[0]
    bias_at_500 = method_data[method_data['N'] == 500]['bias'].iloc[0]
    print(f'  Bias improvement: {bias_at_10:+.3f} → {bias_at_500:+.3f}')
    
    # Precision improvement
    prec_at_10 = method_data[method_data['N'] == 10]['std_alpha'].iloc[0]
    prec_at_500 = method_data[method_data['N'] == 500]['std_alpha'].iloc[0]
    print(f'  Precision improvement: {prec_at_10:.3f} → {prec_at_500:.3f} ({prec_at_10/prec_at_500:.1f}x better)')

# Create histogram of fitted values for largest N
plt.figure(figsize=(10, 6))
n500_mle = df[(df['N'] == 500) & (df['fit_method'] == 'mle')]['alpha_fit']
n500_ls = df[(df['N'] == 500) & (df['fit_method'] == 'ls')]['alpha_fit']

plt.hist(n500_mle, bins=20, alpha=0.7, label='MLE', density=True)
plt.hist(n500_ls, bins=20, alpha=0.7, label='Least Squares', density=True)
plt.axvline(x=2.35, color='red', linestyle='--', label='True value (α = 2.35)')
plt.xlabel('Fitted α')
plt.ylabel('Density')
plt.title('Distribution of Fitted α Values (N=500)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.savefig('results/alpha_distribution_n500.png', dpi=300, bbox_inches='tight')
plt.show()
print('Distribution plot saved to results/alpha_distribution_n500.png')