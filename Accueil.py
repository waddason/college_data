###############################################################################
# College analysis project
# File: Accueil.py
# Version: 1.0.0
# Date: 2024-08-22
###############################################################################

###############################################################################
# Importing libraries
###############################################################################
import streamlit as st
import pandas as pd


###############################################################################
# Importing own modules and data
###############################################################################
file_name: str = "fr-en-college-effectifs-niveau-sexe-lv.csv"
file_relative_path: str = "./data/"
logo_path: str = "./img/data_gouv_fr.png"
logo_link: str = "https://www.data.gouv.fr/fr/"


def load_and_cache_data():
    """
    Load data from file and cache it in session state for cross-pages access.
    """
    data: pd.DataFrame = pd.read_csv(
        filepath_or_buffer=file_relative_path + file_name, sep=";"
    )
    st.session_state["df_init"] = data


def get_regions(data: pd.DataFrame):
    regions = data["region_academique"].unique()
    return list(regions)


def setup_logo():
    lg = f'st.logo(image="{logo_path}", link="{logo_link}", icon_image="{logo_path}")'
    st.session_state["logo"] = lg


def display_logo():
    st.logo(image=logo_path, link="https://www.data.gouv.fr/fr/", icon_image=logo_path)


###############################################################################
# Main
###############################################################################
def __main__():
    # display_logo()
    setup_logo()
    eval(st.session_state["logo"])
    st.title("Effectifs des collèges")
    st.header("Description des régions en 2022")

    # load data in the session state
    load_and_cache_data()
    df = st.session_state["df_init"]
    df_2022 = df[df["rentree_scolaire"] == 2022]
    with st.expander("Description des régions"):
        st.dataframe(
            df_2022.groupby(["region_academique"])[
                [
                    "nombre_eleves_total",
                    "6eme_total",
                    "5eme_total",
                    "4eme_total",
                    "3eme_total",
                ]
            ]
            .sum()
            .sort_values(by="nombre_eleves_total", ascending=False)
        )

    st.subheader("Analyse des genres par niveau")
    st.write(
        "Le tableau ci-dessus présente le ratio de filles par niveau par région académique en 2022."
    )
    df_2022_gender = df_2022.groupby(["region_academique"])[
        [
            "nombre_eleves_total",
            "6eme_total",
            "6eme_filles",
            "5eme_total",
            "5eme_filles",
            "4eme_total",
            "4eme_filles",
            "3eme_total",
            "3eme_filles",
        ]
    ].sum()
    # create the gender ratios for each level by region
    df_2022_gender["6eme_ratio"] = (
        100 * df_2022_gender["6eme_filles"] / df_2022_gender["6eme_total"]
    )
    df_2022_gender["5eme_ratio"] = (
        100 * df_2022_gender["5eme_filles"] / df_2022_gender["5eme_total"]
    )
    df_2022_gender["4eme_ratio"] = (
        100 * df_2022_gender["4eme_filles"] / df_2022_gender["4eme_total"]
    )
    df_2022_gender["3eme_ratio"] = (
        100 * df_2022_gender["3eme_filles"] / df_2022_gender["3eme_total"]
    )
    percent_format = st.column_config.NumberColumn(
        help="ratio de filles par niveau",
        format="%.2f %%",
    )

    st.dataframe(
        data=df_2022_gender[
            [
                "6eme_ratio",
                "5eme_ratio",
                "4eme_ratio",
                "3eme_ratio",
            ]
        ],
        column_config={
            "6eme_ratio": percent_format,
            "5eme_ratio": percent_format,
            "4eme_ratio": percent_format,
            "3eme_ratio": percent_format,
        },
    )
    # plot this
    df_2022_gender.reset_index(inplace=True)
    unpivoted_df = pd.melt(
        df_2022_gender,
        id_vars=["region_academique"],  # Columns to keep as identifiers
        value_vars=[
            "6eme_ratio",
            "5eme_ratio",
            "4eme_ratio",
            "3eme_ratio",
        ],  # Columns to unpivot
        var_name="class_level",  # Name for the new variable column
        value_name="ratio",  # Name for the new value column
    )
    unpivoted_df["niveau"] = (
        unpivoted_df["region_academique"] + " - " + unpivoted_df["class_level"]
    )
    st.dataframe(unpivoted_df[["niveau", "ratio"]])

    st.bar_chart(
        data=unpivoted_df[["niveau", "ratio"]],
        x="niveau",
        y="ratio",
        y_label="Niveau",
        x_label="Ratio de filles (%)",
        horizontal=True,
        stack=None,
    )


if __name__ == "__main__":
    __main__()
