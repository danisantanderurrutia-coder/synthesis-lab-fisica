# components_fisica.py
# Componentes interactivos en HTML/JS puro para los laboratorios de Física Fundamental
# Soporta modo oscuro (Deep Monolith) y modo claro (Paper / Academic Light)

def _get_theme_vars(is_light: bool):
    if is_light:
        return {
            "body_color": "#1e293b",
            "box_bg": "#ffffff",
            "box_border": "1px solid #e2e8f0",
            "box_shadow": "0 2px 14px rgba(0,0,0,0.04)",
            "pill_bg": "#f8fafc",
            "pill_border": "1px solid #e2e8f0",
            "pill_lbl": "#64748b",
            "pill_val": "#0f172a",
            "canvas_bg": "#f8fafc",
            "canvas_border": "1px solid #e2e8f0",
            "btn_bg": "#f1f5f9",
            "btn_color": "#0f172a",
            "btn_border": "1px solid #cbd5e1",
            "btn_play_bg": "#0f172a",
            "btn_play_color": "#ffffff",
            "axis_color": "rgba(0,0,0,0.15)",
            "axis_text": "#64748b",
            "slice_bg": "#f1f5f9",
            "slice_border": "1px solid #cbd5e1",
            "slice_line": "#94a3b8",
            "title_color": "#0f172a",
            "sub_color": "#64748b",
            "res_bg": "#f8fafc",
            "res_border": "1px solid #e2e8f0",
            "res_color": "#0284c7"
        }
    else:
        return {
            "body_color": "#f8fafc",
            "box_bg": "rgba(6, 11, 20, 0.72)",
            "box_border": "1px solid rgba(255, 255, 255, 0.08)",
            "box_shadow": "0 10px 30px rgba(0,0,0,0.4)",
            "pill_bg": "rgba(255, 255, 255, 0.04)",
            "pill_border": "1px solid rgba(255, 255, 255, 0.1)",
            "pill_lbl": "#94a3b8",
            "pill_val": "#ffffff",
            "canvas_bg": "rgba(3, 7, 14, 0.85)",
            "canvas_border": "1px solid rgba(255, 255, 255, 0.06)",
            "btn_bg": "rgba(255, 255, 255, 0.08)",
            "btn_color": "#cbd5e1",
            "btn_border": "1px solid rgba(255, 255, 255, 0.12)",
            "btn_play_bg": "#ffffff",
            "btn_play_color": "#090d16",
            "axis_color": "rgba(255,255,255,0.1)",
            "axis_text": "rgba(255,255,255,0.6)",
            "slice_bg": "#030712",
            "slice_border": "1px solid #1e293b",
            "slice_line": "#334155",
            "title_color": "#F8FAFC",
            "sub_color": "#94a3b8",
            "res_bg": "#050b14",
            "res_border": "1px solid #1e293b",
            "res_color": "#22d3ee"
        }

