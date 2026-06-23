

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
import os

# ── Configuración de página ────────────────────────────────────────────────────
st.set_page_config(
    page_title="Gestión de Arriendos",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CONFIGURACIÓN DEL ARCHIVO Y LOGO ───────────────────────────────────────────
ARCHIVO_EXCEL = "Arriendos_Grupo_Alqueria.xlsx"
HOJA_EXCEL    = "RELACION CONTRATOS"
LOGOTIPO_SIDEBAR = "alqueria_logo.png" 

# ── PALETA CORPORATIVA ALQUERÍA ────────────────────────────────────────────────
ROJO      = "#ec1c2e"
ROJO_OSC  = "#9B0D22"
BLANCO    = "#FFFFFF"
GRIS_CLAR = "#F8F8F8"
GRIS_MED  = "#ECECEC"
NEGRO_PURO = "#000000"
NEGRO_TEXT = "#1A1A1A"

NEGRO_CAJAS = "#000000"
BLANCO_CAJAS_TEXTO = "#FFFFFF"

CSS = f"""
<style>
    /* Fondo general claro */
    .stApp {{ 
        background-color: {BLANCO} !important; 
        color: {NEGRO_TEXT} !important; 
    }}
    
    /* Barra lateral fija en Rojo Alquería */
    [data-testid="stSidebar"], [data-testid="stSidebar"] > div:first-child {{ 
        background-color: {ROJO} !important; 
    }}
    
    /* Centrar e integrar el logo corporativo */
    [data-testid="stSidebar"] [data-testid="stImage"] {{
        text-align: center;
        display: block;
        margin-left: auto;
        margin-right: auto;
        padding-top: 10px;
        padding-bottom: 15px;
    }}

    /* Destruir menús flotantes e iconos del logo en el sidebar */
    [data-testid="stSidebar"] [data-testid="stImageActionButton"],
    [data-testid="stSidebar"] button[title="Expand image"],
    [data-testid="stSidebar"] [data-testid="stElementToolbar"] {{
        display: none !important;
        opacity: 0 !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }}
    [data-testid="stSidebar"] [data-testid="stImage"] img {{
        pointer-events: none !important;
    }}

    /* Textos de las etiquetas de filtros en Sidebar (Títulos) */
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stMultiSelect label,
    [data-testid="stSidebar"] .stSlider label,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] div[data-testid="stWidgetLabel"] p {{
        color: {BLANCO} !important;
        font-weight: 700 !important;
    }}

    /* Cajas de selección (Selectbox y Multiselect) en el Sidebar */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {{
        background-color: {NEGRO_CAJAS} !important;
        color: {BLANCO_CAJAS_TEXTO} !important;
        border: 1px solid {GRIS_MED} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] [data-testid="stMarkdownContainer"] p {{
        color: {BLANCO_CAJAS_TEXTO} !important;
    }}
    [data-testid="stSidebar"] div[data-baseweb="select"] svg {{
        fill: {BLANCO_CAJAS_TEXTO} !important;
    }}

    /* Ajustar las etiquetas internas cuando ya hay elementos seleccionados en Multiselect */
    [data-testid="stSidebar"] div[data-baseweb="select"] div[data-testid="stMultiSelectFloatingTags"] span {{
        background-color: #333333 !important;
        color: {BLANCO} !important;
    }}

    /* ── 🎨 HERRAMIENTA DESLIZABLE EN NEGRO SÓLIDO ── */
    [data-testid="stSidebar"] div[data-testid="stSlider"] div[role="slider"] {{
        background-color: {NEGRO_PURO} !important;
        border: 2px solid {BLANCO} !important;
        box-shadow: 0px 2px 4px rgba(0,0,0,0.4) !important;
    }}
    [data-testid="stSidebar"] div[data-testid="stSlider"] div[data-disabled="false"] > div > div > div {{
        background: {NEGRO_PURO} !important;
    }}
    [data-testid="stSidebar"] div[data-testid="stSlider"] div[data-disabled="false"] > div > div {{
        background: {NEGRO_PURO} !important;
    }}
    [data-testid="stSidebar"] div[data-testid="stSlider"] div[data-testid="stWidgetLabel"] + div div {{
        color: {BLANCO} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stSidebar"] [role="presentation"] div {{
        color: {BLANCO} !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }}
    [data-testid="stSidebar"] div[data-testid="stSlider"] span {{
        color: {BLANCO} !important;
        font-weight: 700 !important;
    }}

    /* ── 🛠️ BARRA DE HERRAMIENTAS DE LA TABLA SIEMPRE VISIBLE ── */
    [data-testid="stDataFrame"] [data-testid="stElementToolbar"] {{
        position: absolute !important;
        top: -38px !important;
        right: 5px !important;
        background-color: {GRIS_CLAR} !important;
        border: 1px solid {GRIS_MED} !important;
        border-radius: 4px !important;
        padding: 2px 6px !important;
        z-index: 99 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
    }}

    [data-testid="stDataFrame"] div:hover [data-testid="stElementToolbar"],
    [data-testid="stDataFrame"] [data-testid="stElementToolbar"] * {{
        opacity: 1 !important;
        visibility: visible !important;
        display: flex !important;
    }}

    [data-testid="stDataFrame"] {{
        position: relative !important;
        margin-top: 45px !important;
    }}

    /* ── 📐 FRANJA ROJA DE CABECERA COMPARTIDA ── */
    .header-bar-container {{
        background: {ROJO};
        padding: 15px 25px;
        border-radius: 8px;
        margin-bottom: 22px;
    }}
    .header-text h1 {{ color: {BLANCO} !important; margin: 0; font-size: 1.8rem; font-weight: 700; }}
    .header-text p  {{ color: {BLANCO} !important; margin: 4px 0 0; font-size: 0.95rem; font-weight: 500; }}
    
    /* Costo Real Integrado en la Franja Roja (AGRANDADO) */
    .header-kpi-box {{
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 6px;
        padding: 10px 18px;
        text-align: right;
    }}
    .header-kpi-value {{ font-size: 2.1rem; font-weight: 800; color: {BLANCO} !important; line-height: 1.1; }}
    .header-kpi-label {{ font-size: 0.85rem; color: {BLANCO} !important; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; opacity: 0.95; margin-top: 3px; }}

    /* Tarjetas KPI de Abajo (AGRANDADOS) */
    .kpi-card {{
        background: {GRIS_CLAR} !important;
        border-left: 6px solid {ROJO} !important;
        border-radius: 6px;
        padding: 18px 22px;
        text-align: center;
        box-shadow: 0 1px 4px rgba(0,0,0,0.15);
    }}
    .kpi-value {{ font-size: 2.2rem; font-weight: 800; color: {NEGRO_PURO} !important; line-height: 1.1; }}
    .kpi-label {{ font-size: 0.95rem; color: {NEGRO_TEXT} !important; font-weight: 700; text-transform: uppercase; letter-spacing: .05em; margin-top: 4px; }}
    
    .stDownloadButton button {{
        background-color: {BLANCO} !important;
        color: {NEGRO_PURO} !important;
        border: 2px solid {ROJO_OSC} !important;
        border-radius: 6px;
        font-weight: 700 !important;
    }}
    div.stButton > button {{
        background-color: {ROJO} !important;
        color: {BLANCO} !important;
        border: none;
        border-radius: 6px;
        font-weight: 700;
    }}
    div[data-testid="stTabs"] button [data-testid="stMarkdownContainer"] p {{
        color: {NEGRO_TEXT} !important;
    }}
    div[data-testid="stTabs"] button[aria-selected="true"] [data-testid="stMarkdownContainer"] p {{
        color: {ROJO} !important;
    }}
    
    h2, h3, h4 {{ color: {NEGRO_PURO} !important; font-weight: 700 !important; }}
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] caption {{ color: {BLANCO} !important; }}

    .grafico-scroll-container {{
        max-height: 450px;
        overflow-y: auto;
        overflow-x: hidden;
        padding-right: 10px;
    }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── Carga de datos ────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos(path, hoja):
    try:
        df = pd.read_excel(path, sheet_name=hoja, header=1)
    except Exception as e:
        st.error(f"❌ Error al abrir la hoja '{hoja}': {e}")
        st.stop()
        
    df.columns = df.columns.astype(str).str.strip()
    df = df.dropna(how="all")
    
    columnas_texto = ["ARTICULO", "CIA", "Direccion completa", "Ciudad", "Area asume Gasto", "Nombre de PROVEEDOR", "CONTRATO", "PRECIO REAL"]
    for col in columnas_texto:
        if col in df.columns:
            df[col] = df[col].fillna("").astype(str).str.strip()
            df[col] = df[col].replace(["None", "NaN", "null"], "")
            
    if "PRECIO" in df.columns:
        precios_limpios = df["PRECIO"].astype(str).str.strip()
        precios_limpios = precios_limpios.str.replace("$", "", regex=False)
        precios_limpios = precios_limpios.str.replace(" ", "", regex=False)
        precios_limpios = precios_limpios.str.replace(".", "", regex=False)
        precios_limpios = precios_limpios.str.replace(",", ".", regex=False)
        df["PRECIO NEGOCIADOR"] = pd.to_numeric(precios_limpios, errors='coerce').fillna(0).astype(float)
    else:
        df["PRECIO NEGOCIADOR"] = 0.0

    if "PRECIO REAL" in df.columns:
        if pd.api.types.is_numeric_dtype(df["PRECIO REAL"]):
            df["PRECIO REAL NUM"] = pd.to_numeric(df["PRECIO REAL"], errors='coerce').fillna(0).astype(float)
        else:
            precios_reales_limpios = df["PRECIO REAL"].astype(str).str.strip()
            precios_reales_limpios = precios_reales_limpios.str.replace("$", "", regex=False)
            precios_reales_limpios = precios_reales_limpios.str.replace(" ", "", regex=False)
            precios_reales_limpios = precios_reales_limpios.str.replace(",", ".", regex=False)
            df["PRECIO REAL NUM"] = pd.to_numeric(precios_reales_limpios, errors='coerce').fillna(0).astype(float)
    else:
        df["PRECIO REAL NUM"] = 0.0
        
    for col in ["FECHA INICIO", "FECHA FIN"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
            
    return df

# ── Funciones de Semáforo ──────────────────────────────────────────────────────
def semaforo(fecha_fin):
    if pd.isna(fecha_fin):
        return "⚪ Sin fecha"
    try:
        hoy   = date.today()
        delta = (fecha_fin.date() - hoy).days
        if delta < 0:
            return "🔴 Vencido"
        elif delta <= 60:
            return "🟡 Próximo (≤60 días)"
        elif delta <= 180:
            return "🟠 Atención (≤180 días)"
        else:
            return "🟢 Vigente"
    except:
        return "⚪ Sin fecha"

def dias_restantes(fecha_fin):
    if pd.isna(fecha_fin):
        return None
    try:
        return (fecha_fin.date() - date.today()).days
    except:
        return None

if not os.path.exists(ARCHIVO_EXCEL):
    st.error(f"❌ No se encontró el archivo **{ARCHIVO_EXCEL}**.")
    st.stop()

df_raw = cargar_datos(ARCHIVO_EXCEL, HOJA_EXCEL)

if "FECHA FIN" in df_raw.columns:
    df_raw["SEMAFORO"]      = df_raw["FECHA FIN"].apply(semaforo)
    df_raw["DÍAS RESTANTES"] = df_raw["FECHA FIN"].apply(dias_restantes)
else:
    df_raw["SEMAFORO"]      = "⚪ Sin fecha"
    df_raw["DÍAS RESTANTES"] = None

def mapear_columna_contrato(valor):
    if pd.isna(valor):
        return "No especifica"
    txt = str(valor).strip().lower()
    if txt in ["", "none", "nan", "null", "n/a"]:
        return "No especifica"
    elif txt == "si" or txt == "sí":
        return "Sí"
    elif "no" in txt:
        return "No"
    return "No especifica"

if "CONTRATO" in df_raw.columns:
    df_raw["TIENE_CONTRATO_FLG"] = df_raw["CONTRATO"].apply(mapear_columna_contrato)
else:
    df_raw["TIENE_CONTRATO_FLG"] = "No especifica"

# ── Sidebar – LOGO Y FILTROS ───────────────────────────────────────────────────
try:
    st.sidebar.image(LOGOTIPO_SIDEBAR, use_container_width=True)
except Exception as e:
    st.sidebar.caption("⚠️ [Configura la ruta del Logo en la variable LOGOTIPO_SIDEBAR]")

st.sidebar.markdown("## 🔍 Filtros")

lista_ciudades = ["Todas"]
if "Ciudad" in df_raw.columns:
    ciudades_unicas = [c for c in df_raw["Ciudad"].unique() if c != ""]
    lista_ciudades += sorted(ciudades_unicas)
ciudad_sel = st.sidebar.selectbox("Ciudad / Municipio", lista_ciudades)

areas = ["Todas"]
if "CIA" in df_raw.columns:
    areas_unicas = [a for a in df_raw["CIA"].unique() if a != ""]
    areas += sorted(areas_unicas)
area_sel = st.sidebar.selectbox("Compañía (CIA)", areas)

p_min = 0
p_max = int(df_raw["PRECIO NEGOCIADOR"].max()) if "PRECIO NEGOCIADOR" in df_raw.columns else 150000000

valores_escala = list(range(p_min, p_max + 500000, 500000))
if p_max not in valores_escala:
    valores_escala.append(p_max)

def formatear_con_puntos(valor):
    return f"${valor:,}".replace(",", ".")

rango_precio_fmt = st.sidebar.select_slider(
    "Rango de precio ($)",
    options=valores_escala,
    value=(p_min, valores_escala[-1]),
    format_func=formatear_con_puntos
)

estados_opciones = ["Todos", "🔴 Vencido", "🟡 Próximo (≤60 días)", "🟠 Atención (≤180 días)", "🟢 Vigente", "⚪ Sin fecha"]
estado_sel = st.sidebar.multiselect("Clasificación por vigencia", estados_opciones[1:], default=[])

contrato_opciones = ["Todos", "Sí", "No", "No especifica"]
contrato_sel = st.sidebar.selectbox("¿Tiene contrato?", contrato_opciones)

st.sidebar.markdown("---")
st.sidebar.caption("Dashboard v1.0 | Gestión Inmobiliaria")

# ── Aplicar filtros globales ───────────────────────────────────────────────────
df = df_raw.copy()

if ciudad_sel != "Todas" and "Ciudad" in df.columns:
    df = df[df["Ciudad"] == ciudad_sel]

if area_sel != "Todas" and "CIA" in df.columns:
    df = df[df["CIA"] == area_sel]

if "PRECIO NEGOCIADOR" in df.columns:
    df = df[
        (df["PRECIO NEGOCIADOR"] >= rango_precio_fmt[0]) &
        (df["PRECIO NEGOCIADOR"] <= rango_precio_fmt[1])
    ]

if estado_sel:
    df = df[df["SEMAFORO"].isin(estado_sel)]

if contrato_sel != "Todos":
    df = df[df["TIENE_CONTRATO_FLG"] == contrato_sel]

# ── Procesamiento de KPIs y Totales ───────────────────────────────────────────
df_principales = df[df["ARTICULO"] != ""]

total_contratos = len(df_principales)
vencidos        = (df_principales["SEMAFORO"] == "🔴 Vencido").sum()
proximos        = (df_principales["SEMAFORO"] == "🟡 Próximo (≤60 días)").sum()
vigentes        = (df_principales["SEMAFORO"] == "🟢 Vigente").sum()

costo_real_total = df_principales["PRECIO REAL NUM"].sum()

str_costo_real = "${:,.0f}".format(costo_real_total).replace(",", "X").replace(".", ",").replace("X", ".")

# ── Encabezado Principal Integrado en Columnas ───────────────────────────────
st.markdown(f"""
<div class="header-bar-container">
    <table style="width:100%; border:none; background:transparent; margin:0; padding:0;">
        <tr style="background:transparent; border:none;">
            <td style="width:68%; text-align:left; vertical-align:middle; border:none; padding:0;">
                <div class="header-text">
                    <h1>🏢 Gestión de Arriendos</h1>
                    <p>Panel de control y clasificación por vigencia de contratos</p>
                </div>
            </td>
            <td style="width:32%; text-align:right; vertical-align:middle; border:none; padding:0;">
                <div class="header-kpi-box">
                    <div class="header-kpi-value">{str_costo_real}</div>
                    <div class="header-kpi-label">Costo Total Mensual</div>
                </div>
            </td>
        </tr>
    </table>
</div>
""", unsafe_allow_html=True)

# ── Fila de KPIs (4 tarjetas robustas con tipografía más grande) ───────────────
k1, k2, k3, k4 = st.columns(4)
for col, val, label in [
    (k1, f"{total_contratos:,}",  "Total Contratos"),
    (k2, str(vigentes),            "🟢 Vigentes"),
    (k3, str(proximos),            "🟡 Próximos a vencer"),
    (k4, str(vencidos),            "🔴 Vencidos"),
]:
    with col:
        st.markdown(f"""
        <div class="kpi-card">
          <div class="kpi-value">{val}</div>
          <div class="kpi-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Tabs ───────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Contratos", "🚦 Clasificación por Vigencia", "📊 Análisis", "📥 Exportar"
])

