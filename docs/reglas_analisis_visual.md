# Protocolo de Análisis Visual de Diseños UI

## Descripción General
La imagen contiene el diseño gráfico de un sitio web con diferentes tipos de bloques de contenido sin un orden específico. Cada rectángulo delimitador corresponde a un bloque de contenido. El **color del borde** de cada rectángulo indica el tipo de bloque que contiene.

## Colores y Tipos de Bloques a Analizar
Analizar únicamente los rectángulos con bordes de los siguientes colores (con tolerancia ±5 en valores RGB):
- **Rectángulo con borde #FFF200 (amarillo)**: Tipo de bloque `bloqueEditor`
- **Rectángulo con borde #0023F5 (azul)**: Tipo de bloque `bloqueLayout`
- **Rectángulo con borde #00FFFF (cian)**: Tipo de bloque `bloqueDynamic`

## Reglas de Detección y Clasificación
### Análisis Visual
1. Analiza **cuidadosamente** la imagen de arriba hacia abajo
2. Clasifica cada tipo de bloque **EXCLUSIVAMENTE** según el color del borde del rectángulo, ignorando:
   - Los colores de los elementos internos
   - Cualquier otro elemento visual

### Identificación de Contenido
3. Para cada bloque identificado, extrae:
   - **Título**: Texto principal o encabezado visible
   - **Descripción**: Breve resumen de los elementos que contiene
   - Si no hay título visible, genera uno descriptivo basado en los componentes que contiene

### Manejo de Bloques Anidados
4. Los bloques tipo `bloqueLayout` pueden contener otros bloques dentro
5. Cuando encuentres bloques anidados:
   - Incluye el bloque contenedor (`bloqueLayout`)
   - Incluye cada bloque anidado como objetos separados en el array de resultados

### Casos Especiales
6. **Contenido ilegible**: Si el contenido no es legible, usa "Contenido no legible" como título
7. **Bloques vacíos**: Si un bloque está vacío, usa "Bloque vacío" como título
8. **Texto puro en bloqueEditor**: Si el contenido es únicamente texto, incluye el texto completo en el campo `contenido_texto`
9. Ignora las zonas de contenido que no se encuentran dentro de un rectángulo con bordes de colores no especificados


## Grid System de Bootstrap
El Grid System de Bootstrap es un sistema de cuadrícula (rejilla) que permite crear diseños web responsivos de forma sencilla y estructurada. Está basado en flexbox y divide la página en 12 columnas por fila, permitiendo distribuir y alinear contenido de manera flexible según el tamaño de pantalla. Los bloques de tipo `bloqueLayout` se distribuyen utilizando este sistema
### ¿Cómo funciona?
- Contenedor (.container o .container-fluid)
Es el elemento base que encierra las filas y columnas del grid.
.container: tiene un ancho fijo según el tamaño de pantalla.
.container-fluid: ocupa el 100% del ancho de la pantalla.
- Fila (.row)
Dentro del contenedor se crean filas que agrupan columnas.
- Columnas (.col)
Las columnas se colocan dentro de una fila y deben sumar 12 unidades para ocupar todo el ancho disponible. Se pueden usar clases como: .col-1, .col-2, ..., .col-12
Responsivas: .col-sm-6, .col-md-4, .col-lg-3, etc.
### Ejemplo básico
<div class="container">
  <div class="row">
    <div class="col-4">Columna 1 (4 columnas)</div>
    <div class="col-4">Columna 2 (4 columnas)</div>
    <div class="col-4">Columna 3 (4 columnas)</div>
  </div>
</div>

