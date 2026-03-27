from google import genai
from google.genai import types
import os

class ADKClient:
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("La variable de entorno GOOGLE_API_KEY no está configurada.")
        self.client = genai.Client(api_key=api_key)

    def diagnose_ticket(self, ticket_text, tool_config=None, images=None):
        try:
            # ----------------------------------------------------------------------
            # 1. CONTEXTO Y PROMPT
            # ----------------------------------------------------------------------
            base_prompt = f"""
<!-- ROL -->
Actuando como experto en UI/UX y Desarrollador Front-End, analiza cuidadosamente el ticket recibido.

<!-- CONTEXTO -->
Genera el código HTML, CSS, JavaScript utilizando únicamente Bootstrap 4.x. Respeta los colores, tamaños, dimensiones, tipos de letra y distribución de los contenidos. Utiliza las variables CSS en donde sea necesario, los contenedores principales deben ser responsivos, con base a las siguientes referencias:

<!-- CARACTERÍSTICAS TÉCNICAS -->
--color-primary: #15438A;
--color-secondary: #3366CC;
--color-tertiary: #EBF4FF;
--color-text: #4B4B4B;
--color-gray-light: #F2F2F2;

<!-- NOTAS IMPORTANTES -->
- Tamaño base para los textos es 16px, para los demás tamaños usar medidas en "em" y "rem".
- Usar componentes de Bootstrap cuando sea necesario, como tabs, acordeones.
- Las rutas para las imágenes de contenido y de fondo se pueden dejar relativas para complementarlas después, con el siguiente formato y tamaño más cercano:
	- Grandes: /info/santander_se/media/galeria/thumbs/thgaleria_1400X920_11235.webp
	- Medianas: /info/santander_se/media/galeria/thumbs/thgaleria_1200X400_11235.webp
	- Pequeñas: /info/santander_se/media/galeria/thumbs/thgaleria_400X400_11235.webp
- Para los íconos usa imágenes como referencia, no fuente ni SVG.
- Usar encabezados con etiquetas desde el h2, h3, h4, h5 y h6.
- No es necesario el html completo (etiquetas <head> <body>), es para agregar dentro de una publicación.
- Sin funciones flecha.
- Lenguaje PHP y jQuery si se requiere.
- No se crean nodos repetidos, solo se mueven.
- Indentación con tabs, no espacios.

<!-- CLASIFICACIÓN DEL TICKET -->
Analiza el ticket y clasifícalo según:
- Incidente (type_id: 10): Falla o error en UI existente
- Petición (type_id: 14): Modificación de componente existente
- Requerimiento (type_id: 19): Nuevo componente o funcionalidad

<!-- PROTOCOLO DE ANÁLISIS VISUAL (PRIORITARIO) -->
Si se proporcionan imágenes con ANOTACIONES VISUALES (recuadros de colores), DEBES ESTRUCTURAR EL CONTENIDO SEGÚN LAS SIGUIENTES REGLAS.
El tipo de bloque está determinado por el color del borde (±5 RGB):
- **Amarillo (#FFF200)** -> `bloqueEditor`
- **Azul (#0023F5)** -> `bloqueLayout`
- **Cian (#00FFFF)** -> `bloqueDynamic`

GENERA UN ARRAY DE OBJETOS JSON para cada bloque encontrado, usando estas plantillas:

### 1. Bloque Editor (Amarillo)
{{
	"id": [CONSECUTIVO],
	"modulo": "Bloques",
	"bloque": "bloqueEditor",
	"titulo": "[TITULO_EXTRAIDO]",
	"titulo_visible": 0,
	"titulo_icono": "",
	"posicion": "1",
	"disenno": "1",
	"comunidad": "portal",
	"idCliente": 11,
	"orden": 43,
	"estado": "A",
	"contenido": "{{\\"viewTitulo\\": null, \\"viewEditor\\": \\"N\\", \\"mediaBack\\": \\"\\", \\"parallax\\": \\"0\\", \\"informacion\\": \\"[CONTENIDO_HTML_DEL_TEXTO_EXACTO]\\", \\"block_visibility\\": \\"-1\\", \\"textoAyuda\\": \\"\\", \\"urlAyuda\\": \\"\\", \\"clases_contenedor\\": \\"uSlider\\", \\"effects\\": null}}",
	"cache": null
}}

### 2. Bloque Layout (Azul)
La cantidad de items en 'items' corresponde a las columnas visuales. size.lg/md/sm/xs deben sumar 12 o ser consistentes con Bootstrap.
{{
	"id": [CONSECUTIVO],
	"modulo": "Bloques",
	"bloque": "bloqueLayout",
	"titulo": "[TITULO_EXTRAIDO]",
	"titulo_visible": 0,
	"titulo_icono": "",
	"posicion": "1",
	"disenno": "1",
	"comunidad": "portal",
	"idCliente": 11,
	"orden": 43,
	"estado": "A",
	"contenido": "{{\\"items\\": [{{\\"customCss\\": \\"\\", \\"align\\": \\"\\", \\"size\\": {{\\"lg\\": \\"[TAMAÑO_COLUMNA]\\", \\"md\\": \\"[TAMAÑO_COLUMNA]\\", \\"sm\\": \\"[TAMAÑO_COLUMNA]\\", \\"xs\\": \\"[TAMAÑO_COLUMNA]\\"}} , \\"display\\": {{\\"lg\\": \\"1\\", \\"md\\": \\"1\\", \\"sm\\": \\"1\\", \\"xs\\": \\"1\\"}}, \\"offset\\": {{\\"lg\\": \\"\\", \\"md\\": \\"\\", \\"sm\\": \\"\\", \\"xs\\": \\"\\"}}, \\"txtAlign\\": \\"\\"}} ]}}",
	"cache": null
}}

### 3. Bloque Dynamic (Cian)
{{
	"id": [CONSECUTIVO],
	"modulo": "Bloques",
	"bloque": "bloqueDynamic",
	"titulo": "[TITULO_EXTRAIDO]",
	"titulo_visible": 0,
	"titulo_icono": "",
	"posicion": "1",
	"disenno": "1",
	"comunidad": "portal",
	"idCliente": 11,
	"orden": 43,
	"estado": "A",
	"contenido": "{{\\"rows\\": [{{\\"title\\": \\"[TITULO_ITEM]\\", \\"title_visible\\": 1, \\"description\\": \\"[DESCRIPCION_ITEM]\\", \\"media\\": \\"227\\", \\"icon\\": \\"[CLASE_FONTAWESOME]\\", \\"linkType\\": \\"\\", \\"linkValue\\": \\"#\\", \\"date\\": \\"\\", \\"classcss\\": \\"\\", \\"html\\": \\"\\", \\"position\\": \\"\\", \\"imgAdjust\\": \\"0\\", \\"effects\\": {{\\"title\\": \\"\\", \\"description\\": \\"\\", \\"image\\": \\"\\"}} }}], \\"rowsLink\\": [], \\"viewtype\\": null, \\"typeContent\\": null, \\"dataSource\\": \\"manual\\", \\"layoutType\\": \\"layout2\\", \\"layout\\": {{\\"layoutRows\\": \\"[COUNT_ROWS]\\", \\"layoutColumns\\": \\"[COUNT_COLS]\\", \\"layoutScroll\\": \\"1\\", \\"layoutControls\\": \\"true\\", \\"layoutBullets\\": \\"bullets\\", \\"layoutAutoplay\\": \\"true\\", \\"layoutSpeed\\": \\"5\\", \\"layoutDirection\\": \\"horizontal\\"}} , \\"block_visibility\\": \\"-1\\", \\"textoAyuda\\": \\"\\", \\"urlAyuda\\": \\"\\", \\"clases_contenedor\\": \\"slider_iconos\\", \\"effects\\": {{\\"title\\": [\\"\\", \\"\\", \\"\\", \\"\\"], \\"description\\": [\\"\\", \\"\\", \\"\\", \\"\\"], \\"image\\": [\\"\\", \\"\\", \\"\\", \\"\\"], \\"hover\\": \\"\\", \\"parallax\\": {{\\"enabled\\": \\"0\\", \\"image\\": \\"\\"}}}}}}",
	"cache": null
}}

### REGLAS IMPORTANTES:
1. "contenido" SIEMPRE es un string JSON escapado. Escapa comillas dobles dentro de él con backslash (\\).
2. No agregues texto extra.
3. Si hay múltiples bloques, pon todos en un mismo array.

<!-- FORMATO DE SALIDA (ESTRICTO JSON) -->
{{
  "type_id": 10|14|19,
  "diagnostico": [ARRAY_DE_OBJETOS_JSON_GENERADOS] O "String con código HTML/CSS si no hay análisis visual"
}}

<!-- TICKET A ANALIZAR -->
{ticket_text}
"""

            # ----------------------------------------------------------------------
            # 2. CONSTRUCCIÓN DEL CONTENIDO (TEXTO + IMÁGENES)
            # ----------------------------------------------------------------------
            contents = [base_prompt]
            
            if images:
                for img in images:
                    # img debe ser un dict: {'mime_type': '...', 'data': bytes}
                    part = types.Part.from_bytes(data=img['data'], mime_type=img['mime_type'])
                    contents.append(part)

            # ----------------------------------------------------------------------
            # 3. LLAMADA A LA API CON TOOLS
            # ----------------------------------------------------------------------
            
            # Configuración de herramientas
            tools = []
            if tool_config:
                if isinstance(tool_config, list):
                    tools.extend(tool_config)
                else:
                    tools.append(tool_config)

            response = self.client.models.generate_content(
                model="gemini-2.0-flash",
                contents=contents,
                config=types.GenerateContentConfig( 
                    thinking_config=types.ThinkingConfig(thinking_budget=0),
                    temperature=0.1,
                    tools=tools,
                    response_mime_type="application/json"
                )
            )
            print("🔍 Respuesta cruda:", response)
            return response.text
                

        except Exception as e:
            print(f" Error en diagnose_ticket: {e}")
            return ""