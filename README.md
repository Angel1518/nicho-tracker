\# 🕷️ Nicho Tracker - YouTube Faceless DaaS (Data-as-a-Service)



Un motor de extracción y base de datos automatizada diseñado para descubrir, filtrar y almacenar canales de YouTube del ecosistema \*Faceless\*. El sistema utiliza la API oficial de YouTube para rastrear palabras clave semilla, aplicar filtros de rentabilidad (Suelo de visitas y Techo de suscriptores) y guardar los canales ganadores en una base de datos PostgreSQL.



Todo el proceso se ejecuta de forma autónoma en la nube (100% \*Serverless\*) mediante GitHub Actions.



\---



\## 🚀 Características Principales



\* \*\*Scraping Inteligente:\*\* Extrae canales masivamente agrupando peticiones (en bloques de 50) para maximizar la cuota gratuita diaria de la API de YouTube Data v3.

\* \*\*Filtro Anti-Basura:\*\* Ignora automáticamente canales gigantes inalcanzables o canales sin tracción, enfocándose solo en aquellos que cumplen el factor MRV (Mejorable, Reciente, Viral).

\* \*\*Base de Datos en Tiempo Real:\*\* Actualización y almacenamiento mediante `Upsert` en \*\*Supabase\*\*. Si el canal es nuevo, lo guarda; si ya existe, actualiza sus estadísticas.

\* \*\*Piloto Automático (Cronjob):\*\* Configurado vía GitHub Actions para ejecutarse silenciosamente todos los días a las 04:00 AM (CEST) sin necesidad de mantener equipos locales encendidos.



\---



\## 🛠️ Arquitectura y Stack Tecnológico



\* \*\*Lenguaje:\*\* Python 3.10

\* \*\*Cloud Computing:\*\* GitHub Actions (Ubuntu environment)

\* \*\*Base de Datos:\*\* Supabase (PostgreSQL)

\* \*\*APIs:\*\* Google Cloud (YouTube Data API v3)



\### Estructura del Proyecto



```text

nicho-tracker/

│

├── spider\_canales.py         # Script principal (La Araña)

├── requirements.txt          # Dependencias de Python

├── README.md                 # Documentación del proyecto

│

└── .github/

&#x20;   └── workflows/

&#x20;       └── automata.yml      # Configuración del Cronjob en GitHub

