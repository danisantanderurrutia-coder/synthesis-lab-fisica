# MASTER SPECIFICATION & MANIFIESTO CIENTÍFICO: GEMELO DIGITAL ÓPTICO-HIDRÁULICO DIFERENCIABLE
## Unificación Multiescala de Transferencia Radiativa (RTM), Fluorescencia Solar (SIF), Desacople Fototérmico (TSEB) y Mecánica de Fluidos Metaestables en el Xilema

**Investigador Principal (PI):** Consorcio Biofísica Vegetal & Computación Diferenciable (Wageningen / Caltech / NASA-JPL / ESA Earth Observation)  
**Clasificación:** Fisiología Vegetal Cuantitativa, Teledetección Cuántica, Hidrodinámica Vascular y Control Óptimo en Agricultura de Precisión.

---

```
                       ARQUITECTURA DE PROPAGACIÓN DIFERENCIABLE END-TO-END
                       
  [Satélite Óptico: S2 / Hiperespectral]     [Satélite Infrarrojo Térmico: TIR]      [Sensor SIF: TROPOMI / FLEX]
     Reflectancia Direccional R(λ)               Temperatura Radiométrica T_rad           Fluorescencia 740 / 685 nm
                   │                                         │                                      │
                   ▼                                         ▼                                      ▼
      ┌─────────────────────────┐               ┌─────────────────────────┐            ┌─────────────────────────┐
      │ WP1: Inversión PROSAIL  │               │ WP3: Desacople TSEB     │            │ WP2: Dinámica Cuántica  │
      │  Operador FNO Bayesiano │               │  Partición Suelo/Canopia│            │  Partición APAR en PSII │
      │  EWT, LMA, LAI, C_ab    │               │  T_c, T_s, H_c, λTr     │            │  Φ_PSII, Φ_NPQ, Φ_SIF   │
      └────────────┬────────────┘               └────────────┬────────────┘            └────────────┬────────────┘
                   │                                         │                                      │
                   │               ┌─────────────────────────┴──────────────────────────────────────┘
                   │               │
                   ▼               ▼
          Propiedades Biofísicas    Conductancia Estomática Pura (g_s) & Transpiración Real (Tr)
          Estructurales Canopia     [Detección de Estrés Estomático en t=0 (Adelanto: 48-72h)]
                   │               │
                   └───────┬───────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ WP4: Hidráulica Vascular│
              │  EDP SPAC No Estacionaria│
              │  Tensión Tallo Ψ_stem   │
              │  Curva Weibull PLC(Ψ)   │
              └────────────┬────────────┘
                           │
                           ▼
              ┌─────────────────────────┐
              │ WP5: Optimizador MPC    │
              │  Bucle Inverso Anti-PLC │
              │  Prescripción Riego     │
              │  min V  s.a. Ψ > Ψ_50   │
              └─────────────────────────┘
```

---

## 1. EL SALTO EPISTEMOLÓGICO: LA PLANTA COMO MÁQUINA HIDRÁULICA METASTABLE

La agronomía del siglo XX incurre en dos aberraciones conceptuales:
1. **La falacia de la «esponja pasiva» ($ET_c = K_c \cdot ET_0$):** Asume que la planta es un grifo pasivo cuya pérdida de agua depende linealmente de la demanda de una pradera hipotética de pasto de $12\text{ cm}$ multiplicada por una constante empírica tabulada ($K_c$). En la realidad, el dosel leñoso ejerce un control alostérico activo y fuertemente no lineal sobre la apertura estomática mediado por el potencial osmótico de las células oclusivas y la síntesis de ácido abscísico (ABA).
2. **La falacia de la «autopsia espectral» (NDVI / NDRE):** Los índices de vegetación son cocientes normalizados de reflectancia que detectan la reducción de la densidad óptica foliar producida por la degradación oxidativa de las clorofilas y la pérdida masiva de área foliar ($LAI$). Cuando el NDVI de un cuartel decae de $0.8$ a $0.6$, el parénquima foliar ya ha sufrido plasmolisis y el sistema vascular ha colapsado. **El NDVI no es un sistema de alerta temprana; es un acta de defunción microscópica.**