def get_wheeler_sim_html(is_light: bool = False):
    """Simulador interactivo enfocado de la línea de mundo de Wheeler y corte de Cauchy."""
    v = _get_theme_vars(is_light)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: transparent !important; color: {v['body_color']}; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 2px; max-width: 860px; margin: 0 auto; }}
        .box {{ background: {v['box_bg']}; border: {v['box_border']}; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px; backdrop-filter: blur(24px); box-shadow: {v['box_shadow']}; }}
        .metrics-row {{ display: flex; gap: 8px; justify-content: flex-end; margin-bottom: 10px; }}
        .pill {{ background: {v['pill_bg']}; border: {v['pill_border']}; border-radius: 8px; padding: 4px 14px; text-align: center; }}
        .pill-lbl {{ font-size: 10px; text-transform: uppercase; font-weight: 600; color: {v['pill_lbl']}; }}
        .pill-val {{ font-size: 15px; font-weight: 700; font-family: monospace; color: {v['pill_val']} !important; }}
        canvas {{ display: block; width: 100%; border-radius: 10px; background: {v['canvas_bg']}; border: {v['canvas_border']}; }}
        .btn {{ background: {v['btn_bg']}; color: {v['btn_color']}; border: {v['btn_border']}; border-radius: 8px; padding: 7px 14px; font-size: 12px; font-weight: 600; cursor: pointer; transition: all 0.2s ease; }}
        .btn:hover {{ background: {v['btn_play_bg']}; color: {v['btn_play_color']}; }}
        .btn#btnPlay {{ background: {v['btn_play_bg']} !important; color: {v['btn_play_color']} !important; border: 1px solid {v['btn_play_bg']} !important; font-weight: 700 !important; }}
        .btn-sec {{ background: {v['pill_bg']}; color: {v['pill_lbl']}; border: {v['pill_border']}; }}
        input[type=range] {{ width: 100%; accent-color: {v['btn_play_bg']}; cursor: pointer; }}
      </style>
    </head>
    <body>
      <div class="metrics-row">
        <div class="pill"><div class="pill-lbl" style="color:#0284c7;">Electrones e⁻</div><div class="pill-val" id="num-e" style="color:#0284c7;">0</div></div>
        <div class="pill"><div class="pill-lbl" style="color:#d97706;">Positrones e⁺</div><div class="pill-val" id="num-p" style="color:#d97706;">0</div></div>
        <div class="pill"><div class="pill-lbl" style="color:#10b981;">Carga Neta Q</div><div class="pill-val" id="num-q" style="color:#10b981;">-1e</div></div>
      </div>

      <div class="box">
        <div style="display:flex; justify-content:space-between; font-size:11px; font-family:monospace; color:{v['pill_lbl']}; margin-bottom:6px;">
          <span>▲ Tiempo coordenado (t) &nbsp;|&nbsp; ► Coordenada espacial (x)</span>
          <span><span style="color:#0284c7;">● dt/dτ > 0 (e⁻)</span> &nbsp; <span style="color:#d97706;">● dt/dτ < 0 (e⁺)</span></span>
        </div>
        <canvas id="cvSpacetime" height="240"></canvas>
      </div>

      <div class="box">
        <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:8px; color:{v['body_color']};">
          <strong>🔭 Foliación espacial de Cauchy (Σ_t) a t = <span id="lblT" style="color:#0284c7; font-family:monospace;">0.50</span>:</strong>
          <span id="turnEvent" style="color:#9333ea; font-family:monospace; font-weight:700;"></span>
        </div>
        <div style="position:relative; height:46px; background:{v['slice_bg']}; border:{v['slice_border']}; border-radius:8px; overflow:hidden;">
          <div style="position:absolute; top:50%; left:0; right:0; height:1px; background:{v['slice_line']};"></div>
          <div id="sliceContainer" style="position:relative; width:100%; height:100%;"></div>
        </div>
      </div>

      <div class="box" style="margin-bottom:0;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
          <div style="display:flex; gap:8px;">
            <button id="btnPlay" class="btn">▶ Evolucionar t</button>
            <button id="btnRegen" class="btn btn-sec">🔄 Nueva Trayectoria</button>
          </div>
          <div style="font-size:12px; color:{v['pill_lbl']};">
            Deslizador temporal Cauchy (t):
          </div>
        </div>
        <input id="sliderT" type="range" min="0" max="1000" value="500">
      </div>

      <script>
        const cv = document.getElementById('cvSpacetime');
        const ctx = cv.getContext('2d');
        const sliderT = document.getElementById('sliderT');
        const lblT = document.getElementById('lblT');
        const btnPlay = document.getElementById('btnPlay');
        const btnRegen = document.getElementById('btnRegen');
        const numE = document.getElementById('num-e');
        const numP = document.getElementById('num-p');
        const numQ = document.getElementById('num-q');
        const sliceBox = document.getElementById('sliceContainer');
        const turnEvent = document.getElementById('turnEvent');

        let isPlaying = false, animId = null;
        let points = [];
        const isLight = {'true' if is_light else 'false'};

        function resize() {{
          const rect = cv.getBoundingClientRect();
          cv.width = rect.width * window.devicePixelRatio;
          cv.height = rect.height * window.devicePixelRatio;
          ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
        }}

        function genLine() {{
          points = [];
          const N = 800;
          for (let i = 0; i <= N; i++) {{
            const s = (i / N) * 4 * Math.PI;
            const x = 0.5 + 0.38 * Math.sin(s * 0.9 + 0.3) + 0.08 * Math.sin(s * 2.8);
            const t = 0.5 + 0.42 * Math.cos(s * 0.7) + 0.06 * Math.sin(s * 3.5);
            points.push({{ x: Math.max(0.04, Math.min(0.96, x)), t: Math.max(0.04, Math.min(0.96, t)) }});
          }}
        }}

        function render() {{
          const rect = cv.getBoundingClientRect();
          const W = rect.width, H = rect.height;
          ctx.clearRect(0, 0, W, H);

          const currT = parseFloat(sliderT.value) / 1000;
          lblT.textContent = currT.toFixed(2);

          // Grid
          ctx.strokeStyle = isLight ? 'rgba(0,0,0,0.06)' : 'rgba(255,255,255,0.05)';
          ctx.lineWidth = 1;
          for (let i = 1; i < 5; i++) {{
            ctx.beginPath(); ctx.moveTo(0, H * i / 5); ctx.lineTo(W, H * i / 5); ctx.stroke();
            ctx.beginPath(); ctx.moveTo(W * i / 5, 0); ctx.lineTo(W * i / 5, H); ctx.stroke();
          }}

          // Worldline
          ctx.lineWidth = 2.5;
          ctx.lineCap = 'round';
          const inters = [];

          for (let i = 0; i < points.length - 1; i++) {{
            const pA = points[i], pB = points[i+1];
            const isFwd = pB.t >= pA.t;
            ctx.beginPath();
            ctx.moveTo(pA.x * W, (1 - pA.t) * H);
            ctx.lineTo(pB.x * W, (1 - pB.t) * H);
            ctx.strokeStyle = isFwd ? (isLight ? '#0284c7' : '#22d3ee') : (isLight ? '#d97706' : '#f59e0b');
            ctx.stroke();

            if ((pA.t <= currT && pB.t >= currT) || (pA.t >= currT && pB.t <= currT)) {{
              const dt = pB.t - pA.t;
              const f = Math.abs(dt) > 1e-6 ? (currT - pA.t) / dt : 0;
              inters.push({{ x: pA.x + f * (pB.x - pA.x), forward: pB.t >= pA.t }});
            }}
          }}

          // Slice line
          const ySlice = (1 - currT) * H;
          ctx.beginPath(); ctx.moveTo(0, ySlice); ctx.lineTo(W, ySlice);
          ctx.lineWidth = 2; ctx.strokeStyle = isLight ? '#0f172a' : '#f8fafc'; ctx.setLineDash([4, 4]); ctx.stroke(); ctx.setLineDash([]);

          let e = 0, p = 0;
          inters.forEach(it => {{
            ctx.beginPath(); ctx.arc(it.x * W, ySlice, 6, 0, Math.PI * 2);
            ctx.fillStyle = it.forward ? (isLight ? '#0284c7' : '#22d3ee') : (isLight ? '#d97706' : '#f59e0b'); ctx.fill();
            if (it.forward) e++; else p++;
          }});

          numE.textContent = e; numP.textContent = p;
          const q = -e + p; numQ.textContent = `${{q >= 0 ? '+' : ''}}${{q}}e`;

          // 1D view
          sliceBox.innerHTML = '';
          let nearTurn = false;
          inters.forEach(it => {{
            const dot = document.createElement('div');
            dot.style.position = 'absolute'; dot.style.top = '50%'; dot.style.transform = 'translate(-50%, -50%)';
            dot.style.left = `${{it.x * 100}}%`; dot.style.display = 'flex'; dot.style.flexDirection = 'column'; dot.style.alignItems = 'center';
            const col = it.forward ? (isLight ? '#0284c7' : '#22d3ee') : (isLight ? '#d97706' : '#f59e0b');
            dot.innerHTML = `<div style="width:12px;height:12px;border-radius:50%;background:${{col}};box-shadow:0 0 8px ${{col}};border:1.5px solid white;"></div><span style="font-size:9px;font-weight:800;font-family:monospace;color:${{col}};margin-top:2px;">${{it.forward ? 'e⁻' : 'e⁺'}}</span>`;
            sliceBox.appendChild(dot);
          }});
          for (let i = 0; i < inters.length; i++) {{
            for (let j = i+1; j < inters.length; j++) {{
              if (inters[i].forward !== inters[j].forward && Math.abs(inters[i].x - inters[j].x) < 0.035) nearTurn = true;
            }}
          }}
          turnEvent.textContent = nearTurn ? '⚡ Evento Vértice: Aniquilación / Creación' : '';
        }}

        sliderT.addEventListener('input', render);
        btnPlay.addEventListener('click', () => {{
          isPlaying = !isPlaying;
          btnPlay.textContent = isPlaying ? '⏸ Pausar' : '▶ Evolucionar t';
          if (isPlaying) runAnim(); else cancelAnimationFrame(animId);
        }});
        function runAnim() {{
          sliderT.value = (parseInt(sliderT.value, 10) + 3) % 1000;
          render();
          if (isPlaying) animId = requestAnimationFrame(runAnim);
        }}
        btnRegen.addEventListener('click', () => {{ genLine(); render(); }});
        window.addEventListener('resize', () => {{ resize(); render(); }});
        resize(); genLine(); render();
      </script>
    </body>
    </html>
    """

def get_planck_sim_html(is_light: bool = False):
    """Simulador interactivo del microscopio cuántico-gravitacional y colapso en microagujero negro (GUP)."""
    v = _get_theme_vars(is_light)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: transparent !important; color: {v['body_color']}; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 2px; max-width: 860px; margin: 0 auto; }}
        .box {{ background: {v['box_bg']}; border: {v['box_border']}; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px; backdrop-filter: blur(24px); box-shadow: {v['box_shadow']}; }}
        .grid-2 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 12px; }}
        .grid-4 {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(110px, 1fr)); gap: 8px; margin-top: 10px; }}
        .pill {{ background: {v['pill_bg']}; border: {v['pill_border']}; border-radius: 8px; padding: 6px 10px; text-align: center; }}
        .pill-lbl {{ font-size: 10px; text-transform: uppercase; font-weight: 600; color: {v['pill_lbl']}; }}
        .pill-val {{ font-size: 14px; font-weight: 700; font-family: monospace; color: {v['pill_val']} !important; }}
        canvas {{ display: block; width: 100%; border-radius: 10px; background: {v['canvas_bg']}; border: {v['canvas_border']}; }}
        input[type=range] {{ width: 100%; accent-color: {v['btn_play_bg']}; cursor: pointer; }}
      </style>
    </head>
    <body>
      <div class="box">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
          <div>
            <h3 style="font-size:14px; color:{v['title_color']}; font-weight:700;">Microscopio Cuántico-Gravitacional</h3>
            <p style="font-size:11px; color:{v['sub_color']};">Colapso de la sonda en microagujero negro cuando Δx < ℓ_P</p>
          </div>
          <div id="stBadge" style="font-size:11px; font-family:monospace; padding:4px 10px; border-radius:20px; font-weight:800; background:rgba(16,185,129,0.15); color:#10b981; border:1px solid #10b981;">
            🟢 Régimen Cuántico Accesible
          </div>
        </div>

        <div style="margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; font-size:11px; font-family:monospace; margin-bottom:4px;">
            <span style="color:{v['body_color']};">Resolución de sonda (Δx):</span>
            <span id="dxVal" style="color:#0284c7; font-weight:800;">1.00 × 10⁻¹⁵ m</span>
          </div>
          <div style="display:flex; align-items:center; gap:8px; font-size:10px; font-family:monospace; color:{v['sub_color']};">
            <span>Protón (10⁻¹⁵m)</span>
            <input id="sliderPlanck" type="range" min="-38" max="-15" step="0.2" value="-15">
            <span>Sub-Planck (10⁻³⁸m)</span>
          </div>
        </div>

        <div class="grid-2">
          <div>
            <div style="font-size:11px; color:{v['sub_color']}; font-family:monospace; margin-bottom:4px;">Vista física: Sonda vs Radio Schwarzschild</div>
            <canvas id="cvProbe" height="170"></canvas>
            <div style="display:flex; justify-content:space-between; font-size:10px; font-family:monospace; margin-top:4px; color:{v['sub_color']};">
              <span>Círculo azul: Sonda Δx</span>
              <span id="rsLabel" style="color:#ef4444;">R_S = 0 m</span>
            </div>
          </div>
          <div>
            <div style="font-size:11px; color:{v['sub_color']}; font-family:monospace; margin-bottom:4px;">Curva GUP: Mínimo Absoluto Δx_mín ≈ ℓ_P</div>
            <canvas id="cvGUP" height="170"></canvas>
            <div style="display:flex; justify-content:space-between; font-size:10px; font-family:monospace; margin-top:4px; color:{v['sub_color']};">
              <span>Eje X: Momento Δp</span>
              <span style="color:#9333ea;">Mínimo = √2β ℓ_P</span>
            </div>
          </div>
        </div>

        <div class="grid-4">
          <div class="pill"><div class="pill-lbl">Energía Fotón E</div><div class="pill-val" id="eVal">1.2 GeV</div></div>
          <div class="pill"><div class="pill-lbl">Masa Equivalente M</div><div class="pill-val" id="mVal">2.1 × 10⁻²⁷ kg</div></div>
          <div class="pill"><div class="pill-lbl">Radio Schwarzschild R_S</div><div class="pill-val" id="rsVal">3.1 × 10⁻⁵⁴ m</div></div>
          <div class="pill"><div class="pill-lbl">Relación R_S / Δx</div><div class="pill-val" id="ratioVal" style="color:#10b981;">0.00 (Seguro)</div></div>
        </div>
      </div>

      <script>
        const sliderP = document.getElementById('sliderPlanck');
        const dxVal = document.getElementById('dxVal');
        const stBadge = document.getElementById('stBadge');
        const rsLabel = document.getElementById('rsLabel');
        const cvP = document.getElementById('cvProbe');
        const cvG = document.getElementById('cvGUP');
        const eVal = document.getElementById('eVal');
        const mVal = document.getElementById('mVal');
        const rsVal = document.getElementById('rsVal');
        const ratioVal = document.getElementById('ratioVal');
        const isLight = {'true' if is_light else 'false'};

        const L_P = 1.616255e-35;

        function update() {{
          const logDx = parseFloat(sliderP.value);
          const dx = Math.pow(10, logDx);
          const E_j = 3.1615e-26 / dx;
          const E_gev = E_j / 1.60218e-10;
          const mass = E_j / 9e16;
          const Rs = (2 * Math.pow(L_P, 2)) / dx;
          const ratio = Rs / dx;

          let name = "";
          if (logDx >= -15.5) name = " (Protón)";
          else if (logDx >= -18.5) name = " (Límite LHC)";
          else if (Math.abs(logDx - (-34.8)) < 1.0) name = " (Escala de Planck ℓ_P)";
          else if (logDx < -34.8) name = " (Sub-Planck)";

          dxVal.textContent = `${{dx.toExponential(2)}} m${{name}}`;
          rsLabel.textContent = `R_S = ${{Rs.toExponential(2)}} m`;
          rsVal.textContent = `${{Rs.toExponential(2)}} m`;
          eVal.textContent = E_gev < 1e6 ? `${{E_gev.toFixed(1)}} GeV` : `${{E_gev.toExponential(2)}} GeV`;
          mVal.textContent = `${{mass.toExponential(2)}} kg`;

          if (ratio < 0.1) {{
            stBadge.textContent = "🟢 Régimen Cuántico Accesible";
            stBadge.style.color = "#10b981"; stBadge.style.borderColor = "#10b981";
            ratioVal.textContent = `${{ratio.toExponential(1)}} (Seguro)`; ratioVal.style.color = "#10b981";
          }} else if (ratio <= 1.2) {{
            stBadge.textContent = "🟡 Umbral de Planck (Δx ~ R_S)";
            stBadge.style.color = "#d97706"; stBadge.style.borderColor = "#d97706";
            ratioVal.textContent = `~ ${{ratio.toFixed(2)}} (Frontera)`; ratioVal.style.color = "#d97706";
          }} else {{
            stBadge.textContent = "🔴 ¡Colapso en Microagujero Negro!";
            stBadge.style.color = "#ef4444"; stBadge.style.borderColor = "#ef4444";
            ratioVal.textContent = `${{ratio.toExponential(1)}} (Atrapado)`; ratioVal.style.color = "#ef4444";
          }}

          drawP(ratio);
          drawG(logDx);
        }}

        function drawP(ratio) {{
          const r = cvP.getBoundingClientRect();
          cvP.width = r.width * window.devicePixelRatio; cvP.height = r.height * window.devicePixelRatio;
          const ctxP = cvP.getContext('2d'); ctxP.scale(window.devicePixelRatio, window.devicePixelRatio);
          const W = r.width, H = r.height, cx = W/2, cy = H/2;
          ctxP.clearRect(0, 0, W, H);

          const baseR = 38;
          let Rs_vis = ratio > 1e-10 ? baseR * Math.pow(ratio, 0.45) : 0;
          Rs_vis = Math.min(Rs_vis, W * 0.45);

          // Probe
          ctxP.beginPath(); ctxP.arc(cx, cy, baseR, 0, Math.PI * 2);
          ctxP.strokeStyle = isLight ? '#0284c7' : '#22d3ee'; ctxP.lineWidth = 2; ctxP.setLineDash([4, 4]); ctxP.stroke(); ctxP.setLineDash([]);
          ctxP.fillStyle = isLight ? 'rgba(2, 132, 199, 0.08)' : 'rgba(34, 211, 238, 0.08)'; ctxP.fill();

          // Black Hole
          if (Rs_vis > 2) {{
            ctxP.beginPath(); ctxP.arc(cx, cy, Rs_vis, 0, Math.PI * 2);
            ctxP.fillStyle = '#0f172a'; ctxP.fill();
            ctxP.strokeStyle = ratio >= 1 ? '#ef4444' : '#d97706'; ctxP.lineWidth = 2.5; ctxP.stroke();
          }}
        }}

        function drawG(logDx) {{
          const r = cvG.getBoundingClientRect();
          cvG.width = r.width * window.devicePixelRatio; cvG.height = r.height * window.devicePixelRatio;
          const ctxG = cvG.getContext('2d'); ctxG.scale(window.devicePixelRatio, window.devicePixelRatio);
          const W = r.width, H = r.height;
          ctxG.clearRect(0, 0, W, H);

          const pad = 28;
          ctxG.strokeStyle = isLight ? 'rgba(0,0,0,0.15)' : 'rgba(255,255,255,0.2)'; ctxG.lineWidth = 1;
          ctxG.beginPath(); ctxG.moveTo(pad, H - pad); ctxG.lineTo(W - 10, H - pad); ctxG.moveTo(pad, H - pad); ctxG.lineTo(pad, 10); ctxG.stroke();

          const pMin = 0.25, pMax = 4.5, xMin = pad + 8, xMax = W - 15, yBottom = H - pad - 8, yTop = 15;
          function mapP(p) {{ return xMin + ((p - pMin)/(pMax - pMin))*(xMax - xMin); }}
          function mapY(y) {{ return yBottom - (Math.min(Math.max((y - 1.4)/4.5, 0), 1))*(yBottom - yTop); }}

          ctxG.beginPath(); ctxG.lineWidth = 2; ctxG.strokeStyle = isLight ? '#0284c7' : '#22d3ee';
          for (let p = pMin; p <= pMax; p += 0.05) {{
            const px = mapP(p), py = mapY(1/p + p);
            if (p === pMin) ctxG.moveTo(px, py); else ctxG.lineTo(px, py);
          }}
          ctxG.stroke();

          // Min
          const minX = mapP(1.0), minY = mapY(2.0);
          ctxG.beginPath(); ctxG.arc(minX, minY, 5, 0, Math.PI*2); ctxG.fillStyle = '#9333ea'; ctxG.fill();

          // Current
          const pProbe = Math.min(Math.max(0.3 + ((-15 - logDx)/23)*3.8, pMin), pMax);
          ctxG.beginPath(); ctxG.arc(mapP(pProbe), mapY(1/pProbe + pProbe), 6, 0, Math.PI*2); ctxG.fillStyle = '#ef4444'; ctxG.fill();
        }}

        sliderP.addEventListener('input', update);
        window.addEventListener('resize', update);
        update();
      </script>
    </body>
    </html>
    """

