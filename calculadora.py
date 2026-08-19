import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Cotizador Multimarca de Crédito", layout="wide")

st.title("📊 Cotizador y Buscador de Crédito Multimarca")
st.write("Ingrese la capacidad de pago del cliente para evaluar las opciones disponibles en todos los plazos.")

# --- BASE DE DATOS EXTENDIDA CON MÚLTIPLES PLAZOS (60, 54, 48, 36, 24, 12 MESES) ---
DATA_CREDITOS = [
    # Consubanco (CSB 4707)
    {"Marca": "Consubanco (CSB 4707)", "Monto": 150000.0, "Plazo_Meses": 60, "Pago_Mensual": 4643.34, "CAT": 26.7, "Tasa_Anual": 23.88},
    {"Marca": "Consubanco (CSB 4707)", "Monto": 120000.0, "Plazo_Meses": 48, "Pago_Mensual": 4120.00, "CAT": 26.7, "Tasa_Anual": 23.88},
    {"Marca": "Consubanco (CSB 4707)", "Monto": 90000.0, "Plazo_Meses": 36, "Pago_Mensual": 3580.00, "CAT": 26.7, "Tasa_Anual": 23.88},
    {"Marca": "Consubanco (CSB 4707)", "Monto": 60000.0, "Plazo_Meses": 24, "Pago_Mensual": 3150.00, "CAT": 26.7, "Tasa_Anual": 23.88},
    {"Marca": "Consubanco (CSB 4707)", "Monto": 30000.0, "Plazo_Meses": 12, "Pago_Mensual": 2850.00, "CAT": 26.7, "Tasa_Anual": 23.88},

    # Opcipres (OPC 4689)
    {"Marca": "Opcipres (OPC 4689)", "Monto": 108000.0, "Plazo_Meses": 60, "Pago_Mensual": 3480.17, "CAT": 28.9, "Tasa_Anual": 25.68},
    {"Marca": "Opcipres (OPC 4689)", "Monto": 80000.0, "Plazo_Meses": 48, "Pago_Mensual": 2850.00, "CAT": 28.9, "Tasa_Anual": 25.68},
    {"Marca": "Opcipres (OPC 4689)", "Monto": 60000.0, "Plazo_Meses": 36, "Pago_Mensual": 2380.00, "CAT": 28.9, "Tasa_Anual": 25.68},
    {"Marca": "Opcipres (OPC 4689)", "Monto": 40000.0, "Plazo_Meses": 24, "Pago_Mensual": 2100.00, "CAT": 28.9, "Tasa_Anual": 25.68},
    {"Marca": "Opcipres (OPC 4689)", "Monto": 20000.0, "Plazo_Meses": 12, "Pago_Mensual": 1900.00, "CAT": 28.9, "Tasa_Anual": 25.68},

    # Mas Nómina (MN 4766)
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 100000.0, "Plazo_Meses": 60, "Pago_Mensual": 3350.00, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 80000.0, "Plazo_Meses": 48, "Pago_Mensual": 2980.00, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 60000.0, "Plazo_Meses": 36, "Pago_Mensual": 2680.00, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 40000.0, "Plazo_Meses": 24, "Pago_Mensual": 2380.00, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 20000.0, "Plazo_Meses": 12, "Pago_Mensual": 1950.00, "CAT": 37.0, "Tasa_Anual": 31.89},

    # Consupago (CSP 3772)
    {"Marca": "Consupago (CSP 3772)", "Monto": 110000.0, "Plazo_Meses": 60, "Pago_Mensual": 3490.00, "CAT": 32.9, "Tasa_Anual": 28.80},
    {"Marca": "Consupago (CSP 3772)", "Monto": 90000.0, "Plazo_Meses": 54, "Pago_Mensual": 3240.00, "CAT": 32.9, "Tasa_Anual": 28.80},
    {"Marca": "Consupago (CSP 3772)", "Monto": 70000.0, "Plazo_Meses": 48, "Pago_Mensual": 2886.48, "CAT": 32.9, "Tasa_Anual": 28.80},
    {"Marca": "Consupago (CSP 3772)", "Monto": 50000.0, "Plazo_Meses": 36, "Pago_Mensual": 2350.00, "CAT": 32.9, "Tasa_Anual": 28.80},
    {"Marca": "Consupago (CSP 3772)", "Monto": 30000.0, "Plazo_Meses": 24, "Pago_Mensual": 1820.00, "CAT": 32.9, "Tasa_Anual": 28.80},
    {"Marca": "Consupago (CSP 3772)", "Monto": 15000.0, "Plazo_Meses": 12, "Pago_Mensual": 1450.00, "CAT": 32.9, "Tasa_Anual": 28.80},
]

