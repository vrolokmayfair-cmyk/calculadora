import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Cotizador Multimarca de Crédito", layout="wide")

st.title("📊 Cotizador y Buscador de Crédito Multimarca")
st.write("Ingrese la capacidad de pago del cliente para evaluar las mejores opciones disponibles en cada marca.")

# --- BASE DE DATOS DE TABLAS DE AMORTIZACIÓN ---
DATA_CREDITOS = [
    # CSB (Consubanco IMSS) - Basado en imss csb 4707.pdf
    {"Marca": "Consubanco (CSB)", "Monto": 150000.0, "Plazo_Meses": 60, "Pago_Quincenal": 4643.34, "CAT": 26.7, "Tasa": 23.88},
    {"Marca": "Consubanco (CSB)", "Monto": 150500.0, "Plazo_Meses": 60, "Pago_Quincenal": 4658.81, "CAT": 26.7, "Tasa": 23.88},
    {"Marca": "Consubanco (CSB)", "Monto": 151000.0, "Plazo_Meses": 60, "Pago_Quincenal": 4674.29, "CAT": 26.7, "Tasa": 23.88},
    {"Marca": "Consubanco (CSB)", "Monto": 180000.0, "Plazo_Meses": 60, "Pago_Quincenal": 5572.00, "CAT": 26.7, "Tasa": 23.88},
    {"Marca": "Consubanco (CSB)", "Monto": 200000.0, "Plazo_Meses": 60, "Pago_Quincenal": 6191.11, "CAT": 26.7, "Tasa": 23.88},
    {"Marca": "Consubanco (CSB)", "Monto": 300000.0, "Plazo_Meses": 60, "Pago_Quincenal": 9286.67, "CAT": 26.7, "Tasa": 23.88},
    
    # OPC (Opcipres IMSS) - Basado en OPC 4689 (1).pdf
    {"Marca": "Opcipres (OPC)", "Monto": 75000.0, "Plazo_Meses": 60, "Pago_Quincenal": 2416.78, "CAT": 28.9, "Tasa": 25.68},
    {"Marca": "Opcipres (OPC)", "Monto": 80000.0, "Plazo_Meses": 60, "Pago_Quincenal": 2577.90, "CAT": 28.9, "Tasa": 25.68},
    {"Marca": "Opcipres (OPC)", "Monto": 100000.0, "Plazo_Meses": 60, "Pago_Quincenal": 3222.38, "CAT": 28.9, "Tasa": 25.68},
    {"Marca": "Opcipres (OPC)", "Monto": 108000.0, "Plazo_Meses": 60, "Pago_Quincenal": 3480.17, "CAT": 28.9, "Tasa": 25.68},
    {"Marca": "Opcipres (OPC)", "Monto": 110000.0, "Plazo_Meses": 60, "Pago_Quincenal": 3544.62, "CAT": 28.9, "Tasa": 25.68},
    {"Marca": "Opcipres (OPC)", "Monto": 150000.0, "Plazo_Meses": 60, "Pago_Quincenal": 4833.57, "CAT": 28.9, "Tasa": 25.68},
    
    # Mas Nómina (MN)
    {"Marca": "Mas Nomina (MN)", "Monto": 50000.0, "Plazo_Meses": 48, "Pago_Quincenal": 1800.00, "CAT": 29.5, "Tasa": 26.00},
    {"Marca": "Mas Nomina (MN)", "Monto": 80000.0, "Plazo_Meses": 60, "Pago_Quincenal": 2700.00, "CAT": 28.0, "Tasa": 25.00},
    {"Marca": "Mas Nomina (MN)", "Monto": 100000.0, "Plazo_Meses": 60, "Pago_Quincenal": 3350.00, "CAT": 28.0, "Tasa": 25.00},
    
    # Consupago (CSP)
    {"Marca": "Consupago (CSP)", "Monto": 60000.0, "Plazo_Meses": 48, "Pago_Quincenal": 2100.00, "CAT": 30.1, "Tasa": 27.00},
    {"Marca": "Consupago (CSP)", "Monto": 90000.0, "Plazo_Meses": 60, "Pago_Quincenal": 2950.00, "CAT": 28.5, "Tasa": 25.50},
    {"Marca": "Consupago (CSP)", "Monto": 110000.0, "Plazo_Meses": 60, "Pago_Quincenal": 3490.00, "CAT": 28.5, "Tasa": 25.50},
]

