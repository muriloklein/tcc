import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import sys
OUT = sys.argv[1]
plt.rcParams.update({"font.family": "serif", "font.serif": ["STIXGeneral", "DejaVu Serif"],
    "mathtext.fontset": "stix", "font.size": 9, "axes.titlesize": 9.5, "axes.labelsize": 9,
    "xtick.labelsize": 8.5, "ytick.labelsize": 8.5, "legend.fontsize": 8.5,
    "axes.edgecolor": "#52514e", "axes.linewidth": 0.6, "xtick.color": "#52514e", "ytick.color": "#52514e",
    "text.color": "#0b0b0b", "axes.labelcolor": "#0b0b0b", "savefig.bbox": "tight", "savefig.pad_inches": 0.03})
INK2, MUTED, GRID = "#52514e", "#8a8984", "#e4e3df"
BLUE, ORANGE = "#2a78d6", "#eb6834"
SEQ = LinearSegmentedColormap.from_list("seq", ["#ffffff", "#cde2fb", "#86b6ef", "#3987e5", "#256abf", "#104281", "#0d366b"])
CLASSES = ["Attack", "Benigno", "C&C", "C&C-HeartBeat", "DDoS", "Okiru", "Portscan"]

# ---------- Fig. 1: matrizes de confusão SVM e CNN (normalizadas por linha) ----------
svm = np.array([[1785,0,0,0,0,0,4],[34,34841,155,180,33,194,1549],[0,7,3207,0,0,0,34],[0,0,0,4706,0,0,0],
                [0,3,4,0,58,0,2],[0,2,0,0,0,184,0],[9,36,802,0,1054,0,4089]])
cnn = np.array([[1781,0,0,0,0,0,8],[70,34359,224,198,35,285,1815],[0,1,3214,0,0,0,33],[0,0,0,4706,0,0,0],
                [0,0,4,0,60,0,3],[0,0,0,0,0,186,0],[42,28,1021,0,1374,0,3525]])
fig, eixos = plt.subplots(1, 2, figsize=(6.3, 3.35), sharey=True)
for eixo, m, titulo in zip(eixos, [svm, cnn], ["(a) SVM", "(b) CNN"]):
    pct = m / m.sum(1, keepdims=True) * 100
    im = eixo.imshow(pct, cmap=SEQ, vmin=0, vmax=100)
    for i in range(7):
        for j in range(7):
            v = pct[i, j]
            if m[i, j] == 0: continue
            txt = f"{v:.0f}" if v >= 1 else "<1"
            eixo.text(j, i, txt, ha="center", va="center", fontsize=7.2,
                      color="white" if v > 55 else "#0b0b0b")
    eixo.set_xticks(range(7)); eixo.set_xticklabels(CLASSES, rotation=45, ha="right")
    eixo.set_yticks(range(7)); eixo.set_yticklabels(CLASSES)
    eixo.set_title(titulo); eixo.set_xlabel("Classe prevista")
    eixo.tick_params(length=0)
    for s in eixo.spines.values(): s.set_visible(False)
eixos[0].set_ylabel("Classe real")
cb = fig.colorbar(im, ax=eixos, fraction=0.025, pad=0.02)
cb.set_label("% dos fluxos da classe real"); cb.outline.set_visible(False); cb.ax.tick_params(length=0)
fig.savefig(f"{OUT}/matrizes_svm_cnn_multiclasse.pdf"); plt.close(fig)

# ---------- Fig. 2: LOSO — taxa de detecção (cenário x modelo) ----------
modelos = ["Random Forest", "Árvore de\nDecisão", "SVM", "CNN"]
cenarios = ["Malware 1-1", "Malware 3-1", "Malware 8-1", "Malware 9-1", "Malware 34-1", "Malware 36-1"]
det = np.array([[95.4, 97.2, 78.5, 95.9], [15.2, 30.8, 34.7, 85.2], [25.0, 0.0, 100.0, 100.0],
                [74.2, 49.5, 100.0, 100.0], [63.6, 25.4, 74.7, 25.5], [0.0, 0.0, 0.0, 0.0]])
