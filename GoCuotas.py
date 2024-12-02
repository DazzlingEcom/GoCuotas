import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Procesador de CSV - Filtrado y Cálculo con GOcuotas")

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    try:
        # Leer el archivo CSV con encoding manejado
        df = pd.read_csv(uploaded_file, sep=';', header=None)
    except UnicodeDecodeError:
        # Intentar con otro encoding en caso de error
        try:
            df = pd.read_csv(uploaded_file, sep=';', encoding='latin1')
        except Exception as e:
            st.error(f"No se pudo leer el archivo CSV: {e}")
            st.stop()

    # Limpiar encabezados eliminando espacios en blanco
    df.columns = df.columns.str.strip()

    # Verificar si las columnas requeridas existen
    required_columns = ["Medio de pago", "Total", "Fecha"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"Faltan las siguientes columnas requeridas en el archivo CSV: {', '.join(missing_columns)}")
    else:
        # Filtrar filas donde "Medio de pago" contenga "GOcuotas"
        filtered_df = df[df["Medio de pago"].str.contains("GOcuotas", na=False)]

        # Convertir la columna "Total" a numérica y aplicar el descuento
        filtered_df["Total"] = pd.to_numeric(filtered_df["Total"], errors="coerce")
        filtered_df["Total con Descuento"] = filtered_df["Total"] * (1 - 0.087)

        # Convertir la columna "Fecha" a formato datetime
        filtered_df["Fecha"] = pd.to_datetime(filtered_df["Fecha"], errors="coerce", format='%d-%m-%Y %H:%M:%S')

        # Agrupar por fecha y sumar los valores de "Total con Descuento"
        grouped_df = filtered_df.groupby(filtered_df["Fecha"].dt.date)["Total con Descuento"].sum().reset_index()
        grouped_df.columns = ["Fecha", "Suma Total con Descuento"]

        # Mostrar los datos procesados
        st.subheader("Datos Filtrados con GOcuotas y Descuento Aplicado:")
        st.dataframe(filtered_df)

        st.subheader("Suma por Fechas:")
        st.dataframe(grouped_df)

        # Descargar los datos agrupados
        csv = grouped_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV Agrupado",
            data=csv,
            file_name='suma_por_fechas.csv',
            mime='text/csv'
        )
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")
