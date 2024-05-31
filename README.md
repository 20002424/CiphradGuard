
# CiphraGuard 🤖 Documentación

## Tabla de Contenidos
- [Requisitos](#requisitos)
- [Librerías Utilizadas](#librerías-utilizadas)
- [Uso](#uso)
- [Proceso](#proceso)
  - [Descripción General](#descripción-general)
  - [Paso 1: Importaciones y Configuración](#paso-1-importaciones-y-configuración)
  - [Paso 2: Cargar Modelos y Definir Variables](#paso-2-cargar-modelos-y-definir-variables)
  - [Paso 3: Autenticación](#paso-3-autenticación)
  - [Paso 4: Interfaz de Usuario](#paso-4-interfaz-de-usuario)
  - [Página Principal](#página-principal)
  - [Paso 5: Entrada de Características y Preprocesamiento](#paso-5-entrada-de-características-y-preprocesamiento)
  - [Paso 6: Predicción y Visualización](#paso-6-predicción-y-visualización)
  - [Paso 7: Control del Flujo de la Interfaz](#paso-7-control-del-flujo-de-la-interfaz)

## Requisitos

- Python 3.9
- Streamlit
- TensorFlow
- Numpy
- Pickle
- Warnings
- Plotly

## Librerías Utilizadas

- **Streamlit**: Para crear la interfaz de la aplicación web.
- **TensorFlow**: Para cargar y utilizar el modelo CNN preentrenado.
- **Numpy**: Para manejar matrices y operaciones numéricas.
- **Pickle**: Para cargar los modelos PCA y escalador preentrenados.
- **Warnings**: Para suprimir advertencias innecesarias.
- **Plotly**: Para crear visualizaciones interactivas.

## Uso

Para ejecutar la aplicación, ejecute el siguiente comando en su terminal:

```bash
streamlit run app.py
```
## Descripción General

La aplicación CiphraGuard es una herramienta para la predicción de clases de peticiones utilizando un modelo de red neuronal convolucional (CNN). Los usuarios deben autenticarse para acceder a la funcionalidad principal, donde ingresan características específicas de la petición para obtener una predicción sobre si la petición es maliciosa y de qué tipo (por ejemplo, Ransomware, Spyware, Trojan). La aplicación también proporciona una visualización de las probabilidades de cada clase utilizando gráficos interactivos.

### Paso 1: Importaciones y Configuración

Primero, se importan las librerías necesarias y se configuran ciertos parámetros, como desactivar advertencias innecesarias y definir las credenciales de usuario. También se establece el título de la página de la aplicación.

### Paso 2: Cargar Modelos y Definir Variables

Se carga el modelo CNN preentrenado usando TensorFlow. Además, se define un diccionario que mapea nombres de variables a sus tipos de datos correspondientes, lo que facilita la entrada de datos por parte del usuario.

### Paso 3: Autenticación

Se define una función de autenticación para validar las credenciales del usuario. Se inicializa el estado de la sesión para controlar si el usuario ha iniciado sesión.

### Paso 4: Interfaz de Usuario

Se crea una página de inicio de sesión donde los usuarios deben ingresar su nombre de usuario y contraseña. Si las credenciales son correctas, se actualiza el estado de la sesión para indicar que el usuario ha iniciado sesión correctamente.

### Página Principal

Si el usuario está autenticado, se muestra la página principal de la aplicación. Aquí, los usuarios ingresan las características de la petición que desean analizar. Se recopilan las entradas del usuario, se convierten a una matriz NumPy y se procesan utilizando PCA y un escalador previamente entrenados.

### Paso 5: Entrada de Características y Preprocesamiento

Los usuarios ingresan las características de la petición, que se convierten en una matriz y se transforman utilizando PCA y un escalador. Estas características preprocesadas se preparan para la predicción.

### Paso 6: Predicción y Visualización

Cuando el usuario presiona el botón de predicción, el modelo CNN realiza una predicción basada en las características preprocesadas. Se determina la clase predicha y se muestran las probabilidades de cada clase. Los resultados se visualizan utilizando un gráfico interactivo creado con Plotly.

### Paso 7: Control del Flujo de la Interfaz

Dependiendo del estado de inicio de sesión del usuario, se muestra la página de inicio de sesión o la página principal de la aplicación. Esto asegura que solo los usuarios autenticados puedan acceder a la funcionalidad principal de la aplicación.