### Principio Biofísico Fundamental: La Tensión Negativa en el Xilema
El agua no es empujada desde la raíz por bombeo metabólico positivo; es **estirada desde las hojas** hacia la atmósfera por el gradiente termodinámico de potencial químico ($\Psi_{\text{atm}} \approx -100\text{ a }-200\text{ MPa}$ frente a $\Psi_{\text{soil}} \approx -0.03\text{ a }-0.5\text{ MPa}$). La columna líquida del xilema se encuentra en un estado físico **metaestable bajo tensión hidrostática negativa extrema** ($P < 0\text{ MPa}$), mantenida exclusivamente por las fuerzas de cohesión intermoleculares de los puentes de hidrógeno ($\sim 29\text{ kJ/mol}$).

Si la tasa de evaporación en la atmósfera supera la capacidad conductiva del suelo y de la arquitectura radicular:
$$\frac{\partial \Psi_{\text{stem}}}{\partial t} < 0 \implies \Psi_{\text{stem}} \to \Psi_{50}$$
Al alcanzarse el umbral de nucleación capilar heterogénea (ecuación de Young-Laplace en los poros de la pared vascular), los meniscos se rompen (*air seeding*). El agua líquida sufre una transición de fase instantánea y explosiva a vapor: **cavitación acústica**. El conducto xilemático se llena de gas, produciéndose una **embolia vascular irreversible**. Si más del 50% de los vasos se embolizan ($\text{PLC} > 50\%$), la planta entra en un circuito de retroalimentación hidráulica desbocada que conduce a la desecación catastrófica por sed.

> **Misión del Gemelo Digital:** Proyectar la física de la luz espectral y térmica recibida en órbita para cuantificar la tensión del agua xilemática ($\Psi_{\text{stem}}$) y gobernar un algoritmo de control predictivo basado en modelo (MPC) que mantenga en todo momento:
> $$\Psi_{\text{stem}}(t) > \Psi_{50} + \text{HSM}_{\text{target}}$$

---

## 2. DESARROLLO EXHAUSTIVO DE LOS 5 PAQUETES DE TRABAJO (WPs)

### WORK PACKAGE 1 (WP1): Inversión Física de Transferencia Radiativa (PROSAIL Diferenciable)

#### 1. Deducción Analítica del Operador Directo PROSPECT + 4SAIL
La interacción de fotones solares en la canopia se modela integrando la ecuación de transporte radiativo (RTE) unidimensional sin término de emisión térmica interna:
$$\mu \frac{dI(z, \mu, \phi)}{dz} = -\sigma_t I(z, \mu, \phi) + \frac{\sigma_s}{4\pi} \int_{-1}^{1} \int_{0}^{2\pi} p(\mu', \phi' \to \mu, \phi) I(z, \mu', \phi') d\mu' d\phi'$$
donde $\mu = \cos\theta$ es el coseno del ángulo cenital, $\sigma_t$ y $\sigma_s$ son los coeficientes de extinción y scattering volumétrico del medio turbio, y $p(\cdot)$ es la función de fase de dispersión dependiente de la función de distribución de inclinación foliar (LIDF).

En la parametrización de **4SAIL**, la solución analítica descompone la radiancia en 4 haces acoplados: flujo directo solar colimado ($E_s$), flujos difusos hemisféricos descendente ($E_d$) y ascendente ($E_u$), y flujo direccional colimado en la línea de mira del sensor ($E_o$):
$$\frac{d}{dz} \begin{pmatrix} E_s(z) \\ E_d(z) \\ E_u(z) \\ E_o(z) \end{pmatrix} = [LAI] \cdot \mathbf{M} \begin{pmatrix} E_s(z) \\ E_d(z) \\ E_u(z) \\ E_o(z) \end{pmatrix}$$
La matriz de interacción $\mathbf{M} \in \mathbb{R}^{4 \times 4}$ depende explícitamente de la reflectancia $\rho(\lambda)$ y transmitancia $\tau(\lambda)$ foliar provistas por el modelo **PROSPECT-D**:
$$\rho(\lambda), \tau(\lambda) = \mathcal{G}_{\text{PROSPECT}}(N, C_{ab}, C_{ar}, C_{\text{ant}}, EWT, LMA)$$
donde el coeficiente de absorción espectral de la hoja $k(\lambda)$ es aditivo según la ley de Beer-Lambert:
$$k(\lambda) = \frac{k_{ab}(\lambda) C_{ab} + k_{ar}(\lambda) C_{ar} + k_w(\lambda) EWT + k_m(\lambda) LMA}{N}$$
* $EWT$ ($\text{g}\cdot\text{cm}^{-2}$ o $\text{cm}$): Contenido de agua foliar equivalente ($d_{\text{water}} = 1\text{ g/cm}^3$).
* $LMA$ ($\text{g}\cdot\text{cm}^{-2}$): Masa seca foliar por unidad de superficie.
* $C_{ab}$ ($\mu\text{g}\cdot\text{cm}^{-2}$): Concentración de clorofilas $a$ y $b$.

