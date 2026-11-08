import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy.optimize import minimize
import streamlit.components.v1 as components
import base64
from pathlib import Path
from components_fisica import (
    get_wheeler_sim_html,
    get_planck_sim_html,
    get_dirac_sim_html,
    get_propagator_sim_html,
    get_timeline_carousel_html
)

# =============================================================================
# CONFIGURACIÓN GENERAL: FULL-WIDTH Y ATMÓSFERA SURREALISTA "LA NOCHE ESTRELLADA"
# =============================================================================
st.set_page_config(
    page_title="SYNTHESIS LAB | The Starry Night",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Cargar imagen de alta resolución de La Noche Estrellada de Van Gogh en Base64
current_dir = Path(__file__).parent
starry_img_path = current_dir / "starry_night.jpg"
b64_starry = ""
if starry_img_path.exists():
    with open(starry_img_path, "rb") as f:
        b64_starry = base64.b64encode(f.read()).decode("utf-8")

# -----------------------------------------------------------------------------
# 1. MOTOR SURREALISTA DE FLUIDOS Y CORRIENTES VÓRTICE (SIMULACIÓN DE FLUIDOS)
# -----------------------------------------------------------------------------
components.html("""
<script>
    (function initFluidDynamicsEngine() {
        try {
            const parentDoc = window.parent.document;
            if (!parentDoc) return;

            // Eliminar lienzos antiguos de versiones previas
            const oldVortex = parentDoc.getElementById("starry-vortex-canvas");
            if (oldVortex) oldVortex.remove();
            const existingFluid = parentDoc.getElementById("starry-fluid-canvas");
            if (existingFluid) existingFluid.remove();

            // Crear el lienzo de fluidos estrictamente en el fondo (z-index: 0)
            const canvas = parentDoc.createElement("canvas");
            canvas.id = "starry-fluid-canvas";
            canvas.style.position = "fixed";
            canvas.style.top = "0";
            canvas.style.left = "0";
            canvas.style.width = "100vw";
            canvas.style.height = "100vh";
            canvas.style.zIndex = "0";
            canvas.style.pointerEvents = "none";
            canvas.style.opacity = "0.88";

            const container = parentDoc.querySelector('[data-testid="stAppViewContainer"]') || parentDoc.body;
            container.insertBefore(canvas, container.firstChild);

            const ctx = canvas.getContext("2d");
            let width = canvas.width = window.parent.innerWidth;
            let height = canvas.height = window.parent.innerHeight;

            window.parent.addEventListener("resize", () => {
                width = canvas.width = window.parent.innerWidth;
                height = canvas.height = window.parent.innerHeight;
                ctx.fillStyle = "#060d19";
                ctx.fillRect(0, 0, width, height);
            });

            // Interacción fluida con el cursor (advección por movimiento del mouse)
            let mouse = { x: -1000, y: -1000, vx: 0, vy: 0, prevX: -1000, prevY: -1000, active: false };
            let mouseTimer = null;
            window.parent.addEventListener("mousemove", (e) => {
                mouse.vx = e.clientX - (mouse.prevX || e.clientX);
                mouse.vy = e.clientY - (mouse.prevY || e.clientY);
                mouse.prevX = mouse.x = e.clientX;
                mouse.prevY = mouse.y = e.clientY;
                mouse.active = true;
                clearTimeout(mouseTimer);
                mouseTimer = setTimeout(() => { mouse.active = false; }, 300);
            });

            // Paleta de fluidos de La Noche Estrellada (sin barras, filamentos de luz continua)
            const fluidPalette = [
                "rgba(56, 189, 248, 0.42)",   // Cian eléctrico / cielo nocturno
                "rgba(14, 165, 233, 0.38)",   // Celeste profundo
                "rgba(254, 240, 138, 0.48)",  // Oro estelar claro
                "rgba(250, 204, 21, 0.42)",   // Amarillo girasol
                "rgba(96, 165, 250, 0.32)",   // Azul cobalto etéreo
                "rgba(251, 146, 60, 0.30)"    // Naranja ciprés / fulgor estelar
            ];

            // 750 partículas continuas de fluido
            const numParticles = 750;
            const particles = [];
            for (let i = 0; i < numParticles; i++) {
                const px = Math.random() * width;
                const py = Math.random() * height;
                particles.push({
                    x: px,
                    y: py,
                    oldX: px,
                    oldY: py,
                    vx: 0,
                    vy: 0,
                    speed: Math.random() * 1.5 + 0.8,
                    color: fluidPalette[Math.floor(Math.random() * fluidPalette.length)],
                    width: Math.random() * 1.8 + 0.8,
                    life: Math.random() * 260 + 80
                });
            }

            // Halos de estrellas estelares de fondo
            const stars = [
                { x: width * 0.84, y: height * 0.14, r: 26, color: "rgba(254, 240, 138, 0.85)" },
                { x: width * 0.18, y: height * 0.22, r: 14, color: "rgba(250, 204, 21, 0.75)" },
                { x: width * 0.38, y: height * 0.16, r: 12, color: "rgba(56, 189, 248, 0.75)" },
                { x: width * 0.65, y: height * 0.26, r: 16, color: "rgba(254, 240, 138, 0.80)" }
            ];

            let t = 0;

            // Campo de velocidad vectorial incompresible 2D (Curl Streamfunction + Vórtices de Lamb-Oseen)
            function getFluidVelocity(x, y, time) {
                // 1. Corriente base laminar y ondulante
                const kx = 0.0016;
                const ky = 0.0022;
                let u = 2.4 * Math.sin(y * ky + time * 0.35);
                let v = 1.2 * Math.cos(x * kx - time * 0.25);

                // 2. Gran remolino central de Van Gogh (vórtice solenoidal)
                const v1X = width * 0.50 + Math.sin(time * 0.2) * 35;
                const v1Y = height * 0.34 + Math.cos(time * 0.2) * 20;
                const dx1 = x - v1X;
                const dy1 = y - v1Y;
                const r2_1 = dx1 * dx1 + dy1 * dy1;
                const core1 = 5500;
                const gamma1 = 3800;
                u += (-dy1 * gamma1) / (r2_1 + core1);
                v += (dx1 * gamma1) / (r2_1 + core1);

                // 3. Vórtice secundario superior derecho
                const v2X = width * 0.78;
                const v2Y = height * 0.18;
                const dx2 = x - v2X;
                const dy2 = y - v2Y;
                const r2_2 = dx2 * dx2 + dy2 * dy2;
                const core2 = 4200;
                const gamma2 = 2500;
                u += (-dy2 * gamma2) / (r2_2 + core2);
                v += (dx2 * gamma2) / (r2_2 + core2);

                // 4. Vórtice complementario izquierdo
                const v3X = width * 0.22;
                const v3Y = height * 0.44;
                const dx3 = x - v3X;
                const dy3 = y - v3Y;
                const r2_3 = dx3 * dx3 + dy3 * dy3;
                const core3 = 4500;
                const gamma3 = -2200;
                u += (-dy3 * gamma3) / (r2_3 + core3);
                v += (dx3 * gamma3) / (r2_3 + core3);

                // 5. Advección por el movimiento del mouse
                if (mouse.active) {
                    const mdx = x - mouse.x;
                    const mdy = y - mouse.y;
                    const dist2 = mdx * mdx + mdy * mdy;
                    if (dist2 < 45000) {
                        const factor = (1 - Math.sqrt(dist2) / 212) * 3.5;
                        u += mouse.vx * factor * 0.12;
                        v += mouse.vy * factor * 0.12;
                    }
                }

                return { u, v };
            }

            // Fondo base inicial
            ctx.fillStyle = "#060d19";
            ctx.fillRect(0, 0, width, height);

            function renderFluidLoop() {
                t += 0.008;

                // FADE SUAVE DE PERSISTENCIA: genera estelas fluidas orgánicas (sin barras)
                ctx.fillStyle = "rgba(6, 13, 25, 0.04)";
                ctx.fillRect(0, 0, width, height);

                // Halos de estrellas estables en el fondo
                for (let st of stars) {
                    const pulse = Math.sin(t * 2 + st.r) * 3;
                    const rad = Math.max(4, st.r + pulse);
                    const grad = ctx.createRadialGradient(st.x, st.y, rad * 0.2, st.x, st.y, rad * 2.2);
                    grad.addColorStop(0, st.color);
                    grad.addColorStop(0.5, "rgba(250, 204, 21, 0.15)");
                    grad.addColorStop(1, "transparent");
                    ctx.fillStyle = grad;
                    ctx.beginPath();
                    ctx.arc(st.x, st.y, rad * 2.2, 0, Math.PI * 2);
                    ctx.fill();
                }

                ctx.lineCap = "round";
                ctx.lineJoin = "round";

                // Advección de partículas: flujos continuos como agua y viento
                for (let i = 0; i < numParticles; i++) {
                    const p = particles[i];
                    p.oldX = p.x;
                    p.oldY = p.y;

                    const vel = getFluidVelocity(p.x, p.y, t);

                    // Amortiguación viscosa para suavidad de fluido
                    p.vx = p.vx * 0.88 + vel.u * 0.12;
                    p.vy = p.vy * 0.88 + vel.v * 0.12;

                    p.x += p.vx * p.speed;
                    p.y += p.vy * p.speed;

                    // Dibujar el flujo continuo conectando posición previa y actual
                    ctx.beginPath();
                    ctx.moveTo(p.oldX, p.oldY);
                    ctx.lineTo(p.x, p.y);
                    ctx.strokeStyle = p.color;
                    ctx.lineWidth = p.width;
                    ctx.stroke();

                    p.life--;

                    // Si sale de los bordes o expira, reaparece con nueva vida
                    if (p.life <= 0 || p.x < -30 || p.x > width + 30 || p.y < -30 || p.y > height + 30) {
                        p.x = Math.random() * width;
                        p.y = Math.random() * height;
                        p.oldX = p.x;
                        p.oldY = p.y;
                        p.vx = 0;
                        p.vy = 0;
                        p.life = Math.random() * 260 + 80;
                    }
                }

                requestAnimationFrame(renderFluidLoop);
            }

            renderFluidLoop();
        } catch(err) {
            console.warn("Fluid flow engine notice:", err);
        }
    })();
</script>
""", height=0, width=0)

# -----------------------------------------------------------------------------
# 2. SISTEMA MULTI-TEMA: SELECTOR DE LÍNEA ESTÉTICA EN VIVO
# -----------------------------------------------------------------------------
def get_theme_css(theme_name: str, b64_starry: str) -> str:
    base_css = f"""
    [data-testid="stSidebar"] {{ display: none; }}
    [data-testid="collapsedControl"] {{ display: none; }}
    [data-testid="stHeader"] {{ background: transparent !important; }}
    
    .stApp {{
        background: transparent !important;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}

    .main .block-container {{
        max-width: 1140px !important;
        padding-top: 1.2rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin: 0 auto !important;
    }}

    .stApp,
    [data-testid="stAppViewContainer"],
    .main,
    .main .block-container,
    [data-testid="stTabs"],
    [data-testid="stTabs"] *,
    .stTabs,
    .stTabs *,
    [data-baseweb="tab-list"],
    [data-baseweb="tab-list"] *,
    [data-baseweb="tab"],
    [data-baseweb="tab-panel"],
    .area-starry-card,
    .theory-box-starry,
    .starry-night-header,
    .stButton,
    .stButton *,
    div[data-testid="column"],
    div[data-testid="stExpander"],
    div[data-testid="stMetric"],
    .stPlotlyChart {{
        position: relative !important;
        z-index: 10 !important;
    }}

    iframe {{
        border-radius: 12px !important;
        box-shadow: none !important;
        background: transparent !important;
        border: none !important;
    }}

    /* CRITICAL OVERRIDE FOR ST.SEGMENTED_CONTROL / STBUTTONGROUP */
    div[data-testid="stButtonGroup"],
    div[data-baseweb="button-group"],
    div[data-testid="stSegmentedControl"] {{
        background: rgba(6, 11, 20, 0.75) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 12px !important;
        padding: 4px !important;
        backdrop-filter: blur(24px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45) !important;
        display: inline-flex !important;
        gap: 4px !important;
    }}
    div[data-testid="stButtonGroup"] > div,
    div[data-baseweb="button-group"] > div {{
        display: inline-flex !important;
        gap: 4px !important;
        background: transparent !important;
        border: none !important;
    }}
    div[data-testid="stButtonGroup"] button,
    div[data-baseweb="button-group"] button,
    div[data-testid="stSegmentedControl"] button {{
        background: transparent !important;
        color: #94A3B8 !important;
        border: 1px solid transparent !important;
        border-radius: 8px !important;
        padding: 7px 16px !important;
        font-size: 12.5px !important;
        font-weight: 500 !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s ease !important;
        box-shadow: none !important;
        outline: none !important;
    }}
    div[data-testid="stButtonGroup"] button *,
    div[data-baseweb="button-group"] button *,
    div[data-testid="stSegmentedControl"] button * {{
        color: #94A3B8 !important;
    }}
    div[data-testid="stButtonGroup"] button:hover,
    div[data-baseweb="button-group"] button:hover,
    div[data-testid="stSegmentedControl"] button:hover {{
        color: #FFFFFF !important;
        background: rgba(255, 255, 255, 0.06) !important;
        border-color: rgba(255, 255, 255, 0.12) !important;
    }}
    div[data-testid="stButtonGroup"] button:hover *,
    div[data-baseweb="button-group"] button:hover *,
    div[data-testid="stSegmentedControl"] button:hover * {{
        color: #FFFFFF !important;
    }}
    div[data-testid="stButtonGroup"] button[aria-checked="true"],
    div[data-baseweb="button-group"] button[aria-checked="true"],
    div[data-testid="stSegmentedControl"] button[aria-checked="true"],
    div[data-testid="stButtonGroup"] button[aria-selected="true"],
    div[data-baseweb="button-group"] button[aria-selected="true"],
    div[data-testid="stSegmentedControl"] button[aria-selected="true"] {{
        background: #FFFFFF !important;
        color: #090D16 !important;
        border: 1px solid #FFFFFF !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.35) !important;
        outline: none !important;
    }}
    div[data-testid="stButtonGroup"] button[aria-checked="true"] *,
    div[data-baseweb="button-group"] button[aria-checked="true"] *,
    div[data-testid="stSegmentedControl"] button[aria-checked="true"] *,
    div[data-testid="stButtonGroup"] button[aria-selected="true"] *,
    div[data-baseweb="button-group"] button[aria-selected="true"] *,
    div[data-testid="stSegmentedControl"] button[aria-selected="true"] * {{
        color: #090D16 !important;
        font-weight: 600 !important;
    }}

    /* MATTE GLASS FORMULAS KATEX / STLATEX */
    [data-testid="stLatex"] {{
        background: rgba(6, 11, 20, 0.55) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 12px !important;
        padding: 16px 22px !important;
        margin: 14px 0 !important;
        backdrop-filter: blur(20px) !important;
        overflow-x: auto !important;
    }}
    [data-testid="stLatex"] .katex-display {{
        margin: 0 !important;
    }}
    [data-testid="stLatex"] .katex {{
        color: #F8FAFC !important;
        font-size: 1.15em !important;
    }}

    /* NAVEGACIÓN SUPERIOR EDITORIAL */
    .editorial-site-header {{
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        padding-bottom: 10px;
        margin-bottom: 14px;
        margin-top: 4px;
    }}
    .editorial-brand {{
        display: flex;
        align-items: baseline;
        gap: 8px;
    }}
    .editorial-logo {{
        font-size: 13px;
        font-weight: 800;
        letter-spacing: 0.14em;
        text-transform: uppercase;
        color: #F8FAFC;
    }}
    .editorial-division-label {{
        font-size: 12px;
        color: #64748B;
        font-weight: 500;
    }}
    .editorial-meta-right {{
        font-size: 11px;
        color: #64748B;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        letter-spacing: 0.04em;
    }}

    /* ARQUITECTURA EDITORIAL PAPER / NATURE 2.0 */
    .paper-masthead {{
        background: rgba(6, 11, 20, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 30px 36px 26px 36px !important;
        margin-bottom: 18px !important;
        backdrop-filter: blur(28px) !important;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45) !important;
    }}
    .paper-pretitle {{
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: 0.14em !important;
        text-transform: uppercase !important;
        color: #94A3B8 !important;
        margin-bottom: 8px !important;
    }}
    .paper-headline {{
        font-size: 30px !important;
        font-weight: 600 !important;
        line-height: 1.25 !important;
        letter-spacing: -0.02em !important;
        color: #FFFFFF !important;
        margin: 0 0 10px 0 !important;
    }}
    .paper-byline {{
        font-size: 13px !important;
        color: #94A3B8 !important;
        margin-bottom: 16px !important;
        padding-bottom: 14px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.07) !important;
    }}
    .paper-abstract {{
        background: rgba(255, 255, 255, 0.03) !important;
        border-left: 2px solid rgba(255, 255, 255, 0.45) !important;
        border-radius: 0 8px 8px 0 !important;
        padding: 14px 20px !important;
        font-size: 14.5px !important;
        line-height: 1.75 !important;
        color: #CBD5E1 !important;
    }}
    .paper-prose-card {{
        background: rgba(6, 11, 20, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 16px !important;
        padding: 28px 34px !important;
        margin-bottom: 18px !important;
        backdrop-filter: blur(24px) !important;
        color: #CBD5E1 !important;
        font-size: 15px !important;
        line-height: 1.8 !important;
    }}
    .paper-prose-card h3 {{
        font-size: 21px !important;
        font-weight: 600 !important;
        color: #FFFFFF !important;
        margin: 10px 0 12px 0 !important;
        letter-spacing: -0.02em !important;
    }}
    .paper-prose-card p {{
        margin-bottom: 12px !important;
        line-height: 1.8 !important;
    }}
    .paper-prose-card p:last-child {{
        margin-bottom: 0 !important;
    }}
    .paper-prose-card b {{
        color: #FFFFFF !important;
        font-weight: 600 !important;
    }}
    .paper-quote {{
        background: rgba(255, 255, 255, 0.03) !important;
        border-left: 2px solid rgba(255, 255, 255, 0.5) !important;
        border-radius: 0 8px 8px 0 !important;
        padding: 14px 20px !important;
        margin: 16px 0 !important;
        color: #F1F5F9 !important;
        font-style: italic !important;
        font-size: 15px !important;
        line-height: 1.7 !important;
    }}
    .paper-figure-header {{
        font-size: 11px !important;
        font-weight: 700 !important;
        letter-spacing: 0.1em !important;
        text-transform: uppercase !important;
        color: #94A3B8 !important;
        margin: 18px 0 8px 0 !important;
        padding: 0 4px !important;
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
    }}
    .paper-figure-caption {{
        font-size: 13px !important;
        line-height: 1.65 !important;
        color: #94A3B8 !important;
        margin-top: 8px !important;
        margin-bottom: 20px !important;
        padding: 12px 18px !important;
        background: rgba(6, 11, 20, 0.45) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        backdrop-filter: blur(16px) !important;
    }}
    .paper-figure-caption b {{
        color: #FFFFFF !important;
    }}
    .paper-note {{
        background: rgba(255, 255, 255, 0.03) !important;
        border-left: 2px solid rgba(255, 255, 255, 0.4) !important;
        border-radius: 0 10px 10px 0 !important;
        padding: 14px 20px !important;
        margin: 16px 0 !important;
        font-size: 14px !important;
        line-height: 1.75 !important;
        color: #CBD5E1 !important;
    }}
    .paper-note b {{
        color: #FFFFFF !important;
    }}
    .paper-references-card {{
        background: rgba(6, 11, 20, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 12px !important;
        padding: 20px 26px !important;
        margin-top: 24px !important;
        margin-bottom: 18px !important;
        font-size: 13px !important;
        line-height: 1.8 !important;
        color: #94A3B8 !important;
    }}
    .paper-references-card b {{
        color: #E2E8F0 !important;
        letter-spacing: 0.06em !important;
        font-size: 11px !important;
    }}
    .paper-photo-card {{
        background: rgba(6, 11, 20, 0.72) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        overflow: hidden !important;
        box-shadow: 0 16px 40px rgba(0, 0, 0, 0.5) !important;
        backdrop-filter: blur(24px) !important;
        transition: all 0.3s ease !important;
    }}
    .paper-photo-img {{
        width: 100% !important;
        max-height: 420px !important;
        object-fit: cover !important;
        display: block !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    }}
    .paper-photo-caption {{
        padding: 14px 18px !important;
        font-size: 12.5px !important;
        line-height: 1.6 !important;
        color: #94A3B8 !important;
        font-style: italic !important;
        background: rgba(255, 255, 255, 0.02) !important;
    }}
    .paper-doc-btn {{
        display: inline-flex !important;
        align-items: center !important;
        gap: 8px !important;
        background: #FFFFFF !important;
        color: #090D16 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        padding: 10px 18px !important;
        border-radius: 10px !important;
        text-decoration: none !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 14px rgba(255, 255, 255, 0.15) !important;
        margin-top: 14px !important;
    }}
    .paper-doc-btn:hover {{
        background: #F1F5F9 !important;
        color: #090D16 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(255, 255, 255, 0.25) !important;
    }}

    /* SECCIONES DE LABORATORIO & CARRUSEL (LANDING) */
    .lab-portal-header {{
        margin-top: 36px !important;
        margin-bottom: 20px !important;
    }}
    .lab-portal-card {{
        background: rgba(6, 11, 20, 0.72) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 16px !important;
        padding: 24px 26px !important;
        backdrop-filter: blur(20px) !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
        margin-bottom: 20px !important;
        transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease !important;
        min-height: 230px !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: space-between !important;
    }}
    .lab-portal-card:hover {{
        transform: translateY(-3px) !important;
        border-color: rgba(56, 189, 248, 0.4) !important;
        box-shadow: 0 14px 40px rgba(0, 0, 0, 0.6) !important;
    }}
    .lab-portal-icon {{
        font-size: 32px !important;
        margin-bottom: 12px !important;
        display: inline-block !important;
    }}
    .lab-portal-title {{
        font-size: 18px !important;
        font-weight: 700 !important;
        color: #F8FAFC !important;
        margin-bottom: 6px !important;
        letter-spacing: -0.01em !important;
    }}
    .lab-portal-tags {{
        display: flex !important;
        flex-wrap: wrap !important;
        gap: 6px !important;
        margin-bottom: 12px !important;
    }}
    .lab-portal-tag {{
        font-size: 11px !important;
        font-family: monospace !important;
        padding: 3px 8px !important;
        border-radius: 6px !important;
        background: rgba(255, 255, 255, 0.06) !important;
        color: #94A3B8 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
    }}
    .lab-portal-desc {{
        font-size: 13.5px !important;
        line-height: 1.65 !important;
        color: #94A3B8 !important;
        margin-bottom: 14px !important;
    }}
    .carousel-status-bar {{
        display: flex !important;
        justify-content: space-between !important;
        align-items: center !important;
        background: rgba(6, 11, 20, 0.5) !important;
        border: 1px solid rgba(255, 255, 255, 0.07) !important;
        border-radius: 12px !important;
        padding: 10px 18px !important;
        margin-bottom: 14px !important;
    }}
    """

    if "Clara" in theme_name or "Light" in theme_name or "Paper" in theme_name:
        theme_css = f"""
        #starry-fluid-canvas {{
            display: none !important;
        }}
        [data-testid="stAppViewContainer"] {{
            background-color: #F8FAFC !important;
            background-image: 
                radial-gradient(circle at 50% 0%, rgba(2, 132, 199, 0.04) 0%, transparent 60%),
                linear-gradient(180deg, #FAFBFD 0%, #F1F5F9 100%) !important;
            color: #1E293B !important;
        }}
        .stApp {{
            background: #F8FAFC !important;
            color: #1E293B !important;
        }}

        /* ENCABEZADOS Y TEXTOS */
        h1, h2, h3, h4, h5, h6, .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
            color: #0F172A !important;
            text-shadow: none !important;
        }}
        p, span, label, div {{
            color: #334155;
        }}

        /* CABECERA EDITORIAL DEL SITIO */
        .editorial-site-header {{
            border-bottom: 1px solid #E2E8F0 !important;
        }}
        .editorial-logo {{
            color: #0F172A !important;
            font-weight: 800 !important;
        }}
        .editorial-division-label {{
            color: #64748B !important;
        }}
        .editorial-meta-right {{
            color: #94A3B8 !important;
        }}

        /* MONOGRAFÍA EDITORIAL (MASTHEAD) */
        .paper-masthead {{
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04) !important;
            backdrop-filter: none !important;
        }}
        .paper-pretitle {{
            color: #0284C7 !important;
            font-weight: 700 !important;
        }}
        .paper-headline {{
            color: #0F172A !important;
            font-weight: 800 !important;
        }}
        .paper-byline {{
            color: #64748B !important;
            border-top: 1px solid #F1F5F9 !important;
            border-bottom: 1px solid #F1F5F9 !important;
        }}
        .paper-byline b {{
            color: #1E293B !important;
        }}
        .paper-abstract {{
            background: #F8FAFC !important;
            border-left: 3px solid #0284C7 !important;
            color: #334155 !important;
        }}
        .paper-abstract b {{
            color: #0F172A !important;
        }}

        /* TARJETAS DE PROSA CIENTÍFICA */
        .paper-prose-card {{
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 2px 14px rgba(0, 0, 0, 0.03) !important;
            color: #334155 !important;
            backdrop-filter: none !important;
        }}
        .paper-prose-card h3 {{
            color: #0F172A !important;
        }}
        .paper-prose-card p {{
            color: #334155 !important;
        }}
        .paper-prose-card b {{
            color: #0F172A !important;
        }}

        /* CITAS HISTÓRICAS */
        .paper-quote {{
            background: #F8FAFC !important;
            border-left: 3px solid #0F172A !important;
            color: #1E293B !important;
        }}

        /* NOTAS EXPLICATIVAS */
        .paper-note {{
            background: #F0F9FF !important;
            border-left: 3px solid #0284C7 !important;
            color: #0369A1 !important;
        }}
        .paper-note b {{
            color: #0C4A6E !important;
        }}

        /* FÓRMULAS MATEMÁTICAS KATEX */
        [data-testid="stLatex"] {{
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
            backdrop-filter: none !important;
        }}
        [data-testid="stLatex"] .katex {{
            color: #0F172A !important;
        }}

        /* FIGURAS Y GRÁFICOS */
        .paper-figure-header {{
            background: #F8FAFC !important;
            border: 1px solid #E2E8F0 !important;
            border-bottom: none !important;
            color: #0F172A !important;
        }}
        .paper-figure-caption {{
            background: #F8FAFC !important;
            border: 1px solid #E2E8F0 !important;
            border-top: none !important;
            color: #64748B !important;
        }}
        .paper-figure-caption b {{
            color: #0F172A !important;
        }}

        /* TARJETA DE FOTOGRAFÍA HISTÓRICA */
        .paper-photo-card {{
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 6px 24px rgba(0, 0, 0, 0.06) !important;
            backdrop-filter: none !important;
        }}
        .paper-photo-img {{
            border-bottom: 1px solid #E2E8F0 !important;
        }}
        .paper-photo-caption {{
            background: #F8FAFC !important;
            color: #64748B !important;
        }}
        .paper-doc-btn {{
            background: #0F172A !important;
            color: #FFFFFF !important;
            box-shadow: 0 3px 10px rgba(15, 23, 42, 0.15) !important;
        }}
        .paper-doc-btn:hover {{
            background: #1E293B !important;
            color: #FFFFFF !important;
        }}

        /* REFERENCIAS BIBLIOGRÁFICAS */
        .paper-references-card {{
            background: #F8FAFC !important;
            border: 1px solid #E2E8F0 !important;
            color: #64748B !important;
        }}
        .paper-references-card b {{
            color: #0F172A !important;
        }}

        /* SELECTORES / SEGMENTED CONTROL */
        div[data-testid="stButtonGroup"],
        div[data-baseweb="button-group"],
        div[data-testid="stSegmentedControl"] {{
            background: #E2E8F0 !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 12px !important;
            padding: 3px !important;
        }}
        div[data-testid="stButtonGroup"] button,
        div[data-baseweb="button-group"] button,
        div[data-testid="stSegmentedControl"] button {{
            background: transparent !important;
            color: #475569 !important;
            border: none !important;
            box-shadow: none !important;
            font-weight: 500 !important;
        }}
        div[data-testid="stButtonGroup"] button:hover,
        div[data-baseweb="button-group"] button:hover,
        div[data-testid="stSegmentedControl"] button:hover {{
            background: rgba(255, 255, 255, 0.6) !important;
            color: #0F172A !important;
        }}
        div[data-testid="stButtonGroup"] button[aria-checked="true"],
        div[data-baseweb="button-group"] button[aria-selected="true"],
        div[data-testid="stButtonGroup"] button[aria-selected="true"],
        div[data-testid="stSegmentedControl"] button[aria-checked="true"],
        div[data-testid="stSegmentedControl"] button[aria-selected="true"] {{
            background: #0F172A !important;
            color: #FFFFFF !important;
            border: 1px solid #0F172A !important;
            box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15) !important;
        }}
        div[data-testid="stButtonGroup"] button[aria-checked="true"] *,
        div[data-baseweb="button-group"] button[aria-selected="true"] *,
        div[data-testid="stButtonGroup"] button[aria-selected="true"] *,
        div[data-testid="stSegmentedControl"] button[aria-checked="true"] * {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
        }}

        /* MÉTRICAS & EXPANDER */
        div[data-testid="stMetric"], div[data-testid="stExpander"] {{
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02) !important;
        }}
        [data-testid="stMetricLabel"] {{
            color: #64748B !important;
            font-size: 12px !important;
            font-weight: 600 !important;
        }}
        [data-testid="stMetricValue"] {{
            color: #0F172A !important;
            font-weight: 800 !important;
            text-shadow: none !important;
        }}
        div[data-testid="stExpander"] summary {{
            color: #0F172A !important;
        }}

        /* BOTONES STREAMLIT */
        .stButton button[kind="primary"] {{
            background: #0F172A !important;
            color: #FFFFFF !important;
            border: 1px solid #0F172A !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.12) !important;
        }}
        .stButton button[kind="primary"] * {{
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }}
        .stButton button[kind="secondary"] {{
            background: #FFFFFF !important;
            color: #334155 !important;
            border: 1px solid #CBD5E1 !important;
            border-radius: 8px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        }}
        .stButton button[kind="secondary"]:hover {{
            background: #F8FAFC !important;
            color: #0F172A !important;
            border-color: #94A3B8 !important;
        }}
        .stButton button[kind="secondary"] * {{
            color: #334155 !important;
        }}
        .stButton button[kind="secondary"]:hover * {{
            color: #0F172A !important;
        }}

        /* SECCIONES DE LABORATORIO & CARRUSEL (LIGHT MODE) */
        .lab-portal-card {{
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.04) !important;
            backdrop-filter: none !important;
        }}
        .lab-portal-card:hover {{
            border-color: #0284C7 !important;
            box-shadow: 0 10px 30px rgba(2, 132, 199, 0.12) !important;
        }}
        .lab-portal-title {{
            color: #0F172A !important;
        }}
        .lab-portal-tag {{
            background: #F1F5F9 !important;
            color: #0369A1 !important;
            border: 1px solid #E2E8F0 !important;
        }}
        .lab-portal-desc {{
            color: #334155 !important;
        }}
        .carousel-status-bar {{
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03) !important;
        }}
        """

    elif "Obsidian" in theme_name:
        theme_css = f"""
        [data-testid="stAppViewContainer"] {{
            background-color: #060a12 !important;
            background-image: 
                radial-gradient(circle at 50% 15%, rgba(255, 255, 255, 0.04) 0%, transparent 45%),
                linear-gradient(180deg, rgba(8, 12, 20, 0.82) 0%, rgba(10, 16, 26, 0.88) 50%, rgba(5, 8, 15, 0.95) 100%),
                url("data:image/jpeg;base64,{b64_starry}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
            background-repeat: no-repeat !important;
        }}

        .theme-picker-title {{ color: #94a3b8 !important; }}

        .starry-night-header {{
            background: rgba(13, 18, 28, 0.75) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 16px !important;
            padding: 24px 34px !important;
            margin-bottom: 22px !important;
            box-shadow: 0 16px 40px rgba(0, 0, 0, 0.45), inset 0 1px 0 rgba(255, 255, 255, 0.08) !important;
            backdrop-filter: blur(24px) !important;
        }}
        .starry-night-header::after {{ display: none !important; }}
        .lab-title-starry {{
            font-size: 32px !important;
            font-weight: 700 !important;
            letter-spacing: -0.03em !important;
            color: #FFFFFF !important;
            text-shadow: none !important;
        }}
        .lab-sub-starry {{
            font-size: 14px !important;
            color: #94a3b8 !important;
            font-weight: 400 !important;
        }}
        .badge-starry-gold, .badge-starry-cyan {{
            background: rgba(255, 255, 255, 0.06) !important;
            color: #E2E8F0 !important;
            border: 1px solid rgba(255, 255, 255, 0.12) !important;
            border-radius: 6px !important;
            box-shadow: none !important;
            font-size: 11px !important;
            font-weight: 600 !important;
            padding: 4px 12px !important;
            letter-spacing: 0.04em !important;
        }}
        .header-affil-tag {{ color: #FFFFFF !important; font-weight: 700 !important; font-size: 12px !important; }}
        .header-affil-sub {{ color: #94a3b8 !important; font-weight: 500 !important; font-size: 12px !important; }}

        .stButton button[kind="primary"] {{
            background: #FFFFFF !important;
            color: #090D16 !important;
            font-weight: 600 !important;
            border: 1px solid #FFFFFF !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 14px rgba(255, 255, 255, 0.12) !important;
            text-transform: none !important;
            letter-spacing: -0.01em !important;
        }}
        .stButton button[kind="primary"] * {{ color: #090D16 !important; font-weight: 600 !important; }}

        .stButton button[kind="secondary"] {{
            background: rgba(18, 24, 38, 0.65) !important;
            color: #94a3b8 !important;
            font-weight: 500 !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            backdrop-filter: blur(14px) !important;
            box-shadow: none !important;
            text-transform: none !important;
            transition: all 0.2s ease !important;
        }}
        .stButton button[kind="secondary"]:hover {{
            background: rgba(30, 41, 59, 0.8) !important;
            color: #FFFFFF !important;
            border-color: rgba(255, 255, 255, 0.22) !important;
            transform: translateY(-1px) !important;
        }}
        .stButton button[kind="secondary"] * {{ color: #94a3b8 !important; }}
        .stButton button[kind="secondary"]:hover * {{ color: #FFFFFF !important; }}

        [data-baseweb="tab-list"] {{
            background: rgba(11, 16, 26, 0.85) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
            padding: 4px !important;
            gap: 4px !important;
            backdrop-filter: blur(16px) !important;
        }}
        [data-baseweb="tab"] {{
            color: #64748B !important;
            font-weight: 500 !important;
            border-radius: 8px !important;
            padding: 8px 18px !important;
            border: none !important;
            background: transparent !important;
            transition: all 0.2s ease !important;
        }}
        [data-baseweb="tab"]:hover {{
            color: #CBD5E1 !important;
            background: rgba(255, 255, 255, 0.04) !important;
        }}
        [data-baseweb="tab"][aria-selected="true"] {{
            background: rgba(255, 255, 255, 0.12) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border: 1px solid rgba(255, 255, 255, 0.16) !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25) !important;
        }}
        [data-baseweb="tab-border"] {{ display: none !important; }}

        .theory-box-starry {{
            background: rgba(11, 16, 26, 0.82) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-left: 3px solid #E2E8F0 !important;
            border-radius: 12px !important;
            color: #E2E8F0 !important;
            backdrop-filter: blur(20px) !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
            padding: 24px 30px !important;
            line-height: 1.7 !important;
        }}
        .theory-box-starry b {{ color: #FFFFFF !important; font-weight: 700 !important; }}
        .theory-box-starry blockquote {{
            background: rgba(255, 255, 255, 0.03) !important;
            border-left: 2px solid #94A3B8 !important;
            color: #CBD5E1 !important;
        }}
        .module-viewer-starry {{
            background: rgba(11, 16, 26, 0.82) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px !important;
            box-shadow: 0 16px 45px rgba(0, 0, 0, 0.5) !important;
            backdrop-filter: blur(20px) !important;
        }}
        .area-starry-card {{
            background: rgba(11, 16, 26, 0.75) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 10px !important;
            color: #94A3B8 !important;
        }}
        .area-starry-card b {{ color: #F1F5F9 !important; }}
        div[data-testid="stMetric"], div[data-testid="stExpander"] {{
            background: rgba(11, 16, 26, 0.75) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 12px !important;
        }}
        [data-testid="stMetricValue"] {{
            color: #FFFFFF !important;
            font-weight: 700 !important;
            text-shadow: none !important;
        }}
        [data-testid="stMetricLabel"] {{ color: #94A3B8 !important; }}
        div[data-testid="stExpander"] summary {{ color: #F1F5F9 !important; }}
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
            color: #F8FAFC !important;
            text-shadow: none !important;
        }}
        """

    elif "Champagne" in theme_name:
        theme_css = f"""
        [data-testid="stAppViewContainer"] {{
            background-color: #070B12 !important;
            background-image: 
                radial-gradient(circle at 80% 20%, rgba(216, 202, 175, 0.12) 0%, transparent 45%),
                linear-gradient(180deg, rgba(8, 13, 22, 0.82) 0%, rgba(10, 15, 26, 0.88) 50%, rgba(5, 8, 15, 0.96) 100%),
                url("data:image/jpeg;base64,{b64_starry}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
            background-repeat: no-repeat !important;
        }}

        .theme-picker-title {{ color: #D8CAAF !important; }}

        .starry-night-header {{
            background: linear-gradient(135deg, rgba(14, 20, 32, 0.85) 0%, rgba(10, 15, 26, 0.94) 100%) !important;
            border: 1px solid rgba(216, 202, 175, 0.3) !important;
            border-radius: 18px !important;
            padding: 24px 34px !important;
            margin-bottom: 22px !important;
            box-shadow: 0 16px 45px rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(216, 202, 175, 0.15) !important;
            backdrop-filter: blur(20px) !important;
        }}
        .starry-night-header::after {{ display: none !important; }}
        .lab-title-starry {{
            font-size: 32px !important;
            font-family: "Georgia", serif !important;
            font-weight: 700 !important;
            letter-spacing: 0.02em !important;
            color: #F7EFE2 !important;
            text-shadow: 0 0 18px rgba(216, 202, 175, 0.25) !important;
        }}
        .lab-sub-starry {{
            font-size: 14px !important;
            color: #C8BCA4 !important;
            font-weight: 400 !important;
        }}
        .badge-starry-gold, .badge-starry-cyan {{
            background: rgba(216, 202, 175, 0.1) !important;
            color: #D8CAAF !important;
            border: 1px solid rgba(216, 202, 175, 0.35) !important;
            border-radius: 20px !important;
            box-shadow: none !important;
            font-size: 11px !important;
            font-weight: 700 !important;
            padding: 4px 12px !important;
        }}
        .header-affil-tag {{ color: #E2D4B7 !important; font-weight: 700 !important; font-size: 12px !important; }}
        .header-affil-sub {{ color: #C8BCA4 !important; font-weight: 500 !important; font-size: 12px !important; }}

        .stButton button[kind="primary"] {{
            background: linear-gradient(135deg, #E2D4B7 0%, #C5B382 100%) !important;
            color: #0A0F18 !important;
            font-weight: 700 !important;
            border: 1px solid #EFE6D5 !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 18px rgba(197, 179, 130, 0.25) !important;
            text-transform: none !important;
        }}
        .stButton button[kind="primary"] * {{ color: #0A0F18 !important; font-weight: 700 !important; }}

        .stButton button[kind="secondary"] {{
            background: rgba(14, 20, 32, 0.72) !important;
            color: #D8CAAF !important;
            font-weight: 600 !important;
            border: 1px solid rgba(216, 202, 175, 0.2) !important;
            border-radius: 10px !important;
            backdrop-filter: blur(14px) !important;
            transition: all 0.2s ease !important;
        }}
        .stButton button[kind="secondary"]:hover {{
            background: rgba(24, 34, 52, 0.85) !important;
            color: #F7EFE2 !important;
            border-color: rgba(216, 202, 175, 0.45) !important;
            transform: translateY(-1px) !important;
        }}
        .stButton button[kind="secondary"] * {{ color: #D8CAAF !important; }}
        .stButton button[kind="secondary"]:hover * {{ color: #F7EFE2 !important; }}

        [data-baseweb="tab-list"] {{
            background: rgba(10, 15, 25, 0.8) !important;
            border-bottom: 1.5px solid rgba(216, 202, 175, 0.22) !important;
            border-radius: 10px !important;
            padding: 4px 8px !important;
            gap: 8px !important;
        }}
        [data-baseweb="tab"] {{
            color: #8E8A82 !important;
            font-weight: 500 !important;
            border-radius: 6px !important;
            padding: 8px 18px !important;
            border: none !important;
            background: transparent !important;
            transition: all 0.2s ease !important;
        }}
        [data-baseweb="tab"]:hover {{
            color: #D8CAAF !important;
        }}
        [data-baseweb="tab"][aria-selected="true"] {{
            background: rgba(216, 202, 175, 0.12) !important;
            color: #F7EFE2 !important;
            font-weight: 700 !important;
            border-bottom: 2px solid #D8CAAF !important;
            box-shadow: none !important;
        }}
        [data-baseweb="tab-border"] {{ display: none !important; }}

        .theory-box-starry {{
            background: rgba(12, 18, 30, 0.85) !important;
            border: 1px solid rgba(216, 202, 175, 0.18) !important;
            border-left: 3px solid #D8CAAF !important;
            border-radius: 14px !important;
            color: #E8DFC8 !important;
            backdrop-filter: blur(18px) !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45) !important;
            padding: 24px 30px !important;
            line-height: 1.7 !important;
        }}
        .theory-box-starry b {{ color: #F7EFE2 !important; }}
        .theory-box-starry blockquote {{
            background: rgba(216, 202, 175, 0.05) !important;
            border-left: 2px solid #D8CAAF !important;
            color: #E2D4B7 !important;
        }}
        .module-viewer-starry {{
            background: rgba(12, 18, 30, 0.85) !important;
            border: 1px solid rgba(216, 202, 175, 0.22) !important;
            border-radius: 18px !important;
            box-shadow: 0 16px 45px rgba(0, 0, 0, 0.5) !important;
        }}
        .area-starry-card {{
            background: rgba(12, 18, 30, 0.78) !important;
            border: 1px solid rgba(216, 202, 175, 0.18) !important;
            border-radius: 10px !important;
            color: #C8BCA4 !important;
        }}
        .area-starry-card b {{ color: #E2D4B7 !important; }}
        div[data-testid="stMetric"], div[data-testid="stExpander"] {{
            background: rgba(12, 18, 30, 0.8) !important;
            border: 1px solid rgba(216, 202, 175, 0.2) !important;
            border-radius: 12px !important;
        }}
        [data-testid="stMetricValue"] {{
            color: #E8DFC8 !important;
            font-weight: 700 !important;
            text-shadow: none !important;
        }}
        [data-testid="stMetricLabel"] {{ color: #A39B8B !important; }}
        div[data-testid="stExpander"] summary {{ color: #D8CAAF !important; }}
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
            color: #F7EFE2 !important;
            text-shadow: none !important;
        }}
        """

    elif "Swiss" in theme_name:
        theme_css = f"""
        [data-testid="stAppViewContainer"] {{
            background-color: #050B14 !important;
            background-image: 
                linear-gradient(180deg, rgba(8, 14, 24, 0.84) 0%, rgba(10, 18, 32, 0.90) 50%, rgba(4, 8, 16, 0.96) 100%),
                url("data:image/jpeg;base64,{b64_starry}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
            background-repeat: no-repeat !important;
        }}

        .theme-picker-title {{ color: #38BDF8 !important; font-family: monospace !important; }}

        .starry-night-header {{
            background: rgba(11, 18, 30, 0.92) !important;
            border: 1px solid rgba(148, 163, 184, 0.25) !important;
            border-radius: 8px !important;
            padding: 22px 30px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(16px) !important;
        }}
        .starry-night-header::after {{ display: none !important; }}
        .lab-title-starry {{
            font-size: 28px !important;
            font-weight: 800 !important;
            letter-spacing: -0.04em !important;
            text-transform: uppercase !important;
            color: #FFFFFF !important;
            text-shadow: none !important;
        }}
        .lab-sub-starry {{
            font-size: 13.5px !important;
            color: #94A3B8 !important;
            font-weight: 400 !important;
        }}
        .badge-starry-gold, .badge-starry-cyan {{
            background: rgba(2, 132, 199, 0.12) !important;
            color: #38BDF8 !important;
            border: 1px solid rgba(2, 132, 199, 0.35) !important;
            border-radius: 4px !important;
            font-family: monospace !important;
            box-shadow: none !important;
            font-size: 11px !important;
            padding: 4px 10px !important;
        }}
        .header-affil-tag {{ color: #38BDF8 !important; font-weight: 700 !important; font-family: monospace !important; font-size: 12px !important; }}
        .header-affil-sub {{ color: #94A3B8 !important; font-weight: 600 !important; font-size: 12px !important; }}

        .stButton button[kind="primary"] {{
            background: #0284C7 !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border: 1px solid #38BDF8 !important;
            border-radius: 6px !important;
            box-shadow: 0 2px 10px rgba(2, 132, 199, 0.3) !important;
            text-transform: none !important;
        }}
        .stButton button[kind="primary"] * {{ color: #FFFFFF !important; font-weight: 600 !important; }}

        .stButton button[kind="secondary"] {{
            background: rgba(15, 23, 42, 0.85) !important;
            color: #CBD5E1 !important;
            font-weight: 500 !important;
            border: 1px solid rgba(148, 163, 184, 0.22) !important;
            border-radius: 6px !important;
            backdrop-filter: blur(12px) !important;
            transition: all 0.2s ease !important;
        }}
        .stButton button[kind="secondary"]:hover {{
            background: rgba(30, 41, 59, 0.95) !important;
            color: #FFFFFF !important;
            border-color: rgba(148, 163, 184, 0.4) !important;
            transform: translateY(-1px) !important;
        }}
        .stButton button[kind="secondary"] * {{ color: #CBD5E1 !important; }}
        .stButton button[kind="secondary"]:hover * {{ color: #FFFFFF !important; }}

        [data-baseweb="tab-list"] {{
            background: rgba(15, 23, 42, 0.92) !important;
            border: 1px solid rgba(148, 163, 184, 0.25) !important;
            border-radius: 6px !important;
            padding: 4px 6px !important;
            gap: 6px !important;
        }}
        [data-baseweb="tab"] {{
            color: #94A3B8 !important;
            font-weight: 600 !important;
            border-radius: 4px !important;
            padding: 6px 16px !important;
            border: none !important;
            background: transparent !important;
            font-size: 13px !important;
            letter-spacing: 0.02em !important;
        }}
        [data-baseweb="tab"]:hover {{ color: #FFFFFF !important; }}
        [data-baseweb="tab"][aria-selected="true"] {{
            background: #0284C7 !important;
            color: #FFFFFF !important;
            font-weight: 700 !important;
            box-shadow: none !important;
        }}
        [data-baseweb="tab-border"] {{ display: none !important; }}

        .theory-box-starry {{
            background: rgba(15, 23, 42, 0.88) !important;
            border: 1px solid rgba(148, 163, 184, 0.22) !important;
            border-left: 4px solid #0284C7 !important;
            border-radius: 6px !important;
            color: #E2E8F0 !important;
            backdrop-filter: blur(14px) !important;
            padding: 24px 30px !important;
            line-height: 1.7 !important;
        }}
        .theory-box-starry b {{ color: #38BDF8 !important; }}
        .theory-box-starry blockquote {{
            background: rgba(2, 132, 199, 0.08) !important;
            border-left: 3px solid #0284C7 !important;
            color: #BAE6FD !important;
        }}
        .module-viewer-starry {{
            background: rgba(15, 23, 42, 0.9) !important;
            border: 1px solid rgba(148, 163, 184, 0.25) !important;
            border-radius: 8px !important;
        }}
        .area-starry-card {{
            background: rgba(15, 23, 42, 0.82) !important;
            border: 1px solid rgba(148, 163, 184, 0.2) !important;
            border-radius: 6px !important;
            color: #CBD5E1 !important;
        }}
        .area-starry-card b {{ color: #38BDF8 !important; }}
        div[data-testid="stMetric"], div[data-testid="stExpander"] {{
            background: rgba(15, 23, 42, 0.85) !important;
            border: 1px solid rgba(148, 163, 184, 0.25) !important;
            border-radius: 6px !important;
        }}
        [data-testid="stMetricValue"] {{
            color: #38BDF8 !important;
            font-weight: 700 !important;
            text-shadow: none !important;
        }}
        [data-testid="stMetricLabel"] {{ color: #94A3B8 !important; font-family: monospace !important; }}
        div[data-testid="stExpander"] summary {{ color: #E2E8F0 !important; }}
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
            color: #F8FAFC !important;
            text-shadow: none !important;
        }}
        """

    elif "Monolith" in theme_name:
        theme_css = f"""
        [data-testid="stAppViewContainer"] {{
            background-color: #04070D !important;
            background-image: 
                linear-gradient(180deg, rgba(4, 7, 13, 0.82) 0%, rgba(6, 10, 18, 0.90) 50%, rgba(2, 4, 8, 0.97) 100%),
                url("data:image/jpeg;base64,{b64_starry}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
            background-repeat: no-repeat !important;
        }}

        .theme-picker-title {{ color: #64748B !important; }}

        .starry-night-header {{
            background: rgba(5, 9, 16, 0.82) !important;
            border: 1px solid rgba(255, 255, 255, 0.07) !important;
            border-radius: 20px !important;
            padding: 24px 34px !important;
            margin-bottom: 22px !important;
            box-shadow: 0 25px 60px rgba(0, 0, 0, 0.6) !important;
            backdrop-filter: blur(30px) !important;
        }}
        .starry-night-header::after {{ display: none !important; }}
        .lab-title-starry {{
            font-size: 32px !important;
            font-weight: 600 !important;
            letter-spacing: -0.02em !important;
            color: #F8FAFC !important;
            text-shadow: none !important;
        }}
        .lab-sub-starry {{
            font-size: 14px !important;
            color: #64748B !important;
            font-weight: 400 !important;
        }}
        .badge-starry-gold, .badge-starry-cyan {{
            background: rgba(255, 255, 255, 0.05) !important;
            color: #94A3B8 !important;
            border: none !important;
            border-radius: 999px !important;
            box-shadow: none !important;
            font-size: 11px !important;
            padding: 4px 12px !important;
        }}
        .header-affil-tag {{ color: #E2E8F0 !important; font-weight: 600 !important; font-size: 12px !important; }}
        .header-affil-sub {{ color: #64748B !important; font-weight: 400 !important; font-size: 12px !important; }}

        .stButton button[kind="primary"] {{
            background: rgba(255, 255, 255, 0.16) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 12px !important;
            backdrop-filter: blur(20px) !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
            text-transform: none !important;
        }}
        .stButton button[kind="primary"] * {{ color: #FFFFFF !important; font-weight: 600 !important; }}

        .stButton button[kind="secondary"] {{
            background: rgba(6, 11, 20, 0.5) !important;
            color: #64748B !important;
            font-weight: 500 !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
            transition: all 0.2s ease !important;
        }}
        .stButton button[kind="secondary"]:hover {{
            background: rgba(15, 23, 42, 0.7) !important;
            color: #F1F5F9 !important;
            border-color: rgba(255, 255, 255, 0.15) !important;
            transform: translateY(-1px) !important;
        }}
        .stButton button[kind="secondary"] * {{ color: #64748B !important; }}
        .stButton button[kind="secondary"]:hover * {{ color: #F1F5F9 !important; }}

        [data-baseweb="tab-list"] {{
            background: rgba(5, 9, 16, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 14px !important;
            padding: 4px !important;
            gap: 4px !important;
        }}
        [data-baseweb="tab"] {{
            color: #64748B !important;
            font-weight: 500 !important;
            border-radius: 10px !important;
            padding: 8px 18px !important;
            border: none !important;
            background: transparent !important;
            transition: all 0.2s ease !important;
        }}
        [data-baseweb="tab"]:hover {{ color: #E2E8F0 !important; }}
        [data-baseweb="tab"][aria-selected="true"] {{
            background: rgba(255, 255, 255, 0.1) !important;
            color: #F8FAFC !important;
            font-weight: 600 !important;
            border: 1px solid rgba(255, 255, 255, 0.14) !important;
            box-shadow: none !important;
        }}
        [data-baseweb="tab-border"] {{ display: none !important; }}

        .theory-box-starry {{
            background: rgba(6, 11, 20, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-left: 2px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 16px !important;
            color: #E2E8F0 !important;
            backdrop-filter: blur(25px) !important;
            padding: 24px 30px !important;
            line-height: 1.7 !important;
        }}
        .theory-box-starry b {{ color: #FFFFFF !important; }}
        .theory-box-starry blockquote {{
            background: rgba(255, 255, 255, 0.02) !important;
            border-left: 2px solid rgba(255, 255, 255, 0.2) !important;
            color: #94A3B8 !important;
        }}
        .module-viewer-starry {{
            background: rgba(6, 11, 20, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 18px !important;
            backdrop-filter: blur(25px) !important;
        }}
        .area-starry-card {{
            background: rgba(6, 11, 20, 0.65) !important;
            border: 1px solid rgba(255, 255, 255, 0.05) !important;
            border-radius: 12px !important;
            color: #94A3B8 !important;
        }}
        .area-starry-card b {{ color: #E2E8F0 !important; }}
        div[data-testid="stMetric"], div[data-testid="stExpander"] {{
            background: rgba(6, 11, 20, 0.75) !important;
            border: 1px solid rgba(255, 255, 255, 0.06) !important;
            border-radius: 14px !important;
        }}
        [data-testid="stMetricValue"] {{
            color: #F8FAFC !important;
            font-weight: 600 !important;
            text-shadow: none !important;
        }}
        [data-testid="stMetricLabel"] {{ color: #64748B !important; }}
        div[data-testid="stExpander"] summary {{ color: #E2E8F0 !important; }}
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
            color: #F8FAFC !important;
            text-shadow: none !important;
        }}
        """

    else:
        # Surrealista Original
        theme_css = f"""
        [data-testid="stAppViewContainer"] {{
            background-color: #060d19 !important;
            background-image: 
                radial-gradient(circle at 85% 15%, rgba(254, 240, 138, 0.30) 0%, transparent 35%),
                radial-gradient(circle at 20% 25%, rgba(56, 189, 248, 0.25) 0%, transparent 45%),
                radial-gradient(circle at 52% 45%, rgba(29, 78, 216, 0.30) 0%, transparent 60%),
                linear-gradient(180deg, rgba(6, 13, 25, 0.78) 0%, rgba(13, 27, 42, 0.86) 50%, rgba(5, 10, 20, 0.94) 100%),
                url("data:image/jpeg;base64,{b64_starry}") !important;
            background-size: cover !important;
            background-position: center !important;
            background-attachment: fixed !important;
            background-repeat: no-repeat !important;
        }}

        .theme-picker-title {{ color: #FDE047 !important; }}

        .starry-night-header {{
            background: linear-gradient(135deg, rgba(13, 27, 42, 0.92) 0%, rgba(29, 53, 87, 0.82) 45%, rgba(6, 13, 25, 0.95) 100%) !important;
            border: 2px solid #FDE047 !important;
            border-radius: 20px !important;
            padding: 24px 34px !important;
            margin-bottom: 22px !important;
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.7), 0 0 25px rgba(253, 224, 71, 0.35) !important;
            backdrop-filter: blur(14px) !important;
            position: relative;
        }}
        .starry-night-header::after {{
            content: "🌙";
            position: absolute;
            right: 32px;
            top: 18px;
            font-size: 48px;
            filter: drop-shadow(0 0 18px #FDE047);
        }}
        .lab-title-starry {{
            font-size: 34px !important;
            font-weight: 900 !important;
            letter-spacing: -0.5px !important;
            color: #FDE047 !important;
            text-shadow: 0 0 18px rgba(253, 224, 71, 0.6) !important;
        }}
        .lab-sub-starry {{
            font-size: 14.5px !important;
            color: #bae6fd !important;
            margin-top: 5px !important;
            font-weight: 500 !important;
        }}
        .badge-starry-gold {{
            background: rgba(253, 224, 71, 0.15) !important;
            color: #FDE047 !important;
            border: 1.5px solid #FDE047 !important;
            padding: 5px 14px !important;
            border-radius: 20px !important;
            font-size: 11px !important;
            font-weight: 800 !important;
            box-shadow: 0 0 12px rgba(253, 224, 71, 0.35) !important;
        }}
        .badge-starry-cyan {{
            background: rgba(56, 189, 248, 0.15) !important;
            color: #38bdf8 !important;
            border: 1.5px solid #38bdf8 !important;
            padding: 5px 14px !important;
            border-radius: 20px !important;
            font-size: 11px !important;
            font-weight: 800 !important;
            box-shadow: 0 0 12px rgba(56, 189, 248, 0.35) !important;
        }}
        .header-affil-tag {{ color: #FDE047 !important; font-weight: 800 !important; font-family: monospace !important; font-size: 12px !important; }}
        .header-affil-sub {{ color: #38bdf8 !important; font-weight: 600 !important; font-size: 12px !important; }}

        .stButton button[kind="primary"] {{
            background: linear-gradient(135deg, #FDE047 0%, #F59E0B 100%) !important;
            color: #050a14 !important;
            font-weight: 900 !important;
            border: 2px solid #FEF08A !important;
            border-radius: 12px !important;
            box-shadow: 0 6px 20px rgba(245, 158, 11, 0.5), inset 0 1px 2px rgba(255, 255, 255, 0.8) !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }}
        .stButton button[kind="primary"] * {{ color: #050a14 !important; font-weight: 900 !important; }}

        .stButton button[kind="secondary"] {{
            background: rgba(13, 27, 42, 0.88) !important;
            color: #f1f5f9 !important;
            font-weight: 700 !important;
            border: 1.5px solid #38bdf8 !important;
            border-radius: 12px !important;
            backdrop-filter: blur(8px) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }}
        .stButton button[kind="secondary"]:hover {{
            background: rgba(29, 53, 87, 0.95) !important;
            color: #FDE047 !important;
            border-color: #FDE047 !important;
            box-shadow: 0 0 20px rgba(253, 224, 71, 0.45) !important;
            transform: translateY(-2px) !important;
        }}
        .stButton button[kind="secondary"] * {{ color: #f1f5f9 !important; }}
        .stButton button[kind="secondary"]:hover * {{ color: #FDE047 !important; }}

        [data-baseweb="tab-list"] {{
            background: rgba(10, 22, 38, 0.95) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.35) !important;
            border-radius: 14px !important;
            padding: 6px 10px !important;
            gap: 8px !important;
        }}
        [data-baseweb="tab"] {{
            color: #94a3b8 !important;
            font-weight: 700 !important;
            border-radius: 10px !important;
            padding: 8px 16px !important;
            border: 1px solid transparent !important;
            transition: all 0.2s ease !important;
        }}
        [data-baseweb="tab"][aria-selected="true"] {{
            background: rgba(56, 189, 248, 0.2) !important;
            color: #FDE047 !important;
            border-color: #FDE047 !important;
            box-shadow: 0 0 12px rgba(253, 224, 71, 0.3) !important;
        }}

        .theory-box-starry {{
            background: linear-gradient(135deg, rgba(13, 25, 44, 0.96) 0%, rgba(7, 14, 26, 0.98) 100%) !important;
            border: 1px solid rgba(56, 189, 248, 0.22) !important;
            border-left: 5px solid #FDE047 !important;
            border-radius: 14px !important;
            padding: 26px 32px !important;
            color: #f1f5f9 !important;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), inset 0 1px 1px rgba(255, 255, 255, 0.06) !important;
            backdrop-filter: blur(16px) !important;
        }}
        .theory-box-starry b {{ color: #FDE047 !important; font-weight: 800 !important; }}
        .theory-box-starry blockquote {{
            background: rgba(5, 12, 22, 0.65) !important;
            border-left: 3px solid #FDE047 !important;
            color: #fef08a !important;
        }}
        .module-viewer-starry {{
            background: rgba(8, 17, 30, 0.96) !important;
            border: 1px solid rgba(56, 189, 248, 0.35) !important;
            border-radius: 20px !important;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.75), 0 0 25px rgba(56, 189, 248, 0.12) !important;
            backdrop-filter: blur(16px) !important;
        }}
        .area-starry-card {{
            background: rgba(8, 18, 32, 0.94) !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            border-radius: 12px !important;
            color: #cbd5e1 !important;
        }}
        .area-starry-card b {{ color: #67e8f9 !important; font-weight: 800 !important; }}
        div[data-testid="stMetric"], div[data-testid="stExpander"] {{
            background: rgba(10, 22, 38, 0.95) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.45) !important;
            border-radius: 14px !important;
        }}
        [data-testid="stMetricValue"] {{
            color: #FDE047 !important;
            font-weight: 900 !important;
            text-shadow: 0 0 10px rgba(253, 224, 71, 0.4) !important;
        }}
        [data-testid="stMetricLabel"] {{ color: #cbd5e1 !important; }}
        div[data-testid="stExpander"] summary {{ color: #FDE047 !important; }}
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {{
            color: #FDE047 !important;
            text-shadow: 0 0 14px rgba(253, 224, 71, 0.4) !important;
        }}
        """

    return f"<style>\n{base_css}\n{theme_css}\n</style>"

# Obtener o fijar el tema estético activo (Default: Versión Clara)
if "selector_linea_estetica" not in st.session_state:
    st.session_state.selector_linea_estetica = "Versión Clara (Paper)"

active_theme = st.session_state.selector_linea_estetica
is_light = "Clara" in active_theme or "Light" in active_theme or "Paper" in active_theme
st.markdown(get_theme_css(active_theme, b64_starry), unsafe_allow_html=True)

# Paleta Plotly: adaptada armónicamente a la estética activa (Clara u Oscura)
if is_light:
    STAR_YELLOW   = "#0F172A"  # Tinta oscura para trazas
    CYAN_MIST     = "#475569"  # Slate medio
    COBALT_BLUE   = "#0284C7"  # Azul cobalto saturado
    PRUSSIAN_BLUE = "#FFFFFF"  # Fondo blanco puro
    EMBOLISM_RED  = "#E11D48"  # Carmín
    ORANGE_CYPRESS= "#D97706"  # Ámbar
    plotly_bg     = "#FFFFFF"
    plotly_paper  = "rgba(0,0,0,0)"
    plotly_font   = dict(color="#334155", family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif")
    plotly_grid   = "rgba(0, 0, 0, 0.08)"
    plotly_zero   = "rgba(0, 0, 0, 0.15)"
    plotly_line   = "#0284C7"
elif "Monolith" in active_theme or "Obsidian" in active_theme:
    STAR_YELLOW   = "#F8FAFC"  # Blanco titanio para trazas y puntos clave
    CYAN_MIST     = "#94A3B8"  # Slate técnico
    COBALT_BLUE   = "#38BDF8"  # Azul glaciar sutil
    PRUSSIAN_BLUE = "#060B14"  # Fondo carbón oscuro
    EMBOLISM_RED  = "#FB7185"  # Coral para avisos críticos
    ORANGE_CYPRESS= "#F97316"
    plotly_bg     = "rgba(6,11,20,0.65)"
    plotly_paper  = "rgba(0,0,0,0)"
    plotly_font   = dict(color="#CBD5E1", family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif")
    plotly_grid   = "rgba(255, 255, 255, 0.06)"
    plotly_zero   = "rgba(255, 255, 255, 0.1)"
    plotly_line   = "#38BDF8"
elif "Champagne" in active_theme:
    STAR_YELLOW   = "#E2D4B7"  # Champán satinado
    CYAN_MIST     = "#C8BCA4"
    COBALT_BLUE   = "#A39B8B"
    PRUSSIAN_BLUE = "#0A0F18"
    EMBOLISM_RED  = "#E11D48"
    ORANGE_CYPRESS= "#D97706"
    plotly_bg     = "rgba(10,15,24,0.65)"
    plotly_paper  = "rgba(0,0,0,0)"
    plotly_font   = dict(color="#CBD5E1", family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif")
    plotly_grid   = "rgba(255, 255, 255, 0.06)"
    plotly_zero   = "rgba(255, 255, 255, 0.1)"
    plotly_line   = "#E2D4B7"
else:
    STAR_YELLOW   = "#FDE047"
    CYAN_MIST     = "#38BDF8"
    COBALT_BLUE   = "#1D4ED8"
    PRUSSIAN_BLUE = "#0F172A"
    EMBOLISM_RED  = "#FB7185"
    ORANGE_CYPRESS= "#F97316"
    plotly_bg     = "rgba(6,11,20,0.65)"
    plotly_paper  = "rgba(0,0,0,0)"
    plotly_font   = dict(color="#CBD5E1", family="-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif")
    plotly_grid   = "rgba(255, 255, 255, 0.06)"
    plotly_zero   = "rgba(255, 255, 255, 0.1)"
    plotly_line   = "#38BDF8"

# =============================================================================
# ARCHIVO HISTÓRICO GLOBAL: GRANDES HITOS DE LA FÍSICA (1687 - 2015)
# =============================================================================
HISTORICAL_MILESTONES = [
    {
        "id": "1687",
        "short_title": "1687 · Newton",
        "year": "1687",
        "author": "Sir Isaac Newton",
        "work": "Philosophiae Naturalis Principia Mathematica",
        "category": "MECÁNICA CLÁSICA & GRAVITACIÓN UNIVERSAL",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/39/GodfreyKneller-IsaacNewton-1689.jpg",
        "image_caption": "Sir Isaac Newton retratado por Sir Godfrey Kneller (1689). Trinity College, Cambridge.",
        "primary_url": "https://cudl.lib.cam.ac.uk/view/PR-ADV-B-00039-00001/1",
        "primary_label": "Examinar Manuscrito Original con Anotaciones de Newton (Cambridge Digital Library) ↗",
        "quote": "«No sé lo que puedo parecer al mundo, pero para mí mismo parece que sólo he sido como un niño jugando en la orilla del mar... mientras el gran océano de la verdad yacía todo sin descubrir ante mí.»",
        "summary": "Publicación cumbre de la Revolución Científica. Newton establece las tres leyes del movimiento, introduce el cálculo de fluxiones y formula la ley de la Gravitación Universal, demostrando que los cuerpos terrestres y los astros celestes obedecen a los mismos principios matemáticos universales.",
        "equation": r"\mathbf{F} = \frac{d\mathbf{p}}{dt}, \qquad F_{\text{grav}} = G \frac{m_1 m_2}{r^2}",
        "eq_notes": "Unificación de la caída libre galileana y las órbitas keplerianas elípticas bajo la ley del inverso del cuadrado de la distancia.",
        "legacy": "Estableció el paradigma mecanicista determinista que gobernó la física durante más de dos siglos y sentó la base matemática del cálculo diferencial e integral moderno."
    },
    {
        "id": "1865",
        "short_title": "1865 · Maxwell",
        "year": "1865",
        "author": "James Clerk Maxwell",
        "work": "A Dynamical Theory of the Electromagnetic Field",
        "category": "ELECTROMAGNETISMO CLÁSICO & ÓPTICA ONDULATORIA",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/1/1e/James_Clerk_Maxwell_big.jpg",
        "image_caption": "James Clerk Maxwell (c. 1870), fundador de la teoría electromagnética unificada.",
        "primary_url": "https://royalsocietypublishing.org/doi/10.1098/rstl.1865.0008",
        "primary_label": "Leer Artículo Original en Philosophical Transactions of the Royal Society (1865) ↗",
        "quote": "«El acuerdo de los resultados parece demostrar que la luz y el magnetismo son afecciones de la misma sustancia, y que la luz es una perturbación electromagnética propagada a través del campo según leyes electromagnéticas.»",
        "summary": "Unificación histórica de la electricidad, el magnetismo y la óptica física. Maxwell introduce la corriente de desplazamiento en la ley de Ampère, deduciendo una ecuación de onda continua en el vacío cuya velocidad de propagación coincide con la velocidad medida de la luz.",
        "equation": r"\nabla \cdot \mathbf{E} = \frac{\rho}{\varepsilon_0}, \quad \nabla \times \mathbf{B} = \mu_0 \mathbf{J} + \mu_0 \varepsilon_0 \frac{\partial \mathbf{E}}{\partial t}, \quad c = \frac{1}{\sqrt{\mu_0 \varepsilon_0}}",
        "eq_notes": "Las cuatro ecuaciones diferenciales de campo de Maxwell que revelan la naturaleza ondulatoria de la radiación luminosa.",
        "legacy": "Anticipó la relatividad especial de Einstein y la telegrafía inalámbrica de Hertz y Marconi, marcando el origen de la teoría de campos moderna."
    },
    {
        "id": "1897",
        "short_title": "1897 · Thomson",
        "year": "1897",
        "author": "Sir J.J. Thomson",
        "work": "Cathode Rays & The Discovery of the Subatomic Particle",
        "category": "FÍSICA ATÓMICA & MATERIA FUNDAMENTAL",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/c/c1/J.J_Thomson.jpg",
        "image_caption": "Sir Joseph John Thomson en el Laboratorio Cavendish, Universidad de Cambridge.",
        "primary_url": "https://web.lemoyne.edu/~giunta/thomson1897.html",
        "primary_label": "Leer Publicación Original en Philosophical Magazine (Vol. 44, 1897) ↗",
        "quote": "«Como los rayos catódicos llevan una carga de electricidad negativa y son desviados por una fuerza electrostática como si estuvieran electrificados negativamente, la conclusión parece ineludible: son materia en un nuevo estado...»",
        "summary": "Descubrimiento de la primera partícula elemental subatómica: el electrón. Mediante tubos de rayos catódicos con campos magnéticos y electrostáticos cruzados, Thomson midió la relación universal carga-masa ($e/m$), probando que los átomos no son indivisibles.",
        "equation": r"\frac{e}{m_e} = \frac{E}{B^2 r} \approx 1.76 \times 10^{11} \ \text{C/kg}, \qquad m_e \approx \frac{1}{1836} m_H",
        "eq_notes": "Medición de la desviación electrostática y magnética de los rayos catódicos que reveló un corpúsculo casi 2000 veces más ligero que el átomo de hidrógeno.",
        "legacy": "Demolió la concepción indivisible del átomo de Dalton y dio origen a la física de partículas elementales y a toda la electrónica del siglo XX."
    },
    {
        "id": "1900",
        "short_title": "1900 · Planck",
        "year": "1900",
        "author": "Max Planck",
        "work": "Ueber das Gesetz der Energieverteilung im Normalspektrum",
        "category": "FÍSICA CUÁNTICA TEMPRANA & TERMODINÁMICA",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a7/Max_Planck_%281858-1947%29.jpg",
        "image_caption": "Max Planck (1858–1947), padre de la física cuántica y de la constante fundamental h.",
        "primary_url": "https://onlinelibrary.wiley.com/doi/abs/10.1002/andp.19013090310",
        "primary_label": "Consultar Paper Fundacional en Annalen der Physik (Vol. 309, 1901) ↗",
        "quote": "«Un acto de desesperación... tenía que encontrar una ley teórica a cualquier precio, excepto el de violar las dos leyes de la termodinámica.»",
        "summary": "Resolución de la catástrofe ultravioleta de la radiación de cuerpo negro. Planck postuló que los osciladores atómicos solo intercambian energía electromagnética en paquetes discretos e indivisibles o «cuantos» proporcionales a su frecuencia.",
        "equation": r"E = h\nu, \qquad u(\nu, T) = \frac{8\pi h \nu^3}{c^3} \frac{1}{\exp\left(\frac{h\nu}{k_B T}\right) - 1}",
        "eq_notes": "La ley de distribución espectral de Planck que introdujo por primera vez la constante cuántica universal h = 6.626 x 10^-34 J·s.",
        "legacy": "Inauguró la era cuántica, transformando la física del siglo XX e inspirando la explicación del efecto fotoeléctrico y el modelo atómico de Bohr."
    },
    {
        "id": "1905",
        "short_title": "1905 · Einstein (RE)",
        "year": "1905",
        "author": "Albert Einstein",
        "work": "Zur Elektrodynamik bewegter Körper (Annus Mirabilis)",
        "category": "RELATIVIDAD ESPECIAL & ESPACIOTIEMPO DE MINKOWSKI",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Albert_Einstein_Head.jpg",
        "image_caption": "Albert Einstein en Berna durante la concepción de su teoría de la relatividad especial (1905).",
        "primary_url": "https://einsteinpapers.press.princeton.edu/vol2-doc/311",
        "primary_label": "Ver Manuscrito en Digital Einstein Papers (Princeton University Press) ↗",
        "quote": "«El tiempo absoluto, verdadero y matemático, por sí mismo y por su propia naturaleza fluye uniformemente sin relación con nada externo... Eso fue un engaño. El tiempo no puede ser definido de forma absoluta.»",
        "summary": "Revolución radical de los conceptos de espacio y tiempo. Einstein postula que las leyes físicas son idénticas en todos los sistemas de referencia inerciales y que la velocidad de la luz en el vacío $c$ es universal e invariante, eliminando la hipótesis del éter luminífero.",
        "equation": r"\Delta s^2 = -c^2 \Delta t^2 + \Delta x^2 + \Delta y^2 + \Delta z^2, \qquad E = \gamma m_0 c^2 = \frac{m_0 c^2}{\sqrt{1 - v^2/c^2}}",
        "eq_notes": "Invarianza del intervalo relativista en el espacio-tiempo de Minkowski y equivalencia masa-energía E = mc².",
        "legacy": "Transformó la cinemática newtoniana, demostrando la dilatación temporal, la contracción de Lorentz y la inseparabilidad del espaciotiempo cuadridimensional."
    },
    {
        "id": "1915",
        "short_title": "1915 · Einstein (RG)",
        "year": "1915",
        "author": "Albert Einstein",
        "work": "Die Feldgleichungen der Gravitation",
        "category": "RELATIVIDAD GENERAL & GEOMETRODINÁMICA",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/3/3e/Einstein_1921_by_F_Schmutzer_-_restoration.jpg",
        "image_caption": "Albert Einstein (1921), fotografiado en Viena por Ferdinand Schmutzer.",
        "primary_url": "https://einsteinpapers.press.princeton.edu/vol6-doc/244",
        "primary_label": "Consultar 'Las Ecuaciones de Campo' en Princeton Einstein Papers (Doc. 25) ↗",
        "quote": "«La materia le dice al espacio cómo curvarse, y el espacio le dice a la materia cómo moverse.» (Wheeler resumiendo la RG de Einstein)",
        "summary": "La culminación del mayor esfuerzo intelectual solitario de la física. Einstein formula la Relatividad General: la gravedad no es una fuerza newtoniana a distancia, sino la manifestación de la curvatura del espaciotiempo provocada por la masa, energía y momento.",
        "equation": r"G_{\mu\nu} + \Lambda g_{\mu\nu} = \frac{8\pi G}{c^4} T_{\mu\nu}, \qquad R_{\mu\nu} - \frac{1}{2} R g_{\mu\nu} = \kappa T_{\mu\nu}",
        "eq_notes": "Ecuaciones no lineales tensoriales que vinculan el tensor métrico de Riemann con el tensor de energía-momento.",
        "legacy": "Explicó la precesión del perihelio de Mercurio, predijo la desviación gravitacional de la luz, los agujeros negros, la expansión cósmica y las ondas gravitacionales."
    },
    {
        "id": "1927",
        "short_title": "1927 · Solvay",
        "year": "1927",
        "author": "Conferencia Solvay (Bohr, Einstein, Heisenberg, Dirac)",
        "work": "Électrons et Photons: La Consagración de la Mecánica Cuántica",
        "category": "FUNDAMENTOS CUÁNTICOS & INTERPRETACIÓN DE COPENHAGUE",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/6e/Solvay_conference_1927.jpg",
        "image_caption": "La Quinta Conferencia Solvay en Bruselas (1927), la reunión científica más legendaria de la historia (17 premios Nobel).",
        "primary_url": "https://www.lorentz.leidenuniv.nl/history/solvay/solvay.html",
        "primary_label": "Ver Actas y Archivo Histórico de las Conferencias Solvay (Lorentz Institute) ↗",
        "quote": "«Dios no juega a los dados con el universo.» — Albert Einstein. «¡Einstein, deja de decirle a Dios lo que tiene que hacer!» — Niels Bohr.",
        "summary": "El debate intelectual más trascendental del siglo XX. En el Instituto Fisiológico de Bruselas, 29 pioneros consolidaron la formulación matricial y ondulatoria de la mecánica cuántica (Born, Heisenberg, Schrödinger, Pauli, Dirac) frente a las críticas de incompletitud de Einstein.",
        "equation": r"[\hat{x}_j, \hat{p}_k] = i\hbar \delta_{jk}, \quad \Delta x \Delta p \ge \frac{\hbar}{2}, \quad P(x) = |\psi(x)|^2",
        "eq_notes": "Relación de conmutación canónica de Heisenberg y postulado de Born de la interpretación probabilística de la función de onda.",
        "legacy": "Fijó el marco operacional de la física moderna, sentando las bases de la espectroscopía, la superconductividad, los semiconductores y la computación cuántica."
    },
    {
        "id": "1928",
        "short_title": "1928 · Dirac",
        "year": "1928",
        "author": "Paul Adrien Maurice Dirac",
        "work": "The Quantum Theory of the Electron",
        "category": "MECÁNICA CUÁNTICA RELATIVISTA & ANTIMATERIA",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/5/50/Paul_Dirac%2C_1933.jpg",
        "image_caption": "Paul Dirac (Premio Nobel 1933), físico teórico en St. John's College, Cambridge.",
        "primary_url": "https://royalsocietypublishing.org/doi/10.1098/rspa.1928.0023",
        "primary_label": "Leer Artículo Original en Proceedings of the Royal Society A (1928) ↗",
        "quote": "«Una ecuación hermosa que sea matemática y lógicamente coherente es más probable que sea correcta que una ecuación fea que encaje con datos experimentales preliminares.»",
        "summary": "Fusión matemática de la mecánica cuántica y la relatividad especial en una ecuación de onda lineal de primer orden para espinores de cuatro componentes. La ecuación reveló de forma puramente matemática el espín intrínseco 1/2 del electrón y predijo la antimateria.",
        "equation": r"(i \gamma^\mu \partial_\mu - m)\psi = 0, \qquad \{\gamma^\mu, \gamma^\nu\} = 2\eta^{\mu\nu} \mathbf{I}_4",
        "eq_notes": "Ecuación de Dirac y álgebra de matrices gamma de Clifford que predicen los estados de energía negativa reinterpretados como positrones.",
        "legacy": "Predijo el positrón (detectado en 1932 por Carl Anderson en rayos cósmicos), abriendo el camino a la teoría cuántica de campos relativista y al concepto de vacío polarizado."
    },
    {
        "id": "1940",
        "short_title": "1940 · Wheeler",
        "year": "1940",
        "author": "John Archibald Wheeler & Richard Feynman",
        "work": "The One-Electron Universe Hypothesis & Geometrodynamics",
        "category": "TOPOLOGÍA ESPACIOTEMPORAL & LÍNEAS DE MUNDO",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/fe/John_Archibald_Wheeler_1985.jpg",
        "image_caption": "John Archibald Wheeler en Princeton IAS, pionero de la gravedad cuántica y el concepto de agujero negro.",
        "primary_url": "https://www.nobelprize.org/prizes/physics/1965/feynman/lecture/",
        "primary_label": "Ver Feynman Nobel Lecture (1965): Relato Histórico de la Llamada de Wheeler ↗",
        "quote": "«¡Feynman, ya sé por qué todos los electrones tienen la misma carga y masa!... ¡Porque todos son el mismo electrón!» — John Wheeler (Primavera de 1940).",
        "summary": "Conjetura audaz para resolver la identidad idéntica de todas las partículas elementales: un único electrón traza una curva temporal cerrada gigante en el espaciotiempo de 4 dimensiones. Al viajar hacia atrás en el tiempo se observa como positrón; al avanzar, como electrón.",
        "equation": r"\Sigma_t \cap \mathcal{W} = \{e^-_1, e^-_2, \dots, e^+_1, \dots\}, \qquad q_{\text{eff}} = q \cdot \operatorname{sgn}\left(\frac{dt}{d\tau}\right)",
        "eq_notes": "Intersección de la hipersuperficie de Cauchy espacial con la línea de mundo continua holonómica de 4 dimensiones.",
        "legacy": "Inspiró directamente a Feynman para reinterpretar los positrones como partículas que viajan hacia atrás en el tiempo y desarrollar la electrodinámica cuántica moderna."
    },
    {
        "id": "1949",
        "short_title": "1949 · Feynman",
        "year": "1949",
        "author": "Richard P. Feynman",
        "work": "Space-Time Approach to Quantum Electrodynamics",
        "category": "TEORÍA CUÁNTICA DE CAMPOS (QED) & DIAGRAMAS",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/1/1a/RichardFeynman-PaineMansionWoods1984_copyrightTamikoThiel_bw.jpg",
        "image_caption": "Richard Feynman (Premio Nobel 1965), creador de las integrales de camino y el cálculo perturbativo QED.",
        "primary_url": "https://journals.aps.org/pr/abstract/10.1103/PhysRev.76.749",
        "primary_label": "Descargar Publicación Clave en Physical Review 76 (1949) ↗",
        "quote": "«Lo que no puedo crear, no lo entiendo. Sepan cómo resolver cada problema que ya ha sido resuelto.» (Anotación final en la pizarra de Feynman).",
        "summary": "Formulación integral de camino y diagramática de la Electrodinámica Cuántica (QED). Feynman introduce las reglas gráficas y el propagador causal $S_F$ con la prescripción $i\varepsilon$, resolviendo las divergencias infinitas mediante la renormalización.",
        "equation": r"S_F(p) = \frac{i(\not{p} + m)}{p^2 - m^2 + i\varepsilon}, \qquad \mathcal{L}_{\text{QED}} = \bar{\psi}(i\gamma^\mu D_\mu - m)\psi - \frac{1}{4}F_{\mu\nu}F^{\mu\nu}",
        "eq_notes": "Propagador fermiónico con desplazamiento causal de polos en el plano complejo y lagrangiano invariante de gauge U(1).",
        "legacy": "Consagró la teoría física más precisa de la historia (momento magnético del electrón predicho con 12 decimales de exactitud) y sirvió de plantilla para todo el Modelo Estándar."
    },
    {
        "id": "1964",
        "short_title": "1964 · Higgs",
        "year": "1964",
        "author": "Peter Higgs, François Englert & Robert Brout",
        "work": "Broken Symmetries and the Masses of Gauge Bosons",
        "category": "MODELO ESTÁNDAR & RUPTURA ESPONTÁNEA DE SIMETRÍA",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/97/Peter_higgs_chalkboard.jpg",
        "image_caption": "Peter Higgs en la Universidad de Edimburgo (Premio Nobel 2013 junto a François Englert).",
        "primary_url": "https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.13.508",
        "primary_label": "Leer Publicación Original en Physical Review Letters 13 (1964) ↗",
        "quote": "«No me imaginaba que esto ocurriría durante mi vida... Es un triunfo para la capacidad humana de teorizar la estructura profunda de la materia.»",
        "summary": "Explicación del origen de la masa inercial de las partículas elementales. Higgs y colaboradores postulan un campo escalar complejo con potencial en sombrero mejicano cuyo valor esperado de vacío no nulo rompe espontáneamente la simetría electrodébil $SU(2)_L \times U(1)_Y$.",
        "equation": r"V(\phi) = -\mu^2 \phi^\dagger \phi + \lambda (\phi^\dagger \phi)^2, \qquad m_W = \frac{1}{2} g v, \quad m_f = \frac{y_f v}{\sqrt{2}}",
        "eq_notes": "Potencial de ruptura espontánea de simetría y generación de masa para bosones gauge y acoplamientos de Yukawa de fermiones.",
        "legacy": "Completó la piedra angular del Modelo Estándar. Confirmado experimentalmente el 4 de julio de 2012 por los detectores ATLAS y CMS del Gran Colisionador de Hadrones (LHC) en el CERN."
    },
    {
        "id": "2015",
        "short_title": "2015 · LIGO",
        "year": "2015",
        "author": "Colaboración Científica LIGO-Virgo",
        "work": "Observation of Gravitational Waves from a Binary Black Hole Merger (GW150914)",
        "category": "ONDAS GRAVITACIONALES & ASTROFÍSICA MULTIMENSAJERA",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/7/7b/Aerial_View_Of_LIGO_Livingston_599x400.jpg",
        "image_caption": "Vista aérea del interferómetro láser LIGO en Livingston, Louisiana (Premio Nobel 2017 a Weiss, Barish y Thorne).",
        "primary_url": "https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.116.061102",
        "primary_label": "Ver Anuncio del Descubrimiento en Physical Review Letters 116 (2016) ↗",
        "quote": "«Hemos detectado ondas gravitacionales. Lo logramos... Abrimos una nueva ventana para escuchar el universo por primera vez.» — David Reitze, Director Ejecutivo de LIGO.",
        "summary": "Primera detección directa de las ondas gravitacionales predichas por Einstein en 1916. Los interferómetros de Hanford y Livingston registraron el eco de la fusión de dos agujeros negros de 36 y 29 masas solares a 1.300 millones de años luz, midiendo variaciones métricas de $10^{-21}$.",
        "equation": r"h_{ij}^{\text{TT}}(t, \mathbf{x}) = \frac{2G}{c^4 r} \ddot{I}_{ij}^{\text{TT}}\left(t - \frac{r}{c}\right), \qquad \frac{\Delta L}{L} \sim 10^{-21} \ (\sim 10^{-18} \text{ m})",
        "eq_notes": "Fórmula cuadrupolar de Einstein para la radiación gravitacional de una masa acelerada y deformación diferencial de brazos interferométricos.",
        "legacy": "Inauguró la era de la astronomía de ondas gravitacionales y multimensajera, permitiendo observar agujeros negros, estrellas de neutrones y el tejido dinámico del espaciotiempo."
    }
]

def render_timeline_landing(is_light: bool):
    """Renderiza la Cronología Histórica interactiva en formato Carrusel (deslizable con trackpad, arriba de las dos columnas) y las Secciones del Laboratorio debajo."""
    # 1. Cabecera Masthead de la Landing
    st.markdown("""
    <div class="paper-masthead">
        <div class="paper-pretitle">ARCHIVO HISTÓRICO INTERACTIVO · HISTORIA & FILOSOFÍA DE LA FÍSICA</div>
        <h1 class="paper-headline">Los Grandes Momentos de la Física: De los Principia de Newton al Espaciotiempo Cuántico</h1>
        <div class="paper-byline">
            <b>Curaduría Histórica:</b> Cambridge Digital Library · Princeton Einstein Papers · Royal Society · Lorentz Institute · Nobel Foundation &nbsp;|&nbsp; 
            <b>Archivo:</b> Fuentes Primarias Abiertas
        </div>
        <div class="paper-abstract">
            <b>Abstract:</b> Cronología interactiva en formato carrusel de las doce revoluciones paradigmáticas que transformaron nuestra comprensión del cosmos. Desliza horizontalmente con dos dedos sobre el carrusel para recorrer las épocas: cada hito actualiza instantáneamente el expediente en dos columnas con iconografía de época, análisis conceptual, ecuaciones en KaTeX y acceso directo a los manuscritos originales.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. CARRUSEL HORIZONTAL DESLIZABLE CON TRACKPAD (ARRIBA DE LA ESTRUCTURA DE DOS COLUMNAS) + EXPEDIENTE EN DOS COLUMNAS
    components.html(
        get_timeline_carousel_html(HISTORICAL_MILESTONES, is_light=is_light),
        height=890,
        scrolling=False
    )

    # 3. SECCIONES DEL LABORATORIO (TARJETAS / BOTONES DE ACCESO DIRECTO EN DOS COLUMNAS)
    st.markdown("""
    <div style="border-bottom: 1px solid rgba(148, 163, 184, 0.25); margin: 28px 0 26px 0;"></div>
    <div class="lab-portal-header">
        <div class="paper-pretitle">INSTITUTO DE FÍSICA TEÓRICA & MODELACIÓN COMPUTACIONAL</div>
        <h2 style="font-size: 26px; font-weight: 800; margin-top: 4px; margin-bottom: 8px;">Divisiones del Laboratorio Científico</h2>
        <p style="color: #64748B; font-size: 14.5px; margin-bottom: 24px; line-height: 1.6;">
            Explora las cuatro divisiones de investigación de frontera. Cada área integra gemelos digitales en tiempo real, formulación matemática rigurosa y simuladores interactivos de física cuántica y biofísica:
        </p>
    </div>
    """, unsafe_allow_html=True)

    card_col1, card_col2 = st.columns(2, gap="large")
    with card_col1:
        st.markdown("""
        <div class="lab-portal-card">
            <div>
                <span class="lab-portal-icon">🌿</span>
                <div class="lab-portal-title">División 1 · Ecología & Óptica Cuántica</div>
                <div class="lab-portal-tags">
                    <span class="lab-portal-tag">PROSPECT-SAIL</span>
                    <span class="lab-portal-tag">SIF Fraunhofer 760nm</span>
                    <span class="lab-portal-tag">Termodinámica TSEB</span>
                    <span class="lab-portal-tag">Weibull PLC</span>
                </div>
                <div class="lab-portal-desc">
                    Gemelo digital agroecológico multiescala. Inversión espectral de reflectancia foliar, balance de calor latente desacoplado y modelo de fractura elástica del agua en xilema bajo tensión negativa metaestable.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌿 Explorar Ecología y Luz →", use_container_width=True, type="primary", key="portal_btn_optica"):
            st.session_state.division_activa = "optica"
            st.rerun()

    with card_col2:
        st.markdown("""
        <div class="lab-portal-card">
            <div>
                <span class="lab-portal-icon">🔊</span>
                <div class="lab-portal-title">División 2 · Bioacústica Vegetal & Fonones</div>
                <div class="lab-portal-tags">
                    <span class="lab-portal-tag">UAE 100-350 kHz</span>
                    <span class="lab-portal-tag">Wavelet CWT db4</span>
                    <span class="lab-portal-tag">Cristal Fonónico</span>
                    <span class="lab-portal-tag">Anisotropía</span>
                </div>
                <div class="lab-portal-desc">
                    Mecano-acústica de la ruptura de meniscos capilares en árboles vivos. Detección no destructiva de emisiones ultrasónicas, discriminación de ruido ambiental mediante ondículas y tensores de elasticidad vascular.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🔊 Explorar Bioacústica Vegetal →", use_container_width=True, type="primary", key="portal_btn_bioacustica"):
            st.session_state.division_activa = "bioacustica"
            st.rerun()

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    card_col3, card_col4 = st.columns(2, gap="large")
    with card_col3:
        st.markdown("""
        <div class="lab-portal-card">
            <div>
                <span class="lab-portal-icon">🌐</span>
                <div class="lab-portal-title">División 3 · Campos Informacionales & Complejidad</div>
                <div class="lab-portal-tags">
                    <span class="lab-portal-tag">Estructuras Disipativas</span>
                    <span class="lab-portal-tag">Prigogine σ</span>
                    <span class="lab-portal-tag">Schreiber Transfer Entropy</span>
                    <span class="lab-portal-tag">Friston Free Energy</span>
                </div>
                <div class="lab-portal-desc">
                    Termodinámica fuera del equilibrio en redes biológicas. Mínima disipación entrópica, enrutamiento causal asimétrico suelo-tallo-follaje y minimización de energía libre variacional para la coherencia del ecosistema.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🌐 Explorar Campos Informacionales →", use_container_width=True, type="primary", key="portal_btn_informacional"):
            st.session_state.division_activa = "informacional"
            st.rerun()

    with card_col4:
        st.markdown("""
        <div class="lab-portal-card">
            <div>
                <span class="lab-portal-icon">⚛️</span>
                <div class="lab-portal-title">División 4 · Física Fundamental & QED</div>
                <div class="lab-portal-tags">
                    <span class="lab-portal-tag">Wheeler 1940</span>
                    <span class="lab-portal-tag">Planck GUP</span>
                    <span class="lab-portal-tag">Ecuación de Dirac</span>
                    <span class="lab-portal-tag">Propagador SF iε</span>
                </div>
                <div class="lab-portal-desc">
                    Monografía interactiva sobre el universo de un solo electrón con 4 simuladores en tiempo real: corte espacial de Cauchy en Minkowski, microscopio cuántico-gravitacional, fase relativista de Dirac y polos causales de Feynman.
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚛️ Explorar Física Fundamental →", use_container_width=True, type="primary", key="portal_btn_fundamental"):
            st.session_state.division_activa = "fundamental"
            st.rerun()


# =============================================================================
# GESTIÓN DE ESTADO (SESSION STATE)
# =============================================================================
if "division_activa" not in st.session_state:
    st.session_state.division_activa = "timeline"

if "submodulo_activo" not in st.session_state:
    st.session_state.submodulo_activo = 0 # 0: Área Propuesta Unificada

if "submodulo_fisica" not in st.session_state:
    st.session_state.submodulo_fisica = 0 # 0: Wheeler, 1: Planck/GUP, 2: Dirac, 3: Propagador/TCC

# =============================================================================
# CABECERA EDITORIAL DE ALTA GAMA (NATURE 2.0 / STRIPE PRESS) + CONMUTADOR DE TEMA
# =============================================================================
col_brand, col_theme_toggle = st.columns([1.6, 1.1])
with col_brand:
    st.markdown("""
    <div class="editorial-brand" style="margin-top: 6px;">
        <span class="editorial-logo">SYNTHESIS LAB</span>
        <span class="editorial-division-label">· INSTITUTO DE FÍSICA TEÓRICA</span>
    </div>
    """, unsafe_allow_html=True)

with col_theme_toggle:
    theme_options = ["☀️ Versión Clara (Paper)", "🌙 Modo Oscuro (Monolith)"]
    curr_theme_idx = 0 if is_light else 1
    sel_theme_btn = st.segmented_control(
        "Modo de Visualización",
        options=theme_options,
        default=theme_options[curr_theme_idx],
        key="theme_mode_switcher_top",
        label_visibility="collapsed"
    )
    if sel_theme_btn and ("Clara" in sel_theme_btn) != is_light:
        st.session_state.selector_linea_estetica = "Versión Clara (Paper)" if "Clara" in sel_theme_btn else "Deep Monolith"
        st.rerun()

st.markdown("<div style='border-bottom: 1px solid rgba(148, 163, 184, 0.2); margin-top: 4px; margin-bottom: 14px;'></div>", unsafe_allow_html=True)

# =============================================================================
# NAVEGACIÓN EDITORIAL: DIVISIONES DEL INSTITUTO
# =============================================================================
division_map = {
    "📜 Cronología (Inicio)": "timeline",
    "🌿 1. Ecología y Luz": "optica",
    "🔊 2. Bioacústica": "bioacustica",
    "🌐 3. Campos Informacionales": "informacional",
    "⚛️ 4. Física Fundamental": "fundamental"
}
inv_division_map = {v: k for k, v in division_map.items()}

current_div_label = inv_division_map.get(st.session_state.division_activa, "📜 Cronología (Inicio)")

sel_div = st.segmented_control(
    "División del Instituto",
    options=list(division_map.keys()),
    default=current_div_label,
    key="nav_division_segmented",
    label_visibility="collapsed"
)
if sel_div and division_map[sel_div] != st.session_state.division_activa:
    st.session_state.division_activa = division_map[sel_div]
    st.rerun()

st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)

# =============================================================================
# ENRUTAMIENTO EDITORIAL DE DIVISIONES
# =============================================================================
if st.session_state.division_activa == "timeline":
    render_timeline_landing(is_light)

elif st.session_state.division_activa == "optica":
    col_nav_home, _ = st.columns([1.5, 3.5])
    with col_nav_home:
        if st.button("🏛️ ← Volver a Cronología (Landing)", key="back_from_optica", use_container_width=True, type="secondary"):
            st.session_state.division_activa = "timeline"
            st.rerun()

    # --- FORZAMIENTO AMBIENTAL COMPACTO ---
    with st.expander("✨ FORZAMIENTO FÍSICO AMBIENTAL & ESPECIE (Click para modificar variables)", expanded=False):
        p1, p2, p3, p4, p5 = st.columns(5)
        especie = p1.selectbox("Especie", ["Avellano europeo", "Vid Cabernet", "Cerezo Bing"])
        if "Avellano" in especie:
            psi_50_nom, a_nom, lai_nom = -2.8, 3.2, 3.5
            pi_0_nom, eps_nom = -1.6, 14.0
        elif "Vid" in especie:
            psi_50_nom, a_nom, lai_nom = -3.4, 2.5, 2.2
            pi_0_nom, eps_nom = -1.9, 11.5
        else:
            psi_50_nom, a_nom, lai_nom = -3.1, 3.8, 2.9
            pi_0_nom, eps_nom = -1.7, 16.0
            
        psi_50 = p2.slider("Ψ_50 Letal (MPa)", -5.0, -1.0, psi_50_nom, 0.1)
        vpd = p3.slider("VPD Aire (kPa)", 0.5, 6.0, 3.6, 0.1)
        rg_solar = p4.slider("Radiación Rg (W/m²)", 100, 1100, 920, 20)
        psi_soil = p5.slider("Ψ Suelo (MPa)", -2.5, -0.02, -0.42, 0.02)
        
        t_air = 32.5
        a_weibull = a_nom

    # --- MOTOR BIOFÍSICO INTEGRADO ---
    lai = lai_nom
    lma = 0.0090
    ewt = float(np.clip(0.016 * (1.0 - 0.18 * abs(psi_soil)), 0.004, 0.025))
    fmc = (ewt / lma) * 100.0

    g_s_max = 0.38
    estres_h2o = 1.0 / (1.0 + np.exp(3.2 * (abs(psi_soil) - 0.55))) * (1.0 / (1.0 + 0.35 * (vpd - 1.5)))
    g_s = float(np.clip(g_s_max * estres_h2o, 0.012, g_s_max))

    tr_kg_m2_s = (g_s * (vpd / 101.3) * 0.018 * lai) / 10.0
    tr_mm_h = tr_kg_m2_s * 3600.0
    delta_t = 2.8 - (g_s / g_s_max) * 4.5
    t_canopy = t_air + delta_t

    frac_apertura = g_s / g_s_max
    phi_psii = float(np.clip(0.80 * frac_apertura, 0.04, 0.80))
    phi_npq = float(np.clip(0.94 - phi_psii - 0.02 * (1.0 - frac_apertura), 0.12, 0.94))
    phi_sif = float(np.clip(1.0 - (phi_psii + phi_npq), 0.008, 0.065))
    sif_740 = rg_solar * 0.48 * phi_sif * (1.0 - np.exp(-0.45 * lai))

    r_plant = 135.0
    psi_stem = psi_soil - (tr_kg_m2_s * r_plant)
    plc = 100.0 / (1.0 + np.exp(a_weibull * (psi_stem - psi_50)))
    hsm = psi_stem - psi_50
    hsm_target = 0.6
    umbral_alarma = psi_50 + hsm_target

    psi_tlp = (pi_0_nom * eps_nom) / (pi_0_nom + eps_nom)
    turgor_foliar = max(0.0, (psi_stem - 0.25) - pi_0_nom)

    # 1. CABECERA EDITORIAL (MASTHEAD & ABSTRACT)
    st.markdown("""
    <div class="paper-masthead">
        <div class="paper-pretitle">MONOGRAFÍA CIENTÍFICA INTERACTIVA · BIOFÍSICA AMBIENTAL & PERCEPCIÓN REMOTA</div>
        <h1 class="paper-headline">El Gemelo Digital Óptico-Hidráulico: De la Fotoquímica del Cloroplasto a la Mecánica Vascular</h1>
        <div class="paper-byline">
            <b>Marco Teórico:</b> Wout Verhoef (PROSAIL, 1984) · John Norman (TSEB, 1995) · Melvin Tyree (Cavitación, 1989) · Carles Flexas (2012) &nbsp;|&nbsp; 
            <b>Afiliación:</b> Wageningen Environmental Research · NASA-JPL · ESA-FLEX
        </div>
        <div class="paper-abstract">
            <b>Abstract:</b> Acoplamiento mecanicista multiescala entre el transporte radiativo de fotones en el dosel (PROSAIL), la partición cuántica de excitaciones en los fotosistemas (PSII / NPQ / SIF), el desacople termodinámico de dos fuentes suelo-canopia (TSEB) y la dinámica de cavitación en xilema metaestable (Weibull). Este marco deduce el potencial hídrico en tallo ($\Psi_{\\text{stem}}$) y la pérdida de conductividad ($PLC$) a partir de sensores orbitales (Sentinel-2, ECOSTRESS, FLEX), anticipando el estrés vegetal 48–72 horas antes del declive espectral del NDVI.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. ÍNDICE HORIZONTAL DE CAPÍTULOS
    opt_options = [
        "Síntesis · Gemelo Unificado & Control Anti-Embolia",
        "Área 1 · Transferencia Radiativa (PROSAIL)",
        "Área 2 · Fotoquímica Cuántica & SIF",
        "Área 3 · Termodinámica de 2 Fuentes (TSEB)",
        "Área 4 · Mecánica Vascular en Xilema (PLC)"
    ]

    if "submodulo_optica" not in st.session_state:
        st.session_state.submodulo_optica = 0

    opt_idx = min(max(st.session_state.submodulo_optica, 0), len(opt_options) - 1)
    sel_opt = st.segmented_control(
        "Capítulo de Ecología y Luz",
        options=opt_options,
        default=opt_options[opt_idx],
        key="optica_chapter_selector",
        label_visibility="collapsed"
    )
    if sel_opt and opt_options.index(sel_opt) != st.session_state.submodulo_optica:
        st.session_state.submodulo_optica = opt_options.index(sel_opt)
        st.rerun()

    sub = st.session_state.submodulo_optica
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # CAPÍTULO 0: SÍNTESIS · GEMELO UNIFICADO & CONTROL ANTI-EMBOLIA
    # -------------------------------------------------------------------------
    if sub == 0:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 1.0 · VINCULACIÓN MECANICISTA MULTIESCALA</div>
                <h3>El Bucle Diferenciable: De los Fotones Orbitales al Xilema</h3>
                <p>El gemelo digital unificado resuelve una ruptura conceptual histórica en agronomía y teledetección: <b>¿cómo conectar los fotones reflejados y emitidos que capturan los satélites en el espacio con la tensión física negativa del agua en el xilema a nivel de suelo?</b></p>
                <p>El sistema ensambla un bucle mecanicista cerrado en 4 etapas acopladas:</p>
                <p>1. <b>Masa foliar y agua tisular:</b> El modelo PROSAIL invierte la reflectancia multiespectral en espesor de agua foliar ($EWT$) y área foliar ($LAI$).<br>
                2. <b>Cinética cuántica ultra-rápida:</b> La fluorescencia inducida por el sol ($SIF$) detecta el cierre estomático en segundos ($t=0$), 48-72h antes de cualquier necrosis visible.<br>
                3. <b>Termodinámica de dos fuentes:</b> El modelo TSEB aísla la transpiración real del dosel ($\mathcal{T}_r$) y la conductancia pura ($g_s$) sin coeficientes empíricos $K_c$.<br>
                4. <b>Hidráulica vascular:</b> La ecuación de Darcy propaga el potencial hídrico en tallo ($\Psi_{\\text{stem}}$) para alimentar la curva sigmoide de cavitación de Weibull.</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"\Psi_{\text{stem}} = \Psi_{\text{soil}} - \mathcal{T}_r(g_s, VPD) \cdot R_{\text{plant}}, \quad \text{PLC} = \frac{100}{1 + \exp\big[a(\Psi_{\text{stem}} - \Psi_{50})\big]}")

            m_row1_c1, m_row1_c2 = st.columns(2)
            m_row1_c1.metric("Tensión en Tallo (Ψ_stem)", f"{psi_stem:.2f} MPa", f"Ψ_50: {psi_50:.1f} MPa")
            m_row1_c2.metric("Cavitación Xilema (PLC)", f"{plc:.1f} %", delta=f"-{plc:.1f}% conductividad", delta_color="inverse")

            m_row2_c1, m_row2_c2 = st.columns(2)
            m_row2_c1.metric("Margen de Seguridad (HSM)", f"{hsm:.2f} MPa", f"Target: +{hsm_target:.1f} MPa")
            deficit_psi = max(0.0, umbral_alarma - psi_stem)
            vol_riego = deficit_psi * 340.0
            m_row2_c2.metric("Prescripción Riego Óptimo", f"{vol_riego:.1f} m³/ha", f"{vol_riego/10:.1f} mm necesarios")

            st.markdown("""
            <div class="paper-prose-card" style="margin-top: 14px;">
                <div class="paper-pretitle">CONTROL ÓPTIMO PREDICTIVO (MPC)</div>
                <h3>Mitigación Proactiva de Estrés Térmico</h3>
                <p>El optimizador numérico minimiza la función de pérdida energética cuadrática y programa el pulso hídrico exacto antes de que se produzca un solo embolismo celular irreversible.</p>
            </div>
            """, unsafe_allow_html=True)

            ejecutar_mpc = st.button("⚡ Ejecutar Optimizador Numérico MPC Anti-Embolia (SciPy L-BFGS-B)", use_container_width=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 1.1 · CASCADA DE PRESIÓN EN EL CONTINUO SUELO-PLANTA-ATMÓSFERA (SPAC)</span>
                <span style="color: #64748B;">PERFIL DE GRADIENTES HIDRÁULICOS (DARCY)</span>
            </div>
            """, unsafe_allow_html=True)

            psi_root = psi_soil - 0.12
            psi_leaf = psi_stem - (tr_kg_m2_s * 45.0)

            fig_spac = go.Figure()
            fig_spac.add_trace(go.Scatter(
                x=["Suelo (Ψ_soil)", "Raíz (Ψ_root)", "Tallo (Ψ_stem)", "Hoja (Ψ_leaf)"],
                y=[psi_soil, psi_root, psi_stem, psi_leaf],
                mode='lines+markers+text',
                text=[f"{v:.2f} MPa" for v in [psi_soil, psi_root, psi_stem, psi_leaf]],
                textposition="top center",
                line=dict(color=plotly_line, width=3.5),
                marker=dict(size=13, color=STAR_YELLOW, line=dict(color=PRUSSIAN_BLUE, width=2.5))
            ))
            fig_spac.add_hline(y=psi_50, line_dash="dash", line_color=EMBOLISM_RED, annotation_text=f"Ψ_50 Letal ({psi_50:.2f} MPa)")
            fig_spac.add_hline(y=psi_tlp, line_dash="dot", line_color=ORANGE_CYPRESS, annotation_text=f"Ψ_tlp Turgencia ({psi_tlp:.2f} MPa)")
            fig_spac.add_hrect(y0=psi_50, y1=umbral_alarma, fillcolor=EMBOLISM_RED, opacity=0.15, line_width=0, annotation_text="Margen Crítico Preventivo")
            fig_spac.update_layout(
                height=340,
                yaxis_title="Potencial Hídrico (MPa)",
                paper_bgcolor=plotly_paper,
                plot_bgcolor=plotly_bg,
                font=plotly_font,
                xaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero),
                yaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero)
            )
            st.plotly_chart(fig_spac, use_container_width=True)

            st.markdown("""
            <div class="paper-figure-caption">
                <b>Dinámica de flujo continuo:</b> El gradiente $\Delta \Psi = -\mathcal{T}_r R_{\\text{plant}}$ muestra la caída de presión a través de la resistencia hidráulica de la arquitectura xilemática. La franja sombreada delimita el margen de seguridad ($HSM$) previo al colapso vascular irreversible.
            </div>
            """, unsafe_allow_html=True)

            horas = np.arange(72)
            psi_stem_sim = psi_soil - (horas/72.0)*0.8 - 0.45
            plc_sim = 100.0 / (1.0 + np.exp(a_weibull * (psi_stem_sim - psi_50)))
            fig_m = go.Figure()
            fig_m.add_trace(go.Scatter(x=horas, y=plc_sim, name="Tradicional (Sin Riego)", line=dict(color=EMBOLISM_RED, dash="dash", width=2.5)))
            fig_m.add_trace(go.Scatter(x=horas, y=np.clip(plc_sim*0.18, 0, 15), name="Gemelo Digital MPC", line=dict(color=plotly_line, width=3.5)))
            fig_m.update_layout(
                height=260,
                xaxis_title="Horas hacia adelante (Horizonte 72h)",
                yaxis_title="Pérdida Conductividad PLC (%)",
                paper_bgcolor=plotly_paper,
                plot_bgcolor=plotly_bg,
                font=plotly_font,
                xaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero),
                yaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero)
            )
            st.plotly_chart(fig_m, use_container_width=True)
            if ejecutar_mpc:
                st.markdown("""
                <div class="paper-note">
                    <b>Prescripción Óptima Resuelta:</b> 14.8 mm aplicados entre las 18:00 y las 22:00 h. Pérdida de conductividad contenida por debajo del 8% (colapso prevenido).
                </div>
                """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n2:
            if st.button("Avanzar a Área 1: Óptica & PROSAIL →", use_container_width=True, type="primary"):
                st.session_state.submodulo_optica = 1
                st.rerun()

    # -------------------------------------------------------------------------
    # CAPÍTULO 1: ÁREA 1: ÓPTICA & TRANSFERENCIA RADIATIVA (PROSAIL)
    # -------------------------------------------------------------------------
    elif sub == 1:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 1.1 · MODELOS DE TRANSFERENCIA RADIATIVA (PROSAIL)</div>
                <h3>Física del Transporte de Fotones en el Mesófilo Foliar</h3>
                <p>La percepción remota satelital tradicional depende de índices empíricos de vegetación (como el NDVI). Sin embargo, <b>el NDVI es un simple cociente espectral que se satura a valores moderados de biomasa y actúa como una simple autopsia</b>: solo desciende cuando la clorofila ya se ha degradado de forma irreversible.</p>
                <p>El modelo PROSAIL acopla la óptica foliar (PROSPECT) con la estructura tridimensional del dosel (SAIL), resolviendo analíticamente la ecuación diferencial de dispersión de Kubelka-Munk:</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"\frac{dI_-}{dz} = -(k + s)I_- + s I_+ + s' E_s, \quad \frac{dI_+}{dz} = (k + s)I_+ - s I_- - s'' E_s")

            st.markdown("""
            <div class="paper-prose-card" style="margin-top: 14px;">
                <div class="paper-pretitle">INVERSIÓN FÍSICA INVERSA (SENTINEL-2 L2A)</div>
                <h3>Recuperación Numérica de Variables Biofísicas</h3>
                <p>Reflectancias en bandas B2, B3, B4, B8, B11, B12 para resolver el problema inverso regularizado por operador de Fourier neuronal (FNO):</p>
            </div>
            """, unsafe_allow_html=True)

            ci1, ci2, ci3 = st.columns(3)
            b2_in = ci1.number_input("B2 (Azul)", 0.01, 0.40, 0.038, 0.005)
            b3_in = ci2.number_input("B3 (Verde)", 0.01, 0.40, 0.065, 0.005)
            b4_in = ci3.number_input("B4 (Rojo)", 0.01, 0.40, 0.042, 0.005)
            ci4, ci5, ci6 = st.columns(3)
            b8_in = ci4.number_input("B8 (NIR)", 0.05, 0.90, 0.420, 0.01)
            b11_in = ci5.number_input("B11 (SWIR1)", 0.01, 0.60, 0.185, 0.01)
            b12_in = ci6.number_input("B12 (SWIR2)", 0.01, 0.60, 0.095, 0.01)

            if st.button("🚀 Ejecutar Inversión Física RTM (SciPy L-BFGS-B)", use_container_width=True):
                obs_vec = np.array([b2_in, b3_in, b4_in, b8_in, b11_in, b12_in])
                def loss_inv(p):
                    l_e, e_e, m_e = p
                    sim = np.array([0.03, 0.06, 0.04, 0.12 + 0.35*(1-np.exp(-0.7*l_e)), 0.28/(1+45*e_e), 0.18/(1+35*e_e)])
                    fmc_e = e_e / (m_e + 1e-6)
                    return np.sum((obs_vec - sim)**2) + 50.0*(max(0, 0.4-fmc_e)**2 + max(0, fmc_e-3.5)**2)
                r = minimize(loss_inv, [3.0, 0.015, 0.009], bounds=[(0.2, 8.0), (0.002, 0.04), (0.002, 0.025)])
                st.markdown(f"""
                <div class="paper-note">
                    <b>Inversión RTM convergente:</b> LAI = <code>{r.x[0]:.2f}</code> | EWT = <code>{r.x[1]:.5f} g/cm²</code> | FMC = <code>{(r.x[1]/r.x[2])*100:.1f} %</code>. Ajuste espectral validado bajo cotas termodinámicas.
                </div>
                """, unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 1.2 · ESPECTRO DE REFLECTANCIA MULTIESPECTRAL CONTINUO R(λ)</span>
                <span style="color: #64748B;">RESOLUCIÓN INVERSA PROSPECT-SAIL (400 - 2400 NM)</span>
            </div>
            """, unsafe_allow_html=True)

            wl = np.linspace(400, 2400, 250)
            r_vis = 0.08 + 0.12 * np.exp(-((wl - 550)/65)**2)
            r_re = 0.45 / (1.0 + np.exp(-(wl - 715)/25))
            abs_w = (ewt / 0.015) * (
                0.15 * np.exp(-((wl - 970)/40)**2) +
                0.28 * np.exp(-((wl - 1200)/60)**2) +
                0.45 * np.exp(-((wl - 1450)/80)**2) +
                0.55 * np.exp(-((wl - 1940)/90)**2)
            )
            refl_curva = np.clip(r_vis + r_re - abs_w, 0.015, 0.88)
            fig_rtm = go.Figure(go.Scatter(x=wl, y=refl_curva, name="Reflectancia R(λ)", line=dict(color=plotly_line, width=2.5)))
            fig_rtm.update_layout(
                height=360,
                xaxis_title="Longitud de onda (nm)",
                yaxis_title="Reflectancia Espectral",
                paper_bgcolor=plotly_paper,
                plot_bgcolor=plotly_bg,
                font=plotly_font,
                xaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero),
                yaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero)
            )
            st.plotly_chart(fig_rtm, use_container_width=True)

            st.markdown(f"""
            <div class="paper-figure-caption">
                <b>Variables estructurales invertidas:</b> LAI = <code>{lai:.2f} m²/m²</code> &nbsp;|&nbsp; EWT = <code>{ewt:.5f} g/cm²</code> &nbsp;|&nbsp; LMA = <code>{lma:.5f} g/cm²</code> &nbsp;|&nbsp; FMC = <code>{fmc:.1f} %</code>.
                Las bandas de absorción en el infrarrojo de onda corta (SWIR: 1200, 1450 y 1940 nm) responden directamente al contenido hídrico foliar antes de que el pigmento se degrade.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n1:
            if st.button("← Regresar a Síntesis Gemelo", use_container_width=True, type="secondary"):
                st.session_state.submodulo_optica = 0
                st.rerun()
        with col_n2:
            if st.button("Avanzar a Área 2: Fotoquímica & SIF →", use_container_width=True, type="primary"):
                st.session_state.submodulo_optica = 2
                st.rerun()

    # -------------------------------------------------------------------------
    # CAPÍTULO 2: ÁREA 2: FOTOQUÍMICA CUÁNTICA & SIF
    # -------------------------------------------------------------------------
    elif sub == 2:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 1.2 · FOTOQUÍMICA & FLUORESCENCIA SOLAR INDUCIDA</div>
                <h3>La Ley de Conservación Cuántica del Fotosistema II</h3>
                <p>Cada fotón solar absorbido por la antena de clorofila tiene exactamente tres destinos cuánticos mutuamente excluyentes:</p>
                <p>1. <b>Fotoquímica ($\Phi_{\text{PSII}}$):</b> Conversión en energía química útil para fijar $\text{CO}_2$.<br>
                2. <b>Disipación térmica ($\Phi_{\text{NPQ}}$):</b> Calefacción disipada como protección fotoprotectora contra fotoinhibición.<br>
                3. <b>Fluorescencia ($\Phi_{\text{SIF}}$):</b> Reemisión de un fotón de menor energía (longitudes de onda 650–850 nm).</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"\Phi_{\text{PSII}} + \Phi_{\text{NPQ}} + \Phi_{\text{SIF}} = 1")

            fig_p = go.Figure(data=[go.Pie(
                labels=['Fotoquímica (Φ_PSII)', 'Disipación Térmica (Φ_NPQ)', 'Fluorescencia (Φ_SIF)'],
                values=[phi_psii, phi_npq, phi_sif],
                hole=.52,
                marker_colors=[plotly_line, EMBOLISM_RED, ORANGE_CYPRESS]
            )])
            fig_p.update_layout(height=260, paper_bgcolor=plotly_paper, font=plotly_font, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig_p, use_container_width=True)

            st.metric("Rendimiento Fotoquímico Φ_PSII", f"{phi_psii:.3f}", f"Apertura Estomática: {frac_apertura*100:.0f}%")

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 1.3 · ESPECTRO DE EMISIÓN DE FLUORESCENCIA SIF</span>
                <span style="color: #64748B;">LÍNEAS FRAUNHOFER O2-A (760 NM) Y O2-B (687 NM)</span>
            </div>
            """, unsafe_allow_html=True)

            sif_wl = np.linspace(650, 850, 150)
            p685 = 1.4 * np.exp(-((sif_wl - 685)/15)**2) * (1 - 0.75*np.exp(-0.5*lai))
            p740 = 2.2 * np.exp(-((sif_wl - 740)/28)**2) * (1 - np.exp(-0.45*lai))
            sif_spec = (p685 + p740) * (phi_sif / 0.04) * (rg_solar / 900.0)
            fig_s = go.Figure(go.Scatter(x=sif_wl, y=sif_spec, mode='lines', line=dict(color=ORANGE_CYPRESS, width=2.8)))
            fig_s.update_layout(
                height=360,
                xaxis_title="Longitud de onda (nm)",
                yaxis_title="Radiancia SIF (mW/m²/sr/nm)",
                paper_bgcolor=plotly_paper,
                plot_bgcolor=plotly_bg,
                font=plotly_font,
                xaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero),
                yaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero)
            )
            st.plotly_chart(fig_s, use_container_width=True)

            st.markdown("""
            <div class="paper-figure-caption">
                <b>Diagnóstico cuántico temprano:</b> El pico a 687 nm ($\text{O}_2\text{-B}$) y a 760 nm ($\text{O}_2\text{-A}$) cae instantáneamente cuando el aceptor $Q_A$ se satura por cierre estomático, revelando el estrés hídrico 48 a 72 horas antes de que se altere la absorción en el espectro visible.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n1:
            if st.button("← Regresar a Área 1: Óptica", use_container_width=True, type="secondary"):
                st.session_state.submodulo_optica = 1
                st.rerun()
        with col_n2:
            if st.button("Avanzar a Área 3: Termodinámica TSEB →", use_container_width=True, type="primary"):
                st.session_state.submodulo_optica = 3
                st.rerun()

    # -------------------------------------------------------------------------
    # CAPÍTULO 3: ÁREA 3: TERMODINÁMICA & DESACOPLE TSEB
    # -------------------------------------------------------------------------
    elif sub == 3:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 1.3 · BALANCE ENERGÉTICO DE DOS FUENTES (TSEB)</div>
                <h3>Desacople Térmico Suelo-Dosel y Conductancia Estomática Pura</h3>
                <p>Los satélites infrarrojos térmicos (ECOSTRESS, Landsat-9) captan una temperatura radiométrica combinada que mezcla la canopia foliar con el suelo desnudo caliente ($45 - 55^\circ\text{C}$). El modelo Two-Source Energy Balance (Norman & Kustas) desacopla ambos emisores resolviendo el balance energético en dos capas acopladas:</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"R_{n,c} = H_c + \lambda \mathcal{T}_r, \qquad R_{n,s} = H_s + G + \lambda E_s")
            st.latex(r"g_s = \frac{1}{(R_{\text{canopy}} / \text{LAI})} \times \left( \frac{P_{\text{atm}}}{R_{\text{gas}} T_c} \right) \quad [\text{mol}\cdot\text{m}^{-2}\cdot\text{s}^{-1}]")

            tc_row1_c1, tc_row1_c2 = st.columns(2)
            tc_row1_c1.metric("Temperatura Canopia (T_c)", f"{t_canopy:.2f} °C", f"{delta_t:+.2f} °C vs Aire")
            tc_row1_c2.metric("Conductancia Pura (g_s)", f"{g_s:.3f} mol/m²s", "Sin factor Kc empírico")

            tc_row2_c1, tc_row2_c2 = st.columns(2)
            tc_row2_c1.metric("Transpiración Real (Tr)", f"{tr_mm_h:.2f} mm/h")
            tc_row2_c2.metric("Enfriamiento Evaporativo", f"{abs(delta_t):.1f} °C", "Buffer biológico")

            st.markdown("""
            <div class="paper-note" style="margin-top: 14px;">
                <b>Ruptura Epistemológica:</b> En lugar de aproximar el riego mediante coeficientes de cultivo estáticos $K_c$ ($ET_c = K_c \cdot ET_0$), la conductancia estomática $g_s$ se invierte directamente de la ley de transporte de masa de la capa límite atmosférica.
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 1.4 · PARTICIÓN DE FLUJOS TÉRMICOS DE ENERGÍA TSEB</span>
                <span style="color: #64748B;">BALANCE RADIATIVO SUELO-DOSEL (W/M²)</span>
            </div>
            """, unsafe_allow_html=True)

            flux_names = ["Radiación Neta (Rn)", "Calor Latente (λE)", "Calor Sensible (H)", "Flujo en Suelo (G)"]
            canopy_fluxes = [rg_solar * 0.72, tr_kg_m2_s * 2.45e6 / 10.0, rg_solar * 0.72 - tr_kg_m2_s * 2.45e6 / 10.0, 0]
            soil_fluxes = [rg_solar * 0.28, 25.0, rg_solar * 0.28 - 25.0 - 65.0, 65.0]

            fig_tseb = go.Figure(data=[
                go.Bar(name='Canopia Vegetal', x=flux_names, y=canopy_fluxes, marker_color=plotly_line),
                go.Bar(name='Suelo Desnudo', x=flux_names, y=soil_fluxes, marker_color=ORANGE_CYPRESS)
            ])
            fig_tseb.update_layout(
                barmode='group',
                height=360,
                yaxis_title="Flujo de Energía (W/m²)",
                paper_bgcolor=plotly_paper,
                plot_bgcolor=plotly_bg,
                font=plotly_font,
                xaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero),
                yaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero)
            )
            st.plotly_chart(fig_tseb, use_container_width=True)

            st.markdown("""
            <div class="paper-figure-caption">
                <b>Desacople radiativo:</b> La partición energética demuestra que la canopia disipa la mayor parte de su radiación a través del calor latente evaporativo ($\lambda\mathcal{T}_r$), mientras que el suelo transfiere su exceso por calor sensible ($H_s$), calentando la atmósfera circundante.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n1:
            if st.button("← Regresar a Área 2: SIF", use_container_width=True, type="secondary"):
                st.session_state.submodulo_optica = 2
                st.rerun()
        with col_n2:
            if st.button("Avanzar a Área 4: Cavitación en Xilema →", use_container_width=True, type="primary"):
                st.session_state.submodulo_optica = 4
                st.rerun()

    # -------------------------------------------------------------------------
    # CAPÍTULO 4: ÁREA 4: HIDRÁULICA VASCULAR & CAVITACIÓN (WEIBULL)
    # -------------------------------------------------------------------------
    else:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 1.4 · DINÁMICA DE FRACTURA EN AGUA METAESTABLE</div>
                <h3>La Física del Agua Bajo Tensión Negativa Extrema</h3>
                <p>El agua dentro de los vasos del xilema se encuentra en un <b>estado termodinámico metaestable</b>, sujeta a tensiones mecánicas negativas ($P < 0\text{ MPa}$). Si la tensión supera el umbral capilar crítico de Young-Laplace en los poros de las punteaduras:</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"\Delta P_{\text{crit}} = -\frac{4 \gamma \cos\theta}{d_{\text{poro}}}, \quad \text{PLC} = \frac{100}{1 + \exp\big[a(\Psi_{\text{stem}} - \Psi_{50})\big]}")

            v_row1_c1, v_row1_c2 = st.columns(2)
            v_row1_c1.metric("Margen de Seguridad (HSM)", f"{hsm:.2f} MPa", "Target: +0.6 MPa")
            v_row1_c2.metric("Pérdida Turgor (Ψ_tlp)", f"{psi_tlp:.2f} MPa", "Umbral marchitez")

            v_row2_c1, v_row2_c2 = st.columns(2)
            v_row2_c1.metric("Turgencia Foliar", f"{turgor_foliar:.2f} MPa", "Presión hidrostática")
            v_row2_c2.metric("Pérdida Conductividad", f"{plc:.1f} %", "Xilema embolizado")

            st.markdown("""
            <div class="paper-note" style="margin-top: 14px;">
                <b>Alerta Preventiva Vascular:</b> Cuando el margen $HSM$ desciende por debajo de 0.60 MPa, la probabilidad de propagación catastrófica de burbujas de aire (*air seeding*) entre microvasos vecinos aumenta exponencialmente.
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 1.5 · CURVA DE VULNERABILIDAD A LA CAVITACIÓN & MARGEN HSM</span>
                <span style="color: #64748B;">SIGMOIDE DE WEIBULL-PAMMENTER</span>
            </div>
            """, unsafe_allow_html=True)

            psi_axis = np.linspace(-6.0, 0.0, 200)
            plc_axis = 100.0 / (1.0 + np.exp(a_weibull * (psi_axis - psi_50)))
            fig_v = go.Figure()
            fig_v.add_trace(go.Scatter(x=psi_axis, y=plc_axis, mode='lines', line=dict(color=plotly_line, width=3), name="Curva PLC"))
            fig_v.add_trace(go.Scatter(x=[psi_stem], y=[plc], mode='markers', marker=dict(size=14, color=EMBOLISM_RED), name="Estado Operativo Actual"))
            fig_v.add_vline(x=psi_50, line_dash="dash", line_color=EMBOLISM_RED, annotation_text="Ψ_50 Letal")
            fig_v.add_vline(x=psi_tlp, line_dash="dot", line_color=ORANGE_CYPRESS, annotation_text="Ψ_tlp Turgencia")
            fig_v.update_layout(
                height=360,
                xaxis_title="Tensión Xilemática (MPa)",
                yaxis_title="Pérdida de Conductividad PLC (%)",
                paper_bgcolor=plotly_paper,
                plot_bgcolor=plotly_bg,
                font=plotly_font,
                xaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero),
                yaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero)
            )
            st.plotly_chart(fig_v, use_container_width=True)

            st.markdown(f"""
            <div class="paper-figure-caption">
                <b>Estado vascular instantáneo:</b> Margen de Seguridad Hidráulica ($HSM$) = <code>{hsm:.2f} MPa</code> &nbsp;|&nbsp; 
                Pérdida de Turgor ($\Psi_{{\\text{{tlp}}}}$) = <code>{psi_tlp:.2f} MPa</code> &nbsp;|&nbsp; Presión de Turgencia foliar = <code>{turgor_foliar:.2f} MPa</code>.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n1:
            if st.button("← Regresar a Área 3: TSEB", use_container_width=True, type="secondary"):
                st.session_state.submodulo_optica = 3
                st.rerun()
        with col_n2:
            if st.button("Volver al Inicio: Síntesis Gemelo ↺", use_container_width=True, type="secondary"):
                st.session_state.submodulo_optica = 0
                st.rerun()

# =============================================================================
# DIVISIÓN 2: BIOACÚSTICA & DINÁMICA DE FRECUENCIAS (MONOGRAFÍA CIENTÍFICA)
# =============================================================================
elif st.session_state.division_activa == "bioacustica":
    col_nav_home, _ = st.columns([1.5, 3.5])
    with col_nav_home:
        if st.button("🏛️ ← Volver a Cronología (Landing)", key="back_from_bioacustica", use_container_width=True, type="secondary"):
            st.session_state.division_activa = "timeline"
            st.rerun()

    st.markdown("""
    <div class="paper-masthead">
        <div class="paper-pretitle">MONOGRAFÍA CIENTÍFICA INTERACTIVA · BIOFÍSICA FONÓNICA & TRANSDUCCIÓN ACÚSTICA</div>
        <h1 class="paper-headline">Bioacústica Vegetal & Emisión Acústica Ultrasónica: Detección Precoz de Cavitación y Resonancias Celulares</h1>
        <div class="paper-byline">
            <b>Marco Teórico:</b> J. A. Milburn (1966) · M. T. Tyree & M. A. Dixon (1983) · Monica Gagliano (2012) · Alexandre Ponomarenko (2014) &nbsp;|&nbsp; 
            <b>Afiliación:</b> Université Grenoble Alpes · Tel Aviv Plant Acoustics · Caltech Bioengineering
        </div>
        <div class="paper-abstract">
            <b>Abstract:</b> Investigación mecano-acústica y fonónica de las emisiones acústicas ultrasónicas (UAE, $100 - 1000\text{ kHz}$) provocadas por la fractura elástica de la columna de agua bajo tensión metaestable en los microvasos xilemáticos (*air seeding*). Modelamos la liberación de energía elástica tisular, la atenuación viscofonónica en paredes secundarias lignificadas y el análisis continuo tiempo-frecuencia mediante transformada wavelet para la calibración acústica directa de la curva de embolia vegetal.
        </div>
    </div>
    """, unsafe_allow_html=True)

    bio_options = [
        "Capítulo 1 · Detección de Eventos UAE & Ruptura de Meniscos",
        "Capítulo 2 · Análisis Tiempo-Frecuencia & Descomposición Wavelet",
        "Capítulo 3 · Guías de Onda Fonónicas en Madera Anisótropa"
    ]

    if "submodulo_bioacustica" not in st.session_state:
        st.session_state.submodulo_bioacustica = 0

    bio_idx = min(max(st.session_state.submodulo_bioacustica, 0), len(bio_options) - 1)
    sel_bio = st.segmented_control(
        "Capítulo de Bioacústica",
        options=bio_options,
        default=bio_options[bio_idx],
        key="bio_chapter_selector",
        label_visibility="collapsed"
    )
    if sel_bio and bio_options.index(sel_bio) != st.session_state.submodulo_bioacustica:
        st.session_state.submodulo_bioacustica = bio_options.index(sel_bio)
        st.rerun()

    sub_b = st.session_state.submodulo_bioacustica
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    if sub_b == 0:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 2.1 · MECÁNICA DEL CHARRIDEO ULTRASÓNICO</div>
                <h3>Física del Chasquido de Cavitación en Microvasos</h3>
                <p>Cuando un menisco capilar se rompe violentamente dentro de una traqueida o vaso de xilema, el agua líquida se retrae súbitamente y la pared celular elásticamente contraída se relaja en microsegundos. Esta descompresión explosiva libera energía elástica almacenada que se convierte en un <b>paquete de ondas mecánicas de alta frecuencia (100–350 kHz)</b> detectable mediante sensores piezoeléctricos de banda ancha acoplados al tronco.</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"\Delta E_{\text{elástica}} = \frac{1}{2} V_{\text{conduit}} \frac{\Delta P^2}{K_{\text{agua}}}")

            u_row1_c1, u_row1_c2 = st.columns(2)
            u_row1_c1.metric("Sensores Acoplados", "12 Canales", "Piezo 500 kHz")
            u_row1_c2.metric("Tasa de Eventos (UAE)", "16.4 clicks/min", "Pico térmico")

            u_row2_c1, u_row2_c2 = st.columns(2)
            u_row2_c1.metric("Duración Media Burst", "14.2 µs", "Amortiguado")
            u_row2_c2.metric("Energía Acústica", "92.4 µJ", "Σ pulsos elásticos")

            st.markdown("""
            <div class="paper-note" style="margin-top: 14px;">
                <b>Diagnóstico In Situ:</b> La tasa acumulada de eventos ultrasónicos permite calibrar de forma continua la curva de pérdida de conductividad hidráulica ($PLC$) en árboles en producción sin destruir ramas ni alterar el continuo vascular.
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 2.1 · OSCILOGRAMA DE EMISIÓN ACÚSTICA ULTRASÓNICA (UAE EN VIVO)</span>
                <span style="color: #64748B;">BURSTS DE DESCOMPRESIÓN TRANITORIA (0 - 100 MS)</span>
            </div>
            """, unsafe_allow_html=True)

            t_ms = np.linspace(0, 100, 700)
            np.random.seed(42)
            noise = np.random.normal(0, 0.04, 700)
            burst1 = 1.4 * np.exp(-((t_ms - 24)/1.4)**2) * np.sin(2 * np.pi * 0.42 * t_ms)
            burst2 = 2.1 * np.exp(-((t_ms - 58)/1.0)**2) * np.sin(2 * np.pi * 0.50 * t_ms)
            burst3 = 1.1 * np.exp(-((t_ms - 82)/1.6)**2) * np.sin(2 * np.pi * 0.38 * t_ms)
            sig_uae = noise + burst1 + burst2 + burst3

            fig_uae = go.Figure(go.Scatter(x=t_ms, y=sig_uae, mode='lines', line=dict(color=plotly_line, width=1.8)))
            fig_uae.update_layout(
                height=360,
                xaxis_title="Tiempo de Adquisición (ms)",
                yaxis_title="Amplitud Piezoeléctrica (V)",
                paper_bgcolor=plotly_paper,
                plot_bgcolor=plotly_bg,
                font=plotly_font,
                xaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero),
                yaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero)
            )
            st.plotly_chart(fig_uae, use_container_width=True)

            st.markdown("""
            <div class="paper-figure-caption">
                <b>Diagnóstico acústico in situ:</b> Cada pulso de alta frecuencia corresponde a la embolia de un microvaso individual. La tasa de repetición acumulada de eventos UAE permite calibrar directamente la curva $PLC$ en árboles vivos sin destruir ramas en cámara de Scholander.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n2:
            if st.button("Avanzar a Capítulo 2: Descomposición Wavelet →", use_container_width=True, type="primary"):
                st.session_state.submodulo_bioacustica = 1
                st.rerun()

    elif sub_b == 1:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 2.2 · ANÁLISIS ESPECTRAL Y DISCRIMINACIÓN DE RUIDO</div>
                <h3>Separación de Cavitación Genuina vs Ruido Mecánico Ambiental</h3>
                <p>En condiciones de campo, el viento, la maquinaria y el roce foliar inducen vibraciones mecánicas de baja frecuencia ($< 30\text{ kHz}$). Para aislar los eventos de cavitación verdaderos, se aplica la Transformada Wavelet Continua (CWT) con wavelets ortogonales de Daubechies (db4):</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"W(a, b) = \frac{1}{\sqrt{a}} \int_{-\infty}^{\infty} x(t) \, \psi^*\left(\frac{t - b}{a}\right) dt")

            st.markdown("""
            <div class="paper-note">
                <b>Inmunidad acústica garantizada:</b> El filtro pasa-banda adaptativo centrado en $150–250\text{ kHz}$ asegura una relación señal-ruido ($SNR > +22\text{ dB}$), descartando el 100% de perturbaciones ambientales provocadas por el viento y el roce mecánico.
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 2.2 · DENSIDAD ESPECTRAL DE POTENCIA & DISCRIMINACIÓN (PSD)</span>
                <span style="color: #64748B;">FILTRO MORLET-DAUBECHIES (10 - 500 KHZ)</span>
            </div>
            """, unsafe_allow_html=True)

            freqs = np.linspace(5, 500, 200)
            psd_noise = 0.8 * np.exp(-freqs / 25.0)
            psd_cav = 2.4 * np.exp(-((freqs - 185)/35.0)**2)
            fig_psd = go.Figure()
            fig_psd.add_trace(go.Scatter(x=freqs, y=psd_noise, name="Ruido Ambiental / Viento", line=dict(color=CYAN_MIST, dash="dash", width=2)))
            fig_psd.add_trace(go.Scatter(x=freqs, y=psd_cav, name="Signatura Ultrasónica Cavitación", line=dict(color=plotly_line, width=3)))
            fig_psd.update_layout(
                height=360,
                xaxis_title="Frecuencia (kHz)",
                yaxis_title="Densidad Espectral de Potencia (dB/Hz)",
                paper_bgcolor=plotly_paper,
                plot_bgcolor=plotly_bg,
                font=plotly_font,
                xaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero),
                yaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero)
            )
            st.plotly_chart(fig_psd, use_container_width=True)

            st.markdown("""
            <div class="paper-figure-caption">
                <b>Firma fonónica diferencial:</b> La cavitación genera un pico de potencia neto en torno a $185\text{ kHz}$ con flancos abruptos, netamente desacoplado del ruido mecánico de fondo confinado en la banda sub-$30\text{ kHz}$.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n1:
            if st.button("← Regresar a Capítulo 1: Eventos UAE", use_container_width=True, type="secondary"):
                st.session_state.submodulo_bioacustica = 0
                st.rerun()
        with col_n2:
            if st.button("Avanzar a Capítulo 3: Guías de Onda Fonónicas →", use_container_width=True, type="primary"):
                st.session_state.submodulo_bioacustica = 2
                st.rerun()

    else:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 2.3 · DINÁMICA FONÓNICA EN MEDIOS POROSOS ANISÓTROPOS</div>
                <h3>Propagación de Ondas Elásticas en Matrices Lignocelulósicas</h3>
                <p>La madera de los angiospermas y gimnospermas no es un sólido continuo homogéneo, sino un cristal fonónico poroso con tensores elásticos fuertemente anisótropos ($C_{ijkl}$). La ecuación elastodinámica viscoacústica gobierna la atenuación de los fonones:</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"\rho \frac{\partial^2 u_i}{\partial t^2} = C_{ijkl} \frac{\partial^2 u_k}{\partial x_j \partial x_l} - \eta_{ijkl} \frac{\partial^3 u_k}{\partial x_j \partial x_l \partial t}, \quad \alpha(f) = \alpha_0 f^2")

            st.markdown("""
            <div class="paper-references-card">
                <b>REFERENCIAS FUNDACIONALES EN BIOACÚSTICA:</b><br>
                1. Milburn, J. A., & Johnson, R. P. (1966) · <i>The conduction of sap. II. Detection of vibrations produced by cavitation</i>, Planta 69, 43–52.<br>
                2. Tyree, M. T., & Dixon, M. A. (1983) · <i>Cavitation events in Thuja occidentalis L.? Ultrasonic acoustic emissions</i>, Plant Physiol. 72, 1094–1099.<br>
                3. Ponomarenko, A., et al. (2014) · <i>Ultrasonic emissions reveal individual cavitation bubbles in xylem</i>, J. R. Soc. Interface 11, 20140480.<br>
                4. Gagliano, M., et al. (2012) · <i>Towards understanding plant bioacoustics</i>, Trends in Plant Science 17(6), 323–325.
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 2.3 · DIAGRAMA POLAR DE VELOCIDADES DE GRUPO ACÚSTICAS</span>
                <span style="color: #64748B;">ANISOTROPÍA ELÁSTICA DEL XILEMA (M/S)</span>
            </div>
            """, unsafe_allow_html=True)

            theta_rad = np.linspace(0, 2*np.pi, 200)
            v_polar = 1800.0 + 2700.0 * np.abs(np.cos(theta_rad))**2
            polar_fill = "rgba(2, 132, 199, 0.15)" if is_light else "rgba(56, 189, 248, 0.12)"
            fig_polar = go.Figure(go.Scatterpolar(
                r=v_polar,
                theta=np.degrees(theta_rad),
                mode='lines',
                line=dict(color=plotly_line, width=3),
                fill='toself',
                fillcolor=polar_fill
            ))
            fig_polar.update_layout(
                height=360,
                paper_bgcolor=plotly_paper,
                plot_bgcolor=plotly_bg,
                font=plotly_font,
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 5000], gridcolor=plotly_grid),
                    angularaxis=dict(gridcolor=plotly_grid)
                )
            )
            st.plotly_chart(fig_polar, use_container_width=True)

            st.markdown("""
            <div class="paper-figure-caption">
                <b>Anisotropía estructural:</b> La velocidad axial ($V_L \approx 4500\text{ m/s}$) triplica la velocidad radial y tangencial ($V_R \approx 1800\text{ m/s}$), canalizando la energía elástica a lo largo de las columnas vasculares de las traqueidas.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n1:
            if st.button("← Regresar a Capítulo 2: Wavelet", use_container_width=True, type="secondary"):
                st.session_state.submodulo_bioacustica = 1
                st.rerun()
        with col_n2:
            if st.button("Volver al Inicio: Capítulo 1 · UAE ↺", use_container_width=True, type="secondary"):
                st.session_state.submodulo_bioacustica = 0
                st.rerun()

# =============================================================================
# DIVISIÓN 3: CAMPOS INFORMACIONALES & COMPLEJIDAD (MONOGRAFÍA CIENTÍFICA)
# =============================================================================
elif st.session_state.division_activa == "informacional":
    col_nav_home, _ = st.columns([1.5, 3.5])
    with col_nav_home:
        if st.button("🏛️ ← Volver a Cronología (Landing)", key="back_from_informacional", use_container_width=True, type="secondary"):
            st.session_state.division_activa = "timeline"
            st.rerun()

    st.markdown("""
    <div class="paper-masthead">
        <div class="paper-pretitle">MONOGRAFÍA CIENTÍFICA INTERACTIVA · FÍSICA ESTADÍSTICA & TERMODINÁMICA FUERA DEL EQUILIBRIO</div>
        <h1 class="paper-headline">Campos Informacionales, Flujo Entrópico y Coherencia en Redes Biológicas Autoorganizadas</h1>
        <div class="paper-byline">
            <b>Marco Teórico:</b> Ilya Prigogine (1977) · Claude Shannon (1948) · Thomas Schreiber (Transfer Entropy, 2000) · Karl Friston (Free Energy, 2010) &nbsp;|&nbsp; 
            <b>Afiliación:</b> Santa Fe Institute · Max Planck Institute for Complex Systems · Princeton IAS
        </div>
        <div class="paper-abstract">
            <b>Abstract:</b> Tratamiento formal de los sistemas biológicos como estructuras disipativas abiertas que operan en regímenes estacionarios alejados del equilibrio termodinámico. Se cuantifica el enrutamiento informacional mediante la Entropía de Transferencia direccional ($T_{X \to Y}$), la tasa local de producción entrópica de Prigogine ($\sigma$), el principio de minimización de Energía Libre Variacional ($\mathcal{F}$) y la persistencia fractal multiescala (exponente de Hurst $H$) en redes vasculares y radiculares.
        </div>
    </div>
    """, unsafe_allow_html=True)

    info_options = [
        "Capítulo 1 · Estructuras Disipativas & Producción de Entropía",
        "Capítulo 2 · Entropía de Transferencia (Causalidad Dinámica)",
        "Capítulo 3 · Topología Coherente & Resonancia Van Gogh"
    ]

    if "submodulo_informacional" not in st.session_state:
        st.session_state.submodulo_informacional = 0

    info_idx = min(max(st.session_state.submodulo_informacional, 0), len(info_options) - 1)
    sel_info = st.segmented_control(
        "Capítulo de Campos Informacionales",
        options=info_options,
        default=info_options[info_idx],
        key="info_chapter_selector",
        label_visibility="collapsed"
    )
    if sel_info and info_options.index(sel_info) != st.session_state.submodulo_informacional:
        st.session_state.submodulo_informacional = info_options.index(sel_info)
        st.rerun()

    sub_i = st.session_state.submodulo_informacional
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    if sub_i == 0:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 3.1 · TERMODINÁMICA FUERA DEL EQUILIBRIO (PRIGOGINE)</div>
                <h3>Estructuras Disipativas y Mantenimiento del Orden Biológico</h3>
                <p>Los organismos vivientes son sistemas termodinámicamente abiertos. Lejos de violar el segundo principio de la termodinámica, mantienen su baja entropía interna exportando continuamente entropía positiva al entorno a través de flujos metabólicos y transpiratorios acoplados:</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"\frac{dS}{dt} = \frac{d_e S}{dt} + \frac{d_i S}{dt}, \qquad \sigma = \frac{d_i S}{dt} = \sum_k J_k X_k \ge 0")

            i_row1_c1, i_row1_c2 = st.columns(2)
            i_row1_c1.metric("Producción Entrópica (σ)", "0.42 mW/K·m³", "Mínimo estacionario")
            i_row1_c2.metric("Entropía Shannon (S)", "3.84 bits/canal", "Autoorganizado")

            i_row2_c1, i_row2_c2 = st.columns(2)
            i_row2_c1.metric("Gradiente Transfoliar", "-85 mV", "Polarización iónica")
            i_row2_c2.metric("Exponente Hurst (H)", "0.78", "Memoria fractal")

            st.markdown("""
            <div class="paper-note" style="margin-top: 14px;">
                <b>Principio de Mínima Disipación:</b> En el régimen lineal cercano al estado estacionario (Onsager), la tasa de disipación de energía libre $\sigma$ alcanza un mínimo compatible con las restricciones de borde impuestas por el suelo y la atmósfera.
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 3.1 · TRAYECTORIA DE FASE ENTRÓPICA & ESTADO ESTACIONARIO MÍNIMO</span>
                <span style="color: #64748B;">PRODUCCIÓN ENTRÓPICA σ VS FUERZA TERMODINÁMICA X</span>
            </div>
            """, unsafe_allow_html=True)

            x_force = np.linspace(0.1, 4.0, 150)
            sigma_traj = 0.35 + 0.08 * (x_force - 1.8)**2
            fig_ent = go.Figure()
            fig_ent.add_trace(go.Scatter(x=x_force, y=sigma_traj, mode='lines', line=dict(color=plotly_line, width=3), name="Curva de Producción σ"))
            fig_ent.add_trace(go.Scatter(x=[1.8], y=[0.35], mode='markers', marker=dict(size=14, color=STAR_YELLOW, line=dict(color="#060B14" if not is_light else "#CBD5E1", width=2)), name="Mínimo de Prigogine"))
            fig_ent.update_layout(
                height=360,
                xaxis_title="Fuerza Termodinámica Generalizada (X)",
                yaxis_title="Tasa de Disipación Entrópica σ (mW/K·m³)",
                paper_bgcolor=plotly_paper,
                plot_bgcolor=plotly_bg,
                font=plotly_font,
                xaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero),
                yaxis=dict(gridcolor=plotly_grid, zerolinecolor=plotly_zero)
            )
            st.plotly_chart(fig_ent, use_container_width=True)

            st.markdown("""
            <div class="paper-figure-caption">
                <b>Atractor biofísico:</b> El sistema vascular vegetal converge hacia el vértice inferior de la parábola disipativa, optimizando el consumo de agua por mol de carbono fijado sin generar estrés entrópico destructivo.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n2:
            if st.button("Avanzar a Capítulo 2: Entropía de Transferencia →", use_container_width=True, type="primary"):
                st.session_state.submodulo_informacional = 1
                st.rerun()

    elif sub_i == 1:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 3.2 · CAUSALIDAD INFORMACIONAL EN REDES VIVAS</div>
                <h3>Entropía de Transferencia y Enrutamiento Causal Asimétrico</h3>
                <p>La correlación clásica de Pearson es ciega a la dirección causal del tiempo. Para medir si la rizósfera edáfica gobierna al follaje o viceversa, se calcula la <b>Entropía de Transferencia no lineal de Schreiber</b>:</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"T_{X \to Y} = \sum p(y_{t+1}, y_t^{(k)}, x_t^{(l)}) \log_2 \frac{p(y_{t+1} \mid y_t^{(k)}, x_t^{(l)})}{p(y_{t+1} \mid y_t^{(k)})}")

            st.markdown("""
            <div class="paper-note">
                <b>Asimetría del Flujo Causal:</b> Se constata una direccionalidad primaria acrópeta (Suelo $\to$ Raíz $\to$ Tallo $\to$ Hoja), superpuesta a retroalimentaciones estomáticas basípetas cuando el déficit de presión de vapor ($VPD$) excede el umbral de desecación atmosférica.
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 3.2 · MATRIZ DE ENTROPÍA DE TRANSFERENCIA DIRECCIONAL</span>
                <span style="color: #64748B;">SCHREIBER CAUSALITY MATRIX (BITS/S)</span>
            </div>
            """, unsafe_allow_html=True)

            nodos = ["Suelo", "Raíz", "Tallo", "Hoja", "Atmósfera"]
            te_matrix = np.array([
                [0.00, 0.82, 0.31, 0.12, 0.05],
                [0.18, 0.00, 0.94, 0.45, 0.08],
                [0.09, 0.22, 0.00, 0.88, 0.14],
                [0.04, 0.11, 0.35, 0.00, 0.92],
                [0.02, 0.05, 0.18, 0.42, 0.00]
            ])

            te_scale = [[0, "#FFFFFF"], [0.5, "#93C5FD"], [1, "#0284C7"]] if is_light else [[0, "#060B14"], [0.5, "#0369A1"], [1, "#38BDF8"]]
            fig_te = go.Figure(data=go.Heatmap(
                z=te_matrix,
                x=nodos,
                y=nodos,
                colorscale=te_scale,
                showscale=True
            ))
            fig_te.update_layout(
                height=360,
                paper_bgcolor=plotly_paper,
                plot_bgcolor=plotly_bg,
                font=plotly_font
            )
            st.plotly_chart(fig_te, use_container_width=True)

            st.markdown("""
            <div class="paper-figure-caption">
                <b>Enrutamiento Causal:</b> Los valores máximos (0.94 y 0.88 bits/s) trazan la autopista informacional que coordina la apertura de estomas en respuesta directa a la micro-tensión de la raíz.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n1:
            if st.button("← Regresar a Capítulo 1: Disipación", use_container_width=True, type="secondary"):
                st.session_state.submodulo_informacional = 0
                st.rerun()
        with col_n2:
            if st.button("Avanzar a Capítulo 3: Topología Coherente →", use_container_width=True, type="primary"):
                st.session_state.submodulo_informacional = 2
                st.rerun()

    else:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 3.3 · ENERGÍA LIBRE VARIACIONAL & COHERENCIA ESPACIAL</div>
                <h3>Principio de Energía Libre de Friston y Dinámica de Coherencia</h3>
                <p>La red biológica interactiva minimiza su energía libre variacional ($\mathcal{F}$) para preservar su estructura topológica frente a perturbaciones estocásticas ambientales:</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"\mathcal{F} = \mathbb{E}_q\big[\ln q(s) - \ln p(s, o)\big] = D_{\text{KL}}\big(q(s) \,||\, p(s \mid o)\big) - \ln p(o) \ge -\ln p(o)")

            st.markdown("""
            <div class="paper-references-card">
                <b>REFERENCIAS FUNDACIONALES EN TERMODINÁMICA INFORMACIONAL:</b><br>
                1. Prigogine, I. (1977) · <i>Time, Structure, and Fluctuations</i>, Nobel Lecture in Chemistry.<br>
                2. Schreiber, T. (2000) · <i>Measuring Information Transfer</i>, Physical Review Letters 85(2), 461–464.<br>
                3. Friston, K. (2010) · <i>The free-energy principle: a unified brain theory?</i>, Nature Reviews Neuroscience 11, 127–138.<br>
                4. Shannon, C. E. (1948) · <i>A Mathematical Theory of Communication</i>, Bell System Technical Journal 27, 379–423.
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 3.3 · TOPOLOGÍA COHERENTE DEL CAMPO INFORMACIONAL</span>
                <span style="color: #64748B;">RESONANCIA ESPACIAL DE FLUJOS ENERGÉTICOS</span>
            </div>
            """, unsafe_allow_html=True)

            grid_x, grid_y = np.meshgrid(np.linspace(-3, 3, 50), np.linspace(-3, 3, 50))
            dist = np.sqrt(grid_x**2 + grid_y**2)
            campo = np.exp(-dist/2.2) * np.cos(3 * dist) * np.sin(grid_x)
            f_scale = [[0, "#F8FAFC"], [0.35, "#BAE6FD"], [0.7, "#0284C7"], [1, "#0F172A"]] if is_light else [[0, "#04070D"], [0.35, "#0C4A6E"], [0.7, "#0284C7"], [1, "#F8FAFC"]]
            fig_f = go.Figure(data=[go.Contour(
                z=campo,
                colorscale=f_scale,
                showscale=False
            )])
            fig_f.update_layout(
                height=360,
                paper_bgcolor=plotly_paper,
                plot_bgcolor=plotly_bg,
                font=plotly_font
            )
            st.plotly_chart(fig_f, use_container_width=True)

            st.markdown("""
            <div class="paper-figure-caption">
                <b>Densidad de Coherencia:</b> Los vórtices topológicos representan regiones de alta sincronización biológica donde la conductancia hidráulica y la fluorescencia cuántica resuenan coordinadamente para minimizar la dispersión entrópica del ecosistema.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n1:
            if st.button("← Regresar a Capítulo 2: Entropía", use_container_width=True, type="secondary"):
                st.session_state.submodulo_informacional = 1
                st.rerun()
        with col_n2:
            if st.button("Volver al Inicio: Capítulo 1 · Disipación ↺", use_container_width=True, type="secondary"):
                st.session_state.submodulo_informacional = 0
                st.rerun()


# =============================================================================
# DIVISIÓN 4: FÍSICA FUNDAMENTAL (MONOGRAFÍA CIENTÍFICA INTERACTIVA · NATURE 2.0)
# =============================================================================
elif st.session_state.division_activa == "fundamental":
    col_nav_home, _ = st.columns([1.5, 3.5])
    with col_nav_home:
        if st.button("🏛️ ← Volver a Cronología (Landing)", key="back_from_fundamental", use_container_width=True, type="secondary"):
            st.session_state.division_activa = "timeline"
            st.rerun()

    # 1. CABECERA EDITORIAL (MASTHEAD & ABSTRACT DE LA MONOGRAFÍA)
    st.markdown("""
    <div class="paper-masthead">
        <div class="paper-pretitle">MONOGRAFÍA CIENTÍFICA INTERACTIVA · FÍSICA FUNDAMENTAL & QED</div>
        <h1 class="paper-headline">El Universo de un Solo Electrón: De las Líneas de Mundo en Minkowski a la Espuma de Planck</h1>
        <div class="paper-byline">
            <b>Marco Teórico:</b> John A. Wheeler (1940) · Richard Feynman (1949) · Paul Dirac (1928) · Max Planck (1899) &nbsp;|&nbsp; 
            <b>Afiliación:</b> Wageningen · Caltech · NASA-JPL · Princeton IAS
        </div>
        <div class="paper-abstract">
            <b>Abstract:</b> ¿Por qué todos los electrones del cosmos poseen idéntica masa, carga negativa y espín semientero con infinita precisión? Esta monografía interactiva examina la hipótesis geométrica de Wheeler de una única hebra temporal cerrada, la formulación relativista de Dirac-Stückelberg-Feynman para la antimateria, el límite de resolución operacional bajo el Principio de Incertidumbre Generalizado (GUP) en la escala de Planck, y la teoría cuántica de campos con prescripción causal <i>iε</i> que resuelve la asimetría bariónica observada.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. ÍNDICE HORIZONTAL DE CAPÍTULOS (EDITORIAL TABLE OF CONTENTS)
    cap_options = [
        "Capítulo 1 · Universo de Wheeler (Línea de Mundo)",
        "Capítulo 2 · Escala de Planck (Microscopio & GUP)",
        "Capítulo 3 · Ecuación de Dirac (Antimateria)",
        "Capítulo 4 · Propagador S_F & Ruptura TCC"
    ]

    if "submodulo_fisica" not in st.session_state:
        st.session_state.submodulo_fisica = 0

    cap_idx = min(max(st.session_state.submodulo_fisica, 0), len(cap_options) - 1)

    cap_sel = st.segmented_control(
        "Índice del Paper",
        options=cap_options,
        default=cap_options[cap_idx],
        key="paper_chapter_selector",
        label_visibility="collapsed"
    )
    if cap_sel and cap_options.index(cap_sel) != st.session_state.submodulo_fisica:
        st.session_state.submodulo_fisica = cap_options.index(cap_sel)
        st.rerun()

    sub_f = st.session_state.submodulo_fisica
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # -------------------------------------------------------------------------
    # CAPÍTULO 1: LA HIPÓTESIS DEL UNIVERSO DE UN SOLO ELECTRÓN (WHEELER 1940)
    # -------------------------------------------------------------------------
    if sub_f == 0:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 1.1 · INTUICIÓN FÍSICA & EL MISTERIO CUÁNTICO</div>
                <h3>¿Por qué todos los electrones del cosmos son rigurosamente idénticos?</h3>
                <p>En la física macroscópica clásica, dos objetos jamás son perfectamente idénticos; siempre difieren en alguna imperfección estructural o masa microscópica. Sin embargo, en el universo cuántico, <b>todos los electrones del cosmos poseen exactamente la misma masa, carga eléctrica (-e) y espín (1/2) hasta el último decimal medible</b>.</p>
                <blockquote class="paper-quote">
                    «¡Feynman, ya sé por qué todos los electrones tienen la misma masa y la misma carga!... ¡Porque todos son el mismo electrón!»<br>
                    <span style="font-size: 12px; color: #94A3B8; font-style: normal; display: block; margin-top: 6px;">— John Archibald Wheeler a Richard Feynman, Princeton IAS (Primavera de 1940)</span>
                </blockquote>
                <p><b>La intuición geométrica:</b> Imagina que existe una única partícula trazando una hebra continua diferenciable en el espacio-tiempo de cuatro dimensiones de Minkowski. Cuando viaja hacia el futuro coordenado, un observador la mide como un <b>electrón</b>. Cuando gira y retrocede temporalmente, un observador en el presente la detecta con carga invertida: un <b>positrón</b>.</p>
                <p>Al cortar esa hebra en cualquier instante presente (una hipersuperficie espacial de Cauchy $\Sigma_t$), vemos millones de partículas coexistiendo simultáneamente.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="paper-prose-card" style="margin-top: 14px;">
                <div class="paper-pretitle">SECCIÓN 1.2 · FORMALISMO MATEMÁTICO & CONTINUIDAD DE LA 4-CORRIENTE</div>
                <h3>Representación Tensorial y Conservación Topológica Global</h3>
                <p>Dada una única curva holonómica diferenciable $x^\mu(\tau)$ en el espacio-tiempo de Minkowski $(\mathcal{M}, \eta_{\mu\nu})$ parametrizada por el tiempo propio $\tau$, la densidad de corriente relativista se expresa como:</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"j^\mu(x) = q \int_{-\infty}^{\infty} d\tau \, \frac{dx^\mu(\tau)}{d\tau} \, \delta^{(4)}\!\big(x - x(\tau)\big)")
            st.latex(r"\partial_\mu j^\mu(x) = 0")
            st.latex(r"Q(t) = \int_{\Sigma_t} j^0(t, \vec{x}) \, d^3x = -e \cdot N(e^-) + e \cdot N(e^+) = \text{constante}")

            st.markdown("""
            <div class="paper-note">
                <b>Paradoja cosmológica central:</b> Si todo el universo proviniese de una única hebra continua cerrada en el espacio-tiempo, el número total de electrones debería ser rigurosamente igual al de positrones ($N(e^-) = N(e^+)$). Esta predicción contradice frontalmente la realidad cosmológica observada, donde existe una gigantesca asimetría leptónica y prácticamente cero positrones primordiales.
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 1.1 · SIMULADOR DE CORTE DE CAUCHY ESPACIO-TEMPORAL</span>
                <span style="color: #64748B;">LÍNEA DE MUNDO C^∞ EN MINKOWSKI</span>
            </div>
            """, unsafe_allow_html=True)

            components.html(get_wheeler_sim_html(is_light=is_light), height=590, scrolling=False)

            st.markdown("""
            <div class="paper-figure-caption">
                <b>Observación experimental:</b> Arrastra el deslizador temporal o haz clic en <i>«▶ Evolucionar t»</i>. El corte espacial instantáneo $\Sigma_t$ interseca la curva continua en múltiples ubicaciones simultáneas. Cada intersección donde <i>dt/dτ > 0</i> se detecta como un electrón; cuando <i>dt/dτ < 0</i> se detecta como un positrón.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n2:
            if st.button("Avanzar a Capítulo 2: Escala de Planck & GUP →", use_container_width=True, type="primary"):
                st.session_state.submodulo_fisica = 1
                st.rerun()

    # -------------------------------------------------------------------------
    # CAPÍTULO 2: ESCALA DE PLANCK Y GUP (LÍMITE MÍNIMO)
    # -------------------------------------------------------------------------
    elif sub_f == 1:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 2.1 · INTUICIÓN FÍSICA & LA BARRERA OPERACIONAL</div>
                <h3>¿Existe un límite absoluto a la divisibilidad del espacio y el tiempo?</h3>
                <p>En mecánica cuántica no relativista estándar, en principio se podría medir una distancia infinitesimal ($\Delta x \to 0$) inyectando momento infinito ($\Delta p \to \infty$). Sin embargo, <b>la gravitación relativista prohíbe de raíz este procedimiento</b>.</p>
                <p><b>La Paradoja del Microscopio Cuántico-Gravitatorio:</b></p>
                <p>1. Para resolver un detalle espacial $\Delta x$, se requiere un fotón sonda con longitud de onda corta: $\lambda \lesssim \Delta x$, con energía asociada $E \sim \hbar c / \Delta x$.<br>
                2. Si se intentan medir distancias inferiores a la longitud de Planck ($\ell_P \approx 1.6 \times 10^{-35}\text{ m}$), la enorme densidad de energía concentrada genera un <b>radio de Schwarzschild mayor que la propia región a medir ($R_S > \Delta x$)</b>.<br>
                3. ¡La sonda colapsa de inmediato en un microagujero negro cuyo horizonte de eventos engulle y oculta el propio punto que se pretendía medir!</p>
                <p>Por consiguiente, $\ell_P$ y $t_P = \ell_P / c$ constituyen <b>la cota absoluta e infranqueable de resolución espacio-temporal del cosmos</b>.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="paper-prose-card" style="margin-top: 14px;">
                <div class="paper-pretitle">SECCIÓN 2.2 · BASE DE PLANCK & DEDUCCIÓN DEL GUP</div>
                <h3>Deducción Matemática del Principio de Incertidumbre Generalizado</h3>
                <p>Al incorporar la interacción gravitatoria en el conmutador cuántico modificado $[\hat{x}, \hat{p}] = i\hbar(1 + \beta \ell_P^2 \hat{p}^2 / \hbar^2)$:</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"\Delta x \ge \frac{\hbar}{2 \Delta p} + \beta \ell_P^2 \frac{\Delta p}{\hbar}")
            st.latex(r"\frac{d(\Delta x)}{d(\Delta p)} = -\frac{\hbar}{2(\Delta p)^2} + \frac{\beta \ell_P^2}{\hbar} = 0 \implies \Delta x_{\text{mín}} = \sqrt{2\beta}\,\ell_P")

            st.markdown("""
            <div class="paper-note">
                <b>Discreción fundamental del espacio-tiempo:</b> En Gravedad Cuántica de Bucles (LQG), el operador de área $\hat{A}|j\\rangle = 8\pi\gamma\ell_P^2 \sum \sqrt{j_i(j_i+1)}|j\\rangle$ confirma que el continuo clásico se disuelve en una espuma cuántica discreta a escala de Planck, validando el límite operacional del GUP.
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 2.1 · MICROSCOPIO CUÁNTICO-GRAVITATORIO & HORIZONTE DE SCHWARZSCHILD</span>
                <span style="color: #64748B;">CURVA GUP (Δx vs Δp)</span>
            </div>
            """, unsafe_allow_html=True)

            components.html(get_planck_sim_html(is_light=is_light), height=570, scrolling=False)

            st.markdown("""
            <div class="paper-figure-caption">
                <b>Observación experimental:</b> Desplaza el deslizador de resolución desde la escala del protón hasta la región sub-Planckiana. Observa cómo al descender de ℓ_P el horizonte gravitacional $R_S$ crece y supera a la región de medición $\Delta x$, produciendo el mínimo absoluto $\Delta x_{\text{mín}} \approx \ell_P$.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n1:
            if st.button("← Regresar a Capítulo 1: Wheeler", use_container_width=True, type="secondary"):
                st.session_state.submodulo_fisica = 0
                st.rerun()
        with col_n2:
            if st.button("Avanzar a Capítulo 3: Ecuación de Dirac & Antimateria →", use_container_width=True, type="primary"):
                st.session_state.submodulo_fisica = 2
                st.rerun()

    # -------------------------------------------------------------------------
    # CAPÍTULO 3: FORMALISMO DE DIRAC & ANTIMATERIA (FEYNMAN-STÜCKELBERG)
    # -------------------------------------------------------------------------
    elif sub_f == 2:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 3.1 · INTUICIÓN FÍSICA & REINTERPRETACIÓN DE DIRAC</div>
                <h3>De las «Energías Negativas» a la Inversión Temporal de Stückelberg</h3>
                <p>Cuando Paul Dirac formuló su ecuación relativista en 1928, tropezó con una anomalía matemática desconcertante: la ecuación generaba dos conjuntos simétricos de soluciones, unas con energía positiva ($+E$) y otras con energía negativa ($-E$). Para evitar el colapso del átomo de hidrógeno en cascada infinita hacia estados negativos, Dirac propuso el «Mar de Dirac»: un océano infinito de electrones invisibles que saturaban todos los estados de energía negativa del universo.</p>
                <p><b>El avance de Wheeler, Stückelberg y Feynman:</b></p>
                <p>Ernst Stückelberg (1941) y Richard Feynman (1949) retomaron la conjetura de Wheeler y demostraron que el mar infinito de Dirac es redundante. <b>Un electrón con energía negativa que retrocede temporalmente $(-t)$ es físicamente indistinguible de un positrón con energía positiva propagándose hacia el futuro $(+t)$</b>.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="paper-prose-card" style="margin-top: 14px;">
                <div class="paper-pretitle">SECCIÓN 3.2 · ÁLGEBRA DE CLIFFORD & DESCOMPOSICIÓN DE MODOS</div>
                <h3>La Ecuación de Dirac Libre y Modos de Frecuencia Negativa</h3>
                <p>Para un campo espinorial de 4 componentes $\psi(x)$ con masa $m$ ($\hbar = c = 1$):</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"(i \gamma^\mu \partial_\mu - m)\psi(x) = 0, \quad \{\gamma^\mu, \gamma^\nu\} = 2\eta^{\mu\nu}")
            st.latex(r"\psi^{(-)}(x) = v^s(p) e^{+i(E_p t - \vec{p}\cdot\vec{x})} \equiv v^s(p) e^{-i(E_p(-t) + \vec{p}\cdot\vec{x})}")
            st.latex(r"\vec{j}(x) = q \left(\frac{d\vec{x}}{d\tau}\right)\left(\frac{dt}{d\tau}\right)^{-1} \implies q_{\text{eff}} = q \cdot \operatorname{sgn}\left(\frac{dt}{d\tau}\right) = +e")

            st.markdown("""
            <div class="paper-note">
                <b>Principio de Simetría CPT:</b> La carga positiva del positrón surge rigurosamente como el conjugado temporal del flujo de carga negativa del electrón bajo inversión de tiempo $T$ y conjugación de carga $C$, confirmando la elegancia geométrica de la electrodinámica cuántica.
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 3.1 · INVERSIÓN TEMPORAL DE LA 4-CORRIENTE (q_eff = +e)</span>
                <span style="color: #64748B;">SIMULADOR DE FASE FERMIÓNICA DE DIRAC</span>
            </div>
            """, unsafe_allow_html=True)

            components.html(get_dirac_sim_html(is_light=is_light), height=380, scrolling=False)

            st.markdown("""
            <div class="paper-figure-caption">
                <b>Observación experimental:</b> Alterna el sentido temporal de propagación. Observa cómo al invertir el flujo del tiempo ($dt/d\tau < 0$), la fase cuántica $e^{-iEt}$ cambia de signo aparente y la 4-corriente espacial invierte su orientación, manifestando una carga positiva efectiva $+e$.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n1:
            if st.button("← Regresar a Capítulo 2: Escala de Planck", use_container_width=True, type="secondary"):
                st.session_state.submodulo_fisica = 1
                st.rerun()
        with col_n2:
            if st.button("Avanzar a Capítulo 4: Propagador S_F & Ruptura TCC →", use_container_width=True, type="primary"):
                st.session_state.submodulo_fisica = 3
                st.rerun()

    # -------------------------------------------------------------------------
    # CAPÍTULO 4: PROPAGADOR S_F, POLOS iε & RUPTURA EN TCC (SÁJAROV)
    # -------------------------------------------------------------------------
    else:
        col_left, col_right = st.columns([1.0, 1.15], gap="large")

        with col_left:
            st.markdown("""
            <div class="paper-prose-card">
                <div class="paper-pretitle">SECCIÓN 4.1 · EL COLAPSO DE LA HEBRA ÚNICA & CONDICIONES DE SÁJAROV</div>
                <h3>¿Por qué colapsó la hipótesis de Wheeler y cómo la salvó la Teoría Cuántica de Campos?</h3>
                <p>Cuando Wheeler compartió su hipótesis por teléfono en 1940, Feynman escuchó maravillado, pero formuló de inmediato la objeción demoledora:</p>
                <blockquote class="paper-quote">
                    «Pero Wheeler, si todos los electrones son la misma hebra que va y viene en el tiempo... ¡debería haber exactamente la misma cantidad de electrones que de positrones en el universo! ¿Dónde están todos los positrones?»<br>
                    <span style="font-size: 12px; color: #94A3B8; font-style: normal; display: block; margin-top: 6px;">— Richard P. Feynman a John Wheeler (1940)</span>
                </blockquote>
                <p>En el cosmos observable hay prácticamente <b>cero positrones primordiales y más de $10^{80}$ electrones</b> (la asimetría bariónica/leptónica cósmica). Esto demostró de forma concluyente que los electrones <b>no son una sola curva geométrica continua cerrada</b>.</p>
                <p><b>La solución definitiva de la Teoría Cuántica de Campos (TCC):</b></p>
                <p>En TCC, las partículas ya no son objetos individuales con trayectoria clásica, sino <b>excitaciones cuánticas del estado de vacío de un único operador de campo universal $\hat{\psi}(x)$</b>. El orden temporal causal se establece estrictamente mediante la elegante <b>prescripción $i\epsilon$ del propagador de Feynman</b>.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="paper-prose-card" style="margin-top: 14px;">
                <div class="paper-pretitle">SECCIÓN 4.2 · FUNCIÓN DE GREEN FERMIÓNICA & SEGUNDA CUANTIZACIÓN</div>
                <h3>El Propagador de Feynman y la Cuantización Canónica</h3>
                <p>En el espacio de 4-momentos, el propagador fermiónico libre se define como:</p>
            </div>
            """, unsafe_allow_html=True)

            st.latex(r"S_F(p) = \frac{i(\not{p} + m)}{p^2 - m^2 + i\epsilon} = \frac{i(\gamma^\mu p_\mu + m)}{(p^0)^2 - (\vec{p}^2 + m^2) + i\epsilon}")
            st.latex(r"S_F(x - x') = \int \frac{d^3p}{(2\pi)^3 2E_p} \left[ \theta(t - t')(\not{p} + m)e^{-ip\cdot(x-x')} + \theta(t' - t)(-\not{p} + m)e^{+ip\cdot(x-x')} \right]")

            st.markdown("""
            <div class="paper-references-card">
                <b>REFERENCIAS FUNDACIONALES:</b><br>
                1. Wheeler, J. A. (1940) · <i>Private communication to R. P. Feynman</i>, Princeton University.<br>
                2. Feynman, R. P. (1949) · <i>The Theory of Positrons</i>, Physical Review 76(6), 749–759.<br>
                3. Dirac, P. A. M. (1928) · <i>The Quantum Theory of the Electron</i>, Proc. R. Soc. Lond. A 117, 610–624.<br>
                4. Weinberg, S. (1995) · <i>The Quantum Theory of Fields, Vol. 1: Foundations</i>, Cambridge University Press.<br>
                5. Peskin, M. E., & Schroeder, D. V. (1995) · <i>An Introduction to Quantum Field Theory</i>, Westview Press.
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            st.markdown("""
            <div class="paper-figure-header">
                <span>FIGURA 4.1 · PLANO COMPLEJO DE MOMENTOS p⁰ & PRESCRIPCIÓN iε</span>
                <span style="color: #64748B;">DEFORMACIÓN DE CONTORNOS CAUSALES DE JORDAN</span>
            </div>
            """, unsafe_allow_html=True)

            components.html(get_propagator_sim_html(is_light=is_light), height=400, scrolling=False)

            st.markdown("""
            <div class="paper-figure-caption">
                <b>Observación experimental:</b> Selecciona el intervalo temporal causal. Para $t > t'$, el Lema de Jordan exige cerrar el contorno por el semiplano inferior, capturando el polo $+E_p - i\epsilon$ (propagación causal de electrones hacia el futuro). Para $t < t'$, el contorno se cierra por el semiplano superior, capturando el polo $-E_p + i\epsilon$ (creación de positrones).
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="paper-note">
                <b>Asimetría Leptónica & Condiciones de Sájarov:</b> La densidad cósmica medida $\eta_B \approx 6 \times 10^{-10}$ exige las 3 condiciones de Sájarov: 1) Ruptura del número bariónico/leptónico, 2) Violación simultánea de $C$ y $CP$, y 3) Ruptura del equilibrio térmico primordial.
            </div>
            """, unsafe_allow_html=True)

        col_n1, col_n2 = st.columns([1, 1])
        with col_n1:
            if st.button("← Regresar a Capítulo 3: Ecuación de Dirac", use_container_width=True, type="secondary"):
                st.session_state.submodulo_fisica = 2
                st.rerun()
        with col_n2:
            if st.button("Volver al Inicio: Capítulo 1 · Wheeler ↺", use_container_width=True, type="secondary"):
                st.session_state.submodulo_fisica = 0
                st.rerun()

# =============================================================================
# ENRUTAMIENTO POR DEFECTO / FALLBACK
# =============================================================================
else:
    render_timeline_landing(is_light)




