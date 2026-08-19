import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Cotizador Multimarca de Crédito", layout="wide")

st.title("📊 Cotizador y Buscador de Crédito Multimarca")
st.write("Ingrese la capacidad de pago del cliente para evaluar las mejores opciones disponibles en cada marca.")

# --- BASE DE DATOS DE TABLAS DE AMORTIZACIÓN CON TASAS ANUALES ---
DATA_CREDITOS = [
    # CSB (Consubanco IMSS) - Material 4707
    {"Marca": "Consubanco (CSB 4707)", "Monto": 150000.0, "Plazo_Meses": 60, "Pago_Mensual": 4643.34, "CAT": 26.7, "Tasa_Anual": 23.88},
    {"Marca": "Consubanco (CSB 4707)", "Monto": 150500.0, "Plazo_Meses": 60, "Pago_Mensual": 4658.81, "CAT": 26.7, "Tasa_Anual": 23.88},
    {"Marca": "Consubanco (CSB 4707)", "Monto": 151000.0, "Plazo_Meses": 60, "Pago_Mensual": 4674.29, "CAT": 26.7, "Tasa_Anual": 23.88},
    {"Marca": "Consubanco (CSB 4707)", "Monto": 180000.0, "Plazo_Meses": 60, "Pago_Mensual": 5572.00, "CAT": 26.7, "Tasa_Anual": 23.88},
    {"Marca": "Consubanco (CSB 4707)", "Monto": 200000.0, "Plazo_Meses": 60, "Pago_Mensual": 6191.11, "CAT": 26.7, "Tasa_Anual": 23.88},
    {"Marca": "Consubanco (CSB 4707)", "Monto": 300000.0, "Plazo_Meses": 60, "Pago_Mensual": 9286.67, "CAT": 26.7, "Tasa_Anual": 23.88},
    
    # OPC (Opcipres IMSS) - Material 4689
    {"Marca": "Opcipres (OPC 4689)", "Monto": 75000.0, "Plazo_Meses": 60, "Pago_Mensual": 2416.78, "CAT": 28.9, "Tasa_Anual": 25.68},
    {"Marca": "Opcipres (OPC 4689)", "Monto": 80000.0, "Plazo_Meses": 60, "Pago_Mensual": 2577.90, "CAT": 28.9, "Tasa_Anual": 25.68},
    {"Marca": "Opcipres (OPC 4689)", "Monto": 100000.0, "Plazo_Meses": 60, "Pago_Mensual": 3222.38, "CAT": 28.9, "Tasa_Anual": 25.68},
    {"Marca": "Opcipres (OPC 4689)", "Monto": 108000.0, "Plazo_Meses": 60, "Pago_Mensual": 3480.17, "CAT": 28.9, "Tasa_Anual": 25.68},
    {"Marca": "Opcipres (OPC 4689)", "Monto": 110000.0, "Plazo_Meses": 60, "Pago_Mensual": 3544.62, "CAT": 28.9, "Tasa_Anual": 25.68},
    {"Marca": "Opcipres (OPC 4689)", "Monto": 150000.0, "Plazo_Meses": 60, "Pago_Mensual": 4833.57, "CAT": 28.9, "Tasa_Anual": 25.68},
    
    # Mas Nómina (MN) - Material 4766
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 50000.0, "Plazo_Meses": 48, "Pago_Mensual": 1800.00, "CAT": 29.5, "Tasa_Anual": 26.00},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 80000.0, "Plazo_Meses": 60, "Pago_Mensual": 2700.00, "CAT": 28.0, "Tasa_Anual": 25.00},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 100000.0, "Plazo_Meses": 60, "Pago_Mensual": 3350.00, "CAT": 28.0, "Tasa_Anual": 25.00},
    
    # Consupago (CSP) - Material 3772
    {"Marca": "Consupago (CSP 3772)", "Monto": 60000.0, "Plazo_Meses": 48, "Pago_Mensual": 2100.00, "CAT": 30.1, "Tasa_Anual": 27.00},
    {"Marca": "Consupago (CSP 3772)", "Monto": 90000.0, "Plazo_Meses": 60, "Pago_Mensual": 2950.00, "CAT": 28.5, "Tasa_Anual": 25.50},
    {"Marca": "Consupago (CSP 3772)", "Monto": 110000.0, "Plazo_Meses": 60, "Pago_Mensual": 3490.00, "CAT": 28.5, "Tasa_Anual": 25.50},
]

df_base = pd.DataFrame(DATA_CREDITOS)

# CÁLCULO AUTOMÁTICO DE TASA MENSUAL (División entre 12)
df_base["Tasa_Mensual"] = df_base["Tasa_Anual"] / 12.0