#### 2. Resolución del Problema Inverso y Mitigación del Mal Condicionamiento
La inversión directa $\mathbf{R}_{\text{obs}}(\lambda) \mapsto \mathbf{x} = [LAI, EWT, LMA, C_{ab}]^T$ presenta el clásico **problema de equifinalidad de Hadamard**: la absorción por agua líquida foliar en las bandas SWIR de Sentinel-2 ($B_{11}$ a $1610\text{ nm}$ y $B_{12}$ a $2190\text{ nm}$) se confunde algebraicamente con variaciones de $LMA$ y saturación de $LAI$.

Para regularizar la inversión, se formula el problema como un estimador Maximum A Posteriori (MAP) condicionado a restricciones termodinámicas convexas:
$$\mathbf{x}^* = \arg\min_{\mathbf{x} \in \Omega} \left\{ \frac{1}{2} \|\mathbf{R}_{\text{obs}} - \mathcal{S}(\mathcal{F}_{\text{RTM}}(\mathbf{x}))\|_{\boldsymbol{\Sigma}_\epsilon^{-1}}^2 + \frac{1}{2} \|\mathbf{x} - \boldsymbol{\mu}_{\text{prior}}\|_{\boldsymbol{\Sigma}_{\text{prior}}^{-1}}^2 + \lambda_{\text{phys}} \mathcal{R}_{\text{FMC}}(\mathbf{x}) \right\}$$
donde $\mathcal{S}(\cdot)$ es la función de convolución con las funciones de respuesta espectral (SRF) del sensor, y $\mathcal{R}_{\text{FMC}}(\mathbf{x})$ es el potencial termodinámico foliar penalizador:
$$\mathcal{R}_{\text{FMC}}(\mathbf{x}) = \left[ \text{ReLU}\left(FMC_{\min} - \frac{EWT}{LMA}\right) \right]^2 + \left[ \text{ReLU}\left(\frac{EWT}{LMA} - FMC_{\max}\right) \right]^2$$
Para especies leñosas vivas: $FMC_{\min} = 0.40$ ($40\%$) y $FMC_{\max} = 3.50$ ($350\%$).

Para ejecutar esta inversión en microsegundos dentro de la app, se utiliza un **Operador Neuronal de Fourier (FNO)** entrenado sobre un hipercubo de simulaciones PROSAIL. El operador aprende la inversa en el dominio frecuencial:
$$\hat{\mathbf{x}} = \mathcal{N}_\theta(\mathbf{R}_{\text{obs}}), \quad \nabla_{\mathbf{R}} \mathcal{N}_\theta \text{ diferenciable por Autodiff}.$$

---

### WORK PACKAGE 2 (WP2): Dinámica Cuántica de la Fotosíntesis y Asimilación de SIF

#### 1. Conservación de la Energía Cuántica en el Complejo Colector de Luz
La absorción de radiación fotosintéticamente activa (APAR, $400-700\text{ nm}$) por las moléculas antena del Fotosistema II (PSII) promueve un electrón desde el estado basal $S_0$ al estado excitado singlete $^{1}\text{Chl}^*$. La desexcitación obedece a un sistema de competencia cinética molecular de primer orden:

$$\Phi_{\text{PSII}} + \Phi_{\text{NPQ}} + \Phi_{\text{SIF}} = 1$$

donde las probabilidades cuánticas normalizadas dependen de las constantes de velocidad:
$$\Phi_{\text{PSII}} = \frac{k_P}{k_F + k_D + k_N + k_P}, \quad \Phi_{\text{NPQ}} = \frac{k_N + k_D}{k_F + k_D + k_N + k_P}, \quad \Phi_{\text{SIF}} = \frac{k_F}{k_F + k_D + k_N + k_P}$$
* $k_F \approx 6.7 \times 10^7\text{ s}^{-1}$ (constante intrínseca radiativa de emisión de fluorescencia).
* $k_D \approx 6.0 \times 10^7\text{ s}^{-1}$ (decaimiento térmico basal no disipativo).
* $k_P(t)$ (velocidad de fotoquímica regulada por el estado redox de la plastoquinona $Q_A$).
* $k_N(t)$ (disipación térmica no fotoquímica inducible por acidificación del lumen y el ciclo de las xantofilas, dependiente de la proteína PsbS).

