# ---------------
# --- IMPORTS ---
# ---------------
import pandas as pd

# ---------------------------------------------------------
# --- BLOC 2 - Chargement des exports des scripts 3 & 4 ---
# ---------------------------------------------------------
ca_par_produit = pd.read_csv("./data/csv/ca_pro_s3.csv")
ca_total = pd.read_csv("./data/csv/ca_tot_s3.csv")
vins_premium = pd.read_csv("./data/csv/vins_premiums.csv")
vins_ordinaires = pd.read_csv("./data/csv/vins_ordinaires.csv")

# ------------------------------------------------
# --- BLOC 3 - Export excel multi-feuilles(CA) ---
# ------------------------------------------------
with pd.ExcelWriter("./livrables/rapport_bottleneck.xlsx", engine="openpyxl") as writer:
    ca_par_produit.to_excel(writer, sheet_name="ca_produit", index=False)
    ca_total.to_excel(writer, sheet_name="ca_total", index=False)

# ---------------------------------------------------
# --- BLOC 4 - Export CSV vins premiums/ordinaires ---
# ---------------------------------------------------
vins_premium.to_csv("./livrables/liste_vins_premiums.csv", index=False)
vins_ordinaires.to_csv("./livrables/liste_vins_ordinaires.csv", index=False)

# -------------------------------------------------------
# --- VERIFICATION - Nombre de lignes correspondantes ---
# -------------------------------------------------------
check_premium = pd.read_csv("./livrables/liste_vins_premiums.csv")
check_ordinaires = pd.read_csv("./livrables/liste_vins_ordinaires.csv")

print(f"Vins premium exportés   : {len(check_premium)}  (attendu: 30)")
print(f"Vins ordinaires exportés : {len(check_ordinaires)}  (attendu: 684)")

print("Export terminé ✅")