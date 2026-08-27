# ---------------
# --- IMPORTS ---
# ---------------
import pandas as pd

# -------------------------------------------------
# --- BLOC 1 - Chargement de la table fusionnée ---
# -------------------------------------------------
fusion = pd.read_csv("./data/csv/fusion_s2.csv")

# --------------------------------------------------------------------
# --- BLOC 2 - Calcul et instance de la moyenne et de l'écart-type ---
# --------------------------------------------------------------------
prix_moyen = fusion["price"].mean()
prix_ecart_type = fusion["price"].std()

print(f"Prix moyen : {prix_moyen}")
print(f"Ecart-type : {prix_ecart_type}")

# ----------------------------------
# --- BLOC 3 - Calcul du z-score ---
# ----------------------------------
fusion["z_score"] = (fusion["price"] - prix_moyen) / prix_ecart_type

# -------------------------------------------------
# --- BLOC 4 - Classification premium/ordinaire ---
# -------------------------------------------------
vins_premium = fusion[fusion["z_score"] > 2]
vins_ordinaires = fusion[fusion["z_score"] < 2]

# ----------------------------------------------------------
# --- VERIFICATION - Comparaison avec attendus du service --
# ----------------------------------------------------------
print(f"Vins premium détectés : {len(vins_premium)}  (attendu: 30)")

# --------------
# --- EXPORT ---
# --------------
vins_premium.to_csv("./data/csv/vins_premiums.csv", index=False)
vins_ordinaires.to_csv("./data/csv/vins_ordinaires.csv", index=False)