import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def main():
    # Configurar la página para que ocupe todo el ancho
    st.set_page_config(layout="wide")

    # Título centrado
    st.title("Estadística de Préstamos v1")

    # Subir el archivo CSV
    uploaded_file = st.file_uploader("Elige un archivo CSV", type=["csv"])

    # Opción para usar un archivo predeterminado si no se carga uno
    if uploaded_file is None:
        use_default_file = st.checkbox("Usar archivo predeterminado")
        if use_default_file:
            default_file_name = "df2_cleaned_updated.csv"  # Nombre del archivo en la carpeta del proyecto
            if os.path.exists(default_file_name):
                uploaded_file = default_file_name
            else:
                st.error("El archivo predeterminado no se encuentra en la carpeta del proyecto.")

    # Opción para usar un archivo predeterminado si no se carga uno
    if uploaded_file is not None:
        try:
            # Leer el archivo CSV
            df = pd.read_csv(uploaded_file)

            # Reemplazar los valores en la columna 'Default_Prestamo': 1 = 'PagoPrestamo', 0 = 'No_PagoPrestamo'
            df['Default_Prestamo'] = df['Default_Prestamo'].replace({1: 'PagoPrestamo', 0: 'No_PagoPrestamo'})

            # Dividir la página en dos columnas (1/2 para gráficos)
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Gráfico de Barras: Cantidad de Pago vs No Pago")
                # Contar la cantidad de cada tipo en la columna 'Default_Prestamo'
                default_counts = df['Default_Prestamo'].value_counts()

                # Generar el gráfico de barras
                fig, ax = plt.subplots()
                bars = default_counts.plot(kind='bar', color=['blue', 'orange'], ax=ax)
                ax.set_title('Cantidad de PagoPrestamo y No_PagoPrestamo')
                ax.set_xlabel('Tipo de Prestamo')
                ax.set_ylabel('Cantidad')
                ax.set_xticks(range(len(default_counts)))
                ax.set_xticklabels(default_counts.index)

                # Agregar las cantidades encima de las barras
                for i, count in enumerate(default_counts):
                    ax.text(i, count + 50, str(count), ha='center', fontsize=12)

                st.pyplot(fig)

            with col2:
                st.subheader("Gráfico de Caja: Distribución de Edades de No Pagadores")
                # Filtrar los datos de aquellos que no pagaron el préstamo
                no_pago_prestamo = df[df['Default_Prestamo'] == 'No_PagoPrestamo']

                # Generar un gráfico de caja (boxplot) para ver la distribución de las edades de los que no pagaron el préstamo
                fig, ax = plt.subplots()
                ax.boxplot(no_pago_prestamo['Edad'], vert=False, patch_artist=True, boxprops=dict(facecolor='lightblue'))
                ax.set_title('Distribución de Edad - No_PagoPrestamo (Boxplot)')
                ax.set_xlabel('Edad')

                st.pyplot(fig)

        except Exception as e:
            st.error(f"Ocurrió un error al procesar el archivo: {e}")

if __name__ == "__main__":
    main()
