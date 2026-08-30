# ---------------
# --- IMPORTS ---
# ---------------

import pandas as pd

# -------------------------------------------------
# --- BLOC 1 - Chargement de la table fusionnée ---
# -------------------------------------------------
fusion = pd.read_csv("./export/fusion_s2.csv")

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

# -----------------------------------------------------------
# --- VERIFICATION - Comparaison avec attendus du service ---
# -----------------------------------------------------------

print(f"Vins premium détectés : {len(vins_premium)}  (attendu: 30)")

# -----------------------------------
# --- TEST - Cohérence du z-score ---
# -----------------------------------

assert len(vins_premium) == 30, f"❌ Premium : {len(vins_premium)} obtenu"
assert len(vins_premium) + len(vins_ordinaires) == 714, "❌ Total vins incohérent"
print(f"✅ Cohérence z-score vérifiée : {len(vins_premium)} premium, {len(vins_ordinaires)} ordinaires")

# --------------
# --- EXPORT ---
# --------------

vins_premium.to_csv("./export/vins_premiums.csv", index=False)
vins_ordinaires.to_csv("./export/vins_ordinaires.csv", index=False)