# TAB 1 – Tabla de contratos
with tab1:
    st.subheader(f"Contratos filtrados ({len(df)})")
    cols_mostrar = [
        c for c in [
            "ARTICULO", "CIA", "Ciudad", "Direccion completa", "Area asume Gasto",
            "Administrador contrato", "Centro Costo", "DESCRIPCIÓN",
            "Nombre de PROVEEDOR", "PRECIO", "PRECIO REAL", "NEGOCIADOR", "CONTRATO", "FECHA INICIO",
            "FECHA FIN", "DÍAS RESTANTES", "SEMAFORO", "DURACION", "AJUSTE", "Vigencia"
        ] if c in df.columns
    ]
    if len(df) > 0:
        st.dataframe(
            df[cols_mostrar].sort_values("DÍAS RESTANTES") if "DÍAS RESTANTES" in cols_mostrar else df[cols_mostrar],
            use_container_width=True, height=450, on_select="ignore",
            column_config={
                "FECHA INICIO": st.column_config.DateColumn("FECHA INICIO", format="DD/MM/YYYY"),
                "FECHA FIN": st.column_config.DateColumn("FECHA FIN", format="DD/MM/YYYY"),
            }
        )
    else:
        st.info("No hay contratos que coincidan con los filtros seleccionados.")

