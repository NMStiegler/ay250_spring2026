"""
Unit tests for IMF core functions.
"""
import numpy as np
import pytest
from imf_core import log_normal_pdf, powerlaw_pdf, generate_log_normal_population, powerlaw_mle_with_bounds


class TestLogNormalPDF:
    """Test log-normal PDF function."""
    
    def test_normalization(self):
        """Test that log-normal PDF is properly normalized."""
        m = np.linspace(0.01, 2.0, 1000)
        pdf = log_normal_pdf(m)
        
        # Numerical integration should be close to 1
        integral = np.trapz(pdf, m)
        assert abs(integral - 1.0) < 0.01, f"PDF not normalized: {integral}"
    
    def test_peak_position(self):
        """Test that PDF peaks at characteristic mass."""
        m = np.linspace(0.01, 2.0, 1000)
        m_c = 0.20
        pdf = log_normal_pdf(m, m_c=m_c)
        
        # Peak should be near m_c
        peak_idx = np.argmax(pdf)
        peak_mass = m[peak_idx]
        assert abs(peak_mass - m_c) < 0.1, f"Peak at {peak_mass}, expected {m_c}"
    
    def test_edge_cases(self):
        """Test edge cases like m=0."""
        with pytest.warns(RuntimeWarning):
            pdf_zero = log_normal_pdf([0.0])
            assert np.isfinite(pdf_zero[0])
        
        pdf_small = log_normal_pdf([1e-10])
        assert np.isfinite(pdf_small[0])


class TestPowerlawPDF:
    """Test power-law PDF function."""
    
    def test_shape(self):
        """Test power-law shape."""
        m = np.linspace(0.1, 1.0, 100)
        alpha = 2.35
        pdf = powerlaw_pdf(m, alpha)
        
        # Should be decreasing function
        assert np.all(np.diff(pdf) <= 0), "Power-law should be decreasing"
    
    def test_alpha_dependence(self):
        """Test alpha parameter affects slope correctly."""
        m = np.array([0.2, 0.4, 0.8])
        pdf_1 = powerlaw_pdf(m, 1.5)
        pdf_3 = powerlaw_pdf(m, 3.0)
        
        # Higher alpha should give steeper decline
        ratio = pdf_3 / pdf_1
        assert np.all(np.diff(ratio) < 0), "Higher alpha should give steeper slope"


class TestPopulationGeneration:
    """Test population generation function."""
    
    def test_population_size(self):
        """Test correct population size."""
        N = 1000
        masses = generate_log_normal_population(N)
        
        assert len(masses) == N, f"Expected {N} masses, got {len(masses)}"
    
    def test_mass_range(self):
        """Test masses are within expected range."""
        N = 1000
        m_max = 1.0
        masses = generate_log_normal_population(N, m_max=m_max)
        
        assert np.all(masses >= 0), "All masses should be positive"
        assert np.all(masses <= m_max), f"All masses should be ≤ {m_max}"
    
    def test_seed_reproducibility(self):
        """Test reproducibility with seed."""
        N = 100
        seed = 42
        
        np.random.seed(seed)
        masses1 = generate_log_normal_population(N)
        
        np.random.seed(seed)
        masses2 = generate_log_normal_population(N)
        
        np.testing.assert_array_equal(masses1, masses2, "Same seed should give same results")
    
    def test_statistical_properties(self):
        """Test statistical properties for large N."""
        N = 100000
        m_c = 0.20
        sigma = 0.69
        
        masses = generate_log_normal_population(N, m_c, sigma)
        
        # For log-normal, log(m) should be normally distributed
        log_masses = np.log(masses)
        
        # Check mean and standard deviation of log(m)
        mean_log = np.mean(log_masses)
        std_log = np.std(log_masses)
        
        # Should be close to theoretical values (within ~5% for N=1e5)
        assert abs(mean_log - np.log(m_c)) < 0.1, f"Log mean: {mean_log}, expected: {np.log(m_c)}"
        assert abs(std_log - sigma) < 0.1, f"Log std: {std_log}, expected: {sigma}"


class TestPowerlawMLE:
    """Test power-law maximum likelihood estimator."""
    
    def test_synthetic_powerlaw(self):
        """Test MLE on synthetic power-law data."""
        np.random.seed(42)
        alpha_true = 2.35
        m_min, m_max = 0.2, 0.8
        
        # Generate synthetic power-law data
        n = 10000
        u = np.random.uniform(0, 1, n)
        x = ((m_max**(1-alpha_true) - m_min**(1-alpha_true)) * u + m_min**(1-alpha_true))**(1/(1-alpha_true))
        
        alpha_mle = powerlaw_mle_with_bounds(x, m_min, m_max)
        
        # Should be close to true value (within ~5%)
        assert abs(alpha_mle - alpha_true) < 0.2, f"MLE: {alpha_mle}, true: {alpha_true}"
    
    def test_edge_cases(self):
        """Test edge cases."""
        # Empty data
        alpha_empty = powerlaw_mle_with_bounds([], 0.1, 1.0)
        assert np.isnan(alpha_empty), "Empty data should give NaN"
        
        # Single point
        alpha_single = powerlaw_mle_with_bounds([0.5], 0.1, 1.0)
        assert np.isfinite(alpha_single), "Single point should give finite result"
    
    def test_bounds_respect(self):
        """Test that MLE respects bounds."""
        np.random.seed(42)
        m_min, m_max = 0.3, 0.7
        
        # Generate data within bounds
        masses = np.random.uniform(m_min, m_max, 1000)
        
        alpha = powerlaw_mle_with_bounds(masses, m_min, m_max)
        
        # Should be reasonable
        assert 1 < alpha < 10, f"Unreasonable alpha: {alpha}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])