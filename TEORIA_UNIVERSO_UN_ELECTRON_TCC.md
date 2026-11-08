# Del Universo de un Solo Electrón al Formalismo de Feynman-Stückelberg en TCC

## 1. Contexto Histórico y Planteamiento Formal

En la primavera de 1940, John Archibald Wheeler propuso a Richard Feynman una conjetura topológica en el espacio-tiempo de Minkowski $(\mathcal{M}, \eta_{\mu\nu})$: la totalidad de los electrones observados en el universo observable son segmentos temporales dirigidos hacia el futuro de una **única línea de mundo compacta o semi-infinita** $x^\mu(\tau)$, parametrizada por el tiempo propio $\tau$.

La motivación original radicaba en la indistinguibilidad cuántica estricta: para todo par de electrones $i, j$, su masa invariante $m$, carga elemental $e$ y número de espín $s$ satisfacen:

$$\Delta m_{ij} = 0, \quad \Delta e_{ij} = 0, \quad \Delta s_{ij} = 0$$

Wheeler conjeturó que esta identidad de parámetros fundamentales no es una simetría accidental del vacío ni una mera consecuencia axiomática de la teoría de campos, sino una identidad ontológica: existe únicamente una curva holonómica cuya intersección con una foliación espacial de Cauchy $\Sigma_t$ produce $N_e$ electrones y $N_p$ positrones.

---

## 2. Inversión Temporal y la Interpretación de Feynman-Stückelberg

El desarrollo formal riguroso de esta idea fue formulado de manera independiente por **Ernst Stückelberg (1941)** y desarrollado operacionalmente por **Richard Feynman (1949)** en su seminal artículo *"The Theory of Positrons"*.

### 2.1. Parametrización Clásica de la 4-Corriente
Consideremos una partícula clásica puntual con carga eléctrica $q = -e$ ($e > 0$) y trayectoria relativista $x^\mu(\tau)$. Su 4-vector densidad de corriente electromagnética viene dado por:

$$j^\mu(x) = q \int_{-\infty}^{\infty} d\tau \, \frac{dx^\mu(\tau)}{d\tau} \, \delta^{(4)}\!\big(x - x(\tau)\big)$$

Si introducimos una inversión en el parámetro de evolución sobre la línea de mundo:

$$\tau \to -\tau \quad \implies \quad \frac{dx^\mu}{d\tau} \to -\frac{dx^\mu}{d\tau}$$

La 4-velocidad cambia de signo $u^\mu \to -u^\mu$. En particular, la componente temporal:

$$u^0 = \frac{dt}{d\tau} < 0$$

indica que la partícula se propaga hacia el pasado coordenado ($dt < 0$). Observando la componente espacial de la corriente con respecto al tiempo coordenado de laboratorio $t$:

$$\vec{j}(x) = q \, \frac{d\vec{x}}{dt} = q \, \left(\frac{d\vec{x}}{d\tau}\right)\left(\frac{dt}{d\tau}\right)^{-1}$$

El producto de la carga $q$ por la orientación temporal $\text{sgn}(dt/d\tau)$ determina la carga aparente detectada por un observador inercial:

$$q_{\text{eff}} = q \cdot \operatorname{sgn}\left(\frac{dt}{d\tau}\right)$$

Si $q = -e$ y la partícula viaja hacia atrás en el tiempo ($dt/d\tau < 0$):

$$q_{\text{eff}} = (-e)(-1) = +e$$

Una carga negativa propagándose hacia el pasado es indistinguible clásicamente de una antipartícula de carga positiva moviéndose hacia el futuro.

---

## 3. Formulación en Mecánica Cuántica Relativista: La Ecuación de Dirac

La ecuación de Dirac para un fermión de espín $1/2$ libre en unidades naturales ($\hbar = c = 1$):

$$(i \gamma^\mu \partial_\mu - m) \psi(x) = 0$$

donde $\{\gamma^\mu, \gamma^\nu\} = 2\eta^{\mu\nu}$ con signatura $(+,-,-,-)$.

### 3.1. Soluciones de Energía Positiva y Negativa
El espacio de soluciones admite una base de ondas planas:

$$\psi_p^{(+)}(x) = u^s(p) e^{-i p \cdot x}, \quad \psi_p^{(-)}(x) = v^s(p) e^{+i p \cdot x}$$

