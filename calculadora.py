import streamlit as st
import pandas as pd
import math

# Configuración de página
st.set_page_config(page_title="Cotizador Multimarca de Crédito", layout="wide")

st.title("📊 Cotizador y Buscador de Crédito Multimarca")
st.write("Ingrese la capacidad de pago del cliente para evaluar las opciones exactas disponibles clasificadas por marca.")

# --- PARÁMETROS FINANCIEROS Y FACTORES EXACTOS POR MATERIAL Y PLAZO ---
MATRICULA_COTIZADORES = {
    "Mas Nomina (MN 4766)": {
        "CAT": 37.0,
        "Tasa_Anual": 31.89,
        "Plazos": {
            60: 36.7777,
            48: 40.1867,
            36: 46.3728,
            24: 59.5768
        }
    },
    "Mas Nomina (MN 3772)": {
        "CAT": 32.9,
        "Tasa_Anual": 28.80,
        "Plazos": {
            54: 36.0155
        }
    },
    "Opcipres (OPC 4689)": {
        "CAT": 28.9,
        "Tasa_Anual": 25.68,
        "Plazos": {
            60: 32.2237,
            48: 35.6248,
            36: 39.6665,
            24: 48.3331
        }
    },
    "Consubanco (CSB 4707)": {
        "CAT": 26.7,
        "Tasa_Anual": 23.88,
        "Plazos": {
            60: 30.9556,
            48: 34.3750,
            36: 38.5000,
            24: 47.2000
        }
    }
}

# --- CÁLCULO DINÁMICO EXACTO BASADO EN CAPACIDAD ---
def calcular_oferta_exacta(capacidad_pago, marca_filtro, incluir_iva):
    resultados = []
    
    for marca, info in MATRICULA_COTIZADORES.items():
        if marca_filtro != "Todas" and marca != marca_filtro:
            continue
            
        cat = info["CAT"]
        tasa_anual = info["Tasa_Anual"]
        tasa_mensual = (tasa_anual * 1.16 / 12.0) if incluir_iva else (tasa_anual / 12.0)
        
        for plazo, factor in info["Plazos"].items():
            # Obtener el monto máximo ajustado en múltiplos de $500
            monto_bruto = (capacidad_pago / factor) * 1000.0
            monto_escalonado = math.floor(monto_bruto / 500.0) * 500.0
            
            if monto_escalonado >= 5000.0:
                if monto_escalonado > 1000000.0:
                    monto_escalonado = 1000000.0
                
                # Pago mensual exacto
                pago_exacto = round((monto_escalonado / 1000.0) * factor, 2)
                
                # Ajuste de seguridad si el redondeo sobrepasa por centavos la capacidad
                if pago_exacto > capacidad_pago and monto_escalonado >= 5500.0:
                    monto_escalonado -= 500.0
                    pago_exacto = round((monto_escalonado / 1000.0) * factor, 2)
                
                resultados.append({
                    "Marca": marca,
                    "Monto": monto_escalonado,
                    "Plazo_Meses": plazo,
                    "Pago_Mensual": pago_exacto,
                    "CAT": cat,
                    "Tasa_Anual": tasa_anual,
                    "Tasa_Mostrar": tasa_mensual
                })
                
    return pd.DataFrame(resultados)

# --- PANEL LATERAL ---
st.sidebar.header("Parámetros de Búsqueda")

with st.sidebar.form(key="search_form"):
    capacidad_input = st.text_input("Capacidad de crédito / Descuento Máximo ($):", value="10,801.15")
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
    
    df_resultados = calcular_oferta_exacta(capacidad_num, marca_seleccionada, incluir_iva)
    
    if df_resultados.empty:
        st.warning("No se encontraron opciones de crédito que se ajusten a la capacidad ingresada.")
    else:
        # Ordenar marcas por Tasa descendente y plazos descendentes
        resultados = df_resultados.sort_values(by=["Tasa_Mostrar", "Plazo_Meses", "Monto"], ascending=[False, False, False])

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
    st.error("Por favor ingrese un monto de capacidad válido (ejemplo: 10801.15).")
