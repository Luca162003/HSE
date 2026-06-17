import matplotlib.pyplot as plt
import pandas as pd

# 1. Preparazione dei dati nell'ordine esatto della foto
data = {
    "Società": [
        "Gruppo SNAM", "BIOENERYS", "RENOVIT", 
        "SET onshore", "SET offshore", "SNAM Rete Gas", 
        "SNAM Rete Gas ENGOS", "SNAM Rete Gas GEST", "SNAM Rete Gas IMP", 
        "SNAM Rete Gas STAFF", "STOGIT", 
    ],
    "Punteggio": [
        83.85, 82.22, 79.11, 78.82, 90.77,
        85.20, 87.65, 85.23, 82.58, 84.93, 78.25
    ]
}

df = pd.DataFrame(data)

# 2. Creazione del plot
plt.figure(figsize=(15, 7))

# Colore blu standard di matplotlib
bars = plt.bar(df["Società"], df["Punteggio"], edgecolor='black', alpha=0.8)

# 3. Aggiunta dei valori sopra le barre
for bar in bars:
    yval = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width()/2, 
        yval + 0.6, 
        f'{yval:.2f}', 
        ha='center', 
        va='bottom', 
        fontsize=10, 
        fontweight='bold'
    )

# Personalizzazione estetica
plt.title("Valutazione per Società", fontsize=16, fontweight='bold', pad=25)
plt.ylabel("Punteggio", fontsize=12)
plt.xlabel("Società", fontsize=12)

# Rotazione etichette e allineamento
plt.xticks(rotation=45, ha='right')

# Limiti asse Y per dare respiro al grafico
plt.ylim(0, 100)

plt.tight_layout()
plt.show()