# TAB 2 – Clasificación por Vigencia
with tab2:
    if len(df_principales) > 0:
        df_pie_data = df_principales.copy()
        
        mapa_nombres_grafica = {
            "🔴 Vencido": "Vencido",
            "🟡 Próximo (≤60 días)": "Próximo (≤60 días)",
            "🟠 Atención (≤180 días)": "Atención (≤180 días)",
            "🟢 Vigente": "Vigente",
            "⚪ Sin fecha": "Sin Fecha"
        }
        df_pie_data["Estado_Grafica"] = df_pie_data["SEMAFORO"].map(mapa_nombres_grafica)
        
        conteo_semaforo = df_pie_data["Estado_Grafica"].value_counts().reset_index()
        conteo_semaforo.columns = ["Estado", "Cantidad"]

        color_map = {
            "Vencido":              "#C8102E",
            "Próximo (≤60 días)":   "#F59E0B",
            "Atención (≤180 días)": "#F97316",
            "Vigente":              "#16A34A",
            "Sin Fecha":            "#9CA3AF",
        }

        fig_pie = px.pie(
            conteo_semaforo, names="Estado", values="Cantidad",
            color="Estado", color_discrete_map=color_map,
            hole=0.55
        )
        
        fig_pie.update_traces(
            textposition="outside",
            textinfo="label+percent",
            domain=dict(x=[0.1, 0.9], y=[0.1, 0.9]),
            textfont=dict(size=13, color="#000000", family="Arial, sans-serif", weight="bold"),
            hovertemplate="<b>%{label}</b><br>Cantidad: %{value}<br>Porcentaje: %{percent}<extra></extra>"
        )
        
        fig_pie.update_layout(
            showlegend=False,  
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(t=25, b=25, l=25, r=25),
            height=400
        )

        c1, c2 = st.columns([1.4, 1.6])
        estado_dinamico = None

        with c1:
            st.markdown("### 📊 Distribución por Estado")
            seleccion = st.plotly_chart(fig_pie, use_container_width=True, on_select="rerun")
            
            st.markdown("<p style='font-size:0.95rem; font-weight:bold; color:#000000; margin-bottom:10px; margin-left:5px;'>Guía de Estados:</p>", unsafe_allow_html=True)
            leg_cols = st.columns(2)
            with leg_cols[0]:
                st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#16A34A; margin-bottom:8px;'>🟢 Vigente</div>", unsafe_allow_html=True)
                st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#F59E0B; margin-bottom:8px;'>🟡 Próximo (≤60 días)</div>", unsafe_allow_html=True)
                st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#9CA3AF;'>⚪ Sin Fecha</div>", unsafe_allow_html=True)
            with leg_cols[1]:
                st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#C8102E; margin-bottom:8px;'>🔴 Vencido</div>", unsafe_allow_html=True)
                st.markdown("<div style='font-size:0.95rem; font-weight:700; color:#F97316; margin-bottom:8px;'>🟠 Atención (≤180 días)</div>", unsafe_allow_html=True)

        mapa_inverso = {
            "Vencido": "🔴 Vencido",
            "Próximo (≤60 días)": "🟡 Próximo (≤60 días)",
            "Atención (≤180 días)": "🟠 Atención (≤180 días)",
            "Vigente": "🟢 Vigente",
            "Sin Fecha": "⚪ Sin fecha"
        }

        if seleccion and "selection" in seleccion:
            puntos = seleccion["selection"]["points"]
            if puntos:
                label_grafica = puntos[0].get("label")
                estado_dinamico = mapa_inverso.get(label_grafica)

        with c2:
            st.markdown("<div style='margin-top: 12px;'></div>", unsafe_allow_html=True)
            if estado_dinamico:
                st.markdown(f"### 📋 Registros Filtrados: {estado_dinamico}")
                df_tabla_vigencia = df_principales[df_principales["SEMAFORO"] == estado_dinamico]
            else:
                st.markdown("### 📋 Vista General: Contratos Críticos (≤60 días)")
                df_tabla_vigencia = df_principales[df_principales["SEMAFORO"].isin(["🔴 Vencido", "🟡 Próximo (≤60 días)"])]

            cols_crit = [c for c in ["ARTICULO", "CIA", "Ciudad", "Nombre de PROVEEDOR", "PRECIO", "PRECIO REAL", "FECHA FIN", "DÍAS RESTANTES", "SEMAFORO"] if c in df_principales.columns]
            
            if len(df_tabla_vigencia) > 0:
                st.dataframe(
                    df_tabla_vigencia[cols_crit].sort_values("DÍAS RESTANTES") if "DÍAS RESTANTES" in cols_crit else df_tabla_vigencia[cols_crit],
                    use_container_width=True, height=400,
                    column_config={ "FECHA FIN": st.column_config.DateColumn("FECHA FIN", format="DD/MM/YYYY") }
                )
            else:
                st.info("No se encontraron registros para esta selección.")
    else:
        st.info("Sin datos para graficar.")