donde $p^0 = E_p = \sqrt{\vec{p}^2 + m^2} > 0$.
* Las soluciones $\psi^{(+)}$ poseen 4-momento físico $p^\mu = (E_p, \vec{p})$:

$$i \frac{\partial}{\partial t}\psi_p^{(+)} = E_p \psi_p^{(+)}$$

* Las soluciones $\psi^{(-)}$ poseen energía formalmente negativa:

$$i \frac{\partial}{\partial t}\psi_p^{(-)} = -E_p \psi_p^{(-)}$$

### 3.2. Transformación de Conjugación de Carga ($C$) y Reversión Temporal ($T$)
En el marco de Dirac original (Teoría del Mar de Dirac), los estados de energía negativa se postulaban llenos hasta el nivel de Fermi. 

En la formulación de Feynman-Stückelberg, un estado con energía negativa que evoluciona como $e^{+i E_p t}$ se reinterpreta geométricamente mediante la simetría $CPT$:

$$e^{+i E_p t} = e^{-i E_p (-t)}$$

Un estado de energía $-E_p$ que viaja hacia adelante en el tiempo equivale formalmente a un estado de energía $+E_p$ que viaja hacia atrás en el tiempo. La aplicación del operador de conjugación de carga $\mathcal{C} = i\gamma^2 \gamma^0$ (en la representación estándar de Dirac-Pauli) mapea:

$$\psi_C = \mathcal{C} \bar{\psi}^T \implies (i\gamma^\mu \partial_\mu + e A_\mu - m)\psi_C = 0$$

invirtiendo el acoplamiento mínimo $e \to -e$.

---

## 4. El Propagador de Feynman: Causalidad y Condiciones de Contorno

