import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Cotizador Multimarca de Crédito", layout="wide")

st.title("📊 Cotizador y Buscador de Crédito Multimarca")
st.write("Ingrese la capacidad de pago del cliente para evaluar las mejores opciones disponibles clasificadas por marca.")

# --- GENERADOR DINÁMICO DE TABLAS DE AMORTIZACIÓN ---
@st.cache_data
def generar_base_datos():
    registros = []
    
    # 1. Mas Nómina (MN 4766) - Plazos: 60, 48, 36, 24 meses
    factores_mn4766 = {60: 36.778, 48: 40.187, 36: 46.373, 24: 59.577}
    for monto in range(5000, 200500, 500):
        for plazo, factor in factores_mn4766.items():
            registros.append({
                "Marca": "Mas Nomina (MN 4766)",
                "Monto": float(monto),
                "Plazo_Meses": plazo,
                "Pago_Mensual": round((monto / 1000.0) * factor, 2),
                "CAT": 37.0,
                "Tasa_Anual": 31.89
            })

    # 2. Mas Nómina (MN 3772) - Plazo: 54 meses
    for monto in range(5000, 200500, 500):
        registros.append({
            "Marca": "Mas Nomina (MN 3772)",
            "Monto": float(monto),
            "Plazo_Meses": 54,
            "Pago_Mensual": round((monto / 1000.0) * 36.015, 2),
            "CAT": 32.9,
            "Tasa_Anual": 28.80
        })

    # 3. Opcipres (OPC 4689) - Plazos: 60, 48, 36, 24 meses
    factores_opc = {60: 32.2238, 48: 35.625, 36: 39.667, 24: 48.333}
    for monto in range(5000, 200500, 500):
        for plazo, factor in factores_opc.items():
            registros.append({
                "Marca": "Opcipres (OPC 4689)",
                "Monto": float(monto),
                "Plazo_Meses": plazo,
                "Pago_Mensual": round((monto / 1000.0) * factor, 2),
                "CAT": 28.9,
                "Tasa_Anual": 25.68
            })

    # 4. Consubanco (CSB 4707) - Plazos: 60, 48, 36, 24 meses
    factores_csb = {60: 30.9556, 48: 34.375, 36: 38.500, 24: 47.200}
    for monto in range(5000, 200500, 500):
        for plazo, factor in factores_csb.items():
            registros.append({
                "Marca": "Consubanco (CSB 4707)",
                "Monto": float(monto),
                "Plazo_Meses": plazo,
                "Pago_Mensual": round((monto / 1000.0) * factor, 2),
                "CAT": 26.7,
                "Tasa_Anual": 23.88
            })
            
    return pd.DataFrame(registros)

df_base = generar_base_datos()

# --- CÁLCULO DE TASAS MENSUALES ---
df_base["Tasa_Mensual_Sin_IVA"] = df_base["Tasa_Anual"] / 12.0
df_base["Tasa_Mensual_Con_IVA"] = (df_base["Tasa_Anual"] * 1.16) / 12.0

# --- PANEL LATERAL ---
st.sidebar.header("Parámetros de Búsqueda")

with st.sidebar.form(key="search_form"):
    capacidad_input = st.text_input("Capacidad de crédito / Descuento Máximo ($):", value="2,000.00")
    marcas_disponibles = ["Todas", "Mas Nomina (MN 4766)", "Mas Nomina (MN 3772)", "Consubanco (CSB 4707)", "Opcipres (OPC 4689)"]
    marca_seleccionada = st.selectbox("Filtrar Marca:", marcas_disponibles)
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
    
    # Filtrar créditos por capacidad
    df_viables = df_base[df_base["Pago_Mensual"] <= capacidad_num].copy()
    
    if marca_seleccionada != "Todas":
        df_viables = df_viables[df_viables["Marca"] == marca_seleccionada]
        
    if df_viables.empty:
        st.warning("No se encontraron opciones de crédito que se ajusten a la capacidad ingresada.")
    else:
        if incluir_iva:
            df_viables["Tasa_Mostrar"] = df_viables["Tasa_Mensual_Con_IVA"]
        else:
            df_viables["Tasa_Mostrar"] = df_viables["Tasa_Mensual_Sin_IVA"]

        # Obtener el MÁXIMO MONTO financiable para cada Marca y Plazo dentro del presupuesto
        idx_mejores = df_viables.groupby(["Marca", "Plazo_Meses"])["Monto"].idxmax()
        resultados = df_viables.loc[idx_mejores].copy()

        # Ordenar marcas por Tasa descendente y plazos descendentes
        resultados = resultados.sort_values(by=["Tasa_Mostrar", "Plazo_Meses", "Monto"], ascending=[False, False, False])

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
        st.subheader("📌 Opciones Disponibles Agrupadas por Marca")
        
        # AGRUPAR VISUALMENTE POR MARCA
        for marca, group in resultados.groupby("Marca", sort=False):
            st.markdown(f"### 🏷️ {marca}")
            
            cols = st.columns(min(len(group), 4))
            for idx, (_, row) in enumerate(group.iterrows()):
                col_target = cols[idx % 4]
                
                card_html = f"""
                <div style="border: 1px solid #0052cc; border-radius: 8px; margin-bottom: 15px; overflow: hidden; background-color: #ffffff; font-family: sans-serif; box-shadow: 0 2px 5px rgba(0,0,0,0.08);">
                    <div style="background-color: #0052cc; color: white; padding: 10px 12px; font-weight: bold; font-size: 13px; display: flex; justify-content: space-between; align-items: center;">
                        <span>{row['Plazo_Meses']} Mensual</span>
                        <span>Monto: ${row['Monto']:,.2f}</span>
                    </div>
                    <div style="padding: 12px; font-size: 12px; color: #333333;">
                        <div style="margin-bottom: 4px; font-weight: bold; color: #0052cc;">{row['Marca']}</div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span style="color: #666666;">Descuento:</span>
                            <span style="font-weight: bold; color: #000000;">${row['Pago_Mensual']:,.2f}</span>
                        </div>
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
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
    st.error("Por favor ingrese un monto de capacidad válido (ejemplo: 2000 o 2,000.00).")
