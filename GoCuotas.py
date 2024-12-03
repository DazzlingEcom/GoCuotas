import streamlit as st
import pandas as pd

# Título de la aplicación
st.title("Procesador de CSV - Filtrado y Cálculo con GOcuotas")

# Subida del archivo CSV
uploaded_file = st.file_uploader("Sube un archivo CSV", type="csv")

if uploaded_file is not None:
    try:
        # Leer el archivo CSV con el separador correcto y manejo de comillas
        df = pd.read_csv(uploaded_file, sep=';', quotechar='"', encoding='utf-8')
    except UnicodeDecodeError:
        # Intentar con otro encoding en caso de error
        try:
            df = pd.read_csv(uploaded_file, sep=';', quotechar='"', encoding='latin1')
        except Exception as e:
            st.error(f"No se pudo leer el archivo CSV: {e}")
            st.stop()

    # Mostrar columnas detectadas y vista previa
    st.write("Columnas detectadas en el archivo:", list(df.columns))
    st.write("Vista previa del archivo CSV:")
    st.dataframe(df.head())

    # Solicitar al usuario que asocie las columnas manualmente
    medio_pago_col = st.selectbox("Selecciona la columna para 'Medio de pago'", options=df.columns)
    total_col = st.selectbox("Selecciona la columna para 'Total'", options=df.columns)
    fecha_col = st.selectbox("Selecciona la columna para 'Fecha'", options=df.columns)

    try:
        # Filtrar filas donde la columna 'Medio de pago' contenga 'GOcuotas'
        filtered_df = df[df[medio_pago_col].str.contains("GOcuotas", na=False)]

        # Convertir la columna 'Total' a numérica y aplicar el descuento
        filtered_df[total_col] = pd.to_numeric(filtered_df[total_col], errors="coerce")
        filtered_df["Total con Descuento"] = filtered_df[total_col] * (1 - 0.087)

        # Convertir la columna 'Fecha' a formato datetime
        filtered_df[fecha_col] = pd.to_datetime(filtered_df[fecha_col], errors="coerce", format='%d/%m/%Y')

        # Agrupar por fecha y sumar los valores de 'Total con Descuento'
        grouped_df = filtered_df.groupby(filtered_df[fecha_col].dt.date)["Total con Descuento"].sum().reset_index()
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
    except Exception as e:
        st.error(f"Error procesando el archivo: {e}")
else:
    st.info("Por favor, sube un archivo CSV para comenzar.")