def get_dirac_sim_html(is_light: bool = False):
    """Simulador interactivo del espinor de Dirac y reversión de 4-corriente."""
    v = _get_theme_vars(is_light)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: transparent !important; color: {v['body_color']}; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 2px; max-width: 860px; margin: 0 auto; }}
        .box {{ background: {v['box_bg']}; border: {v['box_border']}; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px; backdrop-filter: blur(24px); box-shadow: {v['box_shadow']}; }}
        .btn-group {{ display: flex; gap: 8px; margin-bottom: 12px; }}
        .btn {{ background: {v['btn_bg']}; color: {v['btn_color']}; border: {v['btn_border']}; border-radius: 8px; padding: 8px 14px; font-size: 12px; font-weight: 600; cursor: pointer; flex: 1; text-align: center; transition: all 0.2s ease; }}
        .btn:hover {{ background: {v['btn_play_bg']}; color: {v['btn_play_color']}; }}
        .btn.active {{ background: {v['btn_play_bg']} !important; color: {v['btn_play_color']} !important; border-color: {v['btn_play_bg']} !important; font-weight: 700 !important; }}
        canvas {{ display: block; width: 100%; border-radius: 10px; background: {v['canvas_bg']}; border: {v['canvas_border']}; }}
      </style>
    </head>
    <body>
      <div class="box">
        <div style="font-size:12px; color:{v['body_color']}; margin-bottom:8px;">
          <strong>Sentido de propagación temporal en la 4-corriente:</strong>
        </div>
        <div class="btn-group">
          <button id="btnFuturo" class="btn active" onclick="setDir(1)">⏩ Avanzar al Futuro (dt/dτ > 0) ➔ Electrón (q_eff = -e)</button>
          <button id="btnPasado" class="btn" onclick="setDir(-1)">⏪ Retroceder al Pasado (dt/dτ < 0) ➔ Positrón (q_eff = +e)</button>
        </div>

        <canvas id="cvDirac" height="200"></canvas>

        <div style="display:flex; justify-content:space-between; font-size:11px; font-family:monospace; margin-top:8px; color:{v['sub_color']};">
          <span id="txtFase" style="color:#0284c7;">Fase cuántica: e^{{-i(E_p t - p·x)}}</span>
          <span id="txtCarga" style="color:#0284c7; font-weight:800;">Carga efectiva medida: -1e</span>
        </div>
      </div>

      <script>
        const cv = document.getElementById('cvDirac');
        const ctx = cv.getContext('2d');
        const btnF = document.getElementById('btnFuturo');
        const btnP = document.getElementById('btnPasado');
        const txtFase = document.getElementById('txtFase');
        const txtCarga = document.getElementById('txtCarga');
        const isLight = {'true' if is_light else 'false'};

        let dir = 1;
        let t = 0;

        function setDir(d) {{
          dir = d;
          if (dir === 1) {{
            btnF.classList.add('active'); btnP.classList.remove('active');
            txtFase.textContent = "Fase cuántica: e^{{-i(E_p t - p·x)}} (Energía positiva hacia futuro)";
            txtFase.style.color = isLight ? "#0284c7" : "#22d3ee";
            txtCarga.textContent = "Carga efectiva medida: -1e (Electrón ordinario)";
            txtCarga.style.color = isLight ? "#0284c7" : "#22d3ee";
          }} else {{
            btnP.classList.add('active'); btnF.classList.remove('active');
            txtFase.textContent = "Fase cuántica: e^{{+i(E_p t - p·x)}} ≡ e^{{-i(E_p(-t) + p·x)}} (Stückelberg)";
            txtFase.style.color = isLight ? "#d97706" : "#f59e0b";
            txtCarga.textContent = "Carga efectiva medida: +1e (Positrón de Dirac)";
            txtCarga.style.color = isLight ? "#d97706" : "#f59e0b";
          }}
        }}

        function anim() {{
          t += 0.05 * dir;
          const r = cv.getBoundingClientRect();
          cv.width = r.width * window.devicePixelRatio; cv.height = r.height * window.devicePixelRatio;
          ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
          const W = r.width, H = r.height, cy = H/2;
          ctx.clearRect(0, 0, W, H);

          // Eje
          ctx.strokeStyle = isLight ? 'rgba(0,0,0,0.1)' : 'rgba(255,255,255,0.1)'; ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(0, cy); ctx.lineTo(W, cy); ctx.stroke();

          // Onda
          ctx.beginPath();
          ctx.lineWidth = 2.5;
          ctx.strokeStyle = dir === 1 ? (isLight ? '#0284c7' : '#22d3ee') : (isLight ? '#d97706' : '#f59e0b');
          for (let x = 0; x < W; x += 2) {{
            const y = cy + Math.sin(x * 0.04 - t * 3) * 35;
            if (x === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
          }}
          ctx.stroke();

          // Partícula
          const px = ((t * 40) % W + W) % W;
          const py = cy + Math.sin(px * 0.04 - t * 3) * 35;
          ctx.beginPath(); ctx.arc(px, py, 8, 0, Math.PI*2);
          ctx.fillStyle = dir === 1 ? (isLight ? '#0284c7' : '#22d3ee') : (isLight ? '#d97706' : '#f59e0b'); ctx.fill();
          ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2; ctx.stroke();

          requestAnimationFrame(anim);
        }}
        anim();
      </script>
    </body>
    </html>
    """

def get_propagator_sim_html(is_light: bool = False):
    """Simulador interactivo del plano complejo de momentos p^0 y contornos de Jordan en QED."""
    v = _get_theme_vars(is_light)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ background: transparent !important; color: {v['body_color']}; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 2px; max-width: 860px; margin: 0 auto; }}
        .box {{ background: {v['box_bg']}; border: {v['box_border']}; border-radius: 14px; padding: 16px 20px; margin-bottom: 12px; backdrop-filter: blur(24px); box-shadow: {v['box_shadow']}; }}
        .btn-group {{ display: flex; gap: 8px; margin-bottom: 10px; }}
        .btn {{ background: {v['btn_bg']}; color: {v['btn_color']}; border: {v['btn_border']}; border-radius: 8px; padding: 7px 12px; font-size: 12px; font-weight: 600; cursor: pointer; flex: 1; text-align: center; transition: all 0.2s ease; }}
        .btn:hover {{ background: {v['btn_play_bg']}; color: {v['btn_play_color']}; }}
        .btn.active {{ background: {v['btn_play_bg']} !important; color: {v['btn_play_color']} !important; border-color: {v['btn_play_bg']} !important; font-weight: 700 !important; }}
        canvas {{ display: block; width: 100%; border-radius: 10px; background: {v['canvas_bg']}; border: {v['canvas_border']}; }}
      </style>
    </head>
    <body>
      <div class="box">
        <div style="font-size:12px; color:{v['body_color']}; margin-bottom:8px;">
          <strong>Intervalo temporal causal (x⁰ - x'⁰ = t - t'):</strong>
        </div>
        <div class="btn-group">
          <button id="btnFut" class="btn active" onclick="setMode('fut')">t > t' (Futuro: Cierre en Im p⁰ < 0)</button>
          <button id="btnPas" class="btn" onclick="setMode('pas')">t < t' (Pasado: Cierre en Im p⁰ > 0)</button>
        </div>

        <canvas id="cvProp" height="210"></canvas>

        <div id="txtResiduo" style="font-size:11px; font-family:monospace; margin-top:8px; color:{v['res_color']}; background:{v['res_bg']}; border:{v['res_border']}; padding:8px 12px; border-radius:6px;">
          Para t > t': Se encierra el polo en +E_p - iε. Residuo propaga modos de energía positiva e^{{-i E_p (t - t')}} hacia el futuro (Electrón).
        </div>
      </div>

      <script>
        const cv = document.getElementById('cvProp');
        const ctx = cv.getContext('2d');
        const btnFut = document.getElementById('btnFut');
        const btnPas = document.getElementById('btnPas');
        const txtRes = document.getElementById('txtResiduo');
        const isLight = {'true' if is_light else 'false'};

        let mode = 'fut';

        function setMode(m) {{
          mode = m;
          if (m === 'fut') {{
            btnFut.classList.add('active'); btnPas.classList.remove('active');
            txtRes.innerHTML = "<strong>Para t > t':</strong> Se encierra el polo en <span style='color:" + (isLight ? "#0284c7" : "#22d3ee") + ";'>+E_p - iε</span>. Residuo propaga modos de energía positiva e^{{-i E_p (t - t')}} hacia el futuro (Electrón).";
            txtRes.style.color = isLight ? "#0284c7" : "#22d3ee";
          }} else {{
            btnPas.classList.add('active'); btnFut.classList.remove('active');
            txtRes.innerHTML = "<strong>Para t < t':</strong> Se encierra el polo en <span style='color:" + (isLight ? "#d97706" : "#f59e0b") + ";'>-E_p + iε</span>. Residuo propaga modos de energía negativa hacia el pasado ≡ positrón hacia el futuro.";
            txtRes.style.color = isLight ? "#d97706" : "#f59e0b";
          }}
          draw();
        }}

        function draw() {{
          const r = cv.getBoundingClientRect();
          cv.width = r.width * window.devicePixelRatio; cv.height = r.height * window.devicePixelRatio;
          ctx.scale(window.devicePixelRatio, window.devicePixelRatio);
          const W = r.width, H = r.height, cx = W/2, cy = H/2;
          ctx.clearRect(0, 0, W, H);

          // Ejes
          ctx.strokeStyle = isLight ? 'rgba(0,0,0,0.15)' : 'rgba(255,255,255,0.2)'; ctx.lineWidth = 1;
          ctx.beginPath(); ctx.moveTo(15, cy); ctx.lineTo(W - 15, cy); ctx.moveTo(cx, 15); ctx.lineTo(cx, H - 15); ctx.stroke();
          ctx.fillStyle = isLight ? '#64748b' : 'rgba(255,255,255,0.6)'; ctx.font = '10px monospace';
          ctx.fillText('Re(p⁰)', W - 45, cy - 8); ctx.fillText('Im(p⁰)', cx + 8, 22);

          const poleDist = W * 0.25, eps = 16;
          const pLeftX = cx - poleDist, pLeftY = cy - eps;
          const pRightX = cx + poleDist, pRightY = cy + eps;

          // Polos
          ctx.fillStyle = isLight ? '#d97706' : '#f59e0b'; ctx.font = '15px monospace'; ctx.fillText('✕', pLeftX - 5, pLeftY + 5);
          ctx.font = '10px monospace'; ctx.fillText('-E_p + iε', pLeftX - 45, pLeftY - 8);

          ctx.fillStyle = isLight ? '#0284c7' : '#22d3ee'; ctx.font = '15px monospace'; ctx.fillText('✕', pRightX - 5, pRightY + 5);
          ctx.font = '10px monospace'; ctx.fillText('+E_p - iε', pRightX - 25, pRightY + 16);

          // Contorno de Feynman
          ctx.strokeStyle = '#9333ea'; ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(25, cy);
          ctx.lineTo(pLeftX - 25, cy);
          ctx.bezierCurveTo(pLeftX - 10, cy, pLeftX - 10, cy + 20, pLeftX + 15, cy + 20);
          ctx.lineTo(pRightX - 15, cy + 20);
          ctx.bezierCurveTo(pRightX + 10, cy + 20, pRightX + 10, cy, pRightX + 25, cy);
          ctx.lineTo(W - 25, cy);
          ctx.stroke();

          // Cierre de Jordan según modo
          ctx.setLineDash([4, 4]);
          ctx.strokeStyle = mode === 'fut' ? (isLight ? '#0284c7' : '#22d3ee') : (isLight ? '#d97706' : '#f59e0b');
          ctx.beginPath();
          if (mode === 'fut') {{
            ctx.arc(cx, cy, W*0.38, 0, Math.PI, false); // Cierre inferior
          }} else {{
            ctx.arc(cx, cy, W*0.38, Math.PI, 0, false); // Cierre superior
          }}
          ctx.stroke();
          ctx.setLineDash([]);
        }}
        window.addEventListener('resize', draw);
        draw();
      </script>
    </body>
    </html>
    """


import json

def get_timeline_carousel_html(milestones: list, is_light: bool = True):
    """
    Carrusel horizontal interactivo controlado por gestos de trackpad (two-finger swipe),
    ubicado a ancho completo ARRIBA de la estructura de dos columnas.
    Al deslizar el carrusel con el pad, la tarjeta activa hace snap en el centro y
    actualiza instantáneamente los dos bloques columnares de estudio debajo.
    """
    milestones_json = json.dumps(milestones, ensure_ascii=False)

    if is_light:
        bg_shell = "#FFFFFF"
        border_shell = "#E2E8F0"
        shadow_shell = "0 4px 20px rgba(15, 23, 42, 0.04)"
        track_bg = "#F8FAFC"
        card_bg = "#FFFFFF"
        card_border = "#E2E8F0"
        card_active_border = "#0284C7"
        card_active_shadow = "0 12px 28px rgba(2, 132, 199, 0.16)"
        text_primary = "#0F172A"
        text_secondary = "#334155"
        text_muted = "#64748B"
        accent = "#0284C7"
        accent_soft = "#E0F2FE"
        accent_text = "#0369A1"
        quote_bg = "#F8FAFC"
        quote_border = "#0F172A"
        note_bg = "#F0F9FF"
        note_border = "#0284C7"
        note_text = "#0369A1"
        doc_btn_bg = "#0F172A"
        doc_btn_text = "#FFFFFF"
        node_bg = "#F1F5F9"
        node_border = "#CBD5E1"
        math_bg = "#F8FAFC"
    else:
        bg_shell = "rgba(6, 11, 20, 0.78)"
        border_shell = "rgba(255, 255, 255, 0.09)"
        shadow_shell = "0 14px 36px rgba(0, 0, 0, 0.5)"
        track_bg = "rgba(4, 8, 15, 0.65)"
        card_bg = "rgba(12, 19, 33, 0.88)"
        card_border = "rgba(255, 255, 255, 0.09)"
        card_active_border = "#38BDF8"
        card_active_shadow = "0 14px 34px rgba(56, 189, 248, 0.22)"
        text_primary = "#F8FAFC"
        text_secondary = "#CBD5E1"
        text_muted = "#94A3B8"
        accent = "#38BDF8"
        accent_soft = "rgba(56, 189, 248, 0.14)"
        accent_text = "#7DD3FC"
        quote_bg = "rgba(255, 255, 255, 0.03)"
        quote_border = "#38BDF8"
        note_bg = "rgba(56, 189, 248, 0.07)"
        note_border = "#38BDF8"
        note_text = "#E2E8F0"
        doc_btn_bg = "#F8FAFC"
        doc_btn_text = "#090D16"
        node_bg = "rgba(255, 255, 255, 0.05)"
        node_border = "rgba(255, 255, 255, 0.12)"
        math_bg = "rgba(4, 8, 16, 0.65)"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
      <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
      <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
          background: transparent !important;
          color: {text_primary};
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
          padding: 2px 2px 10px 2px;
          overflow-x: hidden;
        }}

        /* =====================================================================
           1. CARRUSEL SUPERIOR DE ANCHO COMPLETO (ANTES DE LAS DOS COLUMNAS)
           ===================================================================== */
        .carousel-shell {{
          background: {bg_shell};
          border: 1px solid {border_shell};
          border-radius: 18px;
          padding: 18px 20px 16px 20px;
          box-shadow: {shadow_shell};
          margin-bottom: 26px;
          position: relative;
        }}

        .carousel-topbar {{
          display: flex;
          justify-content: space-between;
          align-items: center;
          flex-wrap: wrap;
          gap: 10px;
          margin-bottom: 12px;
          padding: 0 4px;
        }}
        .carousel-title-group {{
          display: flex;
          align-items: center;
          gap: 10px;
        }}
        .carousel-eyebrow {{
          font-size: 11px;
          font-weight: 800;
          letter-spacing: 0.12em;
          text-transform: uppercase;
          color: {accent};
        }}
        .carousel-counter {{
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
          font-size: 12px;
          font-weight: 700;
          padding: 3px 9px;
          border-radius: 999px;
          background: {accent_soft};
          color: {accent_text};
        }}
        .pad-hint {{
          font-size: 12px;
          color: {text_muted};
          display: flex;
          align-items: center;
          gap: 6px;
          background: {node_bg};
          border: 1px solid {card_border};
          padding: 5px 12px;
          border-radius: 999px;
          font-weight: 500;
        }}

        /* Barra de años (Nodos cronológicos rápidos) */
        .year-nodes-bar {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 4px;
          margin-bottom: 14px;
          padding: 6px 8px;
          background: {track_bg};
          border: 1px solid {card_border};
          border-radius: 12px;
          overflow-x: auto;
          scrollbar-width: none;
        }}
        .year-nodes-bar::-webkit-scrollbar {{ display: none; }}
        .year-node {{
          flex: 1 0 auto;
          text-align: center;
          padding: 5px 10px;
          border-radius: 8px;
          font-size: 11.5px;
          font-weight: 600;
          color: {text_muted};
          cursor: pointer;
          transition: all 0.2s ease;
          user-select: none;
          white-space: nowrap;
        }}
        .year-node:hover {{
          color: {text_primary};
          background: {card_bg};
        }}
        .year-node.active {{
          background: {accent};
          color: #FFFFFF;
          font-weight: 700;
          box-shadow: 0 2px 8px rgba(2, 132, 199, 0.28);
        }}

        /* Pista deslizable con Trackpad (Scroll-Snap Horizontal) */
        .carousel-viewport-wrap {{
          position: relative;
          background: {track_bg};
          border: 1px solid {card_border};
          border-radius: 14px;
          overflow: hidden;
        }}
        .carousel-track {{
          display: flex;
          align-items: stretch;
          gap: 20px;
          overflow-x: auto;
          scroll-snap-type: x mandatory;
          -webkit-overflow-scrolling: touch;
          padding: 20px calc(50% - 175px);
          scrollbar-width: none;
          cursor: grab;
        }}
        .carousel-track:active {{
          cursor: grabbing;
        }}
        .carousel-track::-webkit-scrollbar {{
          display: none;
        }}

        /* Tarjetas individuales dentro del carrusel horizontal */
        .carousel-card {{
          flex: 0 0 350px;
          scroll-snap-align: center;
          background: {card_bg};
          border: 1.5px solid {card_border};
          border-radius: 14px;
          padding: 16px 18px;
          display: flex;
          gap: 14px;
          align-items: center;
          cursor: pointer;
          user-select: none;
          transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1),
                      opacity 0.28s ease,
                      border-color 0.28s ease,
                      box-shadow 0.28s ease;
          transform: scale(0.92);
          opacity: 0.52;
        }}
        .carousel-card:hover {{
          opacity: 0.82;
        }}
        .carousel-card.active {{
          transform: scale(1.03);
          opacity: 1;
          border-color: {card_active_border};
          box-shadow: {card_active_shadow};
        }}
        .c-thumb {{
          width: 68px;
          height: 68px;
          border-radius: 12px;
          object-fit: cover;
          object-position: top center;
          flex-shrink: 0;
          border: 1px solid {card_border};
        }}
        .c-body {{
          min-width: 0;
          flex: 1;
        }}
        .c-meta-top {{
          display: flex;
          align-items: center;
          justify-content: space-between;
          gap: 6px;
          margin-bottom: 4px;
        }}
        .c-year {{
          font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
          font-size: 14px;
          font-weight: 800;
          color: {accent};
        }}
        .c-focus-pill {{
          font-size: 9.5px;
          font-weight: 800;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          padding: 2px 7px;
          border-radius: 999px;
          background: {accent_soft};
          color: {accent_text};
          opacity: 0;
          transition: opacity 0.2s ease;
        }}
        .carousel-card.active .c-focus-pill {{
          opacity: 1;
        }}
        .c-author {{
          font-size: 15px;
          font-weight: 800;
          color: {text_primary};
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          margin-bottom: 3px;
        }}
        .c-work {{
          font-size: 12px;
          color: {text_muted};
          display: -webkit-box;
          -webkit-line-clamp: 2;
          -webkit-box-orient: vertical;
          overflow: hidden;
          line-height: 1.35;
        }}

        /* Botones laterales flotantes sutiles para apoyo adicional */
        .nav-paddle {{
          position: absolute;
          top: 50%;
          transform: translateY(-50%);
          width: 36px;
          height: 36px;
          border-radius: 999px;
          background: {card_bg};
          border: 1px solid {card_border};
          color: {text_primary};
          font-size: 18px;
          font-weight: 700;
          display: flex;
          align-items: center;
          justify-content: center;
          cursor: pointer;
          z-index: 5;
          box-shadow: 0 4px 12px rgba(0,0,0,0.12);
          transition: all 0.2s ease;
        }}
        .nav-paddle:hover {{
          background: {accent};
          color: #FFFFFF;
          border-color: {accent};
        }}
        .nav-paddle.left {{ left: 10px; }}
        .nav-paddle.right {{ right: 10px; }}

        /* =====================================================================
           2. DIVISOR DE TRANSICIÓN CAROUSEL -> DOS COLUMNAS
           ===================================================================== */
        .split-section-divider {{
          display: flex;
          align-items: center;
          gap: 12px;
          margin: 6px 0 18px 0;
        }}
        .split-line {{
          flex: 1;
          height: 1px;
          background: {border_shell};
        }}
        .split-label {{
          font-size: 11px;
          font-weight: 700;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          color: {text_muted};
        }}

        /* =====================================================================
           3. ESTRUCTURA DE DOS COLUMNAS (DEBAJO DEL CARRUSEL)
           ===================================================================== */
        .two-column-study {{
          display: grid;
          grid-template-columns: 1fr 1.15fr;
          gap: 26px;
          align-items: start;
          transition: opacity 0.2s ease;
        }}
        @media (max-width: 820px) {{
          .two-column-study {{
            grid-template-columns: 1fr;
          }}
        }}

        .photo-card {{
          background: {bg_shell};
          border: 1px solid {border_shell};
          border-radius: 16px;
          overflow: hidden;
          box-shadow: {shadow_shell};
        }}
        .photo-img {{
          width: 100%;
          height: 360px;
          object-fit: cover;
          object-position: top center;
          display: block;
          border-bottom: 1px solid {border_shell};
        }}
        .photo-caption {{
          padding: 12px 16px;
          font-size: 12.5px;
          color: {text_muted};
          font-style: italic;
          line-height: 1.55;
        }}

        .doc-btn {{
          display: inline-flex;
          align-items: center;
          gap: 8px;
          background: {doc_btn_bg};
          color: {doc_btn_text};
          font-size: 13px;
          font-weight: 600;
          padding: 11px 18px;
          border-radius: 10px;
          text-decoration: none;
          margin-top: 14px;
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
          transition: transform 0.15s ease, opacity 0.15s ease;
        }}
        .doc-btn:hover {{
          transform: translateY(-1px);
          opacity: 0.92;
        }}

        .quote-box {{
          background: {quote_bg};
          border-left: 3px solid {quote_border};
          border-radius: 0 10px 10px 0;
          padding: 14px 18px;
          margin-top: 16px;
          font-size: 14.5px;
          font-style: italic;
          line-height: 1.7;
          color: {text_primary};
        }}

        .prose-card {{
          background: {bg_shell};
          border: 1px solid {border_shell};
          border-radius: 16px;
          padding: 22px 26px;
          box-shadow: {shadow_shell};
          margin-bottom: 14px;
        }}
        .pretitle {{
          font-size: 11px;
          font-weight: 800;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          color: {accent};
          margin-bottom: 6px;
        }}
        .headline {{
          font-size: 22px;
          font-weight: 800;
          color: {text_primary};
          margin-bottom: 6px;
          letter-spacing: -0.02em;
        }}
        .work-subtitle {{
          font-size: 14.5px;
          font-weight: 700;
          color: {text_primary};
          margin-bottom: 12px;
        }}
        .summary-text {{
          font-size: 14.5px;
          line-height: 1.75;
          color: {text_secondary};
        }}
        .math-box {{
          background: {math_bg};
          border: 1px solid {card_border};
          border-radius: 12px;
          padding: 16px 18px;
          margin: 10px 0;
          overflow-x: auto;
          text-align: center;
          color: {text_primary};
          font-size: 1.12em;
        }}
        .eq-notes {{
          font-size: 13px;
          color: {text_muted};
          line-height: 1.6;
          margin-top: 8px;
        }}
        .legacy-note {{
          background: {note_bg};
          border-left: 3px solid {note_border};
          border-radius: 0 12px 12px 0;
          padding: 14px 18px;
          font-size: 14px;
          line-height: 1.7;
          color: {note_text};
        }}
      </style>
    </head>
    <body>
      <!-- 1. CARRUSEL HORIZONTAL A ANCHO COMPLETO (ARRIBA DE LAS DOS COLUMNAS) -->
      <div class="carousel-shell" id="carousel-shell">
        <div class="carousel-topbar">
          <div class="carousel-title-group">
            <span class="carousel-eyebrow">CARRUSEL HISTÓRICO INTERACTIVO</span>
            <span class="carousel-counter" id="slide-counter">01 / 12</span>
          </div>
          <div class="pad-hint">
            <span>⟷</span>
            <span>Desliza horizontalmente con dos dedos en el trackpad para cambiar de hito</span>
          </div>
        </div>

        <!-- Barra de nodos de año -->
        <div class="year-nodes-bar" id="year-nodes"></div>

        <!-- Pista del carrusel con física de scroll-snap -->
        <div class="carousel-viewport-wrap">
          <button class="nav-paddle left" id="btn-left" title="Hito anterior">‹</button>
          <div class="carousel-track" id="carousel-track"></div>
          <button class="nav-paddle right" id="btn-right" title="Siguiente hito">›</button>
        </div>
      </div>

      <!-- 2. DIVISOR ANTES DE PARTIR EN DOS COLUMNAS -->
      <div class="split-section-divider">
        <div class="split-line"></div>
        <div class="split-label" id="split-label">EXPEDIENTE DOCUMENTAL EN DOS COLUMNAS · 1687 SIR ISAAC NEWTON</div>
        <div class="split-line"></div>
      </div>

      <!-- 3. ESTRUCTURA EN DOS COLUMNAS (SE ACTUALIZA AL DESLIZAR EL CARRUSEL) -->
      <div class="two-column-study" id="two-column-study">
        <!-- Columna Izquierda: Visual, Manuscrito y Cita -->
        <div class="col-left">
          <div class="photo-card">
            <img id="detail-img" class="photo-img" src="" alt="">
            <div id="detail-caption" class="photo-caption"></div>
          </div>
          <div>
            <a id="detail-link" href="#" target="_blank" class="doc-btn"></a>
          </div>
          <blockquote id="detail-quote" class="quote-box"></blockquote>
        </div>

        <!-- Columna Derecha: Prosa Científica, Ecuación KaTeX y Legado -->
        <div class="col-right">
          <div class="prose-card">
            <div id="detail-pretitle" class="pretitle"></div>
            <h3 id="detail-headline" class="headline"></h3>
            <div id="detail-work" class="work-subtitle"></div>
            <p id="detail-summary" class="summary-text"></p>
          </div>

          <div class="prose-card">
            <div class="pretitle">FORMULACIÓN MATEMÁTICA NUCLEAR</div>
            <div id="detail-math" class="math-box"></div>
            <p id="detail-eq-notes" class="eq-notes"></p>
          </div>

          <div class="legacy-note">
            <b>Legado Histórico & Trascendencia:</b> <span id="detail-legacy"></span>
          </div>
        </div>
      </div>

      <script>
        const MILESTONES = {milestones_json};
        const track = document.getElementById('carousel-track');
        const yearNodesContainer = document.getElementById('year-nodes');
        const counterEl = document.getElementById('slide-counter');
        const splitLabelEl = document.getElementById('split-label');

        let activeIndex = 0;
        let isDragging = false;
        let startX = 0;
        let scrollStart = 0;

        // Construir nodos de año y tarjetas del carrusel
        MILESTONES.forEach((m, idx) => {{
          // Nodo de año
          const node = document.createElement('div');
          node.className = 'year-node' + (idx === 0 ? ' active' : '');
          node.textContent = m.short_title;
          node.addEventListener('click', () => scrollToSlide(idx));
          yearNodesContainer.appendChild(node);

          // Tarjeta del carrusel
          const card = document.createElement('div');
          card.className = 'carousel-card' + (idx === 0 ? ' active' : '');
          card.innerHTML = `
            <img class="c-thumb" src="${{m.image_url}}" alt="${{m.author}}">
            <div class="c-body">
              <div class="c-meta-top">
                <span class="c-year">${{m.year}}</span>
                <span class="c-focus-pill">EN FOCO</span>
              </div>
              <div class="c-author">${{m.author}}</div>
              <div class="c-work">${{m.work}}</div>
            </div>
          `;
          card.addEventListener('click', () => scrollToSlide(idx));
          track.appendChild(card);
        }});

        const cards = Array.from(track.querySelectorAll('.carousel-card'));
        const yearNodes = Array.from(yearNodesContainer.querySelectorAll('.year-node'));

        function syncIframeHeight() {{
          try {{
            if (window.frameElement) {{
              const h = document.body.scrollHeight;
              if (h > 400) {{
                window.frameElement.style.height = (h + 18) + 'px';
              }}
            }}
          }} catch (e) {{}}
        }}

        function renderDetail(idx) {{
          const m = MILESTONES[idx];
          counterEl.textContent = String(idx + 1).padStart(2, '0') + ' / ' + String(MILESTONES.length).padStart(2, '0');
          splitLabelEl.textContent = 'EXPEDIENTE DOCUMENTAL EN DOS COLUMNAS · ' + m.year + ' ' + m.author.toUpperCase();

          document.getElementById('detail-img').src = m.image_url;
          document.getElementById('detail-img').alt = m.author;
          document.getElementById('detail-caption').textContent = m.image_caption;

          const linkEl = document.getElementById('detail-link');
          linkEl.href = m.primary_url;
          linkEl.textContent = '📖 ' + m.primary_label;

          document.getElementById('detail-quote').textContent = m.quote;
          document.getElementById('detail-pretitle').textContent = m.category + ' · AÑO ' + m.year;
          document.getElementById('detail-headline').textContent = m.author + ' (' + m.year + ')';
          document.getElementById('detail-work').textContent = m.work;
          document.getElementById('detail-summary').textContent = m.summary;
          document.getElementById('detail-eq-notes').textContent = m.eq_notes;
          document.getElementById('detail-legacy').textContent = m.legacy;

          const mathEl = document.getElementById('detail-math');
          if (window.katex) {{
            try {{
              katex.render(m.equation, mathEl, {{ displayMode: true, throwOnError: false }});
            }} catch (e) {{
              mathEl.textContent = m.equation;
            }}
          }} else {{
            mathEl.textContent = m.equation;
          }}

          setTimeout(syncIframeHeight, 40);
        }}

        function setActiveSlide(idx) {{
          if (idx < 0 || idx >= MILESTONES.length) return;
          if (idx === activeIndex && document.getElementById('detail-headline').textContent !== '') return;
          activeIndex = idx;

          cards.forEach((c, i) => c.classList.toggle('active', i === idx));
          yearNodes.forEach((n, i) => n.classList.toggle('active', i === idx));

          // Mantener visible el nodo del año activo en la barra superior
          const activeNode = yearNodes[idx];
          if (activeNode) {{
            const nLeft = activeNode.offsetLeft - yearNodesContainer.clientWidth / 2 + activeNode.clientWidth / 2;
            yearNodesContainer.scrollTo({{ left: nLeft, behavior: 'smooth' }});
          }}

          renderDetail(idx);
        }}

        function scrollToSlide(idx) {{
          const targetIndex = (idx + MILESTONES.length) % MILESTONES.length;
          const card = cards[targetIndex];
          if (!card) return;
          const trackCenter = track.clientWidth / 2;
          const cardCenter = card.offsetLeft + card.offsetWidth / 2;
          track.scrollTo({{
            left: cardCenter - trackCenter,
            behavior: 'smooth'
          }});
          setActiveSlide(targetIndex);
        }}

        // Detectar qué tarjeta está en el centro al deslizar con el trackpad
        let ticking = false;
        track.addEventListener('scroll', () => {{
          if (!ticking) {{
            window.requestAnimationFrame(() => {{
              const trackRect = track.getBoundingClientRect();
              const centerX = trackRect.left + trackRect.width / 2;
              let closestIdx = activeIndex;
              let minDistance = Infinity;

              cards.forEach((card, i) => {{
                const r = card.getBoundingClientRect();
                const cardCenter = r.left + r.width / 2;
                const dist = Math.abs(centerX - cardCenter);
                if (dist < minDistance) {{
                  minDistance = dist;
                  closestIdx = i;
                }}
              }});

              if (closestIdx !== activeIndex) {{
                setActiveSlide(closestIdx);
              }}
              ticking = false;
            }});
            ticking = true;
          }}
        }}, {{ passive: true }});

        // Soporte para gesto de trackpad o rueda sobre el contenedor del carrusel
        document.getElementById('carousel-shell').addEventListener('wheel', (e) => {{
          // Si el usuario desliza horizontalmente con dos dedos (deltaX), el navegador ya desplaza .carousel-track si está encima;
          // si está sobre otra parte de .carousel-shell o usa rueda vertical dentro de la pista, redirigimos suavemente:
          if (Math.abs(e.deltaX) > Math.abs(e.deltaY)) {{
            if (!track.contains(e.target)) {{
              track.scrollLeft += e.deltaX;
              e.preventDefault();
            }}
          }} else if (Math.abs(e.deltaY) > 4 && track.contains(e.target)) {{
            track.scrollLeft += e.deltaY;
            e.preventDefault();
          }}
        }}, {{ passive: false }});

        // Soporte para arrastrar con el cursor (drag)
        track.addEventListener('mousedown', (e) => {{
          isDragging = true;
          startX = e.pageX - track.offsetLeft;
          scrollStart = track.scrollLeft;
        }});
        window.addEventListener('mouseup', () => {{ isDragging = false; }});
        track.addEventListener('mousemove', (e) => {{
          if (!isDragging) return;
          e.preventDefault();
          const x = e.pageX - track.offsetLeft;
          track.scrollLeft = scrollStart - (x - startX) * 1.4;
        }});

        // Botones laterales de apoyo
        document.getElementById('btn-left').addEventListener('click', () => scrollToSlide(activeIndex - 1));
        document.getElementById('btn-right').addEventListener('click', () => scrollToSlide(activeIndex + 1));

        // Inicialización
        window.addEventListener('load', () => {{
          renderDetail(0);
          syncIframeHeight();
          document.getElementById('detail-img').addEventListener('load', syncIframeHeight);
        }});
        window.addEventListener('resize', syncIframeHeight);
        renderDetail(0);
      </script>
    </body>
    </html>
    """

