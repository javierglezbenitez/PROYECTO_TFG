# 📊 Resultados

## 🗺️ Niveles turísticos por municipio

Los mapas muestran la distribución geoespacial de los niveles turísticos detectados mediante clustering HDBSCAN en cada isla del archipiélago canario. La determinación del nivel turístico por municipio se realiza posteriormente mediante la media del nivel de los clústeres que se encuentran en cada municipio.

| Color | Nivel | Descripción |
|-------|-------|-------------|
| 🟦 | Nivel 1 | Turismo Muy Bajo — < 25% fotos de turistas |
| 🟨 | Nivel 2 | Turismo Bajo — 25–50% fotos de turistas |
| 🟧 | Nivel 3 | Turismo Alto — 50–75% fotos de turistas |
| 🟥 | Nivel 4 | Turismo Muy Alto — > 75% fotos de turistas |

---

### Gran Canaria

![Mapa Gran Canaria](/results/niveles_turisticos_hdbscan_Gran_canaria.png)

---

### Tenerife

![Mapa Tenerife](/results/niveles_turisticos_hdbscan_tenerife.png)

---

### Lanzarote

![Mapa Lanzarote](/results/niveles_turisticos_hdbscan_lanzarote.png)

---

### Fuerteventura

![Mapa Fuerteventura](/results/niveles_turisticos_hdbscan_fuerteventura.png)

---

### La Palma

![Mapa La Palma](/results/niveles_turisticos_hdbscan_La_Palma.png)

---

### La Gomera y El Hierro

![Mapa La Gomera](/results/niveles_turisticos_hdbscan_gomera_hierro.png)

---


## 🤖 Agente conversacional — Casos de uso

El agente es accesible desde Telegram y genera recomendaciones turísticas personalizadas en lenguaje natural. Dispone de dos ambientes de recomendación.

---

### Ambiente Estándar

> El agente recomienda municipios en función del nivel de intención turística expresado por el usuario. Un turista recibe destinos con alta presencia turística; un local recibe sitios poco masificados.

![Conversación ambiente estándar — inicio](/results/introduccion_agente.png)

---

> 👤 *" Hola, me llamo Carla, soy local de Gran Canaria y vivo en Agaete, quiero visitar sitios muy locales, poco turísticos, de toda la vida. "*


![Conversación ambiente estándar — recomendación](/results/munciipio_recomendado.png)

---

> # Se otorga información relevante acerca del municipio.

![Conversación ambiente estándar — información contextual](/results/recomendaciones_municipio.png)

---

> # Se recomienda otros municipios con el mismo nivel turístico o similar al recomendado principalmente.

![Otros municipios ambiente estándarl](/results/recomienda_otros_municipios.png)

---

> # Finalmente el agente almacena automáticamente toda la información de la consulta en la base de datos.

![Otros municipios ambiente estándarl](/results/base_datos.png)

---

### Ambiente Auténtico

> El agente invierte la lógica: un local recibe recomendaciones turísticas (Nivel 4) para descubrir su isla como visitante; un turista recibe experiencias locales (Nivel 1) para vivir la isla como un canario más. Mismo flujo de conversación que "Ambiente Estándar".

---

> 👤 *" Me llamo Andrés, soy turista y vengo de Valencia, estoy en Lanzarote y quiero sentirme como un canario más, conocer la isla desde dentro y su vida cotidiana. "*


![Conversación ambiente auténtico — inicio](/results/autentico_muni_recomendado.png)

---

> # Información relevante del municipio.

![Conversación ambiente auténtico — recomendación](/results/recomendaciones_municipio_autentico.png)

---

> # Otros municipios.

![Conversación ambiente auténtico — información contextual](/results/otros_municipios_autnetico.png)

---

> # Información de la consulta en la base de datos.

![Conversación ambiente auténtico — información contextual](/results/otros_municipios_autnetico.png)

