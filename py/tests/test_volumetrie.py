# ---------------
# --- IMPORTS ---
# ---------------

import pandas as pd

# ------------------------------------
# --- BLOC 1 - Chargement de la db ---
# ------------------------------------

erp_uni = pd.read_csv("./data/csv/erp_s1.csv")
web_uni = pd.read_csv("./data/csv/web_s1.csv")
liaison_uni = pd.read_csv("./data/csv/liaison_s1.csv")

# ----------------------------------------
# --- BLOC 2 - Assertion de volumétrie ---
# ----------------------------------------

nb_lignes_erp = len(erp_uni)
valeur_attendue_erp = 825

nb_lignes_web = len(web_uni)
valeur_attendue_web = 714

nb_lignes_liaison = len(liaison_uni)
valeur_attendue_liaison = 825

# --------------------------------------
# --- BLOC 3 - Comptage des doublons ---
# --------------------------------------

nb_doublons_erp = erp_uni.duplicated().sum()
doublons_attendus_erp = 0

nb_doublons_web = web_uni.duplicated().sum()
doublons_attendus_web = 0

nb_doublons_liaison = liaison_uni.duplicated().sum()
doublons_attendus_liaison = 0

# --------------------------------
# --- TEST VOLUMETRIE/DOUBLONS RESULTAT ---
# --------------------------------

assert nb_lignes_erp == valeur_attendue_erp, f"❌ ERP : {nb_lignes_erp} lignes obtenues, {valeur_attendue_erp} attendues"
assert nb_lignes_web == valeur_attendue_web, f"❌ WEB : {nb_lignes_web} lignes obtenues, {valeur_attendue_web} attendues"
assert nb_lignes_liaison == valeur_attendue_liaison, f"❌ LIAISON : {nb_lignes_liaison} lignes obtenues, {valeur_attendue_liaison} attendues"

assert nb_doublons_erp == doublons_attendus_erp, f"❌ Doublons ERP : {nb_doublons_erp} doublons, {doublons_attendus_erp} attendues"
assert nb_doublons_web == doublons_attendus_web, f"❌ Doublons WEB : {nb_doublons_web} doublons, {doublons_attendus_web} attendues"
assert nb_doublons_liaison == doublons_attendus_liaison, f"❌ Doublons LIAISON : {nb_doublons_liaison} doublons, {doublons_attendus_liaison} attendues"

print(f"✅ Test doublons ERP réussi : {nb_doublons_erp} doublons")
print(f"✅ Test doublons WEB réussi : {nb_doublons_web} doublons")
print(f"✅ Test doublons LIAISON réussi : {nb_doublons_liaison} doublons")

print(f"✅ Test volumétrie ERP réussi : {nb_lignes_erp} lignes")
print(f"✅ Test volumétrie WEB réussi : {nb_lignes_web} lignes")
print(f"✅ Test volumétrie LIAISON réussi : {nb_lignes_liaison} lignes")