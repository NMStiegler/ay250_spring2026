#!/usr/bin/env python3
"""
Analysis and Visualization Pipeline for Stellar IMF Monte Carlo Simulation
Creates plots and statistical analysis from simulation results
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import argparse
from scipy import stats


class IMFAnalysis:
    def __init__(self):
        plt.style.use('default')
        sns.set_palette("husl")
        
    def load_results(self, filename):
        """Load simulation results from CSV file"""
        return pd.read_csv(f"results/{filename}")
    
    def plot_precision_vs_cluster_size(self, results_df, save_path=None):
        """Plot recovery precision vs cluster size"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Precision plot
        for method in results_df['fit_method'].unique():
            method_data = results_df[results_df['fit_method'] == method]
            precision_by_N = []
            N_values = []
            
            for N in sorted(method_data['N'].unique()):
                n_data = method_data[method_data['N'] == N]
                if len(n_data) > 0:
                    precision_by_N.append(np.std(n_data['alpha_fit']))
                    N_values.append(N)
            
            if len(precision_by_N) > 0:
                ax1.loglog(N_values, precision_by_N, 'o-', 
                          label=f"{method.upper()}", markersize=6, linewidth=2)
        
        # Theoretical 1/sqrt(N) scaling
        N_theory = np.logspace(1, 4, 100)
        sigma_theory = 0.5 / np.sqrt(N_theory)  # Normalized for visibility
        ax1.loglog(N_theory, sigma_theory, 'k--', alpha=0.5, 
                  label=r'$\propto N^{-1/2}$', linewidth=1)
        
        ax1.set_xlabel('Cluster Size N')
        ax1.set_ylabel('Precision $\\sigma_\\alpha$')
        ax1.set_title('Recovery Precision vs Cluster Size')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Bias plot
        for method in results_df['fit_method'].unique():
            method_data = results_df[results_df['fit_method'] == method]
            bias_by_N = []
            N_values = []
            bias_err = []
            
            for N in sorted(method_data['N'].unique()):
                n_data = method_data[method_data['N'] == N]
                if len(n_data) > 0:
                    bias = np.mean(n_data['alpha_fit']) - self.get_true_alpha(n_data)
                    bias_by_N.append(bias)
                    N_values.append(N)
                    bias_err.append(stats.sem(n_data['alpha_fit']))
            
            if len(bias_by_N) > 0:
                ax2.errorbar(N_values, bias_by_N, yerr=bias_err, 
                           fmt='o-', label=f"{method.upper()}", 
                           markersize=6, linewidth=2, capsize=3)
        
        ax2.axhline(y=0, color='k', linestyle='--', alpha=0.5)
        ax2.set_xscale('log')
        ax2.set_xlabel('Cluster Size N')
        ax2.set_ylabel('Bias $\\langle\\alpha_{fit}\\rangle - \\alpha_{true}$')
        ax2.set_title('Recovery Bias vs Cluster Size')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_method_comparison(self, analysis_df, save_path=None):
        """Plot method comparison bar charts"""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
        
        # Prepare data for largest N value
        max_N = analysis_df['N'].max()
        comparison_data = analysis_df[analysis_df['N'] == max_N]
        
        # Precision comparison
        ax1.bar(comparison_data['method'], comparison_data['std_alpha'])
        ax1.set_ylabel('Precision $\\sigma_\\alpha$')
        ax1.set_title(f'Precision Comparison (N={max_N})')
        ax1.tick_params(axis='x', rotation=45)
        
        # Bias comparison
        ax2.bar(comparison_data['method'], np.abs(comparison_data['bias']))
        ax2.set_ylabel('|Bias|')
        ax2.set_title(f'Bias Comparison (N={max_N})')
        ax2.tick_params(axis='x', rotation=45)
        
        # Success rate comparison
        ax3.bar(comparison_data['method'], comparison_data['success_rate'] * 100)
        ax3.set_ylabel('Success Rate (%)')
        ax3.set_title('Convergence Success Rate')
        ax3.tick_params(axis='x', rotation=45)
        
        # Runtime comparison (if available)
        if 'runtime_ms' in comparison_data.columns:
            ax4.bar(comparison_data['method'], comparison_data['runtime_ms'])
            ax4.set_ylabel('Runtime (ms)')
            ax4.set_title('Average Runtime per Fit')
            ax4.tick_params(axis='x', rotation=45)
        else:
            ax4.text(0.5, 0.5, 'Runtime data not available', 
                    ha='center', va='center', transform=ax4.transAxes)
            ax4.set_title('Runtime Comparison')
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_mass_ratio_effects(self, results_df, save_path=None):
        """Plot effects of mass ratio on precision"""
        if 'M_ratio' not in results_df.columns:
            print("Mass ratio data not available")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        
        # Precision vs mass ratio
        for method in results_df['fit_method'].unique():
            method_data = results_df[results_df['fit_method'] == method]
            precision_by_ratio = []
            ratios = []
            
            for ratio in sorted(method_data['M_ratio'].unique()):
                r_data = method_data[method_data['M_ratio'] == ratio]
                if len(r_data) > 0:
                    precision_by_ratio.append(np.std(r_data['alpha_fit']))
                    ratios.append(ratio)
            
            if len(precision_by_ratio) > 0:
                ax1.loglog(ratios, precision_by_ratio, 'o-', 
                          label=f"{method.upper()}", markersize=6, linewidth=2)
        
        ax1.set_xlabel('Mass Ratio $M_{max}/M_{min}$')
        ax1.set_ylabel('Precision $\\sigma_\\alpha$')
        ax1.set_title('Precision vs Mass Ratio')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Success rate vs mass ratio
        for method in results_df['fit_method'].unique():
            method_data = results_df[results_df['fit_method'] == method]
            success_by_ratio = []
            ratios = []
            
            for ratio in sorted(method_data['M_ratio'].unique()):
                r_data = method_data[method_data['M_ratio'] == ratio]
                if len(r_data) > 0:
                    success_by_ratio.append(100 * len(r_data) / len(method_data[method_data['M_ratio'] == ratio]))
                    ratios.append(ratio)
            
            if len(success_by_ratio) > 0:
                ax2.semilogx(ratios, success_by_ratio, 'o-', 
                            label=f"{method.upper()}", markersize=6, linewidth=2)
        
        ax2.set_xlabel('Mass Ratio $M_{max}/M_{min}$')
        ax2.set_ylabel('Success Rate (%)')
        ax2.set_title('Success Rate vs Mass Ratio')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def plot_alpha_distributions(self, results_df, save_path=None):
        """Plot histograms of fitted alpha values for different N"""
        methods = results_df['fit_method'].unique()
        N_values = sorted(results_df['N'].unique())
        
        n_methods = len(methods)
        fig, axes = plt.subplots(n_methods, len(N_values), 
                                figsize=(4*len(N_values), 3*n_methods))
        
        if n_methods == 1:
            axes = axes.reshape(1, -1)
        
        for i, method in enumerate(methods):
            for j, N in enumerate(N_values):
                ax = axes[i, j]
                method_data = results_df[results_df['fit_method'] == method]
                n_data = method_data[method_data['N'] == N]
                
                if len(n_data) > 0:
                    ax.hist(n_data['alpha_fit'], bins=20, alpha=0.7, density=True)
                    alpha_true = n_data['alpha_true'].iloc[0]
                    ax.axvline(alpha_true, color='red', linestyle='--', 
                              label=f"$\\alpha_{{true}}$ = {alpha_true}")
                    ax.set_title(f'{method.upper()}, N={N}')
                    ax.set_xlabel('$\\alpha_{fit}$')
                    ax.set_ylabel('Density')
                    if j == 0:
                        ax.legend()
                else:
                    ax.text(0.5, 0.5, 'No data', ha='center', va='center', 
                           transform=ax.transAxes)
        
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
    
    def get_true_alpha(self, data_subset):
        """Get true alpha value from data subset"""
        return data_subset['alpha_true'].iloc[0]
    
    def generate_summary_report(self, results_df, analysis_df, save_path=None):
        """Generate a comprehensive summary report"""
        report_lines = []
        report_lines.append("# Stellar IMF Monte Carlo Simulation Results")
        report_lines.append(f"Generated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Summary statistics
        report_lines.append("## Summary Statistics")
        report_lines.append("")
        
        for method in results_df['fit_method'].unique():
            method_data = results_df[results_df['fit_method'] == method]
            report_lines.append(f"### {method.upper()} Method")
            
            total_fits = len(method_data)
            successful_fits = len(method_data[method_data['converged'] == True])
            success_rate = successful_fits / total_fits * 100
            
            report_lines.append(f"- Total fits: {total_fits}")
            report_lines.append(f"- Success rate: {success_rate:.1f}%")
            
            if successful_fits > 0:
                successful_data = method_data[method_data['converged'] == True]
                avg_bias = np.mean(successful_data['alpha_fit'] - successful_data['alpha_true'])
                avg_precision = np.mean(successful_data['alpha_uncertainty'])
                avg_runtime = np.mean(successful_data['runtime_ms'])
                
                report_lines.append(f"- Average bias: {avg_bias:.4f}")
                report_lines.append(f"- Average precision: {avg_precision:.4f}")
                report_lines.append(f"- Average runtime: {avg_runtime:.2f} ms")
            
            report_lines.append("")
        
        # Scaling analysis
        report_lines.append("## Scaling Analysis")
        report_lines.append("")
        
        for method in results_df['fit_method'].unique():
            method_data = results_df[results_df['fit_method'] == method]
            method_analysis = analysis_df[analysis_df['method'] == method]
            
            if len(method_analysis) > 1:
                N_vals = method_analysis['N'].values
                precision_vals = method_analysis['std_alpha'].values
                
                # Fit power law to precision vs N
                if len(N_vals) > 2 and np.all(precision_vals > 0):
                    logN = np.log10(N_vals)
                    logp = np.log10(precision_vals)
                    slope, intercept, r_value, p_value, std_err = stats.linregress(logN, logp)
                    
                    report_lines.append(f"### {method.upper()} Scaling")
                    report_lines.append(f"- Precision ∝ N^{slope:.2f}")
                    report_lines.append(f"- Expected scaling: N^-0.50")
                    report_lines.append(f"- R² = {r_value**2:.3f}")
                    report_lines.append("")
        
        report_text = "\n".join(report_lines)
        
        if save_path:
            with open(save_path, 'w') as f:
                f.write(report_text)
        
        return report_text
    
    def analyze_file(self, filename):
        """Complete analysis of a results file"""
        print(f"Analyzing {filename}...")
        
        results_df = self.load_results(filename)
        analysis_df = results_df.groupby(['fit_method', 'N']).agg({
            'alpha_fit': ['mean', 'std'],
            'alpha_true': 'first',
            'convergence_status': 'mean',
            'runtime_ms': 'mean'
        }).reset_index()
        
        analysis_df.columns = ['fit_method', 'N', 'mean_alpha', 'std_alpha', 
                              'alpha_true', 'success_rate', 'avg_runtime']
        analysis_df['bias'] = analysis_df['mean_alpha'] - analysis_df['alpha_true']
        
        # Generate plots
        self.plot_precision_vs_cluster_size(results_df, 
                                           save_path=f"plots/precision_vs_N_{filename.replace('.csv', '.png')}")
        
        self.plot_method_comparison(analysis_df, 
                                  save_path=f"plots/method_comparison_{filename.replace('.csv', '.png')}")
        
        if 'M_ratio' in results_df.columns:
            self.plot_mass_ratio_effects(results_df, 
                                       save_path=f"plots/mass_ratio_effects_{filename.replace('.csv', '.png')}")
        
        self.plot_alpha_distributions(results_df, 
                                    save_path=f"plots/alpha_distributions_{filename.replace('.csv', '.png')}")
        
        # Generate report
        report = self.generate_summary_report(results_df, analysis_df, 
                                             save_path=f"reports/summary_report_{filename.replace('.csv', '.md')}")
        
        print(f"Analysis complete for {filename}")
        return results_df, analysis_df, report


def main():
    parser = argparse.ArgumentParser(description='Analyze IMF simulation results')
    parser.add_argument('filename', nargs='?', help='Results CSV file to analyze')
    parser.add_argument('--all', action='store_true', help='Analyze all CSV files in results directory')
    
    args = parser.parse_args()
    
    # Create directories
    Path('plots').mkdir(exist_ok=True)
    Path('reports').mkdir(exist_ok=True)
    
    analyzer = IMFAnalysis()
    
    if args.all:
        results_files = list(Path('results').glob('*.csv'))
        for file in results_files:
            analyzer.analyze_file(file.name)
    elif args.filename:
        analyzer.analyze_file(args.filename)
    else:
        print("Please provide a filename or use --all to analyze all files")


if __name__ == "__main__":
    main()