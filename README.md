🌡 TermoStrat-EP
Simulador de Estratificación Térmica en Termotanques Domiciliarios  
Modelo Multi-Nodo compatible con EnergyPlus `WaterHeater:Stratified` v26-1-0
![License: AGPL v3](https://img.shields.io/badge/License-AGPL_v3-blue.svg)
![Python 3.10+](https://img.shields.io/badge/Python-3.10+-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red.svg)
---
Descripción
TermoStrat-EP simula la estratificación térmica de un termotanque cilíndrico vertical
siguiendo la formulación 1-DIM del objeto `WaterHeater:Stratified` de EnergyPlus V26-1-0.
El modelo resuelve el balance de energía por nodo mediante integración numérica de
Euler explícito, considerando condiciones de reposo y consumo típico de una familia
de 4 integrantes. La temperatura ambiente se mantiene constante (sin variación
climática horaria).

Características
Modelo 1-DIM multi-nodo (3–12 nodos)
Integración numérica de Euler explícito
Balance de energía por nodo: calefactor, pérdidas térmicas, conducción axial,
advección y mezcla por inversión de densidad (InversionMixing)
Control termostático con histéresis (setpoint + banda muerta)
Perfil de consumo configurable por eventos (hora, duración, caudal)
Perfiles predefinidos: sin consumo, familia 4 personas día típico, uso intensivo
Verificación automática de estabilidad numérica (número de Fourier)
Verificación del balance energético (error relativo)
Interfaz web interactiva desarrollada en Streamlit
Visualizaciones: evolución temporal, mapa de estratificación,
análisis energético, perfil de consumo
Exportación de resultados en formato CSV

Instalación y ejecución local
Requisitos
Python 3.10 o superior
Anaconda (recomendado) o pip
Pasos
```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/termostrat-ep.git
cd termostrat-ep

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la app
streamlit run app_termotanque.py
```

Uso en línea
La app está desplegada públicamente en Streamlit Community Cloud:
🔗 https://tu-usuario-termostrat-ep.streamlit.app
(Reemplazar con la URL real una vez desplegada)

Estructura del repositorio
```
termostrat-ep/
├── app_termotanque.py     # Aplicación Streamlit principal
├── requirements.txt       # Dependencias Python
├── LICENSE                # GNU Affero General Public License v3.0
└── README.md              # Este archivo
```
---
Modelo matemático
Cada nodo i satisface el balance de energía:
```
M·Cp·dT/dt = Q̇_calef − Q̇_pérd + Q̇_cond + Q̇_advec + Q̇_inv
```
Término	Descripción
Q̇_calef	Calor inyectado por el calefactor a gas
Q̇_pérd	Pérdidas al ambiente a través del aislamiento
Q̇_cond	Conducción axial entre nodos adyacentes (Fourier discreto)
Q̇_advec	Advección por entrada/salida de agua
Q̇_inv	Mezcla por inversión de densidad (flotabilidad)
Estabilidad numérica: criterio de Fourier `Fo = k·Δt / (ρ·Cp·Δz²) ≤ 0.5`

Referencias
EnergyPlus Engineering Reference, v26.1.0 — §19.3.3 Stratified Water Thermal Tank
ASHRAE Standard 90.1 — Requisitos de eficiencia para calentadores de agua
ISO 9459-2 — Sistemas de calentamiento de agua solar

Cita
Si utilizás este software en tu investigación, por favor citá:
```
Creus, M. (2025). TermoStrat-1D: Simulador de Estratificación Térmica
en Termotanques Domiciliarios compatible con EnergyPlus WaterHeater:Stratified
[Software]. SISEDlab, Facultad de Arquitectura y Urbanismo,
Universidad Nacional de La Plata. GNU AGPL v3.0.
https://github.com/tu-usuario/termostrat-ep
```
Con DOI de Zenodo (reemplazar con el DOI real una vez generado):
```
Creus, M. (2025). TermoStrat-EP v1.0 [Software].
Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX
```
---
Autoría
Mariano Creus  
Laboratorio de Sistemas Edilicios — SISEDlab  
Facultad de Arquitectura y Urbanismo (FAU)  
Universidad Nacional de La Plata (UNLP)  
La Plata, Buenos Aires, Argentina  
📧 mcreus@fau.unlp.edu.ar
---
Licencia
Copyright © 2025 Mariano Creus — SISEDlab, FAU-UNLP
Este programa es software libre: podés redistribuirlo y/o modificarlo
bajo los términos de la GNU Affero General Public License publicada
por la Free Software Foundation, versión 3 de la Licencia.
Este programa se distribuye con la esperanza de que sea útil,
pero SIN NINGUNA GARANTÍA. Ver la GNU AGPL v3.0 para más detalles.
🔗 https://www.gnu.org/licenses/agpl-3.0
