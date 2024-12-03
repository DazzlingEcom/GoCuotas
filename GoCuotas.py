import streamlit as st
import pandas as pd
import chardet

st.title("Inspección del Archivo CSV")

uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    try:
        # Detectar el encoding del archivo
        raw_data = uploaded_file.read()
        result = chardet.detect(raw_data)
        encoding_detected = result['encoding']
        st.write(f"Encoding detectado: {encoding_detected}")

        # Leer el archivo con el encoding detectado
        uploaded_file.seek(0)  # Volver al inicio del archivo
        df = pd.read_csv(uploaded_file, sep=';', encoding=encoding_detected, quotechar='"')
        st.write("Archivo leído correctamente con el encoding detectado.")
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
