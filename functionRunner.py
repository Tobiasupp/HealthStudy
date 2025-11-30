import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class HealthAnalyzer:
    def __init__(self, df):
        self.df = df

    
    def regression_age_bp(self, age_col="age", bp_col="systolic_bp", alpha=0.3):
        """
        Utför en linjär regression mellan ålder och systoliskt blodtryck.
        Visar både scatterplot och trendlinje.
        """

        # Hämta data
        x = self.df[age_col].values
        y = self.df[bp_col].values

        # Beräkna linjär regression
        coef = np.polyfit(x, y, 1)   # lutning + intercept
        trend = np.poly1d(coef)

        # Rita scatter + linje
        plt.scatter(x, y, alpha=alpha, label="Data")
        plt.plot(x, trend(x), linewidth=2, label=f"Trendlinje (k={coef[0]:.2f})")

        plt.xlabel("Ålder")
        plt.ylabel("Systoliskt blodtryck")
        plt.title("Linjär regression: ålder → blodtryck")
        plt.legend()
        plt.show()

        # Returnera värden om du vill använda dom vidare
        return None
    
    def minmaxmed(self):
        """Skriver ut medel, min och max värde för age, height, weight, systolic_bp och cholesterol"""
    
        grouped_statistics = self.df[["age", "weight", "height", "systolic_bp", "cholesterol"]].agg(["median", "min", "max"])
        flipped_grouped = grouped_statistics.T

        return flipped_grouped
    
    def andel(self):

        actual_rate = self.df["disease"].mean()
        simulated = np.random.binomial(n=1, p=actual_rate, size=1000)
        simulated_rate = simulated.mean()

        result = (f"Verklig andel:  {actual_rate}\n"
                  f"Simulerad andel: {simulated_rate}\n"
                  f"Skillnad:  {simulated_rate - actual_rate}"
                  )
        return result

       

    def bootstrap(self):
        """Den här metoden använder bootstrap för att få ut 95%ci"""

        data = self.df["systolic_bp"].values
        b_range = 10000  

        boot_means = []

        for _ in range(b_range):
            sample = np.random.choice(data, size=len(data), replace=True)
            boot_means.append(np.mean(sample))

        lower = np.percentile(boot_means, 2.5)
        upper = np.percentile(boot_means, 97.5)

        result = (
        f"Bootstrap 95% KI: [{lower:.2f}, {upper:.2f}]\n"
        f"Bootstrap-medel: {np.mean(boot_means):.2f}"
        )

        return result

    def smokerCheck(self):

        """Gör en jämförelse av systoliskt blodtryck mellan röckare och icke rökare med hjälp av bootstrap metoden. 
            """

        smokers_bp = self.df[self.df["smoker"] == "Yes"]["systolic_bp"]
        nonsmokers_bp = self.df[self.df["smoker"] == "No"]["systolic_bp"]

        b_range = 5000
        boot_diffs = []

        for i in range(b_range):
            boot_smokers_bp = np.random.choice(smokers_bp, size=len(smokers_bp), replace=True)
            boot_nonsmokers_bp = np.random.choice(nonsmokers_bp, size=len(nonsmokers_bp), replace=True)
            boot_diffs.append(boot_smokers_bp.mean() - boot_nonsmokers_bp.mean())


        mean_smokers_bp = smokers_bp.mean()
        mean_nonsmokers_bp = nonsmokers_bp.mean()
        difference = mean_smokers_bp - mean_nonsmokers_bp

        lower = np.percentile(boot_diffs, 2.5)
        upper = np.percentile(boot_diffs, 97.5)

        result = (f"Medelvärde rökare:, {mean_smokers_bp:.3f}\n"
                  f"Medelvärde icke-rökare:, {mean_nonsmokers_bp:.3f}\n"
                  f"Skillnad i medelvärde:, {difference:.3f}\n"
                  f"Bootstrap 95% CI:, ({lower:.3f}, {upper:.3f})")
        
        return result


