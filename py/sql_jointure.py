# -------------------------------------
# --- BLOC 1 - Imports et connexion ---
# -------------------------------------
import duckdb
import pandas as pd

con = duckdb.connect()

# ---------------------------------------------------
# --- BLOC 2 - Chargement des exports du Script 1 ---
# ---------------------------------------------------
# On repart des fichiers nettoyés produits par le script précédent
# (pas des fichiers _raw !)

erp_uni = pd.read_csv("______")
web_uni = pd.read_csv("______")
liaison_uni = pd.read_csv("______")

con.register("erp_uni", erp_uni)
con.register("web_uni", web_uni)
con.register("liaison_uni", liaison_uni)

# ------------------------------------------------
# --- BLOC 3 — Vérification des types de clés ---
# ------------------------------------------------
# Avant de joindre, on vérifie que les types matchent
# (on a déjà eu un souci de nom de colonne, restons prudents sur les types)

print(erp_uni["______"].dtype)
print(liaison_uni["______"].dtype)
print(liaison_uni["______"].dtype)
print(web_uni["______"].dtype)

# -----------------------------------------------------
# --- BLOC 4 — Fusion en 2 étapes (erp→liaison→web) ---
# -----------------------------------------------------
# Étape A : erp JOIN liaison sur product_id
# Étape B : résultat JOIN web sur id_web = sku

fusion = con.execute("""
    SELECT ______
    FROM erp_uni AS e
    _____ JOIN liaison_uni AS l
        ON e.______ = l.______
    _____ JOIN web_uni AS w
        ON l.______ = w.______
""").df()

# ------------------------------------------
# --- BLOC 5 — Vérification de volumétrie ---
# ------------------------------------------
print(f"Table fusionnée : {len(fusion)} lignes  (attendu: 714)")

# ------------------------------------------
# --- EXPORT ---
# ------------------------------------------
fusion.to_csv("______", index=False)