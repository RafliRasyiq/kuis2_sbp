import numpy as np

# Data kriteria, alternatif, dan evaluasi
criteria = [
    ('Luas Lahan', 0.133, 'benefit'),
    ('Jarak ke Pusat Kota', 0.053, 'cost'),
    ('Sistem Informasi Pendukung', 0.080, 'benefit'),
    ('Keunggulan Transportasi Umum dibanding Angkutan Pribadi', 0.067, 'benefit'),
    ('Promosi oleh Institusi Umum', 0.027, 'benefit'),
    ('Frekuensi Angkutan Umum di lokasi', 0.093, 'benefit'),
    ('Harga Tempat Parkir', 0.187, 'cost'),
    ('Trafik Angkutan Umum di Lokasi', 0.107, 'cost'),
    ('Lokasi Parkir Gratis di Pusat Kota', 0.040, 'cost'),
    ('Total Biaya Parkir dan Angkutan Umum', 0.160, 'cost'),
]

alternatives = [
    'Lot 51', 'Petak 61', 'Petak 77', 'Area 51', 'Lot 61', 'Petak 57', 'Komplek 51'
]

evaluations = [
    [4, 3, 7, 6, 8, 6, 4, 4, 5, 4],  # Lot 51
    [2, 4, 4, 8, 5, 6, 5, 2, 3, 3],  # Petak 61
    [4, 3, 7, 9, 7, 4, 5, 3, 4, 3],  # Petak 77
    [4, 5, 8, 8, 8, 3, 5, 4, 3, 3],  # Area 51
    [4, 4, 4, 9, 6, 3, 3, 3, 5, 3],  # Lot 61
    [2, 3, 6, 8, 7, 3, 3, 4, 5, 3],  # Petak 57
    [4, 5, 4, 9, 5, 6, 4, 3, 3, 4]   # Komplek 51
]

# Konversi ke numpy array
evaluations = np.array(evaluations)

# Menghitung nilai solusi rata-rata (average_solution)
average_solution = evaluations.mean(axis=0)

# Inisialisasi array untuk Positif Deviance dan Negatif Deviance
positive_deviance = np.zeros_like(evaluations, dtype=float)
negative_deviance = np.zeros_like(evaluations, dtype=float)

# Menghitung Positif Deviance dan Negatif Deviance berdasarkan tipe kriteria (benefit/cost)
for idx, (criterion, weight, type) in enumerate(criteria):
    if type == 'benefit':
        positive_deviance[:, idx] = np.maximum(0, (evaluations[:, idx] - average_solution[idx]) / average_solution[idx])
        negative_deviance[:, idx] = np.maximum(0, (average_solution[idx] - evaluations[:, idx]) / average_solution[idx])
    else:
        positive_deviance[:, idx] = np.maximum(0, (average_solution[idx] - evaluations[:, idx]) / average_solution[idx])
        negative_deviance[:, idx] = np.maximum(0, (evaluations[:, idx] - average_solution[idx]) / average_solution[idx])

# Menghitung jumlah terbobot Positif Deviance dan Negatif Deviance
weights = np.array([weight for _, weight, _ in criteria])
weighted_positive_deviance = positive_deviance @ weights
weighted_negative_deviance = negative_deviance @ weights

# Normalisasi Positif Deviance dan Negatif Deviance
normalized_positive_deviance = weighted_positive_deviance / weighted_positive_deviance.max()
normalized_negative_deviance = 1 - (weighted_negative_deviance / weighted_negative_deviance.max())

# Menghitung nilai skor penilaian (assessment_score)
assessment_score = 0.5 * (normalized_positive_deviance + normalized_negative_deviance)

# Perankingan
ranking = np.argsort(assessment_score)[::-1]

# Menampilkan hasil nilai solusi rata-rata (average_solution) dalam bentuk tabel
print("Nilai Rata-rata : ")
print("+--------------------------------------------------------------+---------+")
print("|                      Kriteria                                |   AV    |")
print("+------------------------------------------------------------- +---------+")
for i, nilai in enumerate(average_solution):
    print(f"| {criteria[i][0]:<60} | {nilai:<7.4f} |")
print("+--------------------------------------------------------------+---------+")

# Menampilkan Positif Deviance dan Negatif Deviance 
print("+------------------------------------------------------------------------------+-------------------------------------------------------------------------------+")
print("|                                  Positif Deviance                             |                                 Negatif Deviance                             |")
print("+------------------------------------------------------------------------------+-------------------------------------------------------------------------------+")
for i in range(len(criteria)):
    print("|", end=" ")
    for val in positive_deviance[:, i]:
        print("{:<10.6f}".format(val), end=" ")
    print("|", end=" ")
    for val in negative_deviance[:, i]:
        print("{:<10.6f}".format(val), end=" ")
    print("|")
print("+-----------------------------------------------------------------------------+-------------------------------------------------------------------------------+")

# Menampilkan hasil Positif Deviance, Negatif Deviance, Normalisasi Positif Deviance, Normalisasi Negatif Deviance, dan Skor Penilaian dalam bentuk tabel
print("\n+---------------------+")
print("|   Weighted PD       |")
print("+---------------------+")
max_len = max(len('Weighted PD'), len(max(map(str, weighted_positive_deviance), key=len)))
for val in weighted_positive_deviance:
    print(f"| {val:<{max_len}} |")
print("+---------------------+")

print("\n+----------------------+")
print("|   Weighted ND        |")
print("+----------------------+")
max_len = max(len('Weighted ND'), len(max(map(str, weighted_negative_deviance), key=len)))
for val in weighted_negative_deviance:
    print(f"| {val:<{max_len}} |")
print("+----------------------+")

print("\n+--------------------+")
print("|   Normalized PD    |")
print("+--------------------+")
max_len = max(len('Normalized PD'), len(max(map(str, normalized_positive_deviance), key=len)))
for val in normalized_positive_deviance:
    print(f"| {val:<{max_len}} |")
print("+--------------------+")

print("\n+---------------------+")
print("|   Normalized ND     |")
print("+---------------------+")
max_len = max(len('Normalized ND'), len(max(map(str, normalized_negative_deviance), key=len)))
for val in normalized_negative_deviance:
    print(f"| {val:<{max_len}} |")
print("+---------------------+")

print("\n+---------------------+")
print("|   Assessment Score  |")
print("+---------------------+")
max_len = max(len('Assessment Score'), len(max(map(str, assessment_score), key=len)))
for val in assessment_score:
    print(f"| {val:<{max_len}} |")
print("+---------------------+")

# Menampilkan hasil perangkingan
print("+----------+-----------------+-----------------+")
print("| Rangking |    Alternatif   |  Assessment Score |")
print("+----------+-----------------+-----------------+")
for i, rank in enumerate(ranking):
    print(f"|    {i+1:<3}   | {alternatives[rank]:<15} | {assessment_score[rank]:<15.8f} |")
print("+----------+-----------------+-----------------+")