## Formato de Salida Requerido
### Estructura JSON bloques de tipo `bloqueEditor`
Retorna un **objeto JSON** para cada uno de los los bloques encontrados de tipo `bloqueEditor`:
{
	"id": [IDENTIFICADOR_UNICO_DEL_BLOQUE_NUMERO_CONSECUTIVO],
	"modulo":"Bloques",
	"bloque": "[TIPO_DE_BLOQUE]",
	"titulo": "[TÍTULO_EXTRAÍDO_O_GENERADO]",
	"titulo_visible":0,
	"titulo_icono":"",
	"posicion":"1",
	"disenno":"1",
	"comunidad":"portal",
	"idCliente":11,
	"orden":43,
	"estado":"A",
	"contenido": "{
		"viewTitulo": null,
		"viewEditor": "N",
		"mediaBack": "",
		"parallax": "0",
		"informacion": "[CONTENIDO_HTML_DEL_TEXTO_EXACTO_ENCONTRADO_EN_EL_BLOQUE_SI_ES_DE_TIPO_BLOQUEDITOR]",
		"block_visibility": "-1",
		"textoAyuda": "",
		"urlAyuda": "",
		"clases_contenedor": "uSlider",
		"effects": null
	}",
	"cache":null
}

### Estructura JSON bloques de tipo `bloqueLayout`
Retorna un **objeto JSON** para cada uno de los bloques encontrados de tipo `bloqueLayout`. La cantidad de elementos dentro del campo `items` corresponde a la cantidad de columnas del layout:
{
	"id": [IDENTIFICADOR_UNICO_DEL_BLOQUE_NUMERO_CONSECUTIVO],
	"modulo":"Bloques",
	"bloque": "[TIPO_DE_BLOQUE]",
	"titulo": "[TÍTULO_EXTRAÍDO_O_GENERADO]",
	"titulo_visible":0,
	"titulo_icono":"",
	"posicion":"1",
	"disenno":"1",
	"comunidad":"portal",
	"idCliente":11,
	"orden":43,
	"estado":"A",
	"contenido": "{
		"items": [
		  {
			"customCss": "",
			"align": "",
			"size": {
			  "lg": "[AQUI_VA_EL_TAMAÑO_QUE_OCUPA_ESTA_COLUMNA_DENTRO_DE_SU_CONTENEDOR._LOS_VALORES_PUEDEN_SER_3,_6,_9_O_12_DEPENDIENDO_DE_SI_SE_ENCUENTRAN_4,_3,_2,_O_1_COLUMNAS]",
			  "md": "[AQUI_VA_EL_TAMAÑO_QUE_OCUPA_ESTA_COLUMNA_DENTRO_DE_SU_CONTENEDOR._LOS_VALORES_PUEDEN_SER_3,_6,_9_O_12_DEPENDIENDO_DE_SI_SE_ENCUENTRAN_4,_3,_2,_O_1_COLUMNAS]",
			  "sm": "[AQUI_VA_EL_TAMAÑO_QUE_OCUPA_ESTA_COLUMNA_DENTRO_DE_SU_CONTENEDOR._LOS_VALORES_PUEDEN_SER_3,_6,_9_O_12_DEPENDIENDO_DE_SI_SE_ENCUENTRAN_4,_3,_2,_O_1_COLUMNAS]",
			  "xs": "[AQUI_VA_EL_TAMAÑO_QUE_OCUPA_ESTA_COLUMNA_DENTRO_DE_SU_CONTENEDOR._LOS_VALORES_PUEDEN_SER_3,_6,_9_O_12_DEPENDIENDO_DE_SI_SE_ENCUENTRAN_4,_3,_2,_O_1_COLUMNAS]"
			},
			"display": {"lg": "1", "md": "1", "sm": "1", "xs": "1"},
			"offset": {"lg": "", "md": "", "sm": "", "xs": ""},
			"txtAlign": ""
		  }
	  ]
	}",
	"cache":null
}

