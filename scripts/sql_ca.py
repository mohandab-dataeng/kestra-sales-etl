# -------------------------
# --- IMPORTS/CONNEXION ---
# -------------------------

import duckdb
import pandas as pd

con = duckdb.connect()

# -------------------------------------------------
# --- BLOC 1 - Chargement de la table fusionnée ---
# -------------------------------------------------
fusion = pd.read_csv("./export/fusion_s2.csv")
con.register("fusion", fusion)

# -------------------------------
# --- BLOC 2 - CA par produit ---
# -------------------------------
# Un CA par ligne de produit (price * total_sales)

ca_par_produit = con.execute("""
    SELECT
        product_id,
        post_title,
        price,
        total_sales,
        total_sales * price AS ca_produit
    FROM fusion
""").df()

# -------------------------
# --- BLOC 3 - CA total ---
# -------------------------
# La somme de tous les CA produit

ca_total = con.execute("""
    SELECT
        SUM(total_sales * price) AS ca_total
    FROM fusion
""").df()

# ----------------------------------------------------------------
# --- VERIFICATION - Comparaison avec le CA  du service métier ---
# ----------------------------------------------------------------

print(f"CA total calculé : {ca_total['ca_total'].iloc[0]:.2f}  (attendu: 70568.60)")

# ---------------------------------
# --- TEST - Chiffre d'affaires ---
# ---------------------------------

ca_calcule = round((fusion["total_sales"] * fusion["price"]).sum(), 2)
assert ca_calcule == 70568.60, f"❌ CA incohérent : {ca_calcule} obtenu"
print(f"✅ Cohérence CA vérifiée : {ca_calcule} €")

# --------------
# --- EXPORT ---
# --------------

ca_par_produit.to_csv("./export/ca_pro_s3.csv", index=False)
ca_total.to_csv("./export/ca_tot_s3.csv", index=False)