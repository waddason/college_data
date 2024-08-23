###############################################################################
# College analysis project
# File: 1_TdB_regions.py
# Version: 1.0.0
# Date: 2024-08-22
###############################################################################

###############################################################################
# Importing libraries
###############################################################################
import streamlit as st


###############################################################################
# Main
###############################################################################


st.title("Statistiques par région")
st.header("Description des régions")

if "df_init" not in st.session_state:
    st.warning("Data not loaded, please go to the homepage first")
    st.page_link("Accueil.py", label="Home", icon="🏠")
    print("Data not loaded")
    st.stop()

# logo
eval(st.session_state["logo"])

region_list: list[str] = list(st.session_state["df_init"]["region_academique"].unique())
region_name: str = st.selectbox("Choix de la région académique", region_list)

# display the Region table
# if region_name is None:
#     st.stop()

sub_df = st.session_state["df_init"][
    st.session_state["df_init"]["region_academique"] == region_name
]
cols_to_display = st.columns(2)

# column de gauche
with cols_to_display[0]:
    st.subheader("Statistiques globales")
    st.write(f"Nombre d'élèves total: {sub_df['nombre_eleves_total'].sum()}")
    st.write(f"Nombre de collèges: {sub_df['numero_college'].nunique()}")
    st.metric("dont ulis", sub_df["nombre_eleves_ulis"].sum(), 10)


# column de droite
with cols_to_display[1]:
    st.subheader("Genre")
    st.metric("dont ulis", sub_df["nombre_eleves_ulis"].sum())

st.write("Thats all folks!")
# st.dataframe(sub_df)
