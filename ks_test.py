from statistics import mean
from scipy import stats
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

class KsTest:
    """
    Clase que implementa la Prueba de Kolmogorov-Smirnov (KS) para una secuencia de números generados.
    """
    def __init__(self, ri_nums=[], n_intervals=10):
        self.ri = ri_nums           # Lista de números generados
        self.n = len(ri_nums)       # Cantidad total de números
        self.average = 0
        self.d_max = 0
        self.d_max_p = 0
        self.min = 0
        self.max = 0
        self.oi = []                # Frecuencias observadas en cada intervalo
        self.oia = []               # Frecuencia acumulada observada
        self.prob_oi = []           # Probabilidades observadas en cada intervalo
        self.oia_a = []             # Frecuencia acumulada esperada
        self.prob_esp = []          # Probabilidades esperadas
        self.diff = []              # Diferencia entre probabilidades observadas y esperadas
        self.passed = False         # Resultado de la prueba
        self.alpha = 0.05
        self.intervals = []         # Lista de intervalos
        self.n_intervals = n_intervals  # Número de intervalos para la prueba

    # Calcula la sumatoria acumulada de las frecuencias observadas (oia)
    def calculate_oia(self):
        cum_freq = 0
        for freq in self.oi:
            cum_freq += freq
            self.oia.append(cum_freq)

    # Calcula el valor mínimo de la secuencia
    def calculate_min(self):
        if self.n != 0:
            self.min = min(self.ri)

    # Calcula el valor máximo de la secuencia
    def calculate_max(self):
        if self.n != 0:
            self.max = max(self.ri)

    # Calcula el promedio de la secuencia
    def calculateAverage(self):
        if self.n != 0:
            self.average = mean(self.ri)

    # Ejecuta todos los cálculos y realiza la prueba KS
    def checkTest(self):
        self.calculate_min()
        self.calculate_max()
        self.calculateAverage()
        self.calculate_intervals()
        self.calculate_oi()
        self.calculate_oia()
        self.calculate_prob_oi()
        self.calculate_oia_a()
        self.calculate_prob_esp()
        self.calculate_diff()
        self.d_max = max(self.diff)
        self.calculate_KS()
        if self.d_max <= self.d_max_p:
            self.passed = True
        else:
            self.passed = False

    # Calcula el valor crítico de KS según el tamaño de la muestra
    def calculate_KS(self):
        alpha = self.alpha
        n = self.n
        if self.n <= 50 and self.n > 0:
            critical_value = stats.ksone.ppf(1 - alpha / 2, n)
        if self.n > 50:
            critical_value = stats.kstwobign.isf(alpha) / np.sqrt(n)
        self.d_max_p = critical_value

    # Calcula las probabilidades esperadas para cada intervalo
    def calculate_prob_esp(self):
        for i in range(len(self.oia_a)):
            self.prob_esp.append(self.oia_a[i] / self.n)

    # Calcula la diferencia absoluta entre las probabilidades observadas y esperadas
    def calculate_diff(self):
        for i in range(len(self.prob_esp)):
            self.diff.append(abs(self.prob_esp[i] - self.prob_oi[i]))

    # Calcula la frecuencia acumulada esperada (oia_a)
    def calculate_oia_a(self):
        n1 = self.n / self.n_intervals
        for i in range(self.n_intervals):
            self.oia_a.append(n1 * (i + 1))

    # Calcula las probabilidades observadas en cada intervalo
    def calculate_prob_oi(self):
        for i in range(len(self.oia)):
            self.prob_oi.append(self.oia[i] / self.n)

    # Calcula las frecuencias observadas (oi) en cada intervalo
    def calculate_oi(self):
        self.ri.sort()
        self.oi = [0] * self.n_intervals
        # Para cada valor, determinar en qué intervalo se encuentra
        for valor in self.ri:
            for i, intervalo in enumerate(self.intervals):
                if intervalo[0] <= valor < intervalo[1]:
                    self.oi[i] += 1
                    break
        return self.oi

    # Calcula los intervalos utilizados para la prueba KS
    def calculate_intervals(self):
        if self.n != 0:
            interval_size = (self.max - self.min) / self.n_intervals
            initial = self.min
            for _ in range(self.n_intervals):
                new_interval = (initial, initial + interval_size)
                self.intervals.append(new_interval)
                initial = new_interval[1]

    # Genera un gráfico que muestra Dmax y Dmax_p
    def plotDs(self):
        labels = ["Dmax (calculado)", "Dmax_p (crítico KS)"]
        values = [self.d_max, self.d_max_p]
        fig, ax = plt.subplots()
        bars = plt.bar(labels, values, color=['red', 'blue'])
        plt.title("Comparación de Dmax vs Dmax_p")
        plt.ylabel("Valor")
        plt.xlabel("Estadístico KS")
        for bar, value in zip(bars, values):
            ax.annotate(str(value), xy=(bar.get_x() + bar.get_width() / 2, value),
                        xytext=(0, 1), textcoords='offset points', ha='center', va='bottom')
        plt.show()

    # Genera un gráfico que muestra las probabilidades observadas y esperadas en cada intervalo
    def plotIntervals(self):
        interval_labels = []
        observed_probabilities = []
        expected_probabilities = []
        for i, interval in enumerate(self.intervals):
            label = f"Int {i + 1}: [{interval[0]:.3f}, {interval[1]:.3f})"
            interval_labels.append(label)
            observed_probabilities.append(self.prob_esp[i])
            expected_probabilities.append(self.prob_oi[i])
        x = np.arange(len(interval_labels))
        width = 0.35
        fig, ax = plt.subplots()
        ax.bar(x - width/2, observed_probabilities, width, label='Prob. Observada')
        ax.bar(x + width/2, expected_probabilities, width, label='Prob. Esperada')
        ax.set_xlabel("Intervalos")
        ax.set_ylabel("Probabilidades")
        ax.set_title("Probabilidades Observadas vs Esperadas")
        ax.set_xticks(x)
        ax.set_xticklabels(interval_labels, rotation=45, ha='right')
        ax.legend()
        plt.tight_layout()
        plt.show()

    # Genera un gráfico que muestra las frecuencias observadas en cada intervalo
    def plotIntervalsFreq(self):
        interval_labels = []
        observed_frequencies = []
        for i, interval in enumerate(self.intervals):
            label = f"Int {i + 1}: [{interval[0]:.3f}, {interval[1]:.3f})"
            interval_labels.append(label)
            observed_frequencies.append(self.oi[i])
        x = np.arange(len(interval_labels))
        width = 0.35
        fig, ax = plt.subplots()
        bars = ax.bar(x, observed_frequencies, width, label='Frecuencia Observada')
        ax.set_xlabel("Intervalos")
        ax.set_ylabel("Frecuencia")
        ax.set_title("Frecuencias Observadas en Cada Intervalo")
        ax.set_xticks(x)
        ax.set_xticklabels(interval_labels, rotation=45, ha='right')
        for bar, oi in zip(bars, observed_frequencies):
            height = bar.get_height()
            ax.annotate(f'{oi}', xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3), textcoords="offset points",
                        ha='center', va='bottom')
        ax.legend()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    # Solicita al usuario que ingrese los números Ri separados por comas
    user_input = input("Ingresa los números Ri separados por comas: ")
    try:
        ri_nums = [float(x.strip()) for x in user_input.split(",")]
    except ValueError:
        print("Error: asegúrate de ingresar únicamente números separados por comas.")
        exit(1)

    # Solicita opcionalmente la cantidad de intervalos para la prueba KS
    intervals_input = input("Ingresa la cantidad de intervalos (por defecto 10): ")
    try:
        n_intervals = int(intervals_input) if intervals_input else 10
    except ValueError:
        print("Error: La cantidad de intervalos debe ser un número entero. Se usará 10.")
        n_intervals = 10

    # Crea la instancia de KsTest y ejecuta la prueba
    ks_test = KsTest(ri_nums=ri_nums, n_intervals=n_intervals)
    ks_test.checkTest()

    # Muestra resultados en consola
    print("\nNúmeros Ri ingresados:", ks_test.ri)
    print("Valor mínimo:", ks_test.min)
    print("Valor máximo:", ks_test.max)
    print("Promedio:", ks_test.average)
    print("Frecuencias observadas por intervalo:", ks_test.oi)
    print("Frecuencias acumuladas observadas:", ks_test.oia)
    print("Probabilidades observadas:", ks_test.prob_oi)
    print("Frecuencias acumuladas esperadas:", ks_test.oia_a)
    print("Probabilidades esperadas:", ks_test.prob_esp)
    print("Diferencias entre prob. observadas y esperadas:", ks_test.diff)
    print("Dmax (error calculado):", ks_test.d_max)
    print("Dmax_p (valor crítico KS):", ks_test.d_max_p)
    print("¿Prueba KS superada?:", ks_test.passed)

    # Muestra los gráficos
    ks_test.plotDs()
    ks_test.plotIntervals()
    ks_test.plotIntervalsFreq()
