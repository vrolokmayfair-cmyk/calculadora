import streamlit as st
import pandas as pd

# Configuración de página
st.set_page_config(page_title="Cotizador Multimarca de Crédito", layout="wide")

st.title("📊 Cotizador y Buscador de Crédito Multimarca")
st.write("Consulta exacta de ofertas extraídas directamente de los PDF oficiales sin variaciones de centavos.")

# ==============================================================================
# BASE DE DATOS EXACTA Y REVISADA CONTRA HOJAS IMPRESAS OFICIALES
# ==============================================================================
DATA_CREDITOS = [
    # --------------------------------------------------------------------------
    # 1. MAS NÓMINA (MN 4766) - Tasa Anual 31.89%, CAT 37.0%
    # --------------------------------------------------------------------------
    # Plazo 60 Meses
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 10000.0, "Plazo_Meses": 60, "Pago_Mensual": 367.78, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 20000.0, "Plazo_Meses": 60, "Pago_Mensual": 735.57, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 30000.0, "Plazo_Meses": 60, "Pago_Mensual": 1103.35, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 40000.0, "Plazo_Meses": 60, "Pago_Mensual": 1471.14, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 50000.0, "Plazo_Meses": 60, "Pago_Mensual": 1838.92, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 55500.0, "Plazo_Meses": 60, "Pago_Mensual": 2041.20, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 70000.0, "Plazo_Meses": 60, "Pago_Mensual": 2574.48, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 70500.0, "Plazo_Meses": 60, "Pago_Mensual": 2592.87, "CAT": 37.0, "Tasa_Anual": 31.89},

    # Plazo 48 Meses
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 10000.0, "Plazo_Meses": 48, "Pago_Mensual": 401.87, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 50500.0, "Plazo_Meses": 48, "Pago_Mensual": 2029.43, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 55500.0, "Plazo_Meses": 48, "Pago_Mensual": 2230.36, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 64000.0, "Plazo_Meses": 48, "Pago_Mensual": 2571.99, "CAT": 37.0, "Tasa_Anual": 31.89},

    # Plazo 36 Meses
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 10000.0, "Plazo_Meses": 36, "Pago_Mensual": 463.73, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 44000.0, "Plazo_Meses": 36, "Pago_Mensual": 2040.41, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 55500.0, "Plazo_Meses": 36, "Pago_Mensual": 2573.72, "CAT": 37.0, "Tasa_Anual": 31.89},

    # Plazo 24 Meses
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 10000.0, "Plazo_Meses": 24, "Pago_Mensual": 595.77, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 34000.0, "Plazo_Meses": 24, "Pago_Mensual": 2025.62, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 43000.0, "Plazo_Meses": 24, "Pago_Mensual": 2561.81, "CAT": 37.0, "Tasa_Anual": 31.89},
    {"Marca": "Mas Nomina (MN 4766)", "Monto": 55500.0, "Plazo_Meses": 24, "Pago_Mensual": 3306.53, "CAT": 37.0, "Tasa_Anual": 31.89},

    # --------------------------------------------------------------------------
    # 2. MAS NÓMINA (MN 3772) - Tasa Anual 28.80%, CAT 32.9%
    # --------------------------------------------------------------------------
    {"Marca": "Mas Nomina (MN 3772)", "Monto": 10000.0, "Plazo_Meses": 54, "Pago_Mensual": 360.15, "CAT": 32.9, "Tasa_Anual": 28.80},
    {"Marca": "Mas Nomina (MN 3772)", "Monto": 20000.0, "Plazo_Meses": 54, "Pago_Mensual": 720.31, "CAT": 32.9, "Tasa_Anual": 28.80},
    {"Marca": "Mas Nomina (MN 3772)", "Monto": 30000.0, "Plazo_Meses": 54, "Pago_Mensual": 1080.46, "CAT": 32.9, "Tasa_Anual": 28.80},
    {"Marca": "Mas Nomina (MN 3772)", "Monto": 40000.0, "Plazo_Meses": 54, "Pago_Mensual": 1440.62, "CAT": 32.9, "Tasa_Anual": 28.80},
    {"Marca": "Mas Nomina (MN 3772)", "Monto": 56500.0, "Plazo_Meses": 54, "Pago_Mensual": 2034.87, "CAT": 32.9, "Tasa_Anual": 28.80},
    {"Marca": "Mas Nomina (MN 3772)", "Monto": 71500.0, "Plazo_Meses": 54, "Pago_Mensual": 2575.10, "CAT": 32.9, "Tasa_Anual": 28.80},  # <--- Corregido exacto a la imagen del PDF

    # --------------------------------------------------------------------------
    # 3. OPCIPRES (OPC 4689) - Tasa Anual 25.68%, CAT 28.9%
    # --------------------------------------------------------------------------
    {"Marca": "Opcipres (OPC 4689)", "Monto": 75000.0, "Plazo_Meses": 60, "Pago_Mensual": 2416.78, "CAT": 28.9, "Tasa_Anual": 25.68},
    {"Marca": "Opcipres (OPC 4689)", "Monto": 80000.0, "Plazo_Meses": 60, "Pago_Mensual": 2577.90, "CAT": 28.9, "Tasa_Anual": 25.68},

    # --------------------------------------------------------------------------
    # 4. CONSUBANCO (CSB 4707) - Tasa Anual 23.88%, CAT 26.7%
    # --------------------------------------------------------------------------
    {"Marca": "Consubanco (CSB 4707)", "Monto": 150000.0, "Plazo_Meses": 60, "Pago_Mensual": 4643.34, "CAT": 26.7, "Tasa_Anual": 23.88},
    {"Marca": "Consubanco (CSB 4707)", "Monto": 160000.0, "Plazo_Meses": 60, "Pago_Mensual": 4952.89, "CAT": 26.7, "Tasa_Anual": 23.88},
]

