import os
from googleapiclient.discovery import build
from supabase import create_client, Client
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DE APIS (Ocultas para la nube)
# Usamos variables de entorno para que sea seguro en GitHub Actions
# ==========================================
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not YOUTUBE_API_KEY or not SUPABASE_URL:
    raise ValueError("Faltan las credenciales de API. Configura las variables de entorno.")

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# 2. LA BÓVEDA DE NICHOS (Extraídos de tus PDFs)
# Coste de búsqueda: 40 keywords x 100 puntos = 4.000 puntos de cuota.
# ==========================================
KEYWORDS_SEMILLA = [
    # 🇪🇸 NICHOS EN ESPAÑOL (49 palabras)
    "fondos soberanos inversión", "guerra de los chips", "startups que quebraron", 
    "tierras raras negocio", "aerolíneas que quebraron", "ciudades fantasma china", 
    "negocio transporte marítimo", "fondos de capital privado explicado", 
    "negocio de las farmacéuticas", "negocio centros de datos ia", 
    "crear agentes ia sin código", "power bi finanzas tutorial", 
    "cold email herramientas", "crear saas sin código", "automatizar videos con ia", 
    "modelo financiero excel tutorial", "automatizar ecommerce make", 
    "servidor casero autohospedaje", "ia para contratos legales", 
    "chatbot con tus documentos", "protocolos de longevidad", 
    "placas solares rentabilidad", "invertir bienes raíces comerciales", 
    "crear empresa en el extranjero", "invertir en relojes de lujo", 
    "impuestos criptomonedas estrategia", "terapia de testosterona", 
    "negocio cargadores coche eléctrico", "dropshipping alto ticket", 
    "compra de clínicas dentales", "ciberseguridad para pymes", 
    "subvenciones para empresas", "energía nuclear futuro", 
    "invertir en franquicias rentabilidad", "clonar voz con ia", "invertir en arte", 
    "automatización cadena de suministro", "gestión financiera para empresas", 
    "fraudes de seguros casos", "monetizar una api", "negocio del agua escasez", 
    "configurar crm para ventas", "cartera de dividendos crecientes", 
    "empresas de robótica futuro", "negocio de logística transporte", 
    "ia para agentes inmobiliarios", "espionaje industrial casos", 
    "accesibilidad web normativa", "invertir en hoteles boutique",

    # 🇺🇸 NICHOS EN INGLÉS (49 palabras)
    "sovereign wealth fund explained", "semiconductor war explained", 
    "startup failure case study", "rare earth minerals explained", 
    "airline bankruptcy explained", "china ghost cities explained", 
    "shipping industry explained", "private equity explained documentary", 
    "pharmaceutical industry explained", "data center boom explained", 
    "build ai agents no code", "power bi finance dashboard", 
    "cold email setup tutorial", "build saas no code", "ai video automation workflow", 
    "financial modeling tutorial excel", "make automation ecommerce", 
    "self hosting homelab tutorial", "ai legal document drafting", 
    "build rag chatbot tutorial", "longevity peptides explained", 
    "solar battery roi analysis", "real estate syndication explained", 
    "offshore company structure explained", "luxury watch investment", 
    "crypto tax strategy explained", "trt hormone optimization", 
    "ev charging business explained", "high ticket dropshipping", 
    "dental practice private equity", "cybersecurity for small business", 
    "government grants for business", "nuclear energy comeback explained", 
    "franchise business roi explained", "ai voice cloning tutorial", 
    "art investment explained", "supply chain automation case study", 
    "cash flow management business", "insurance fraud case study", 
    "monetize your api tutorial", "water scarcity economics explained", 
    "crm setup for agencies", "dividend growth investing strategy", 
    "robotics startups explained", "freight brokerage business explained", 
    "ai tools for realtors", "corporate espionage case study", 
    "web accessibility compliance tutorial", "boutique hotel investment"
]

# Límites para encontrar el "Factor MRV" (Ni gigantes inalcanzables, ni canales muertos)
MIN_SUBS = 1000
MAX_SUBS = 200000

def cazar_canales():
    canales_descubiertos = set()
    print(f"🕷️ Iniciando la Araña. Escaneando {len(KEYWORDS_SEMILLA)} nichos...")

    # FASE 1: Búsqueda
    for keyword in KEYWORDS_SEMILLA:
        try:
            request = youtube.search().list(
                q=keyword,
                part="snippet",
                type="video",
                maxResults=50,
                order="date", # Prioriza la frescura
                regionCode="US" # Ampliamos a mercado global para robar formatos
            )
            response = request.execute()
            
            for item in response.get('items', []):
                channel_id = item['snippet']['channelId']
                canales_descubiertos.add((channel_id, keyword))
        except Exception as e:
            print(f"⚠️ Error buscando '{keyword}': {e}")

    print(f"✅ Se han encontrado {len(canales_descubiertos)} canales potenciales. Iniciando filtrado en bloques...")

    # FASE 2: Extracción en bloques de 50 (Ahorro masivo de cuota)
    canales_lista = list(canales_descubiertos)
    canales_validos = 0
    
    for i in range(0, len(canales_lista), 50):
        bloque = canales_lista[i:i+50]
        ids_bloque = [canal[0] for canal in bloque]
        ids_string = ",".join(ids_bloque)
        
        try:
            req_canales = youtube.channels().list(
                part="statistics,snippet",
                id=ids_string
            )
            res_canales = req_canales.execute()
            
            # FASE 3: Inyección en Base de Datos
            for item in res_canales.get('items', []):
                stats = item.get('statistics', {})
                if 'subscriberCount' not in stats: continue
                    
                subs = int(stats['subscriberCount'])
                views = int(stats.get('viewCount', 0))
                video_count = int(stats.get('videoCount', 0))
                titulo = item['snippet']['title']
                channel_id = item['id']
                nicho_asignado = next(canal[1] for canal in bloque if canal[0] == channel_id)

                if MIN_SUBS <= subs <= MAX_SUBS:
                    guardar_en_bd(channel_id, titulo, nicho_asignado, subs, views, video_count)
                    canales_validos += 1
        except Exception as e:
            print(f"⚠️ Error procesando bloque de canales: {e}")

    print(f"🏁 Batida terminada. {canales_validos} canales guardados/actualizados hoy.")

def guardar_en_bd(channel_id, titulo, nicho, subs, views, video_count):
    datos = {
        "channel_id": channel_id,
        "titulo": titulo,
        "nicho": nicho,
        "subs": subs,
        "total_views": views,
        "video_count": video_count
    }
    try:
        supabase.table("canales").upsert(datos).execute()
    except Exception as e:
        pass # Silenciamos errores menores de inserción para mantener limpia la consola

if __name__ == "__main__":
    cazar_canales()
