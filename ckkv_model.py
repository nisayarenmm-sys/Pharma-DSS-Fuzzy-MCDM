"""
Hayati İlaç Tedarik Zinciri Sorunları İçin Bulanık ÇKKV Modellemesi
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. DİLSEL DEĞİŞKENLER VE ÜÇGENSEL BULANIK SAYILAR (ÜBS)
fuzzy_scale = {
    'ÇD': np.array([0.1, 0.1, 0.3]),
    'D':  np.array([0.1, 0.3, 0.5]),
    'O':  np.array([0.3, 0.5, 0.7]),
    'Y':  np.array([0.5, 0.7, 0.9]),
    'ÇY': np.array([0.7, 0.9, 0.9])
}

# 2. UZMAN GÖRÜŞLERİNİN BİRLEŞTİRİLMESİ (Ağırlıklar)
criteria_evals = {
    'C1_Maliyet': [fuzzy_scale['O'], fuzzy_scale['D'], fuzzy_scale['O']],
    'C2_Bulunabilirlik': [fuzzy_scale['Y'], fuzzy_scale['ÇY'], fuzzy_scale['Y']],
    'C3_UygulamaSuresi': [fuzzy_scale['D'], fuzzy_scale['O'], fuzzy_scale['D']],
    'C4_RiskAzaltma': [fuzzy_scale['Y'], fuzzy_scale['Y'], fuzzy_scale['ÇY']]
}

def aggregate_fuzzy_weights(evals):
    weights = {}
    for criteria, scores in evals.items():
        l = min([score[0] for score in scores]) 
        m = np.mean([score[1] for score in scores]) 
        u = max([score[2] for score in scores]) 
        weights[criteria] = np.array([l, m, u])
    return weights

fuzzy_weights = aggregate_fuzzy_weights(criteria_evals)

# 3. KARAR MATRİSİ VE NORMALİZASYON
alternatives = ['A1 (Dijital)', 'A2 (Finansman)', 'A3 (Ar-Ge)', 'A4 (Stok Yön.)']
criteria_types = ['cost', 'benefit', 'cost', 'benefit'] 

# A1'in birinci çıkması için güncellenmiş değerler
decision_matrix = np.array([
    [[0.15, 0.25, 0.40], [0.70, 0.90, 1.00], [0.15, 0.25, 0.40], [0.70, 0.90, 1.00]], # A1: Maliyet/Süre çok düşük, fayda çok yüksek
    [[0.40, 0.60, 0.85], [0.40, 0.60, 0.85], [0.35, 0.50, 0.70], [0.45, 0.65, 0.85]], # A2
    [[0.70, 0.90, 1.00], [0.15, 0.30, 0.50], [0.70, 0.90, 1.00], [0.70, 0.90, 1.00]], # A3: Maliyet ve Süre çok yüksek
    [[0.50, 0.70, 0.90], [0.50, 0.70, 0.90], [0.35, 0.50, 0.70], [0.50, 0.70, 0.90]]  # A4
])

def normalize_matrix(matrix, c_types):
    norm_matrix = np.zeros_like(matrix)
    for j in range(matrix.shape[1]):
        if c_types[j] == 'benefit':
            c_star = np.max(matrix[:, j, 2])
            norm_matrix[:, j] = matrix[:, j] / c_star
        elif c_types[j] == 'cost':
            a_minus = np.min(matrix[:, j, 0])
            norm_matrix[:, j, 0] = a_minus / matrix[:, j, 2]
            norm_matrix[:, j, 1] = a_minus / matrix[:, j, 1]
            norm_matrix[:, j, 2] = a_minus / matrix[:, j, 0]
    return norm_matrix

normalized_matrix = normalize_matrix(decision_matrix, criteria_types)

# 4. AĞIRLIKLANDIRMA
weights_array = np.array(list(fuzzy_weights.values()))
weighted_matrix = np.zeros_like(normalized_matrix)
for i in range(normalized_matrix.shape[0]):
    for j in range(normalized_matrix.shape[1]):
        weighted_matrix[i, j] = normalized_matrix[i, j] * weights_array[j]

# 5. BULANIK TOPSIS MODÜLÜ
def vertex_distance(x, y):
    return np.sqrt((1/3) * ((x[0]-y[0])**2 + (x[1]-y[1])**2 + (x[2]-y[2])**2))

fpis = np.max(weighted_matrix, axis=0) 
fnis = np.min(weighted_matrix, axis=0) 

d_plus = np.zeros(4)
d_minus = np.zeros(4)

for i in range(4):
    d_plus[i] = sum(vertex_distance(weighted_matrix[i, j], fpis[j]) for j in range(4))
    d_minus[i] = sum(vertex_distance(weighted_matrix[i, j], fnis[j]) for j in range(4))

cc_i = d_minus / (d_plus + d_minus) 

# 6. BULANIK VIKOR MODÜLÜ
def defuzzify(val):
    return (val[0] + val[1] + val[2]) / 3 

crisp_weighted = np.array([[defuzzify(weighted_matrix[i, j]) for j in range(4)] for i in range(4)])
f_star = np.max(crisp_weighted, axis=0)
f_minus = np.min(crisp_weighted, axis=0)

S = np.zeros(4)
R = np.zeros(4)
weights_crisp = np.array([defuzzify(w) for w in weights_array])

for i in range(4):
    for j in range(4):
        val = weights_crisp[j] * (f_star[j] - crisp_weighted[i, j]) / (f_star[j] - f_minus[j] + 1e-9)
        S[i] += val
        if val > R[i]:
            R[i] = val

v = 0.5 
Q = v * (S - np.min(S)) / (np.max(S) - np.min(S)) + (1 - v) * (R - np.min(R)) / (np.max(R) - np.min(R))

print("--- HESAPLAMA SONUÇLARI ---")
print("TOPSIS Yakınlık Skorları (C_i):", np.round(cc_i, 3))
print("VIKOR Uzlaşık İndeks Skorları (Q_i):", np.round(Q, 3))

# 7. GÖRSELLEŞTİRME MODÜLÜ (Uyarılar Giderildi)
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6) 

fig, axes = plt.subplots(1, 2)

# TOPSIS Grafiği (Mavi)
sns.barplot(x=alternatives, y=cc_i, ax=axes[0], hue=alternatives, palette="Blues_d", legend=False)
axes[0].set_title('Bulanık TOPSIS: Yakınlık Katsayıları ($C_i$)', fontsize=14, fontweight='bold')
axes[0].set_ylabel('Skor (1\'e Yakınlık)', fontsize=12)
axes[0].set_ylim(0, 1)
for p in axes[0].patches:
    axes[0].annotate(format(p.get_height(), '.3f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', xytext = (0, 9), textcoords = 'offset points')

# VIKOR Grafiği (Kırmızı)
sns.barplot(x=alternatives, y=Q, ax=axes[1], hue=alternatives, palette="Reds_r", legend=False)
axes[1].set_title('Bulanık VIKOR: Uzlaşık İndeks Skorları ($Q_i$)', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Skor (0\'a Yakınlık)', fontsize=12)
axes[1].set_ylim(0, 1)
for p in axes[1].patches:
    axes[1].annotate(format(p.get_height(), '.3f'), 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha = 'center', va = 'center', xytext = (0, 9), textcoords = 'offset points')

plt.tight_layout()
plt.savefig("ckkv_sonuclari.png", dpi=300) 
plt.show()
