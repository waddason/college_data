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
import pandas as pd


###############################################################################
# Main
###############################################################################
st.title("Statistiques par région")

if "df_init" not in st.session_state:
    st.warning("Data not loaded, please go to the homepage first")
    st.page_link("Accueil.py", label="Home", icon="🏠")
    print("Data not loaded")
    st.stop()

# If here, the session is correctly initialize, display logo and the rest of the page
eval(st.session_state["logo"])


# Chose the region from a side bar
with st.sidebar:
    region_list: list[str] = list(
        st.session_state["df_init"]["region_academique"].unique()
    )
    region_name: str = st.selectbox("Choix de la région académique", region_list)
    anne_list: list[int] = list(
        st.session_state["df_init"]["rentree_scolaire"].unique()
    )
    anne_list.sort(reverse=True)
    anne_choix: int = st.selectbox(
        label="Choix de l'année de rentrée scolaire",
        options=anne_list,
        index=0,
        disabled=False,
    )

# update the session state
sub_df = st.session_state["df_init"][
    st.session_state["df_init"]["region_academique"] == region_name
]
# Create the national metrics:
with st.expander(f"Moyennes nationales {anne_choix}"):
    df_national = st.session_state["df_init"][
        st.session_state["df_init"]["rentree_scolaire"] == anne_choix
    ]
    df_national = df_national.drop(
        columns=[
            "rentree_scolaire",
            "academie",
            "departement",
            "commune",
            "numero_college",
            "denomination_principale",
            "patronyme",
            "secteur",
        ],
    )

    df_national = df_national.groupby("region_academique").sum().reset_index()
    # add the national row with the mean
    df_mean = (
        df_national.drop(columns=["region_academique"]).mean().to_frame().T.astype(int)
    )
    df_mean["region_academique"] = "NATIONAL"
    st.dataframe(df_mean)

    df_national = pd.concat([df_national, df_mean])
    st.dataframe(df_national)
# -----------------------------------------------------------------------------
st.header("Statistiques de la région")
# Display some stats
col_1, col_2 = st.columns(2)


def display_metric(label: str, col_name: str, collapse: bool = False):
    metric_to_display: int = int(
        df_national[df_national["region_academique"] == region_name][col_name].values[0]
    )
    delta = int(
        metric_to_display
        - df_national[df_national["region_academique"] == "NATIONAL"][col_name].values[
            0
        ]
    )
    value_str = f"{metric_to_display:,} ".replace(",", " ") + (
        label if collapse else ""
    )
    delta_str = f"{delta:,}".replace(",", " ")

    st.metric(
        label=label,
        value=value_str,
        delta=delta_str,
        label_visibility="collapsed" if collapse else "visible",
    )


# column de gauche
with col_1:
    st.subheader("Statistiques globales")
    display_metric("Élèves de la région", "nombre_eleves_total")
    st.metric("Nombre d'académies", sub_df["academie"].nunique())
    st.metric("Nombre de départements", sub_df["departement"].nunique())
    st.metric("Nombre de communes", sub_df["commune"].nunique())
    st.metric("Nombre de collèges", sub_df["numero_college"].nunique())
    st.metric(
        "dont collèges privés",
        sub_df[sub_df["secteur"] == "PRIVE"]["numero_college"].nunique(),
        delta=f"{sub_df[sub_df["secteur"] == "PRIVE"]["numero_college"].nunique() / sub_df["numero_college"].nunique():.2%}",
        delta_color="off",
    )

# column de droite
with col_2:
    st.subheader("nombre d'élèves par niveau")
    st.write("Delta par rapport à la moyenne nationale")
    display_metric("6e", "6eme_total", collapse=True)
    display_metric("5e", "5eme_total", collapse=True)
    display_metric("4e", "4eme_total", collapse=True)
    display_metric("3e", "3eme_total", collapse=True)

    st.subheader("Genre")
    st.metric("dont ulis", sub_df["nombre_eleves_ulis"].sum())


# Display the table of the region
with st.expander("Données de la région"):
    st.dataframe(sub_df)

# -----------------------------------------------------------------------------
st.header("Évolution des effectifs")
# Display the evolution of the number of students
df_evolution = sub_df.groupby("rentree_scolaire")[
    ["6eme_total", "5eme_total", "4eme_total", "3eme_total", "nombre_eleves_total"]
].sum()
df_evolution = df_evolution.reset_index()
df_evolution.columns = [
    "rentree_scolaire",
    "6e",
    "5e",
    "4e",
    "3e",
    "nombre_eleves_total",
]


with st.expander("Données"):
    st.dataframe(df_evolution)
st.bar_chart(
    data=df_evolution,
    x="rentree_scolaire",
    y=["6e", "5e", "4e", "3e"],
    x_label="Cumul du nombre d'élèves par niveau",
    y_label="Rentrée",
    horizontal=True,
    stack=True,
)


st.write("Thats all folks!")
# st.dataframe(sub_df)
