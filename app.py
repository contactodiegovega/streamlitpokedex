import streamlit as st
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Pokedex", page_icon=":pokeball:", layout="wide")
st.title("Pokedex")
st.write("¡Bienvenido a la Pokedex! Aquí encontrarás información sobre los Pokémon de la primera generación.")


@st.cache_data
def cargar():
    return pd.read_csv(Path(__file__).parent / "pokemon.csv")

df = cargar()


st.sidebar.title("Filtros")
busca = st.sidebar.text_input("Busca por nombre", placeholder="Ejemplo: Pikachu")
sel_tipo = st.sidebar.multiselect("Tipo principal", sorted(df["type_1"].dropna().unique()))
solo_legendarios = st.sidebar.checkbox("Solo legendarios")
total_min = st.sidebar.slider("Total de stats mínimo", 0, int(df["total"].max()), 0, 10)

f = df.copy()
if busca:
    f = f[f["name"].str.contains(busca, case=False, na=False)] #case=False para que no distinga mayúsculas de minúsculas, na=False para que no de error con los valores nulos
if sel_tipo:
    f = f[f["type_1"].isin(sel_tipo)]
if solo_legendarios:
    f = f[f["legendary"]]
f = f[f["total"] >= total_min]    

st.dataframe(f)


tab_inicio, tab_dex, tab_ficha, tab_versus = st.tabs(["Inicio", "Pokedex", "Ficha", "Comparador"])

with tab_ficha:
    izq, der = st.columns([1,2 ]) # [1,2] significa que la columna izquierda ocupa 1/3 del ancho y la derecha 2/3
    with izq:
        nombre = st.selectbox("Elige un Pokémon", f["name"].sort_values())
        p = f[f["name"] == nombre].iloc[0]
        st.image(p["sprite"], width=230)
        tipos_txt = " . ".join([t for t in [p["type_1"], p["type_2"]] if pd.notna(t)])
        st.markdown(f"### {int(p['id']):03d} - {p['name']}")
        st.markdown(f"**Tipo:** {tipos_txt}")