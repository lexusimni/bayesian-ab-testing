import numpy as np
import pandas as pd
from scipy.stats import beta
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

def get_posteriors(success_a, total_a, success_b, total_b, alpha_prior=1, beta_prior=1):
    """
    Return posterior Beta distributions for A and B groups.
    """
    posterior_a = beta(alpha_prior + success_a, beta_prior + total_a - success_a)
    posterior_b = beta(alpha_prior + success_b, beta_prior + total_b - success_b)
    return posterior_a, posterior_b

def sample_posteriors(posterior_a, posterior_b, n_samples=100_000):
    """
    Sample from two Beta distributions and calculate difference.
    """
    samples_a = posterior_a.rvs(n_samples)
    samples_b = posterior_b.rvs(n_samples)
    diff = samples_b - samples_a
    prob_b_better = (samples_b > samples_a).mean()
    
    return samples_a, samples_b, diff, prob_b_better

def plot_posteriors(posterior_a, posterior_b, x_range=(0, 0.2), save_path=None):
    """
    Plot posterior distributions.
    """
    x = np.linspace(*x_range, 1000)
    plt.figure(figsize=(10, 5))
    plt.plot(x, posterior_a.pdf(x), label='Control (A)', color='blue')
    plt.plot(x, posterior_b.pdf(x), label='Treatment (B)', color='green')
    plt.axvline(posterior_a.mean(), color='blue', linestyle='--', alpha=0.5)
    plt.axvline(posterior_b.mean(), color='green', linestyle='--', alpha=0.5)
    plt.title("Posterior Distributions of Conversion Rates")
    plt.xlabel("Conversion Rate")
    plt.ylabel("Density")
    plt.legend()
    if save_path:
        plt.tight_layout()
        plt.savefig(save_path)
    plt.show()

def plot_difference(diff, save_path=None):
    """
    Plot histogram of conversion rate differences (B - A).
    """
    plt.figure(figsize=(10, 5))
    sns.histplot(diff, kde=True, bins=100, color="purple")
    plt.axvline(0, color='red', linestyle='--')
    plt.title("Distribution of Difference: B - A")
    plt.xlabel("Conversion Rate Difference")
    plt.ylabel("Frequency")
    if save_path:
        plt.tight_layout()
        plt.savefig(save_path)
    plt.show()
