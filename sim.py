import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# PRNG Classes (Same as original implementation)
class LCG:
    def __init__(self, seed=1, a=1664525, c=1013904223, m=2**32):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m

    def random(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed / self.m

class MiddleSquare:
    def __init__(self, seed=675248):
        self.seed = seed
        self.n_digits = len(str(seed))

    def random(self):
        squared = str(self.seed ** 2).zfill(2 * self.n_digits)
        mid_start = (len(squared) - self.n_digits) // 2
        self.seed = int(squared[mid_start: mid_start + self.n_digits])
        return self.seed / (10 ** self.n_digits)

class UniformGenerator:
    def __init__(self, seed=1):
        self.seed = seed
        self.a = 1103515245
        self.c = 12345
        self.m = 2**31

    def random(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed / self.m

class MiddleSquareWeyl:
    def __init__(self, seed=675248, weyl=362436069, delta=0x61c88647):
        self.seed = seed
        self.weyl = weyl
        self.delta = delta

    def random(self):
        self.seed = (self.seed * self.seed + self.weyl) & 0xffffffff
        self.weyl = (self.weyl + self.delta) & 0xffffffff
        return self.seed / 2**32

# Statistical Test Functions (Same as original implementation)
def ks_test(data):
    statistic, p_value = stats.kstest(data, 'uniform', args=(0, 1))
    return statistic, p_value

def mean_test(data):
    n = len(data)
    sample_mean = np.mean(data)
    theoretical_mean = 0.5
    se = np.sqrt(1/12) / np.sqrt(n)
    z_stat = (sample_mean - theoretical_mean) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    return sample_mean, z_stat, p_value

def variance_test(data):
    n = len(data)
    sample_variance = np.var(data, ddof=1)
    theoretical_variance = 1/12
    chi2_stat = (n - 1) * sample_variance / theoretical_variance
    p_lower = stats.chi2.cdf(chi2_stat, n - 1)
    p_upper = 1 - p_lower
    p_value = 2 * min(p_lower, p_upper)
    p_value = min(p_value, 1.0)
    return sample_variance, chi2_stat, p_value

def chi_square_test(data, bins=10):
    observed, bin_edges = np.histogram(data, bins=bins, range=(0, 1))
    expected = [len(data)/bins] * bins
    chi2_stat, p_value = stats.chisquare(observed, f_exp=expected)
    return chi2_stat, p_value, observed, bin_edges

def generate_sample(prng, sample_size):
    return [prng.random() for _ in range(sample_size)]

class StatisticalTestingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Statistical Testing Program")
        self.root.geometry("800x600")
        
        # PRNG and Test Mapping
        self.prng_map = {
            "LCG": LCG,
            "Middle Square Method": MiddleSquare,
            "Uniform Distribution Generator": UniformGenerator,
            "Middle Square Weyl Sequence": MiddleSquareWeyl
        }
        
        self.test_map = {
            "Kolmogorov-Smirnov Test": self.run_ks_test,
            "Mean Test": self.run_mean_test,
            "Variance Test": self.run_variance_test,
            "Chi-Square Test": self.run_chi_square_test
        }
        
        self.create_widgets()
        
    def create_widgets(self):
        # Test Selection
        test_frame = ttk.LabelFrame(self.root, text="Test Selection")
        test_frame.pack(padx=10, pady=10, fill="x")
        
        self.test_var = tk.StringVar()
        test_dropdown = ttk.Combobox(test_frame, textvariable=self.test_var, 
                                     values=list(self.test_map.keys()), state="readonly")
        test_dropdown.pack(padx=10, pady=10, fill="x")
        test_dropdown.set("Select Statistical Test")
        
        # PRNG Selection
        prng_frame = ttk.LabelFrame(self.root, text="PRNG Selection")
        prng_frame.pack(padx=10, pady=10, fill="x")
        
        self.prng_var = tk.StringVar()
        prng_dropdown = ttk.Combobox(prng_frame, textvariable=self.prng_var, 
                                     values=list(self.prng_map.keys()), state="readonly")
        prng_dropdown.pack(padx=10, pady=10, fill="x")
        prng_dropdown.set("Select PRNG")
        
        # Sample Size
        size_frame = ttk.LabelFrame(self.root, text="Sample Size")
        size_frame.pack(padx=10, pady=10, fill="x")
        
        self.size_var = tk.StringVar(value="1000")
        size_entry = ttk.Entry(size_frame, textvariable=self.size_var)
        size_entry.pack(padx=10, pady=10, fill="x")
        
        # Run Button
        run_button = ttk.Button(self.root, text="Run Test", command=self.run_test)
        run_button.pack(padx=10, pady=10)
        
        # Results Frame
        self.results_frame = ttk.LabelFrame(self.root, text="Results")
        self.results_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Export Button
        export_button = ttk.Button(self.root, text="Export Data", command=self.export_data)
        export_button.pack(padx=10, pady=10)
        
    def run_test(self):
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
        
        # Validate inputs
        try:
            prng_name = self.prng_var.get()
            test_name = self.test_var.get()
            sample_size = int(self.size_var.get())
            
            if prng_name == "Select PRNG" or test_name == "Select Statistical Test":
                raise ValueError("Please select both a PRNG and a test")
            
            # Generate sample
            prng_class = self.prng_map[prng_name]
            prng = prng_class()
            sample = generate_sample(prng, sample_size)
            
            # Run selected test
            test_func = self.test_map[test_name]
            test_func(sample, prng_name)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        
    def run_ks_test(self, sample, prng_name):
        statistic, p_value = ks_test(sample)
        
        result_text = tk.Text(self.results_frame, height=10, wrap=tk.WORD)
        result_text.pack(padx=10, pady=10, fill="both", expand=True)
        
        result_text.insert(tk.END, f"Kolmogorov-Smirnov Test Results:\n")
        result_text.insert(tk.END, f"PRNG: {prng_name}\n")
        result_text.insert(tk.END, f"KS Statistic: {statistic:.4f}\n")
        result_text.insert(tk.END, f"P-Value: {p_value:.4f}\n")
        result_text.config(state=tk.DISABLED)
        
        # Create histogram
        self.create_histogram(sample)
        
    def run_mean_test(self, sample, prng_name):
        sample_mean, z_stat, p_val = mean_test(sample)
        
        result_text = tk.Text(self.results_frame, height=10, wrap=tk.WORD)
        result_text.pack(padx=10, pady=10, fill="both", expand=True)
        
        result_text.insert(tk.END, f"Mean Test Results:\n")
        result_text.insert(tk.END, f"PRNG: {prng_name}\n")
        result_text.insert(tk.END, f"Sample Mean: {sample_mean:.4f}\n")
        result_text.insert(tk.END, f"Z-Statistic: {z_stat:.4f}\n")
        result_text.insert(tk.END, f"P-Value: {p_val:.4f}\n")
        result_text.config(state=tk.DISABLED)
        
        # Create histogram
        self.create_histogram(sample)
        
    def run_variance_test(self, sample, prng_name):
        sample_variance, chi2_stat, p_val = variance_test(sample)
        
        result_text = tk.Text(self.results_frame, height=10, wrap=tk.WORD)
        result_text.pack(padx=10, pady=10, fill="both", expand=True)
        
        result_text.insert(tk.END, f"Variance Test Results:\n")
        result_text.insert(tk.END, f"PRNG: {prng_name}\n")
        result_text.insert(tk.END, f"Sample Variance: {sample_variance:.4f}\n")
        result_text.insert(tk.END, f"Chi-Square Statistic: {chi2_stat:.4f}\n")
        result_text.insert(tk.END, f"P-Value: {p_val:.4f}\n")
        result_text.config(state=tk.DISABLED)
        
        # Create histogram
        self.create_histogram(sample)
        
    def run_chi_square_test(self, sample, prng_name):
        chi2_stat, p_val, observed, bin_edges = chi_square_test(sample, bins=10)
        
        result_text = tk.Text(self.results_frame, height=10, wrap=tk.WORD)
        result_text.pack(padx=10, pady=10, fill="both", expand=True)
        
        result_text.insert(tk.END, f"Chi-Square Test Results:\n")
        result_text.insert(tk.END, f"PRNG: {prng_name}\n")
        result_text.insert(tk.END, f"Chi-Square Statistic: {chi2_stat:.4f}\n")
        result_text.insert(tk.END, f"P-Value: {p_val:.4f}\n\n")
        result_text.insert(tk.END, "Observed Frequencies per Bin:\n")
        for i in range(len(observed)):
            result_text.insert(tk.END, f"Bin {i+1} ({bin_edges[i]:.2f}-{bin_edges[i+1]:.2f}): {observed[i]}\n")
        result_text.config(state=tk.DISABLED)
        
        # Create histogram
        self.create_histogram(sample)
        
    def create_histogram(self, sample):
        # Create a matplotlib figure
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(sample, bins=10, range=(0, 1), edgecolor='black')
        ax.set_title('Sample Distribution')
        ax.set_xlabel('Value')
        ax.set_ylabel('Frequency')
        
        # Embed the plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.results_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(padx=10, pady=10)
        canvas.draw()
        
    def export_data(self):
        try:
            # Check if sample exists
            prng_name = self.prng_var.get()
            prng_class = self.prng_map[prng_name]
            sample_size = int(self.size_var.get())
            
            prng = prng_class()
            sample = generate_sample(prng, sample_size)
            
            # Open file dialog to choose export location
            filename = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                    filetypes=[("CSV files", "*.csv")])
            if filename:
                df = pd.DataFrame(sample, columns=["Random Numbers"])
                df.to_csv(filename, index=False)
                messagebox.showinfo("Export Successful", f"Data exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", str(e))

def main():
    root = tk.Tk()
    app = StatisticalTestingApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()