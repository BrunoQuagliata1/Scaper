### How to run:

#### Option 1

```
cd webcrawler
scrapy crawl full_site_spider -a start_url=http://eagerworks.com
```

#### Option 2

```
curl -X POST -H "Content-Type: application/json" -d '{"websiteUrl": "http://eagerworks.com"}' http://localhost:5001/link-website
```

### Implementación del Scraper

1. **Instalación y Configuración Inicial**

   - **Scrapy**: Un framework de scraping en Python que nos permite extraer datos de sitios web de manera eficiente.
   - **Flask**: Un microframework web de Python para manejar las solicitudes de URL y desencadenar el proceso de scraping.
   - **MongoDB**: Una base de datos NoSQL donde almacenamos los datos extraídos.

2. **Estructura del Proyecto**

   - **Directorio del Proyecto**: `scraper`
   - **Proyecto Scrapy**: `webcrawler`
   - **Spider de Scrapy**: `full_site_spider.py`
   - **Aplicación Flask**: `app.py`

3. **Código del Spider (full_site_spider.py)**

   - **Inicialización del Spider**: Configura las URL iniciales y el dominio permitido.
   - **Reglas de Extracción**: Usa `LinkExtractor` para seguir enlaces en el sitio web.
   - **Extracción y Procesamiento de Datos**: Utiliza BeautifulSoup para analizar el HTML y extraer solo el contenido principal, excluyendo elementos como navegaciones y pies de página.
   - **Almacenamiento en MongoDB**: Guarda el contenido extraído en una colección de MongoDB.

4. **Código de la Aplicación Flask (app.py)**
   - **Endpoint de Flask**: Define un endpoint `/link-website` que recibe una URL y desencadena el scraper.
   - **Subproceso para Scrapy**: Usa `subprocess.Popen` para ejecutar el spider de Scrapy desde la aplicación Flask.
   - **Manejo de Respuestas**: Devuelve mensajes de éxito o error basados en el resultado del scraping.

### Escalabilidad de la Solución

1. **Optimización del Scraping**:

   - **Concurrent Requests**: Configurar Scrapy para manejar múltiples solicitudes concurrentes.
   - **Politeness Policy**: Respetar el `robots.txt` de cada sitio y establecer un `DOWNLOAD_DELAY` para evitar sobrecargar el servidor.

2. **Procesamiento de Datos**:
   - **Limpieza de Datos**: Implementar técnicas adicionales de limpieza de datos para asegurar que solo se almacene información relevante.
   - **Normalización**: Normalizar los datos para un mejor manejo y consistencia en las consultas.