#### 2. Acople Fotoquímico y Sensibilidad Temporal de SIF
La corriente neta de asimilación de $\text{CO}_2$ ($A_n$) y el flujo de transporte electrónico ($J$) responden al modelo Farquhar-von Caemmerer-Berry (FvCB):
$$J = \text{APAR} \cdot \Phi_{\text{PSII}} \cdot \alpha_{\text{leaf}} \cdot \beta_{\text{PSII}}$$
$$A_n = \frac{J (C_i - \Gamma^*)}{4 C_i + 8 \Gamma^*} - R_d = g_{\text{sc}} (C_a - C_i)$$
donde $g_{\text{sc}} = g_s / 1.6$ es la conductancia estomática al $\text{CO}_2$.

##### Demostración Analítica del Adelanto Pre-Sintomático de 48 a 72 Horas
Cuando ocurre déficit hídrico edáfico o atmosférico:
$$\Psi_{\text{soil}} \downarrow \text{ o } \text{VPD} \uparrow \implies g_s \downarrow \implies C_i \to \Gamma^*$$
Al disminuir $C_i$, la enzima RuBisCO carece de sustrato carboxilante. El aceptor primario de electrones $Q_A$ queda completamente reducido ($Q_A^- / Q_A^{\text{total}} \to 1$). La constante fotoquímica $k_P$ colapsa a $0$ en una escala de **segundos**.

En consecuencia, el rendimiento de fluorescencia $\Phi_{\text{SIF}}$ y la señal re-emitida capturada por satélite en la banda de absorción de oxígeno $\text{O}_2\text{-A}$ ($740\text{ nm}$):
$$\text{SIF}_{740} = \text{APAR} \cdot \Phi_{\text{SIF}} \cdot f_{\text{esc}}(740, LAI)$$
sufre un desplome inmediato detectable en el día $t=0$.

Por el contrario, el índice de reflectancia espectral clásico $\text{NDVI}$ responde a:
$$\text{NDVI} = \frac{R_{\text{NIR}}(LAI) - R_{\text{Red}}(C_{ab})}{R_{\text{NIR}}(LAI) + R_{\text{Red}}(C_{ab})}$$
La clorofila solo se descompone enzimáticamente mediante las vías catabólicas de la feofitinasa tras una senescencia tisular sostenida:
$$\tau_{\text{clorofila}} \sim 72\text{ a }120\text{ horas}$$
Por lo tanto:
$$\left. \frac{\partial \text{SIF}}{\partial t} \right|_{t=0} \ll 0 \quad \text{mientras que} \quad \left. \frac{\partial \text{NDVI}}{\partial t} \right|_{t=0} \approx 0$$
**Conclusión Formal:** La asimilación satelital de SIF detecta el colapso funcional estomático con un horizonte de anticipación de **2 a 3 días** antes de que sea detectable por cualquier índice de reflectancia convencional.

---

### WORK PACKAGE 3 (WP3): Desacople Fototérmico de Dos Fuentes (TSEB) y Conductancia Estomática Real

#### 1. El Problema de Mezcla Térmica en Cultivos Leñosos
En huertos de frutales o viñedos con espaciamiento inter-hilera, el radiómetro térmico satelital (ECOSTRESS / Landsat-9 TIRS) integra dentro de su píxel una radiación infrarroja compuesta gobernada por la ley de Stefan-Boltzmann:
$$\sigma T_{\text{rad}}^4(\theta) = f_c(\theta) \epsilon_c \sigma T_c^4 + [1 - f_c(\theta)] \epsilon_s \sigma T_s^4$$
donde $f_c(\theta) = 1 - \exp\left(-\frac{k_{be}(\theta) LAI}{\sqrt{1 + 2/\tan\theta_\ell}}\right)$ es la fracción de cobertura foliar en la dirección de visión $\theta$.

Si no se desacopla, la alta temperatura del suelo desnudo caliente ($T_s \approx 45-55^\circ\text{C}$) contamina la señal e impide evaluar la temperatura termodinámica real del follaje ($T_c$).

