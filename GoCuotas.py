import streamlit as st
import pandas as pd

st.title("Inspección del Archivo CSV")

uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    try:
        # Probar diferentes configuraciones de separador
        df = pd.read_csv(uploaded_file, sep=';', quotechar='"', encoding='utf-8')
        st.write("Archivo leído con separador ';'")
    except:
        try:
            df = pd.read_csv(uploaded_file, sep=',', quotechar='"', encoding='utf-8')
            st.write("Archivo leído con separador ','")
        except:
            try:
                df = pd.read_csv(uploaded_file, sep='\t', quotechar='"', encoding='utf-8')
                st.write("Archivo leído con separador tab ('\\t')")
            except Exception as e:
                st.error(f"No se pudo leer el archivo: {e}")
                st.stop()

    # Mostrar la cantidad de columnas y sus nombres
    st.write("Cantidad de columnas detectadas:", len(df.columns))
    st.write("Columnas detectadas:", list(df.columns))

    # Mostrar las primeras filas para inspección
    st.write("Vista previa del archivo:")
    st.dataframe(df.head())
else:
    st.info("Por favor, sube un archivo CSV para inspeccionar.")
