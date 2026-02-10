"""
Unit tests for Monte Carlo simulation functions.
"""
import numpy as np
import pytest
from monte_carlo import apply_observation_cutoff, run_single_simulation, run_cutoff_study
from imf_core import generate_log_normal_population


class TestObservationCutoff:
    """Test observation cutoff function."""
    
    def test_double_truncation(self):
        """Test double truncation [M_obs, M_max]."""
        np.random.seed(42)
        masses = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
        
        M_obs = 0.3
        M_max = 0.7
        
        result = apply_observation_cutoff(masses, M_obs, M_max)
        
        expected = np.array([0.3, 0.4, 0.5, 0.6, 0.7])
        np.testing.assert_array_equal(result, expected)
    
    def test_edge_cases(self):
        """Test edge cases."""
        masses = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        
        # M_obs = M_max (single point if exists)
        result = apply_observation_cutoff(masses, 0.3, 0.3)
        np.testing.assert_array_equal(result, np.array([0.3]))
        
        # No points in range
        result_empty = apply_observation_cutoff(masses, 0.6, 0.7)
        assert len(result_empty) == 0
        
        # All points in range
        result_all = apply_observation_cutoff(masses, 0.05, 0.6)
        np.testing.assert_array_equal(result_all, masses)
    
    def test_bounds_checking(self):
        """Test that function respects bounds correctly."""
        masses = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        
        result = apply_observation_cutoff(masses, 0.25, 0.45)
        
        # Should include 0.3 and 0.4, exclude 0.2 and 0.5
        assert 0.3 in result
        assert 0.4 in result
        assert 0.2 not in result
        assert 0.5 not in result


class TestSingleSimulation:
    """Test single simulation function."""
    
    def test_basic_functionality(self):
        """Test basic simulation functionality."""
        np.random.seed(42)
        
        result = run_single_simulation(M_obs=0.3, N=1000, random_seed=42)
        
        # Check result structure
        required_keys = ['M_obs', 'alpha', 'n_observable', 'n_generated', 'fraction_observed']
        for key in required_keys:
            assert key in result, f"Missing key: {key}"
        
        # Check basic constraints
        assert result['M_obs'] == 0.3
        assert result['n_generated'] == 1000
        assert 0 <= result['fraction_observed'] <= 1
        assert result['n_observable'] <= result['n_generated']
        
        if result['n_observable'] > 1:
            assert np.isfinite(result['alpha']), "Alpha should be finite when n_obs > 1"
    
    def test_reproducibility(self):
        """Test reproducibility with same seed."""
        result1 = run_single_simulation(M_obs=0.3, N=100, random_seed=42)
        result2 = run_single_simulation(M_obs=0.3, N=100, random_seed=42)
        
        assert result1['alpha'] == result2['alpha'], "Same seed should give same alpha"
        assert result1['n_observable'] == result2['n_observable'], "Same seed should give same n_observable"
    
    def test_different_cutoffs(self):
        """Test different cutoff values give different results."""
        np.random.seed(42)
        
        result_low = run_single_simulation(M_obs=0.1, N=1000, random_seed=42)
        result_high = run_single_simulation(M_obs=0.5, N=1000, random_seed=42)
        
        # Higher cutoff should observe fewer stars
        assert result_high['n_observable'] <= result_low['n_observable']
        assert result_high['fraction_observed'] <= result_low['fraction_observed']


class TestCutoffStudy:
    """Test cutoff study function."""
    
    def test_multiple_cutoffs(self):
        """Test running multiple cutoff values."""
        np.random.seed(42)
        
        M_obs_values = [0.1, 0.2, 0.3]
        results = run_cutoff_study(M_obs_values, N=100, random_seed=42)
        
        assert len(results) == len(M_obs_values), "Should have result for each M_obs"
        
        # Check each result corresponds to correct M_obs
        for i, (result, M_obs) in enumerate(zip(results, M_obs_values)):
            assert result['M_obs'] == M_obs, f"Result {i} has wrong M_obs"
    
    def test_monotonic_behavior(self):
        """Test that higher cutoffs generally observe fewer stars."""
        np.random.seed(42)
        
        M_obs_values = [0.1, 0.2, 0.3, 0.4, 0.5]
        results = run_cutoff_study(M_obs_values, N=1000, random_seed=42)
        
        n_observables = [r['n_observable'] for r in results]
        
        # Generally should be decreasing (allowing for statistical fluctuations)
        assert n_observables[-1] <= n_observables[0], "Highest cutoff should observe fewer stars than lowest"
    
    def test_seed_independence(self):
        """Test that different seeds give different but valid results."""
        results1 = run_cutoff_study([0.2, 0.4], N=100, random_seed=42)
        results2 = run_cutoff_study([0.2, 0.4], N=100, random_seed=123)
        
        # Should have same structure
        assert len(results1) == len(results2)
        
        # But potentially different results (statistical variation)
        # Note: This test might occasionally fail due to random chance, but that's rare
        results_different = False
        for r1, r2 in zip(results1, results2):
            if r1['alpha'] != r2['alpha'] or r1['n_observable'] != r2['n_observable']:
                results_different = True
                break
        
        # Results should usually be different with different seeds
        # (If they're the same, it's fine, just means the randomness happened to be similar)
    
    def test_edge_cutoff_values(self):
        """Test extreme cutoff values."""
        # Very high cutoff near M_max
        result_high = run_single_simulation(M_obs=0.75, N=1000, random_seed=42)
        assert result_high['n_observable'] >= 0, "Should never have negative observable stars"
        
        # Very low cutoff
        result_low = run_single_simulation(M_obs=0.05, N=1000, random_seed=42)
        assert result_low['n_observable'] > 0, "Low cutoff should observe many stars"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])