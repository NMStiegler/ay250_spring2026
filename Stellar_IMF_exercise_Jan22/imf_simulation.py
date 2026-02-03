import numpy as np
import scipy.optimize as opt
import emcee
import pandas as pd
import time
from datetime import datetime
from tqdm import tqdm
import matplotlib.pyplot as plt
from pathlib import Path


class StellarIMFSimulation:
    def __init__(self, config=None):
        if config is None:
            self.config = {
                'alpha_true': 2.35,
                'M_min': 0.1,
                'M_max': 100.0,
                'N_values': [10, 50, 100, 500, 1000, 5000],
                'K_simulations': 1000,
                'r_ratios': [10, 100, 1000],
                'random_seed': 42
            }
        else:
            self.config = config
        
        np.random.seed(self.config['random_seed'])
        
    def generate_stellar_masses(self, N, alpha, M_min, M_max):
        """Generate stellar masses using inverse transform sampling"""
        if alpha == 1.0:
            # Special case for alpha = 1 (uniform in log space)
            log_M_min, log_M_max = np.log(M_min), np.log(M_max)
            log_masses = np.random.uniform(log_M_min, log_M_max, N)
            masses = np.exp(log_masses)
        else:
            u = np.random.random(N)
            exponent = 1.0 - alpha
            
            # Correct inverse transform sampling formula
            M_max_term = M_max**exponent
            M_min_term = M_min**exponent
            
            masses = ((M_max_term - M_min_term) * u + M_min_term)**(1.0/exponent)
            
        # Ensure masses are within bounds
        masses = np.clip(masses, M_min, M_max)
        return masses
    
    def mle_fit_powerlaw(self, masses, M_min, M_max):
        N = len(masses)
        if N < 2:
            return None, None
        
        # Ensure all masses are within bounds and > M_min
        masses = np.clip(masses, M_min + 1e-10, M_max)
        
        # MLE for bounded power law
        log_masses = np.log(masses / M_min)
        if np.any(np.isinf(log_masses)) or np.any(np.isnan(log_masses)):
            return None, None
            
        alpha_mle = 1 + N / np.sum(log_masses)
        
        if alpha_mle <= 1.0 or not np.isfinite(alpha_mle):
            return None, None
            
        sigma_alpha = (alpha_mle - 1) / np.sqrt(N)
        
        return alpha_mle, sigma_alpha
    
    def least_squares_fit(self, masses, M_min, M_max):
        N = len(masses)
        if N < 10:
            return None, None, None, None
            
        hist, bin_edges = np.histogram(masses, bins=np.logspace(np.log10(M_min), np.log10(M_max), 20))
        bin_centers = np.sqrt(bin_edges[:-1] * bin_edges[1:])
        bin_widths = bin_edges[1:] - bin_edges[:-1]
        
        mask = hist > 0
        if np.sum(mask) < 5:
            return None, None, None, None
            
        x = np.log10(bin_centers[mask])
        y = np.log10(hist[mask] / bin_widths[mask])
        
        coeffs = np.polyfit(x, y, 1)
        alpha_fit = -coeffs[0]
        
        y_pred = np.polyval(coeffs, x)
        residuals = y - y_pred
        sigma_alpha = np.sqrt(np.sum(residuals**2) / (len(residuals) - 2)) / np.sqrt(np.sum((x - np.mean(x))**2))
        
        r_squared = 1 - np.sum(residuals**2) / np.sum((y - np.mean(y))**2)
        
        return alpha_fit, sigma_alpha, r_squared, coeffs
    
    def log_prior(self, alpha, M_min, M_max):
        if 1.0 <= alpha <= 4.0:
            return 0.0
        return -np.inf
    
    def log_likelihood(self, alpha, masses, M_min, M_max):
        N = len(masses)
        if alpha <= 1.0:
            return -np.inf
            
        term = (M_max**(1-alpha) - M_min**(1-alpha))
        if term <= 0:
            return -np.inf
            
        norm = (1-alpha) / term
        log_like = N * np.log(-norm) - alpha * np.sum(np.log(masses))
        
        return log_like
    
    def log_probability(self, alpha, masses, M_min, M_max):
        lp = self.log_prior(alpha, M_min, M_max)
        if not np.isfinite(lp):
            return -np.inf
        return lp + self.log_likelihood(alpha, masses, M_min, M_max)
    
    def mcmc_fit(self, masses, M_min, M_max):
        n_walkers = 20
        n_burn = 100
        n_steps = 500
        
        alpha_guess = 2.35
        pos = alpha_guess + 1e-4 * np.random.randn(n_walkers, 1)
        
        n_dim = 1
        sampler = emcee.EnsembleSampler(n_walkers, n_dim, self.log_probability, 
                                       args=(masses, M_min, M_max))
        
        try:
            sampler.run_mcmc(pos, n_burn + n_steps, progress=False)
            samples = sampler.get_chain(discard=n_burn, thin=5, flat=True)
            
            if len(samples) < 50:
                return None, None, False
            
            alpha_fit = np.median(samples)
            sigma_alpha = np.std(samples)
            
            gelman_rubin = np.mean([np.var(sampler.get_chain()[:, i, :]) 
                                   for i in range(n_walkers)]) / np.var(samples.flatten())
            converged = gelman_rubin < 1.1
            
            return alpha_fit, sigma_alpha, converged
            
        except Exception:
            return None, None, False
    
    def fit_cluster(self, masses, M_min, M_max, methods=['mle', 'ls', 'mcmc']):
        results = {}
        
        if 'mle' in methods:
            start_time = time.time()
            alpha_mle, sigma_mle = self.mle_fit_powerlaw(masses, M_min, M_max)
            results['mle'] = {
                'alpha': alpha_mle,
                'sigma': sigma_mle,
                'runtime_ms': (time.time() - start_time) * 1000,
                'converged': alpha_mle is not None
            }
        
        if 'ls' in methods:
            start_time = time.time()
            alpha_ls, sigma_ls, r2, coeffs = self.least_squares_fit(masses, M_min, M_max)
            results['ls'] = {
                'alpha': alpha_ls,
                'sigma': sigma_ls,
                'r_squared': r2,
                'runtime_ms': (time.time() - start_time) * 1000,
                'converged': alpha_ls is not None
            }
        
        if 'mcmc' in methods:
            start_time = time.time()
            alpha_mcmc, sigma_mcmc, converged = self.mcmc_fit(masses, M_min, M_max)
            results['mcmc'] = {
                'alpha': alpha_mcmc,
                'sigma': sigma_mcmc,
                'runtime_ms': (time.time() - start_time) * 1000,
                'converged': converged
            }
        
        return results
    
    def run_simulation_cluster(self, N, M_min, M_max, K, methods=['mle', 'ls', 'mcmc']):
        alpha_true = self.config['alpha_true']
        results = []
        
        for iteration in tqdm(range(K), desc=f"N={N}"):
            masses = self.generate_stellar_masses(N, alpha_true, M_min, M_max)
            fit_results = self.fit_cluster(masses, M_min, M_max, methods)
            
            for method, result in fit_results.items():
                if result['converged']:
                    row = {
                        'iteration': iteration,
                        'N': N,
                        'M_min': M_min,
                        'M_max': M_max,
                        'M_ratio': M_max / M_min,
                        'alpha_true': alpha_true,
                        'fit_method': method,
                        'alpha_fit': result['alpha'],
                        'alpha_uncertainty': result['sigma'],
                        'convergence_status': result['converged'],
                        'timestamp': datetime.now().isoformat(),
                        'runtime_ms': result['runtime_ms']
                    }
                    
                    if method == 'ls' and 'r_squared' in result:
                        row['r_squared'] = result['r_squared']
                    
                    results.append(row)
        
        return pd.DataFrame(results)
    
    def save_results(self, df, filename):
        output_dir = Path('results')
        output_dir.mkdir(exist_ok=True)
        df.to_csv(output_dir / filename, index=False)
    
    def analyze_results(self, df):
        analysis = {}
        
        for method in df['fit_method'].unique():
            method_data = df[df['fit_method'] == method]
            
            for N in method_data['N'].unique():
                n_data = method_data[method_data['N'] == N]
                
                if len(n_data) > 0:
                    key = f"{method}_N{N}"
                    analysis[key] = {
                        'method': method,
                        'N': N,
                        'mean_alpha': np.mean(n_data['alpha_fit']),
                        'std_alpha': np.std(n_data['alpha_fit']),
                        'bias': np.mean(n_data['alpha_fit']) - self.config['alpha_true'],
                        'success_rate': len(n_data) / len(method_data[method_data['N'] == N]),
                        'count': len(n_data)
                    }
        
        return pd.DataFrame(analysis.values())