# TAB 3 – Análisis
with tab3:
    if len(df_principales) > 0:
        st.markdown("## 📊 Análisis de Costos")
        col1, col2 = st.columns(2)

        COLOR_ROJO_ALQUERIA = "#ec1c2e"
        COLOR_TEXTO = "#1A1A1A"
        COLOR_GRID = "#E5E7EB"

        if "CIA" in df_principales.columns and "PRECIO REAL NUM" in df_principales.columns:
            with col1:
                st.markdown("### 📉 Costo total mensual por Compañía (CIA)")
                df_grafica_cia = df_principales[df_principales["CIA"] != ""].copy()
                costo_cia = df_grafica_cia.groupby("CIA")["PRECIO REAL NUM"].sum().reset_index().sort_values("PRECIO REAL NUM", ascending=True)
                costo_cia["PRECIO_MILLONES"] = costo_cia["PRECIO REAL NUM"] / 1000000
                max_cia = costo_cia["PRECIO_MILLONES"].max() if not costo_cia.empty else 100
                
                fig_cia = px.bar(
                    costo_cia, y="CIA", x="PRECIO_MILLONES", orientation="h",
                    color_discrete_sequence=[COLOR_ROJO_ALQUERIA],
                    text=costo_cia["PRECIO_MILLONES"].apply(lambda v: "${:,.1f}M".format(v).replace(",", "X").replace(".", ",").replace("X", ".")),
                )
                
                fig_cia.update_traces(
                    textposition="outside", cliponaxis=False,
                    textfont=dict(color=COLOR_TEXTO, size=12, weight="bold")
                )
                
                fig_cia.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10, b=30, l=80, r=40),
                    font=dict(color=COLOR_TEXTO, size=12),
                    xaxis=dict(title="Costo (Millones COP)", range=[0, max_cia * 1.2], 
                               title_font=dict(color=COLOR_TEXTO, size=12, weight="bold"),
                               tickfont=dict(color=COLOR_TEXTO), gridcolor=COLOR_GRID),
                    yaxis=dict(title="Compañía", title_font=dict(color=COLOR_TEXTO, size=12, weight="bold"),
                               tickfont=dict(color=COLOR_TEXTO)),
                    height=420
                )
                st.plotly_chart(fig_cia, use_container_width=True)

        if "Area asume Gasto" in df_principales.columns and "PRECIO REAL NUM" in df_principales.columns:
            with col2:
                st.markdown("### 📉 Costo por Área que asume Gasto")
                df_grafica_area = df_principales[df_principales["Area asume Gasto"] != ""].copy()
                costo_area = df_grafica_area.groupby("Area asume Gasto")["PRECIO REAL NUM"].sum().reset_index().sort_values("PRECIO REAL NUM", ascending=True)
                costo_area["PRECIO_MILLONES"] = costo_area["PRECIO REAL NUM"] / 1000000
                total_barras = len(costo_area)
                
                fig_area = px.bar(
                    costo_area, y="Area asume Gasto", x="PRECIO_MILLONES", orientation="h",
                    color_discrete_sequence=[COLOR_ROJO_ALQUERIA],
                    text=costo_area["PRECIO_MILLONES"].apply(lambda v: "${:,.1f}M".format(v).replace(",", "X").replace(".", ",").replace("X", ".")),
                )
                
                fig_area.update_traces(
                    textposition="outside", cliponaxis=False,
                    textfont=dict(color=COLOR_TEXTO, size=12, weight="bold")
                )
                
                fig_area.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(t=10, b=30, l=150, r=40),
                    font=dict(color=COLOR_TEXTO, size=12),
                    xaxis=dict(title="Costo (Millones COP)", range=[0, costo_area["PRECIO_MILLONES"].max() * 1.2],
                               title_font=dict(color=COLOR_TEXTO, size=12, weight="bold"),
                               tickfont=dict(color=COLOR_TEXTO), gridcolor=COLOR_GRID),
                    yaxis=dict(type='category', title="Área",
                               range=[max(0, total_barras - 9), total_barras],
                               title_font=dict(color=COLOR_TEXTO, size=12, weight="bold"),
                               tickfont=dict(color=COLOR_TEXTO)),
                    height=420
                )
                st.plotly_chart(fig_area, use_container_width=True)
    else:
        st.info("Sin datos para analizar.")

# TAB 4 – Exportar
with tab4:
    st.subheader("📥 Exportar datos filtrados")
    if len(df) > 0:
        st.write(f"Exportar {len(df)} filas de registros con los filtros actuales.")

        @st.cache_data
        def to_excel(dataframe):
            from io import BytesIO
            with pd.ExcelWriter(buf := BytesIO(), engine="openpyxl") as writer:
                dataframe.to_excel(writer, index=False, sheet_name="Arriendos")
            return buf.getvalue()

        excel_bytes = to_excel(df)
        st.download_button(label=" Descargar Excel filtrado", data=excel_bytes, file_name="arriendos_filtrado.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

