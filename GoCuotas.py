import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Procesador de CSV - Ventas por SKU con GoCuotas")

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

        # Convertir las columnas 'Total' y 'Fecha de pago' a sus formatos correspondientes
        filtered_df["Total"] = pd.to_numeric(filtered_df["Total"], errors="coerce")
        filtered_df["Fecha de pago"] = pd.to_datetime(filtered_df["Fecha de pago"], errors="coerce", format='%d/%m/%Y')

        # Calcular el monto neto con descuento
        filtered_df["Total con Descuento"] = filtered_df["Total"] * (1 - 0.087)

        # Agrupar por fecha de pago y SKU, sumando los valores ajustados
        grouped_sku_df = filtered_df.groupby(
            [filtered_df["Fecha de pago"].dt.date, "SKU"]
        )["Total con Descuento"].sum().reset_index()
        grouped_sku_df.columns = ["Fecha de pago", "SKU", "Monto Neto por SKU"]

        # Agrupar por fecha de pago, sumando los valores totales ajustados
        grouped_date_df = grouped_sku_df.groupby("Fecha de pago")["Monto Neto por SKU"].sum().reset_index()
        grouped_date_df.columns = ["Fecha de pago", "Suma Total con Descuento"]

        # Mostrar los datos procesados
        st.subheader("Datos Filtrados con GOcuotas y Descuento Aplicado por SKU:")
        st.dataframe(grouped_sku_df)

        st.subheader("Suma Total por Fecha:")
        st.dataframe(grouped_date_df)

        # Descargar los datos agrupados por SKU
        csv_sku = grouped_sku_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV Agrupado por SKU",
            data=csv_sku,
            file_name='suma_por_sku.csv',
            mime='text/csv'
        )

        # Descargar los datos agrupados por fecha
        csv_date = grouped_date_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Descargar CSV Agrupado por Fecha",
            data=csv_date,
            file_name='suma_por_fecha.csv',
            mime='text/csv'
        )
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")
