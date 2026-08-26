# -------------------------------------
# --- BLOC 1 - Imports et connexion ---
# -------------------------------------
import duckdb                   # moteur SQL embarqué
import pandas as pd              # lecture des xlsx
import os

con = duckdb.connect()            # connexion en mémoire (pas de fichier, pas de serveur)

# ------------------------------------------------
# --- BLOC 2 - Chargement des fichiers sources ---
# ------------------------------------------------
# On lit les xlsx avec pandas (plus fiable que DuckDB pour l'xlsx)
# puis on les enregistre comme tables DuckDB en mémoire

# charge les excel en dataframe pandas
erp_raw = pd.read_excel("./data/Fichier_erp.xlsx")         
web_raw = pd.read_excel("./data/Fichier_web.xlsx")
liaison_raw = pd.read_excel("./data/fichier_liaison.xlsx")

# On rend ces DataFrames requetable en SQL via DuckDB avec register, 
con.register("erp_raw", erp_raw)
con.register("web_raw", web_raw)
con.register("liaison_raw", liaison_raw)

# ---------------------------------------------------------------
# --- BLOC 3 — Nettoyage : suppression des valeurs manquantes ---
# ---------------------------------------------------------------
# Pour chaque table, on supprime les lignes qui ont des nulls
# sur la colonne clé (celle qu'on utilisera pour joindre)

# On identifie les colonnes 100% null
null_counts = con.execute("""
    SELECT * FROM (
    SUMMARIZE web_raw
    )
""").df()

# Garde seulement les colonnes qui ont au moins une valeur non-null
cols_valides = null_counts[
    null_counts['null_percentage'] < 100
]['column_name'].tolist()

# DuckDB fait le SELECT en SQL avec uniquement les colonnes non-vides
cols_sql = ', '.join(cols_valides) # Instance de la liste des colonnes en string

web_cla = con.execute(f"""
    SELECT DISTINCT {cols_sql}
    FROM web_raw
    WHERE sku IS NOT NULL
""").df()

erp_cla = con.execute("""
    SELECT * FROM erp_raw
    WHERE product_id IS NOT NULL""").df()

# ----------------------------------------
# --- BLOC 4 — Dédoublonnage - Unicité ---
# ----------------------------------------
# On ne garde qu'une seule ligne par clé unique

web_uni = con.execute("""
    SELECT DISTINCT * FROM web_cla
    WHERE post_type = 'product'
""").df()

erp_uni = con.execute("""
    SELECT DISTINCT ON (product_id)*  
    FROM erp_cla 
""").df()

liaison_uni = con.execute("""
    SELECT DISTINCT * FROM liaison_raw
    WHERE product_id IS NOT NULL
""").df()
# On garde les null pour garder la logique metier car 11% de NAN, sinon on perd les 825

# ------------------------------------------------
# --- EXPORT - Sauvegarde des tables nettoyées ---
# ------------------------------------------------

os.makedirs("./data/csv", exist_ok=True) 

erp_uni.to_csv("./data/csv/erp_s1", index=False)
web_uni.to_csv("./data/csv/web_s1", index=False)
liaison_uni.to_csv("./data/csv/liaison_s1", index=False)

# -----------------------------------------------------------------------
# --- VERIFICATION - Comparaison avec les chiffres attendus du métier ---
# -----------------------------------------------------------------------

print(f"ERP nettoyé   : {len(erp_uni)} lignes  (attendu: 825)")
print(f"Liaison nettoyée : {len(liaison_uni)} lignes  (attendu: 825)")
print(f"Web nettoyé   : {len(web_uni)} lignes  (attendu: 714)")