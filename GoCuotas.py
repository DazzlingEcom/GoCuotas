import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Procesador de CSV - GOcuotas")

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    try:
        # Detectar y leer el archivo con encoding 'ISO-8859-1' y separador ';'
        df = pd.read_csv(uploaded_file, sep=';', quotechar='"', encoding='ISO-8859-1')
        st.write("Archivo leído correctamente.")
    except Exception as e:
        st.error(f"No se pudo leer el archivo: {e}")
        st.stop()

    # Mostrar columnas detectadas y vista previa
    st.write("Columnas detectadas:", list(df.columns))
    st.write("Vista previa del archivo:")
    st.dataframe(df.head())

    try:
        # Filtrar filas donde 'Medio de pago' es 'GOcuotas'
        filtered_df = df[df["Medio de pago"].str.contains("GOcuotas", na=False)]

        # Convertir la columna 'Total' a numérico y aplicar el descuento
        filtered_df["Total"] = pd.to_numeric(filtered_df["Total"], errors="coerce")
        filtered_df["Total con Descuento"] = filtered_df["Total"] * (1 - 0.087)

        # Convertir la columna 'Fecha de pago' a datetime
        filtered_df["Fecha de pago"] = pd.to_datetime(filtered_df["Fecha de pago"], errors="coerce", format='%d/%m/%Y')

        # Agrupar por fecha de pago y sumar los valores ajustados
        grouped_df = filtered_df.groupby(filtered_df["Fecha de pago"].dt.date)["Total con Descuento"].sum().reset_index()
        grouped_df.columns = ["Fecha de pago", "Suma Total con Descuento"]

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
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")