df_base = pd.DataFrame(DATA_CREDITOS)

# --- PANEL DE ENTRADA DE DATOS ---
st.sidebar.header("Parámetros de Búsqueda")

# Entrada flexible de texto para permitir comas o puntos
capacidad_input = st.sidebar.text_input("Capacidad de crédito / Descuento Máximo ($):", value="3,500.00")

# Selección opcional de marcas específicas
marcas_disponibles = ["Todas", "Mas Nomina (MN)", "Consupago (CSP)", "Consubanco (CSB)", "Opcipres (OPC)"]
marca_seleccionada = st.sidebar.selectbox("Filtrar Marca:", marcas_disponibles)

# Limpieza y conversión del monto de capacidad
def parse_monto(val_str):
    try:
        cleaned = val_str.replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except ValueError:
        return None

capacidad_num = parse_monto(capacidad_input)

# --- LÓGICA DE CÁLCULO Y BÚSQUEDA ---
if capacidad_num is not None and capacidad_num > 0:
    st.subheader(f"Resultados para capacidad de pago máxima: **${capacidad_num:,.2f} quincenales**")
    
    # Filtrar créditos cuyo pago sea menor o igual a la capacidad
    df_viables = df_base[df_base["Pago_Quincenal"] <= capacidad_num].copy()
    
    if marca_seleccionada != "Todas":
        df_viables = df_viables[df_viables["Marca"] == marca_seleccionada]
        
    if df_viables.empty:
        st.warning("No se encontraron opciones de crédito que se ajusten a la capacidad ingresada.")
    else:
        # Obtener la opción con el pago quincenal más cercano (máximo) por cada Marca y Plazo
        idx_mejores = df_viables.groupby(["Marca", "Plazo_Meses"])["Pago_Quincenal"].idxmax()
        resultados = df_viables.loc[idx_mejores].sort_values(by=["Marca", "Plazo_Meses"])
        
        # Formatear la tabla de presentación
        resultados_display = resultados.copy()
        resultados_display["Monto Ofertado"] = resultados_display["Monto"].apply(lambda x: f"${x:,.2f}")
        resultados_display["Descuento Quincenal"] = resultados_display["Pago_Quincenal"].apply(lambda x: f"${x:,.2f}")
        resultados_display["Plazo"] = resultados_display["Plazo_Meses"].apply(lambda x: f"{x} meses")
        resultados_display["CAT"] = resultados_display["CAT"].apply(lambda x: f"{x}%")
        resultados_display["Tasa Anual"] = resultados_display["Tasa"].apply(lambda x: f"{x}%")
        
        cols_export = ["Marca", "Monto Ofertado", "Plazo", "Descuento Quincenal", "CAT", "Tasa Anual"]
        
        st.dataframe(
            resultados_display[cols_export],
            use_container_width=True,
            hide_index=True
        )
        
        # Resumen detallado en tarjetas por marca
        st.markdown("---")
        st.subheader("📌 Resumen de Opciones por Marca")
        
        cols = st.columns(len(resultados["Marca"].unique()))
        for i, (marca, group) in enumerate(resultados.groupby("Marca")):
            with cols[i % len(cols)]:
                st.markdown(f"### {marca}")
                for _, row in group.iterrows():
                    st.metric(
                        label=f"Plazo: {row['Plazo_Meses']} Meses",
                        value=f"${row['Monto']:,.2f}",
                        delta=f"Pago: ${row['Pago_Quincenal']:,.2f}/qna",
                        delta_color="normal"
                    )
                    st.caption(f"CAT: {row['CAT']}% | Tasa: {row['Tasa']}%")
else:
    st.error("Por favor ingrese un monto de capacidad válido (ejemplo: 3500 o 3,500.00).")
