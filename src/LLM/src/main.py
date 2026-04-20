from src.LLM.src.db.db_manager import ensure_db
from src.LLM.src.telegram.telegram_bot import init_bot

def main():
    print("[MAIN] Creando base de datos…")
    ensure_db()

    print("[MAIN] Iniciando bot…")
    init_bot()

if __name__ == "__main__":
    main()


####FRASES#####

# AMBIENTE ESTANDAR

#NIVEL 1 --> Hola, me llamo Carla, soy local de Gran Canaria y vivo en Agaete, quiero visitar sitios muy locales, poco turísticos, de toda la vida.

#NIVEL 2 --> Me llamo Manuel, soy residente en Tenerife y vivo en Adeje, me apetece conocer otros municipios tranquilos y salir un poco de lo habitual

#NIVEL 3 --> Me llamo Panna, vengo de Berlín, estoy visitando Fuerteventura y busco lugares con ambiente pero que no estén masificados

#NIVEL 4 --> Hola, me llamo David, vengo de Madrid, estoy de vacaciones en Gran Canaria y quiero visitar zonas turísticas con buenas playas y servicios


# AMBIENTE AUTÉNTICO

#NIVEL 1 --> Me llamo Andres, soy turista y vengo de Valencia, estoy en Lanzarote y quiero sentirme como un canario más, conocer la isla desde dentro y su vida cotidiana

#NIVEL 4 --> Hola, me llamo María, soy local de Gran Canaria y vivo en Ingenio, pero esta vez quiero vivir la isla como un turista, conocer zonas más turísticas y hacer planes diferentes a los habituales