# --- PANEL DE ENTRADA CON FORMULARIO (SOPORTA BOTÓN Y ENTER) ---
st.sidebar.header("Parámetros de Búsqueda")

with st.sidebar.form(key="search_form"):
    capacidad_input = st.text_input("Capacidad de crédito / Descuento Máximo ($):", value="3,500.00")
    marcas_disponibles = ["Todas", "Mas Nomina (MN 4766)", "Consupago (CSP 3772)", "Consubanco (CSB 4707)", "Opcipres (OPC 4689)"]
    marca_seleccionada = st.selectbox("Filtrar Marca:", marcas_disponibles)
    
    submit_button = st.form_submit_button(label="🔍 Calcular Oferta", use_container_width=True)

# Limpieza y conversión del monto de capacidad
def parse_monto(val_str):
    try:
        cleaned = val_str.replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except ValueError:
        return None

capacidad_num = parse_monto(capacidad_input)

# --- LÓGICA DE CÁLCULO Y DESPLIEGUE ---
if capacidad_num is not None and capacidad_num > 0:
    st.subheader(f"Resultados para capacidad de pago máxima: **${capacidad_num:,.2f} mensuales**")
    
    # Filtrar créditos cuyo pago sea menor o igual a la capacidad
    df_viables = df_base[df_base["Pago_Mensual"] <= capacidad_num].copy()
    
    if marca_seleccionada != "Todas":
        df_viables = df_viables[df_viables["Marca"] == marca_seleccionada]
        
    if df_viables.empty:
        st.warning("No se encontraron opciones de crédito que se ajusten a la capacidad ingresada.")
    else:
        # Obtener la mejor opción por cada marca y plazo
        idx_mejores = df_viables.groupby(["Marca", "Plazo_Meses"])["Pago_Mensual"].idxmax()
        resultados = df_viables.loc[idx_mejores].sort_values(by=["Marca", "Plazo_Meses"], ascending=[True, False])
        
        # Tabla resumen con formato
        resultados_display = resultados.copy()
        resultados_display["Monto Ofertado"] = resultados_display["Monto"].apply(lambda x: f"${x:,.2f}")
        resultados_display["Descuento Mensual"] = resultados_display["Pago_Mensual"].apply(lambda x: f"${x:,.2f}")
        resultados_display["Plazo"] = resultados_display["Plazo_Meses"].apply(lambda x: f"{x} meses")
        resultados_display["CAT"] = resultados_display["CAT"].apply(lambda x: f"{x}%")
        resultados_display["Tasa Mensual"] = resultados_display["Tasa_Mensual"].apply(lambda x: f"{x:.2f}%")
        
        cols_export = ["Marca", "Monto Ofertado", "Plazo", "Descuento Mensual", "CAT", "Tasa Mensual"]
        
        st.dataframe(
            resultados_display[cols_export],
            use_container_width=True,
            hide_index=True
        )
        
        st.markdown("---")
        st.subheader("📌 Resumen de Ofertas")
        
        # Agrupar y desplegar tipo catálogo por Marca
        for marca, group in resultados.groupby("Marca"):
            st.markdown(f"### 🏷️ {marca}")
            
            cols = st.columns(min(len(group), 4))
            
            for idx, (_, row) in enumerate(group.iterrows()):
                col_target = cols[idx % 4]
                
                card_html = f"""
                <div style="border: 1px solid #0052cc; border-radius: 8px; margin-bottom: 15px; overflow: hidden; background-color: #ffffff; font-family: sans-serif; box-shadow: 0 2px 5px rgba(0,0,0,0.08);">
                    <div style="background-color: #0052cc; color: white; padding: 10px 12px; font-weight: bold; font-size: 14px; display: flex; justify-content: space-between; align-items: center;">
                        <span>{row['Plazo_Meses']} Mensual</span>
                        <span>Monto: ${row['Monto']:,.2f}</span>
                    </div>
                    <div style="padding: 12px; font-size: 13px; color: #333333;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                            <span style="color: #666666;">Descuento:</span>
                            <span style="font-weight: bold; color: #000000;">${row['Pago_Mensual']:,.2f}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
                            <span style="color: #666666;">Tasa mensual:</span>
                            <span style="font-weight: bold; color: #000000;">{row['Tasa_Mensual']:.2f}%</span>
                        </div>
                        <div style="display: flex; justify-content: space-between;">
                            <span style="color: #666666;">CAT:</span>
                            <span style="font-weight: bold; color: #000000;">{row['CAT']}%</span>
                        </div>
                    </div>
                </div>
                """
                col_target.markdown(card_html, unsafe_allow_html=True)
else:
    st.error("Por favor ingrese un monto de capacidad válido (ejemplo: 3500 o 3,500.00).")