#### 2. Formulación del Balance Energético de Dos Fuentes
El sistema se resuelve desacoplando el balance de calor latente ($\lambda \mathcal{T}_r$ y $\lambda E_s$) y calor sensible ($H_c$ y $H_s$):

$$\begin{cases}
R_{n,c} = H_c + \lambda \mathcal{T}_r \\
R_{n,s} = H_s + G + \lambda E_s
\end{cases}$$

El flujo de calor en el suelo se acopla a la radiación neta del suelo: $G = c_g R_{n,s}$.

```
                     Atmósfera Libre (T_air, e_air)
                                    │
                                   [R_A]  Resistencia Aerodinámica Atmosférica
                                    │
                                    ▼
                         Vértice de Mezcla (T_AC)
                                    ▲
                     ┌──────────────┴──────────────┐
                    [R_x]                         [R_s]
         Resistencia Capa Límite           Resistencia Superficie Suelo
                     │                             │
                     ▼                             ▼
              Dosel Foliar (T_c)               Suelo (T_s)
             R_nc = H_c + λTr              R_ns = H_s + G + λEs
```

Los flujos convectivos de calor sensible convergen al nodo de mezcla inturadosel ($T_{\text{AC}}$):
$$H_c = \rho_{\text{aire}} c_p \frac{T_c - T_{\text{AC}}}{R_x}, \quad H_s = \rho_{\text{aire}} c_p \frac{T_s - T_{\text{AC}}}{R_s}$$
$$H = H_c + H_s = \rho_{\text{aire}} c_p \frac{T_{\text{AC}} - T_{\text{air}}}{R_A}$$
donde $R_A$ se obtiene integrando la teoría de similitud de Monin-Obukhov (MOST) dependiente de la escala de longitud de estabilidad térmica $L_{\text{MO}}$.

#### 3. Despeje Analítico de la Conductancia Estomática ($g_s$) sin Factores $K_c$
Una vez resuelto iterativamente el sistema no lineal y hallada la transpiración real del dosel vegetal $\lambda \mathcal{T}_r$ ($\text{W}\cdot\text{m}^{-2}$), se invierte analíticamente la ecuación de difusión molecular de vapor a través de los estomas:
$$\mathcal{T}_r = \frac{\rho_{\text{aire}} c_p}{\gamma \lambda} \frac{e_{\text{sat}}(T_c) - e_{\text{AC}}}{R_x + R_{\text{canopy}}}$$
donde $e_{\text{sat}}(T_c) = 0.61078 \exp\left(\frac{17.27 T_c}{T_c + 237.3}\right)\text{ kPa}$ y $\gamma \approx 0.066\text{ kPa}\cdot\text{K}^{-1}$.

Despejando la resistencia estomática pura del dosel:
$$R_{\text{canopy}} = \frac{\rho_{\text{aire}} c_p}{\gamma} \frac{e_{\text{sat}}(T_c) - e_{\text{AC}}}{\lambda \mathcal{T}_r} - R_x \quad [\text{s}\cdot\text{m}^{-1}]$$
Normalizando por el área foliar activa ($LAI$) y aplicando la ley de los gases ideales para convertir a unidades molares del sistema internacional:
$$g_s = \frac{1}{R_{\text{canopy}} / LAI} \times \left( \frac{P_{\text{atm}}}{R_{\text{gas}} T_c} \right) \quad \left[\text{mol}_{\text{H}_2\text{O}} \cdot \text{m}^{-2} \cdot \text{s}^{-1}\right]$$
**Ruptura Epistemológica:** La conductancia estomática $g_s$ y la transpiración $\mathcal{T}_r$ se obtienen por termodinámica directa sin requerir coeficientes arbitrarios $K_c$.

---

### WORK PACKAGE 4 (WP4): Mecánica de Fluidos en el Xilema y Predicción de Embolia (Curvas PLC)

