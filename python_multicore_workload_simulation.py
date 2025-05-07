import matplotlib.pyplot as plt # Görselleştirme için

def simulate_amdahl(total_workload_time, parallelizable_fraction, num_cores):
    """
    Amdahl Yasası'na göre çok çekirdekli sistemdeki çalışma süresini ve hızlanmayı simüle eder.

    Args:
        total_workload_time (float): İş yükünün tek çekirdekteki toplam süresi.
        parallelizable_fraction (float): İş yükünün paralelleştirilebilir kısmı (0.0 ile 1.0 arası).
        num_cores (int): Kullanılan çekirdek sayısı (N >= 1).

    Returns:
        tuple: (multi_core_time, speedup)
               multi_core_time: Hesaplanan çok çekirdekli çalışma süresi.
               speedup: Hesaplanan hızlanma.
    """
    if not (0.0 <= parallelizable_fraction <= 1.0):
        raise ValueError("Paralelleştirilebilir oran 0.0 ile 1.0 arasında olmalıdır.")
    if num_cores < 1:
        raise ValueError("Çekirdek sayısı en az 1 olmalıdır.")
    if total_workload_time <= 0:
         raise ValueError("Toplam iş yükü süresi pozitif olmalıdır.")

    serial_fraction = 1.0 - parallelizable_fraction # S = 1 - P

    # Süreleri hesapla
    serial_time = total_workload_time * serial_fraction
    parallelizable_time = total_workload_time * parallelizable_fraction

    # Çok çekirdekli süreyi hesapla
    # Seri kısım değişmez, paralel kısım N'e bölünür
    if num_cores == 1:
         multi_core_time = total_workload_time
    else:
         multi_core_time = serial_time + (parallelizable_time / num_cores)

    # Hızlanmayı hesapla
    speedup = total_workload_time / multi_core_time

    return multi_core_time, speedup

# --- Simülasyonu Çalıştırma ve Görselleştirme ---

# Parametreleri ayarla
total_time = 100.0 # Örnek toplam iş yükü süresi (tek çekirdekte)
parallel_fractions = [0.50, 0.75, 0.90, 0.95, 0.99] # Farklı P değerleri
core_counts = range(1, 65) # Denenecek çekirdek sayıları (1'den 64'e kadar)

results = {} # Sonuçları saklamak için dictionary

# Farklı P değerleri için simülasyonu çalıştır
for p_frac in parallel_fractions:
    speedups = []
    for n_cores in core_counts:
        _, speedup = simulate_amdahl(total_time, p_frac, n_cores)
        speedups.append(speedup)
    results[f'P = {p_frac:.2f}'] = speedups # P değeri ile sonuçları etiketle

# Sonuçları Görselleştirme (Matplotlib kullanarak)
plt.figure(figsize=(10, 6))
for label, speedup_list in results.items():
    # Teorik limit (1/S) çizgisini de ekleyebiliriz
    p = float(label.split('=')[1])
    s = 1.0 - p
    theoretical_limit = 1/s if s > 0 else float('inf') # S=0 ise limit sonsuz
    plt.plot(core_counts, speedup_list, marker='.', linestyle='-', label=f'{label} (Limit: {theoretical_limit:.2f})')

plt.title("Amdahl Yasası Simülasyonu: Hızlanma vs Çekirdek Sayısı")
plt.xlabel("Çekirdek Sayısı (N)")
plt.ylabel("Hızlanma (Speedup)")
plt.grid(True)
plt.legend()
plt.ylim(bottom=0) # Hızlanma negatif olamaz
# Grafik üzerindeki maksimum y değerini limitlere göre ayarlamak isteyebilirsiniz.
# plt.ylim(top=max_theoretical_limit * 1.1) # gibi
plt.show() # Grafiği göster