df_base = pd.DataFrame(DATA_CREDITOS)

# --- CÁLCULO PRECISO DE TASAS MENSUALES ---
df_base["Tasa_Mensual_Sin_IVA"] = df_base["Tasa_Anual"] / 12.0
df_base["Tasa_Mensual_Con_IVA"] = (df_base["Tasa_Anual"] * 1.16) / 12.0

# --- PANEL DE ENTRADA EN LA BARRA LATERAL ---
st.sidebar.header("Parámetros de Búsqueda")

with st.sidebar.form(key="search_form"):
    capacidad_input = st.text_input("Capacidad de crédito / Descuento Máximo ($):", value="3,500.00")
    marcas_disponibles = ["Todas", "Mas Nomina (MN 4766)", "Consupago (CSP 3772)", "Consubanco (CSB 4707)", "Opcipres (OPC 4689)"]
    marca_seleccionada = st.selectbox("Filtrar Marca:", marcas_disponibles)
    
    # Casilla para seleccionar si se requiere IVA
    incluir_iva = st.checkbox("Incluir IVA (16%) en Tasa Mensual", value=False)
    
    submit_button = st.form_submit_button(label="🔍 Calcular Oferta", use_container_width=True)

def parse_monto(val_str):
    try:
        cleaned = val_str.replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except ValueError:
        return None

capacidad_num = parse_monto(capacidad_input)

if capacidad_num is not None and capacidad_num > 0:
    st.subheader(f"Resultados para capacidad de pago máxima: **${capacidad_num:,.2f} mensuales**")
    
    # Filtrar créditos por capacidad de descuento
    df_viables = df_base[df_base["Pago_Mensual"] <= capacidad_num].copy()
    
    if marca_seleccionada != "Todas":
        df_viables = df_viables[df_viables["Marca"] == marca_seleccionada]
        
    if df_viables.empty:
        st.warning("No se encontraron opciones de crédito que se ajusten a la capacidad ingresada.")
    else:
        # Seleccionar la mejor oferta por CADA Marca y CADA Plazo alcanzado
        idx_mejores = df_viables.groupby(["Marca", "Plazo_Meses"])["Pago_Mensual"].idxmax()
        resultados = df_viables.loc[idx_mejores].sort_values(by=["Marca", "Plazo_Meses"], ascending=[True, False])
        
        # Selección de Tasa
        if incluir_iva:
            resultados["Tasa_Mostrar"] = resultados["Tasa_Mensual_Con_IVA"]
        else:
            resultados["Tasa_Mostrar"] = resultados["Tasa_Mensual_Sin_IVA"]

        # Tabla Resumen
        resultados_display = resultados.copy()
        resultados_display["Monto Ofertado"] = resultados_display["Monto"].apply(lambda x: f"${x:,.2f}")
        resultados_display["Descuento Mensual"] = resultados_display["Pago_Mensual"].apply(lambda x: f"${x:,.2f}")
        resultados_display["Plazo"] = resultados_display["Plazo_Meses"].apply(lambda x: f"{x} meses")
        resultados_display["CAT"] = resultados_display["CAT"].apply(lambda x: f"{x}%")
        resultados_display["Tasa Mensual"] = resultados_display["Tasa_Mostrar"].apply(lambda x: f"{x:.2f}%")
        
        cols_export = ["Marca", "Monto Ofertado", "Plazo", "Descuento Mensual", "CAT", "Tasa Mensual"]
        st.dataframe(resultados_display[cols_export], use_container_width=True, hide_index=True)
        
        st.markdown("---")
        st.subheader("📌 Resumen de Ofertas por Plazo Alcanzado")
        
        # Despliegue en Tarjetas por Marca y Plazo
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
                            <span style="font-weight: bold; color: #000000;">{row['Tasa_Mostrar']:.2f}%</span>
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