#### 1. Dinámica No Estacionaria en el Continuo Suelo-Planta-Atmósfera (SPAC)
El flujo en los micro-conductos de la albura vegetal se rige por la conservación de masa hidrodinámica con capacitancia elástica tisular no lineal ($C_{\text{stem}}(\Psi) = dV_{\text{water}}/d\Psi$):
$$C_{\text{stem}}(\Psi_{\text{stem}}) \frac{\partial \Psi_{\text{stem}}}{\partial t} = \frac{\partial}{\partial z} \left[ K_{\text{stem}}(\Psi_{\text{stem}}) \left( \frac{\partial \Psi_{\text{stem}}}{\partial z} + \rho_w g \right) \right] - S_{\text{radic}}(z, t)$$
En su formulación de parámetros concentrados para la escala del árbol:
$$C_{\text{stem}} \frac{d\Psi_{\text{stem}}}{dt} = K_{\text{plant}}(\Psi_{\text{stem}}) \left( \Psi_{\text{soil}} - \Psi_{\text{stem}} - \rho_w g h \right) - \mathcal{T}_r(g_s, \text{VPD})$$
donde $\mathcal{T}_r$ es la tasa transpiratoria instantánea inferida desde WP3 y modulada por WP2.

#### 2. Ley de Vulnerabilidad a la Cavitación de Pammenter-Weibull
La pérdida de conductividad hidráulica del xilema por nucleación heterogénea capilar sigue una función acumulativa sigmoide:
$$\text{PLC}(\Psi_{\text{stem}}) = \frac{100}{1 + \exp\left(a \cdot (\Psi_{\text{stem}} - \Psi_{50})\right)} \quad [\%]$$
donde:
* $\Psi_{50}$ ($\text{MPa}$, negativo): Potencial hídrico del tallo en el cual se pierde el $50\%$ de la capacidad de transporte vascular.
* $a$ ($\text{MPa}^{-1}$): Pendiente de vulnerabilidad del tejido xilemático.
* La conductividad hidráulica residual efectiva del sistema es:
  $$K_{\text{plant}}(\Psi_{\text{stem}}) = K_{\max} \cdot \left[1 - \frac{\text{PLC}(\Psi_{\text{stem}})}{100}\right]$$

#### 3. Métricas de Resiliencia Vascular
* **Margen de Seguridad Hidráulica ($HSM$):**
  $$HSM = \Psi_{\min} - \Psi_{50}$$
  donde $\Psi_{\min}$ es el potencial hídrico mínimo alcanzado a mediodía solar.
* **Punto de Pérdida de Turgencia ($\Psi_{\text{tlp}}$):** Determinado termodinámicamente a partir del potencial osmótico a plena turgencia $\pi_0$ y el módulo de elasticidad volumétrica celular $\varepsilon$:
  $$\Psi_{\text{tlp}} = \frac{\pi_0 \varepsilon}{\pi_0 + \varepsilon}$$
  Si $\Psi_{\text{leaf}} < \Psi_{\text{tlp}}$, las células oclusivas sufren colapso mecánico y pierden la capacidad de cierre estomático regulado.

---

### WORK PACKAGE 5 (WP5): Bucle Diferenciable y Algoritmo de «Riego Anti-Embolia»

#### 1. Formulación del Problema de Control Predictivo Basado en Modelo (MPC)
El objetivo agronómico es responder a la pregunta operativa del productor:
> *«Dado el pronóstico meteorológico para las próximas 72 horas, ¿cuál es el volumen mínimo de agua $V^*$ y el momento de inyección óptimo $t^*$ para garantizar que el xilema no cruce el umbral crítico de cavitación $\Psi_{50}$ en el pico de demanda de la tarde?»*

El problema de optimización dinámico se formula matemáticamente como:
$$\min_{\mathbf{u} \in \mathbb{U}} \mathcal{J} = \int_{0}^{T} \left[ \|\mathbf{u}(t)\|_1 + \omega_{\text{risk}} \cdot \mathcal{P}_{\text{embolia}}(\Psi_{\text{stem}}(t)) \right] dt$$
sujeto a las ligaduras de la física del sistema:
$$\begin{cases}
\dot{\mathbf{x}}(t) = \mathbf{f}_{\text{SPAC}}(\mathbf{x}(t), \mathbf{u}(t), \mathbf{w}_{\text{meteo}}(t)) & \text{(Dinámica hidráulica no lineal)} \\
\mathbf{y}_{\text{sat}}(t) = \mathcal{H}(\mathbf{x}(t)) & \text{(Ecuaciones de observación RTM/SIF/TSEB)} \\
\Psi_{\text{stem}}(t) \ge \Psi_{50} + HSM_{\text{target}} & \forall t \in [0, T] \quad \text{(Restricción de no-cavitación)} \\
0 \le u(t) \le u_{\max} & \text{(Capacidad de impulsión del sistema de riego)}
\end{cases}$$
donde $\mathbf{u}(t)$ es el caudal de riego milimétrico aplicado, $\mathbf{w}_{\text{meteo}}(t) = [R_g, T_{\text{air}}, \text{VPD}, u]^T$ es el vector exógeno de forzamiento meteorológico, y la función de penalización por riesgo de embolia es cuadrática y asimétrica:
$$\mathcal{P}_{\text{embolia}}(\Psi_{\text{stem}}) = \left[ \max\left(0, (\Psi_{50} + HSM_{\text{target}}) - \Psi_{\text{stem}}(t)\right) \right]^2$$

