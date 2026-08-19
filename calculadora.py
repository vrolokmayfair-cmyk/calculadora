import streamlit as st
import pandas as pd
import pdfplumber
import requests
import io
import re

# Configuración de página
st.set_page_config(page_title="Cotizador y Buscador de Crédito Multimarca", layout="wide")

st.title("📊 Cotizador y Buscador de Crédito Multimarca")
st.write("Consulta y filtrado directo desde los documentos PDF oficiales alojados en Google Drive.")

# ==============================================================================
# ENLACES DIRECTOS A LOS DOCUMENTOS PDF EN GOOGLE DRIVE
# ==============================================================================
ENLACES_PDF = {
    "Mas Nomina (MN 4766)": {
        "url": "https://drive.google.com/uc?export=download&id=17Z4j3lt8-WDJ9BVIQVeRilwqVqdzhlCX",
        "CAT": 37.0,
        "Tasa_Anual": 31.89
    },
    "Mas Nomina (MN 3772)": {
        "url": "https://drive.google.com/uc?export=download&id=1lYTpq6vhwJh8xzwlwAXl4LG4tcrWeN65",
        "CAT": 32.9,
        "Tasa_Anual": 28.80
    },
    "Opcipres (OPC 4689)": {
        "url": "https://drive.google.com/uc?export=download&id=1SqPnw8a94-3-aa5rgr-fF9CeEuT9iTcI",
        "CAT": 28.9,
        "Tasa_Anual": 25.68
    },
    "Consubanco (CSB 4707)": {
        "url": "https://drive.google.com/uc?export=download&id=1D4bA086uIUNdA99ush5ljfPyOHiyR6Z7",
        "CAT": 26.7,
        "Tasa_Anual": 23.88
    }
}

# ==============================================================================
# FUNCIÓN DE EXTRACCIÓN DIRECTA DE TABLAS DESDE GOOGLE DRIVE
# ==============================================================================
@st.cache_data(ttl=86400) # Cachea los datos durante 24 horas para mantener velocidad
def extraer_tablas_desde_drive():
    registros = []
    
    for marca, info in ENLACES_PDF.items():
        try:
            response = requests.get(info["url"])
            if response.status_code == 200:
                pdf_file = io.BytesIO(response.content)
                
                with pdfplumber.open(pdf_file) as pdf:
                    for page in pdf.pages:
                        tables = page.extract_tables()
                        for table in tables:
                            for row in table:
                                # Limpieza y extracción de columnas numéricas del PDF
                                row_cleaned = [str(cell).strip() for cell in row if cell is not None]
                                
                                # Filtrar filas numéricas que contienen montos y pagos
                                if len(row_cleaned) >= 3:
                                    try:
                                        monto_str = re.sub(r"[^\d.]", "", row_cleaned[0].replace(",", ""))
                                        pago_str = re.sub(r"[^\d.]", "", row_cleaned[-1].replace(",", ""))
                                        
                                        monto = float(monto_str)
                                        pago = float(pago_str)
                                        
                                        # Identificación básica de plazo (ejemplo: 60, 54, 48, 36, 24)
                                        plazo = 60
                                        for elem in row_cleaned:
                                            if elem in ["60", "54", "48", "36", "24"]:
                                                plazo = int(elem)
                                                break
                                                
                                        if monto > 0 and pago > 0:
                                            registros.append({
                                                "Marca": marca,
                                                "Monto": monto,
                                                "Plazo_Meses": plazo,
                                                "Pago_Mensual": pago,
                                                "CAT": info["CAT"],
                                                "Tasa_Anual": info["Tasa_Anual"]
                                            })
                                    except ValueError:
                                        continue
        except Exception as e:
            st.error(f"Error al conectar con el PDF de {marca}: {e}")
            
    return pd.DataFrame(registros)

# Cargar base de datos leyendo los PDF en tiempo real
with st.spinner("Conectando y leyendo tablas oficiales desde Google Drive..."):
    df_base = extraer_tablas_desde_drive()

# ==============================================================================
# PANEL LATERAL DE CONTROLES
# ==============================================================================
st.sidebar.header("Parámetros de Búsqueda")

with st.sidebar.form(key="search_form", clear_on_submit=False):
    capacidad_input = st.text_input(
        "Capacidad de crédito / Descuento Máximo ($):", 
        value="10,000.00"
    )
    
    marcas_disponibles = ["Todas"] + list(ENLACES_PDF.keys())
    marca_seleccionada = st.selectbox("Filtrar Marca:", marcas_disponibles)
    incluir_iva = st.checkbox("Incluir IVA (16%) en Tasa Mensual", value=False)
    
    btn_cotizar = st.form_submit_button(label="🔍 Calcular Oferta", use_container_width=True)

# Limpieza de entrada
def parse_monto_limpio(val_str):
    if not val_str:
        return None
    limpio = re.sub(r"[^\d.]", "", str(val_str))
    try:
        val = float(limpio)
        return val if val > 0 else None
    except ValueError:
        return None

capacidad_num = parse_monto_limpio(capacidad_input)

# Cálculo exigido de tasa mensual (Tasa Anual / 12)
if not df_base.empty:
    if incluir_iva:
        df_base["Tasa_Mostrar"] = (df_base["Tasa_Anual"] * 1.16) / 12.0
    else:
        df_base["Tasa_Mostrar"] = df_base["Tasa_Anual"] / 12.0

# ==============================================================================
# LÓGICA DE BÚSQUEDA SOBRE LA EXTRACCIÓN EN VIVO
# ==============================================================================
if capacidad_num is not None and not df_base.empty:
    st.subheader(f"Resultados para capacidad de pago máxima: **${capacidad_num:,.2f} mensuales**")
    
    # 1. Filtrar filas con pago mensual menor o igual a la capacidad
    df_viables = df_base[df_base["Pago_Mensual"] <= capacidad_num].copy()
    
    if marca_seleccionada != "Todas":
        df_viables = df_viables[df_viables["Marca"] == marca_seleccionada]
        
    if df_viables.empty:
        st.warning("⚠️ No aplican opciones de crédito para la capacidad ingresada.")
    else:
        # 2. Seleccionar el MÁXIMO MONTO financiable para cada Marca y Plazo
        idx_mejores = df_viables.groupby(["Marca", "Plazo_Meses"])["Monto"].idxmax()
        resultados = df_viables.loc[idx_mejores].copy()

        # Ordenar por Tasa (descendente), Plazo (descendente) y Monto
        resultados = resultados.sort_values(by=["Tasa_Mostrar", "Plazo_Meses", "Monto"], ascending=[False, False, False])

        # 3. Presentación en Tabla
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
        
        # 4. Tarjetas Informativas
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
    st.error("Por favor ingrese un monto de capacidad válido (ejemplo: 10000 o 10,000.00).")
