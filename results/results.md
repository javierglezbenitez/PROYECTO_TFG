# 📊 Resultados

## 🗺️ Niveles turísticos por municipio

Los mapas muestran la distribución geoespacial de los niveles turísticos detectados mediante clustering HDBSCAN en cada isla del archipiélago canario.

| Color | Nivel | Descripción |
|-------|-------|-------------|
| 🟦 | Nivel 1 | Turismo Muy Bajo — < 25% fotos de turistas |
| 🟨 | Nivel 2 | Turismo Bajo — 25–50% fotos de turistas |
| 🟧 | Nivel 3 | Turismo Alto — 50–75% fotos de turistas |
| 🟥 | Nivel 4 | Turismo Muy Alto — > 75% fotos de turistas |

---

### Gran Canaria

![Mapa Gran Canaria](results/mapa_gran_canaria.png)

---

### Tenerife

![Mapa Tenerife](results/mapa_tenerife.png)

---

### Lanzarote

![Mapa Lanzarote](results/mapa_lanzarote.png)

---

### Fuerteventura

![Mapa Fuerteventura](results/mapa_fuerteventura.png)

---

### La Palma

![Mapa La Palma](results/mapa_la_palma.png)

---

### La Gomera

![Mapa La Gomera](results/mapa_la_gomera.png)

---

### El Hierro

![Mapa El Hierro](results/mapa_el_hierro.png)

---

## 🤖 Agente conversacional — Casos de uso

El agente es accesible desde Telegram y genera recomendaciones turísticas personalizadas en lenguaje natural. Dispone de dos ambientes de recomendación.

---

### Ambiente Estándar

> El agente recomienda municipios en función del nivel de intención turística expresado por el usuario. Un turista recibe destinos con alta presencia turística; un local recibe sitios poco masificados.

![Conversación ambiente estándar — inicio](results/agente_estandar_1.png)

---

![Conversación ambiente estándar — recomendación](results/agente_estandar_2.png)

---

![Conversación ambiente estándar — información contextual](results/agente_estandar_3.png)

---

### Ambiente Auténtico

> El agente invierte la lógica: un local recibe recomendaciones turísticas (Nivel 4) para descubrir su isla como visitante; un turista recibe experiencias locales (Nivel 1) para vivir la isla como un canario más.

![Conversación ambiente auténtico — inicio](results/agente_autentico_1.png)

---

![Conversación ambiente auténtico — recomendación](results/agente_autentico_2.png)

---

![Conversación ambiente auténtico — información contextual](results/agente_autentico_3.png)