### Estructura JSON bloques de tipo `bloqueDynamic`
Retorna un **objeto JSON** para cada uno de los bloques encontrados de tipo `bloqueDynamic`. Cada elemento dentro del campo `rows` corresponde a una columna del framework Bootstrap que contiene un titulo y un icono:
[
  {
	"id": [IDENTIFICADOR_UNICO_DEL_BLOQUE_NUMERO_CONSECUTIVO],
	"modulo":"Bloques",
    "bloque": "[TIPO_DE_BLOQUE]",
    "titulo": "[TÍTULO_EXTRAÍDO_O_GENERADO]",
	"titulo_visible":0,
	"titulo_icono":"",
	"posicion":"1",
	"disenno":"1",
	"comunidad":"portal",
	"idCliente":11,
	"orden":43,
	"estado":"A",
	"contenido": "{
		"rows": [
		  {
			"title": "[AQUI_VA_EL_TITULO_EXACTO_ENCONTRADO_DENTRO_DEL_ELEMENTO]", 
			"title_visible": 1,
			"description": "[AQUI_VA_LA_DESCRIPCION_EXACTA_ENCONTRADA_DENTRO_DEL_ELEMENTO]",
			"media": "227",
			"icon": "[AQUI_VAN_LAS_CLASES_CSS_CORRESPONDIENTES_A_LOS_ICONOS_DE_LA_LIBRERIA_FONT-AWESOME_SEGUN_EL_ICONO_ENCONTRADO_EN_EL_ELEMENTO]",
			"linkType": "",
			"linkValue": "#",
			"date": "",
			"classcss": "",
			"html": "",
			"position": "",
			"imgAdjust": "0",
			"effects": {"title": "", "description": "", "image": ""}
		  }
		],
		"rowsLink": [],
		"viewtype": null,
		"typeContent": null,
		"dataSource": "manual",
		"layoutType": "layout2",
		"layout": {
		  "layoutRows": "[AQUI_VA_LA_CANTIDAD_DE_FILAS_DE_ELEMENTOS_ENCONTRADOS_EN_ESTE_BLOQUE]",
		  "layoutColumns": "[AQUI_VA_LA_CANTIDAD_DE_COLUMNAS_ENCONTRADOS_EN_ESTE_BLOQUE]",
		  "layoutScroll": "1",
		  "layoutControls": "true",
		  "layoutBullets": "bullets",
		  "layoutAutoplay": "true",
		  "layoutSpeed": "5",
		  "layoutDirection": "horizontal"
		},
		"block_visibility": "-1",
		"textoAyuda": "",
		"urlAyuda": "",
		"clases_contenedor": "slider_iconos",
		"effects": {
		  "title": ["", "", "", ""],
		  "description": ["", "", "", ""],
		  "image": ["", "", "", ""],
		  "hover": "",
		  "parallax": {"enabled": "0", "image": ""}
		}
	}",
	"cache": null
  }
]

### Campos Obligatorios
- `bloque`: Uno de: `bloqueEditor`, `bloqueLayout`, `bloqueDynamic`
- `titulo`: Título exacto extraído

## Instrucciones de Procesamiento
### Restricciones Importantes
- Procesa **ÚNICAMENTE** rectángulos con bordes de los colores especificados
- El tipo de bloque está determinado **EXCLUSIVAMENTE** por el color del borde
- **NO** agregues explicaciones, comentarios, o texto adicional
- **NO** incluyas bloques con bordes de otros colores
- Extrae los textos **UNICAMENTE** como se encuentran en los elementos de cada bloque
- **Escapa con un backslash (\) todas las doble comillas (") que están dentro del elemento "contenido" de los objetos JSON**
- Cada objeto JSON debe estar en una sola línea en la respuesta final

### Validación de Colores
- Acepta variaciones de ±5 en valores RGB para cada componente de color
- Ejemplo: #FFF200 acepta variaciones desde #FAF000 hasta #FFF705

### Orden de Procesamiento
- Procesa bloques de arriba hacia abajo
- En caso de bloques al mismo nivel horizontal, procesa de izquierda a derecha
- Genera una cadena JSON con todas las indicaciones dadas