df_base = pd.DataFrame(DATA_CREDITOS)

# --- CONTROLES LATERALES REACTIVOS ---
st.sidebar.header("Parámetros de Búsqueda")

capacidad_input = st.sidebar.text_input("Capacidad de crédito / Descuento Máximo ($):", value="2,591.79")
marcas_disponibles = ["Todas"] + list(df_base["Marca"].unique())
marca_seleccionada = st.sidebar.selectbox("Filtrar Marca:", marcas_disponibles)
incluir_iva = st.sidebar.checkbox("Incluir IVA (16%) en Tasa Mensual", value=False)

def parse_monto(val_str):
    try:
        cleaned = val_str.replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except ValueError:
        return None

capacidad_num = parse_monto(capacidad_input)

# La tasa mensual se obtiene estrictamente dividiendo la tasa anual entre 12
if incluir_iva:
    df_base["Tasa_Mostrar"] = (df_base["Tasa_Anual"] * 1.16) / 12.0
else:
    df_base["Tasa_Mostrar"] = df_base["Tasa_Anual"] / 12.0

if capacidad_num is not None and capacidad_num > 0:
    st.subheader(f"Resultados para capacidad de pago máxima: **${capacidad_num:,.2f} mensuales**")
    
    df_viables = df_base[df_base["Pago_Mensual"] <= capacidad_num].copy()
    
    if marca_seleccionada != "Todas":
        df_viables = df_viables[df_viables["Marca"] == marca_seleccionada]
        
    if df_viables.empty:
        st.warning("⚠️ No aplican créditos para la capacidad ingresada.")
    else:
        idx_mejores = df_viables.groupby(["Marca", "Plazo_Meses"])["Monto"].idxmax()
        resultados = df_viables.loc[idx_mejores].copy()

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
    st.error("Por favor ingrese un monto de capacidad válido (ejemplo: 2591.79).")