Dado que todas las componentes del gemelo digital (PROSAIL $\to$ FvCB/SIF $\to$ TSEB $\to$ SPAC) están programadas en operadores diferenciables (Autodiff en JAX), el gradiente de la función de coste respecto al plan de riego:
$$\nabla_{\mathbf{u}} \mathcal{J} = \frac{\partial \mathcal{J}}{\partial \mathbf{u}}$$
se evalúa de forma exacta mediante retropropagación temporal (*backpropagation through time / adjoint state method*), permitiendo al solver L-BFGS-B converger al perfil de riego óptimo en segundos.

---

## 3. PROTOCOLO DE VALIDACIÓN EXPERIMENTAL GROUND-TRUTH EN TERRENO

Para calibrar y validar las predicciones del gemelo digital en especies frutales leñosas (*Corylus avellana*, *Vitis vinifera*, *Prunus avium*), se establece un protocolo instrumental de alta resolución:

```
=============================================================================================================
VARIABLE FISIOLÓGICA      INSTRUMENTAL DE CAMPO              FRECUENCIA TEMPORAL    ROL EN EL GEMELO DIGITAL
=============================================================================================================
Potencial Hídrico de      Bomba de Presión de Scholander     Solar Noon (13:00 h)   Estándar de oro para calibrar
Tallo (Ψ_stem)            (Cámara de Presión hermética)      y Predawn (04:30 h)    el gradiente SPAC de WP4.
                          Hojas embolsadas en aluminio       (n = 20 réplicas/ha)   Curvas Presión-Volumen (P-V)
                          2 horas antes de la medición.                             para extraer Ψ_tlp, π_0, ε.

Tensión Xilemática        Psicrómetros de Tallo In-Situ      Registro continuo      Monitoreo dinámico continuo
Continua (Ψ_stem(t))      (Cámaras Peltier termopar PSY1)    cada 15 minutos        de la onda de tensión
                          instaladas en albura viva.         Resolución: ±0.01 MPa  y recarga nocturna.

Flujo de Savia /          Sondas térmicas de disipación      Registro continuo      Validación directa de la
Transpiración Real (Tr)   de Granier (TDP) con agujas        cada 10 minutos        transpiración pura canopia
                          calefactoras axiales en tronco.    Resolución: 0.1 L/h    desacoplada en TSEB (WP3).

Emisión Acústica de       Sensores piezoeléctricos           Registro continuo      Validación empírica en tiempo
Cavitación Ultrasónica    de banda ancha (100-1000 kHz)      Eventos transitorios   real de la curva sigmoide de
(UAE)                     adheridos a la madera.             (chasquidos acústicos) rotura capilar PLC(Ψ).

Temperatura Superficial   Radiómetros infrarrojos térmicos   Registro continuo      Validación de la separación
de Canopia Pura (T_c)     de campo estrecho (Apogee IRT)     cada 5 minutos         fototérmica T_c vs T_s del
                          apuntando al dosel superior.       Resolución: ±0.1 °C    algoritmo TSEB (WP3).
=============================================================================================================
```

---

## 4. INTEGRACIÓN DE ESTA ESPECIFICACIÓN EN LA APLICACIÓN

Esta fundamentación no es solo un documento estático: **está conectada funcionalmente con la aplicación interactiva de observabilidad.**

1. **Base Matemática de la App:** Las ecuaciones deducidas en los 5 Work Packages son las que alimentan los gráficos interactivos del dashboard en [`gemelo_digital_app.py`](file:///Users/danielsantander/Downloads/Fisica/gemelo_digital_app.py).
2. **Pestaña Documental en la App:** La aplicación incorpora una pestaña interactiva específica (`📜 Especificación Master PI`) donde el investigador o usuario puede consultar las deducciones analíticas, las matrices de transferencia radiativa y el protocolo de validación directamente mientras manipula los controles de simulación en vivo.
