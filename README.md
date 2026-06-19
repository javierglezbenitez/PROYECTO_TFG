# 🏝️ Canarian Tourist Intelligence — TFG ULPGC 2026

> **Análisis de puntos de interés turístico en Canarias mediante clustering geoespacial y agente conversacional con LLM**

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![ULPGC](https://img.shields.io/badge/TFG-ULPGC%202026-orange)](https://www.ulpgc.es)
[![Methodology](https://img.shields.io/badge/Methodology-CRISP--DM-blueviolet)]()

---

## 📌 Descripción

Pipeline completo de Data Science aplicado al turismo en Canarias.
A partir de fotografías geolocalizadas extraídas de la **API de Flickr**, el sistema:

1. **Clasifica usuarios** en turistas y locales mediante criterios espaciales, temporales y de comportamiento
2. **Detecta zonas de interés turístico** aplicando y comparando cuatro algoritmos de clustering geoespacial
3. **Asigna un nivel turístico (1–4)** a cada uno de los municipios del archipiélago canario
4. **Expone los resultados** a través de una API REST
5. **Genera recomendaciones personalizadas** mediante un agente conversacional accesible desde Telegram

---

## 🏗️ Arquitectura del sistema

```
Flickr API
    │
    ▼
┌─────────────────────┐
│  Extracción de datos │  ← Descarga paralelizada por islas · YAML reproducible
│  (JSON por isla/mes) │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Clasificación        │  ← Espacial · Temporal · Volumen · Movilidad · Popularidad
│ Local / Turista      │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Clustering espacial  │  ← K-Means · GMM · DBSCAN · HDBSCAN ✓ (ganador)
│ (comparativa 4 alg.) │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Nivel turístico      │  ← Escala 1–4 por municipio
│ por municipio        │
└─────────┬───────────┘
          │
    ┌─────┴──────┐
    ▼            ▼
┌────────┐  ┌──────────────────────┐
│API REST│  │ Agente IA en Telegram │  ← LLM + MCP Tools + SQLite
└────────┘  └──────────────────────┘
```

---

## 🔬 Comparativa de algoritmos de clustering

| Algoritmo | Nº clusters | Ruido (%) | Radio r90 mediana (m) | Cobertura |
|-----------|-------------|-----------|----------------------|-----------|
| K-Means   | 25          | 0%        | 364.000              | 100%      |
| GMM       | 12          | 0%        | 251.000              | 100%      |
| DBSCAN    | 174         | 15%       | 284.000              | 85%       |
| **HDBSCAN ✓** | **292** | **31%**   | **237.000**          | **69%**   |

**¿Por qué HDBSCAN?**
- Mayor **granularidad espacial**: 292 clusters vs 12–25 de K-Means/GMM
- **Radio más compacto**: clusters más precisos y representativos
- **Filtro de calidad nativo**: el 31% de ruido elimina fotos erráticas sin forzar cobertura total, garantizando clusters puros

---

## 🤖 Sistema de recomendación inteligente

El agente combina cuatro componentes:

| Componente | Función |
|------------|---------|
| **Agent Core (LLM)** | Gestión del contexto, clasificación de intención, identificación del perfil del usuario |
| **Base de datos SQLite** | Almacena perfil, nivel de intención, municipios recomendados y historial |
| **Herramientas MCP** | Datos turísticos por isla/municipio, clima actual, selección de recomendaciones |
| **Interfaz Telegram** | Bot conversacional en lenguaje natural |

### Ambientes del recomendador

- **Ambiente Estándar**: recomienda según el nivel de intención turística expresado por el usuario (escala 1–4)
- **Ambiente Auténtico**: invierte la lógica — un local recibe recomendaciones turísticas (nivel 4) y un turista recibe experiencias locales (nivel 1)

---

## 🗺️ Resultados — Niveles turísticos por municipio

📂 [Ver mapas por isla y casos de uso del agente →](/results/results.md)
---

## 🌐 API REST

Base URL: `http://localhost:8000`

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/islas` | Lista todas las islas |
| GET | `/islas/{isla}` | Datos de una isla |
| GET | `/islas/{isla}/{municipio}` | Datos completos de un municipio |
| GET | `/islas/{isla}/nivel/{n}` | Municipios filtrados por nivel turístico |
| GET | `/all` | Todos los datos del archipiélago |

**Ejemplo de respuesta:**
```json
{
  "Firgas": {
    "nivel_turistico": 2,
    "n_clusters": 3,
    "n_fotos_turistico": 207,
    "n_fotos_local": 96,
    "alojamientos": [...],
    "restaurantes": [...],
    "playas": []
  }
}
```

---

## 🛠️ Stack tecnológico

| Categoría | Tecnologías |
|-----------|-------------|
| Lenguaje | Python 3.10+ |
| Datos y análisis | pandas, NumPy, Flickr API |
| Clustering | scikit-learn (K-Means, GMM, DBSCAN), hdbscan |
| Geoespacial | QGIS, Folium, GeoPandas |
| Visualización | Matplotlib, Seaborn, Plotly |
| API | FastAPI / Flask |
| Agente IA | LLM (Groq API), MCP Tools, Prompt Engineering |
| Mensajería | Telegram Bot API |
| Base de datos | SQLite |
| Config | YAML |

---

## 📊 Metodología

El proyecto sigue la metodología **CRISP-DM** en 6 fases:

1. **Comprensión del negocio** — análisis del sector turístico en Canarias
2. **Comprensión de los datos** — exploración de la API de Flickr y metadatos disponibles
3. **Preparación de los datos** — limpieza, clasificación local/turista, ingeniería de características
4. **Modelado** — comparativa de 4 algoritmos de clustering geoespacial
5. **Evaluación** — selección de HDBSCAN como algoritmo óptimo
6. **Implementación** — API REST + agente conversacional en Telegram

---

## ⚠️ Limitaciones conocidas

- **Declive de Flickr**: datos más escasos desde 2024, menor representatividad reciente
- **Clasificador basado en reglas**: pesos asignados manualmente, introduciendo cierta subjetividad
- **Límites de velocidad**: uso de la API gratuita de Groq impone restricciones de respuesta

---

## 🔭 Líneas futuras

- Integrar fuentes adicionales: Instagram, Google Maps, TripAdvisor
- Sustituir el clasificador manual por un modelo supervisado con datos etiquetados
- Añadir memoria persistente al agente entre sesiones
- Escalar la metodología a otros destinos: Baleares, Andalucía

---

## 👤 Autor

**Javier González Benítez**
Data Scientist & Engineer · ULPGC 2026

[![LinkedIn](https://img.shields.io/badge/LinkedIn-javiergonzalez--benitez-blue?logo=linkedin)](https://www.linkedin.com/in/javier-gonzalez-benitez-78052838b)
[![Email](https://img.shields.io/badge/Email-javierglezbenitez@gmail.com-red?logo=gmail)](mailto:javierglezbenitez@gmail.com)

---

