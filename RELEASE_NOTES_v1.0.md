# TermoStrat-1D — Release Notes v1.0

## Versión inicial
Primera versión del simulador de estratificación térmica multi-nodo
para termotanques domiciliarios a gas, compatible con la formulación del objeto
`WaterHeater:Stratified` de EnergyPlus V26-1-0.

## Características implementadas
- Modelo 1-DIM multi-nodo (3–12 nodos) con integración numérica de Euler explícito
- Balance de energía por nodo: calefactor, pérdidas térmicas, conducción axial,
  advección y mezcla por inversión de densidad (InversionMixing)
- Control termostático con histéresis (setpoint + banda muerta)
- Perfil de consumo configurable por eventos (hora, duración, caudal)
- Perfiles predefinidos: sin consumo, familia 4 personas día típico, uso intensivo
- Verificación automática de estabilidad numérica (número de Fourier, Fo ≤ 0.5)
- Verificación del balance energético (error relativo < 1 %)
- Interfaz web interactiva desarrollada en Streamlit
- Visualizaciones: evolución temporal, mapa de estratificación térmica,
  análisis energético y perfil de consumo
- Exportación de resultados en formato CSV

## Parámetros configurables
- Geometría del tanque: volumen, altura, diámetro interior, diámetro tubo de
  gases, radio y altura del casquete esférico
- Número de nodos de estratificación (3–12)
- Propiedades físicas del agua: densidad, calor específico, conductividad térmica
- Aislamiento: espesor y conductividad del poliuretano rígido (PUR)
- Calefactor: potencia útil, temperatura de setpoint, banda muerta del termostato
- Condiciones iniciales: temperatura inicial, ambiente y agua de red
- Simulación temporal: paso de tiempo y duración total
- Coeficiente de mezcla por inversión de densidad

## Limitaciones conocidas
- Temperatura ambiente constante (sin variación climática horaria)
- Un único quemador a gas
- Sin modelado de pérdidas por tuberías externas

## Requisitos
- Python 3.10 o superior
- streamlit
- numpy
- pandas
- matplotlib

## Referencias
- EnergyPlus Engineering Reference, v26.1.0 — §19.3.3 Stratified Water Thermal Tank
- ASHRAE Standard 90.1 — Requisitos de eficiencia para calentadores de agua
- ISO 9459-2 — Sistemas de calentamiento de agua solar

## Licencia
GNU Affero General Public License v3.0 (AGPL v3.0)
https://www.gnu.org/licenses/agpl-3.0

## Autoría
Mariano Creus  
Laboratorio de Sistemas Edilicios — SISEDlab  
Facultad de Arquitectura y Urbanismo (FAU)  
Universidad Nacional de La Plata (UNLP)  
La Plata, Buenos Aires, Argentina  
mcreus@fau.unlp.edu.ar  

Copyright © 2025 Mariano Creus — SISEDlab. FAU-UNLP