La condición matemática fundamental que formaliza esta dinámica es la prescripción de contorno $i\epsilon$ en la transformada de Fourier de la función de Green de 2 puntos (el propagador de Feynman $S_F(x - x')$):

$$(i\gamma^\mu \partial_\mu - m) S_F(x - x') = i \delta^{(4)}(x - x')$$

En el espacio de momentos:

$$S_F(p) = \frac{i(\not{p} + m)}{p^2 - m^2 + i\epsilon} = \frac{i(\gamma^\mu p_\mu + m)}{(p^0)^2 - (\vec{p}^2 + m^2) + i\epsilon}$$

Los polos en el plano complejo de $p^0$ se ubican en:

$$p^0 = \pm \sqrt{\vec{p}^2 + m^2} \mp i\epsilon = \pm E_p \mp i\epsilon$$

Al evaluar la integral temporal mediante el teorema de los residuos:

$$S_F(x - x') = \int \frac{d^3 p}{(2\pi)^3 2E_p} \left[ \theta(t - t') (\not{p} + m) e^{-i p \cdot (x - x')} + \theta(t' - t) (-\not{p} + m) e^{+i p \cdot (x - x')} \right]_{p^0 = E_p}$$

### Significado Físico:
1. Para **$t > t'$** (el futuro relativo): el contorno encierra el polo en $+E_p - i\epsilon$. Se propagan **únicamente estados de energía positiva** ($e^-$).
2. Para **$t < t'$** (el pasado relativo): el contorno encierra el polo en $-E_p + i\epsilon$. Se propagan **únicamente estados de energía negativa hacia el pasado**, lo que físicamente corresponde a la propagación hacia el futuro de **positrones de energía positiva**.

Esta condición de frontera fue descrita explícitamente por Feynman en 1949:
> *"La prescripción causal estándar equivale a tratar las soluciones de frecuencia negativa como partículas que retroceden en el tiempo."*

---

## 5. Ruptura de la Hipótesis del Universo de un Solo Electrón en TCC

A pesar de que el formalismo de Feynman resolvió la cinemática relativista de las antipartículas, la hipótesis ontológica de Wheeler (un solo electrón global) colapsa por razones fundamentales al pasar a la Teoría Cuántica de Campos moderna:

### 5.1. Violación Estricta de la Simetría de Carga (Asimetría Bariónica y Leptónica)
Si la totalidad de electrones y positrones proviniese de una única línea continua compacta $x^\mu(\tau)$, la integral topológica de la 4-corriente a través de una hipersuperficie espacial $\Sigma_t$ implicaría conservación neta del número leptónico en cada corte de Cauchy:

$$N_e(t) - N_{e^+}(t) = \text{constante} \in \{0, \pm 1\}$$

Experimentalmente, la densidad numérica en el universo observable satisface:

$$\eta_B = \frac{n_B - n_{\bar{B}}}{n_\gamma} \sim 6 \times 10^{-10}, \quad n_{e^+} \ll n_{e^-}$$

La asimetría requiere procesos que violen el número leptónico/bariónico ($B-L$), violación de $C$ y $CP$, y pérdida de equilibrio térmico (**Condiciones de Sájarov**), incompatibles con una línea de mundo única cerrada.

### 5.2. Espacio de Fock y Operadores de Campo
En TCC no se cuantiza la coordenada $x^\mu(\tau)$ de una partícula única (cuantización en primera cuantización), sino el campo local $\hat{\psi}(x)$ sobre el espacio de Fock $\mathcal{F}$:

$$\hat{\psi}(x) = \int \frac{d^3 p}{(2\pi)^3 \sqrt{2E_p}} \sum_{s=1,2} \left( a_s(\vec{p}) u^s(\vec{p}) e^{-ip \cdot x} + b_s^\dagger(\vec{p}) v^s(\vec{p}) e^{+ip \cdot x} \right)$$

con relaciones canónicas de anticonmutación fermiónicas:

$$\{a_r(\vec{p}), a_s^\dagger(\vec{q})\} = (2\pi)^3 \delta_{rs} \delta^{(3)}(\vec{p} - \vec{q}), \quad \{b_r(\vec{p}), b_s^\dagger(\vec{q})\} = (2\pi)^3 \delta_{rs} \delta^{(3)}(\vec{p} - \vec{q})$$

* Los electrones no son «objetos geométricos individuales», sino **estados excitados del vacío fermiónico**: $|e^-(\vec{p})\rangle = a^\dagger(\vec{p})|0\rangle$.
* La indistinguibilidad de los fermiones no proviene de ser la misma partícula individual, sino del hecho fundamental de que **todos son excitaciones cuánticas del mismo campo universal subyacente $\hat{\psi}(x)$**.

### 5.3. Espín-Estadística y Antisimétrica de la Función de Onda
Para un estado de $N$ electrones $| \Psi_{1...N} \rangle = a^\dagger(p_1) ... a^\dagger(p_N) |0\rangle$, la anticonmutación de los operadores implica:

$$| \Psi_{...i...j...} \rangle = - | \Psi_{...j...i...} \rangle$$

En la formulación de una sola línea de mundo continua, describir el entrelazamiento multipartícula multipartito y la antisimetrización global sin introducir el formalismo de campos de operadores resulta matemáticamente no unitario y no causal.

---

## 6. Límites Fundamentales: Longitud de Planck, Tiempo Mínimo y Espuma Cuántica de Wheeler

La hipótesis de Wheeler presupone una variedad continua suave $(\mathcal{M}, \eta_{\mu\nu})$ donde la trayectoria $x^\mu(\tau)$ es diferenciable de clase $\mathcal{C}^\infty$ en todo punto, incluidos los vértices de reversión temporal. Sin embargo, al unificar Relatividad General y Mecánica Cuántica, emerge una escala cinemática y operacional infranqueable: **la escala de Planck**.

### 6.1. Análisis Dimensional y Escalas Naturales de Planck
A partir de la constante de Planck reducida $\hbar$ (cuántica), la velocidad de la luz $c$ (relatividad especial) y la constante de gravitación universal $G$ (relatividad general):

$$\text{Longitud de Planck: } \ell_P = \sqrt{\frac{\hbar G}{c^3}} \approx 1.616 \times 10^{-35} \text{ m}$$

$$\text{Tiempo de Planck: } t_P = \frac{\ell_P}{c} = \sqrt{\frac{\hbar G}{c^5}} \approx 5.391 \times 10^{-44} \text{ s}$$

$$\text{Masa de Planck: } M_P = \sqrt{\frac{\hbar c}{G}} \approx 2.176 \times 10^{-8} \text{ kg} \approx 1.22 \times 10^{19} \text{ GeV}/c^2$$

$$\text{Energía de Planck: } E_P = M_P c^2 = \sqrt{\frac{\hbar c^5}{G}} \approx 1.956 \times 10^9 \text{ J}$$

### 6.2. El Límite Operacional: Paradoja del Microscopio Cuántico-Gravitatorio
¿Por qué $\ell_P$ y $t_P$ constituyen un límite operacional absoluto?

1. **Resolución Cuántica (Principio de Incertidumbre de Heisenberg):**  
   Para localizar una partícula o punto espacio-temporal dentro de una incertidumbre espacial $\Delta x$, la longitud de onda de De Broglie de la sonda cuántica debe satisfacer $\lambda \lesssim \Delta x$. El momento transferido es:
   $$p \sim \frac{\hbar}{\Delta x} \implies E \sim p c \sim \frac{\hbar c}{\Delta x}$$
   A medida que $\Delta x \to 0$, la densidad de energía requerida diverge asintóticamente ($E \to \infty$).

2. **Respuesta Gravitacional de Einstein:**  
   Según la Relatividad General, concentrar una energía $E$ (masa equivalente $M = E/c^2$) dentro de una región de radio $\Delta x$ curva la geometría circundante. El radio gravitacional de Schwarzschild asociado es:
   $$R_S = \frac{2GM}{c^2} = \frac{2GE}{c^4} \sim \frac{2G\hbar}{c^3 \Delta x} = \frac{2\ell_P^2}{\Delta x}$$

3. **El Colapso del Proceso de Medición:**  
   Si intentamos medir por debajo de la longitud de Planck ($\Delta x < \ell_P$):
   $$R_S > \Delta x$$
   El radio de Schwarzschild supera el radio de confinamiento de la sonda. **El propio proceso de medición colapsa en un microagujero negro**, cuyo horizonte de eventos atrapa los fotones o señales de la sonda. Cualquier intento de aumentar la resolución inyectando mayor energía $E$ únicamente incrementa el tamaño del horizonte ($R_S \propto E$), destruyendo irrevocablemente la resolución espacial.

Por tanto, $\ell_P$ y $t_P = \ell_P/c$ no son barreras tecnológicas, sino límites axiomáticos impuestos conjuntamente por $\hbar, c$ y $G$.

### 6.3. Principio de Incertidumbre Generalizado (GUP)
En gravedad cuántica y teoría de cuerdas, el retroceso gravitacional de la sonda altera el conmutador fundamental de Heisenberg $[\hat{x}, \hat{p}] = i\hbar (1 + \beta \ell_P^2 \hat{p}^2 / \hbar^2)$, produciendo la relación de indeterminación generalizada:

$$\Delta x \ge \frac{\hbar}{2 \Delta p} + \beta \frac{G}{c^3} \Delta p = \frac{\hbar}{2 \Delta p} + \beta \ell_P^2 \frac{\Delta p}{\hbar}$$

Minimizando $\Delta x$ respecto a $\Delta p$:

$$\frac{d(\Delta x)}{d(\Delta p)} = -\frac{\hbar}{2 (\Delta p)^2} + \beta \frac{\ell_P^2}{\hbar} = 0 \implies (\Delta p)_{\text{crítico}} = \frac{\hbar}{\ell_P \sqrt{2\beta}}$$

Evaluando el valor mínimo absoluto:

$$\Delta x_{\text{mín}} = \sqrt{2\beta} \, \ell_P \sim \mathcal{O}(\ell_P)$$

A diferencia de la mecánica cuántica ordinaria (donde $\Delta x \to 0$ si $\Delta p \to \infty$), en presencia de gravedad cuántica **ningún estado físico puede poseer una dispersión posicional menor que $\sim \ell_P$**.

### 6.4. Discreción vs. Continuidad en Modelos Modernos

* **Gravedad Cuántica de Bucles (Loop Quantum Gravity - LQG):**  
  La geometría no es una variedad continua de fondo, sino un operador cuántico. El operador de área $\hat{A}$ sobre los estados de red de espín $|s\rangle$ posee un espectro de autovalores estrictamente discreto:
  $$\hat{A} |s\rangle = 8\pi \gamma \ell_P^2 \sum_{i} \sqrt{j_i(j_i + 1)} |s\rangle, \quad j_i \in \left\{\frac{1}{2}, 1, \frac{3}{2}, \dots\right\}$$
  donde $\gamma \approx 0.2375$ es el parámetro de Barbero-Immirzi. El área mínima no nula (el *gap* cuántico de área) es:
  $$\Delta A_{\text{mín}} = 4\sqrt{3}\pi \gamma \ell_P^2$$
  El espacio no es continuo, sino granular y poliedral a escala $\ell_P$.

* **Teoría de Cuerdas y Dualidad T:**  
  La sonda elemental no es puntual, sino una cuerda unidimensional de longitud intrínseca $\ell_s \sim \ell_P$. Al compactificar una dimensión espacial en un círculo de radio $R$, la masa de los modos de Kaluza-Klein ($M_{\text{momentum}} \sim n/R$) y de devanado (*winding*, $M_{\text{winding}} \sim m R / \alpha'$) es invariante bajo la transformación de dualidad T:
  $$R \longleftrightarrow \frac{\alpha'}{R} = \frac{\ell_s^2}{R}$$
  Cualquier intento de sondear una geometría a radio $R < \ell_s$ es físicamente idéntico a medir una geometría dual a radio $R' > \ell_s$. La escala $\ell_s$ actúa como una cota inferior infranqueable.

### 6.5. Implicaciones sobre la Hipótesis de Wheeler: La Espuma Cuántica (Quantum Foam)
Fue el propio John Wheeler quien en 1955 demostró que a escala de Planck la noción de variedad diferenciable colapsa. Las fluctuaciones métricas satisfacen:

$$\Delta g_{\mu\nu} \sim \frac{\ell_P}{L}$$

Cuando la escala de observación $L \to \ell_P$, las fluctuaciones de la métrica son del orden de la unidad ($\Delta g \sim 1$). A esta escala:
1. La topología del espacio-tiempo deja de ser conexa y suave; se convierte en **espuma cuántica** (*Wheeler's Spacetime Foam*), con fluctuaciones violentas de micro-agujeros negros y agujeros de gusano euclidianos.
2. Los puntos de giro clásicos donde $dt/d\tau$ cambia de signo (aniquilación/creación) requieren que la hebra trace una curvatura infinita o no diferenciable si ocurre en tiempos $\Delta t < t_P$.
3. Debido al principio de indeterminación tiempo-energía $\Delta E \Delta t \ge \hbar/2$, revertir temporalmente en un intervalo $\Delta t \sim t_P$ inyecta fluctuaciones de energía $\Delta E \sim E_P$, lo que desgarra la geometría de fondo e invalida la existencia de una trayectoria clásica continua $x^\mu(\tau)$.

---

## 7. Bibliografía Fundamental

1. **Stueckelberg, E. C. G.** (1941). *La signification du temps propre en théorie des quanta*. Helvetica Physica Acta, 14, 322–323.
2. **Stueckelberg, E. C. G.** (1942). *La mécanique du point matériel en théorie de la relativité et en théorie des quanta*. Helvetica Physica Acta, 15, 23–37.
3. **Feynman, R. P.** (1949). *The Theory of Positrons*. Physical Review, 76(6), 749–759.
4. **Feynman, R. P.** (1949). *Space-Time Approach to Quantum Electrodynamics*. Physical Review, 76(6), 769–789.
5. **Wheeler, J. A., & Feynman, R. P.** (1945). *Interaction with the Absorber as the Mechanism of Radiation*. Reviews of Modern Physics, 17(2-3), 157–181.
6. **Wheeler, J. A.** (1955). *Geons*. Physical Review, 97(2), 511–536 (Introducción formal del concepto de espuma cuántica / *spacetime foam*).
7. **Planck, M.** (1899). *Über irreversible Strahlungsvorgänge*. Sitzungsberichte der Königlich Preußischen Akademie der Wissenschaften zu Berlin, 440–480.
8. **Rovelli, C., & Smolin, L.** (1995). *Discreteness of area and volume in quantum gravity*. Nuclear Physics B, 442(3), 593–619.
9. **Kempf, A., Mangano, G., & Mann, R. B.** (1995). *Hilbert space representations of the minimal length uncertainty relation*. Physical Review D, 52(2), 1108–1118 (Formalismo de GUP).
10. **Weinberg, S.** (1995). *The Quantum Theory of Fields, Volume 1: Foundations*. Cambridge University Press.
11. **Peskin, M. E., & Schroeder, D. V.** (1995). *An Introduction to Quantum Field Theory*. Addison-Wesley.
