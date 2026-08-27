# -------------------------
# --- IMPORTS/CONNEXION ---
# -------------------------
import duckdb
import pandas as pd

con = duckdb.connect()

# ---------------------------------------------------
# --- BLOC 1 - Chargement des exports du Script 1 ---
# ---------------------------------------------------
# On repart des fichiers nettoyés produits par le script précédent
# (pas des fichiers _raw mais les export csv)

erp_uni = pd.read_csv("./data/csv/erp_s1.csv")
web_uni = pd.read_csv("./data/csv/web_s1.csv")
liaison_uni = pd.read_csv("./data/csv/liaison_s1.csv")

con.register("erp_uni", erp_uni)
con.register("web_uni", web_uni)
con.register("liaison_uni", liaison_uni)

# -----------------------------------------------
# --- BLOC 2 - Vérification des types de clés ---
# -----------------------------------------------
# Avant de joindre, on vérifie que les types matchent entre la table de liaison. 
# Les types doivent correspondre pour chacune des jointures

print(erp_uni["product_id"].dtype)
print(liaison_uni["product_id"].dtype)
print(liaison_uni["id_web"].dtype)
print(web_uni["sku"].dtype)

# ---------------------------------------
# --- BLOC 3 - Fusion erp>liaison>web ---
# ---------------------------------------
# 1 : erp JOIN liaison sur product_id = product_id
# 2 : liaison JOIN web sur id_web = sku

fusion = con.execute("""
    SELECT
        e.product_id,
        w.sku,
        w.post_title,
        w.total_sales,
        e.price,
    FROM erp_uni AS e
    INNER JOIN liaison_uni AS l
        ON e.product_id = l.product_id
    INNER JOIN web_uni AS w
        ON l.id_web = w.sku
""").df()

# -------------------------------------------
# --- BLOC 4 - Vérification  nb de lignes ---
# -------------------------------------------
print(f"Table fusionnée : {len(fusion)} lignes  (attendu: 714)")

# --------------
# --- EXPORT ---
# --------------
fusion.to_csv("./data/csv/fusion_s2.csv", index=False)
print(fusion.columns.tolist())