media = det.mean(0)
dados = np.vstack([det, media])
fig, eixo = plt.subplots(figsize=(5.0, 3.6))
im = eixo.imshow(dados, cmap=SEQ, vmin=0, vmax=100, aspect="auto")
for i in range(dados.shape[0]):
    for j in range(4):
        v = dados[i, j]
        eixo.text(j, i, f"{v:.1f}".replace(".", ","), ha="center", va="center", fontsize=8.5,
                  color="white" if v > 55 else "#0b0b0b", fontweight="bold" if i == 6 else "normal")
eixo.axhline(5.5, color="white", lw=3)
eixo.set_xticks(range(4)); eixo.set_xticklabels(modelos)
eixo.set_yticks(range(7)); eixo.set_yticklabels(cenarios + ["Média"])
eixo.get_yticklabels()[-1].set_fontweight("bold")
eixo.xaxis.tick_top(); eixo.tick_params(length=0)
eixo.set_ylabel("Captura retirada do treino")
for s in eixo.spines.values(): s.set_visible(False)
cb = fig.colorbar(im, ax=eixo, fraction=0.04, pad=0.03)
cb.set_label("% dos fluxos maliciosos detectados"); cb.outline.set_visible(False); cb.ax.tick_params(length=0)
fig.savefig(f"{OUT}/loso_deteccao.pdf"); plt.close(fig)

# ---------- Fig. 3: efeito da representação das portas ----------
rotulos = ["numérica", "sem portas", "numérica", "sem portas", "numérica", "categóricas", "numérica"]
grupos = [("Random Forest", 0.5), ("Árvore de Decisão", 3.1), ("CNN", 5.7), ("SVM", 7.8)]
normal = [0.9983, 0.8286, 0.9990, 0.8281, 0.9713, 0.9937, 0.9554]
loso   = [0.4654, 0.7800, 0.3483, 0.8499, 0.6475, 0.3297, 0.6537]
x = np.array([0, 1, 2.6, 3.6, 5.2, 6.2, 7.8]); w = 0.38
fig, eixo = plt.subplots(figsize=(6.3, 2.9))
eixo.yaxis.grid(True, color=GRID, lw=0.6); eixo.set_axisbelow(True)
b1 = eixo.bar(x - w/2 - 0.01, normal, w, color=BLUE, label="Teste convencional", edgecolor="white", lw=0.8)
b2 = eixo.bar(x + w/2 + 0.01, loso, w, color=ORANGE, label="LOSO (média dos 6 cenários)",
              hatch="////", edgecolor="white", lw=0.8)
for barras in (b1, b2):
    for b in barras:
        eixo.text(b.get_x() + b.get_width()/2, b.get_height() + 0.015, f"{b.get_height():.2f}".replace(".", ","),
                  ha="center", va="bottom", fontsize=7, color=INK2)
eixo.set_xticks(x); eixo.set_xticklabels(rotulos, fontsize=7.8, color=INK2)
for nome, pos in grupos:
    eixo.text(pos, -0.17, nome, ha="center", va="top", fontsize=8.8, transform=eixo.get_xaxis_transform())
eixo.text(-0.75, -0.055, "Portas:", ha="right", va="top", fontsize=7.8, color=INK2, transform=eixo.get_xaxis_transform())
eixo.set_ylabel("F1-macro (tarefa binária)"); eixo.set_ylim(0, 1.12)
eixo.set_yticks([0, .2, .4, .6, .8, 1]); eixo.set_yticklabels(["0", "0,2", "0,4", "0,6", "0,8", "1,0"])
for s in ["top", "right", "left"]: eixo.spines[s].set_visible(False)
eixo.tick_params(axis="x", length=0); eixo.tick_params(axis="y", length=0)
eixo.legend(loc="upper center", bbox_to_anchor=(0.5, 1.13), ncol=2, frameon=False)
fig.savefig(f"{OUT}/portas_normal_vs_loso.pdf"); plt.close(fig)
print("ok")
