# Orien chatbot
To openfarma from quantit.

## Overview
The chatbot presented in this project aims sellers with information about cosmetic products. The main idea is to create a chat enviroment where sellers could consult, through a retrieval tool called RAG (Retrieval Augmentated Generation), technical information about cosmetic products. The following cosmetic brands are included:
- Cepage
- Cetaphil
- Eucerin
- Eximia
- Isdin
- La Roche-Posay
- L'Oreal
- Revlon
- Vichy

## Directory Structure
```
root/
├── database/
├── figures/
├── json/
├── logs/
├── requirements
├── run/
├── src/
├── .streamlit/
├── main.py
├── requirements.txt
└── README.md
```

## Instalación de paquetes
Los paquetes necessarios se encuentran listados en el archivo *requirements.txt*.
- Crear el entorno virtual: `python3.10 -m venv venv`
- Activar el entorno virtual: `source venv/bin/activate`
- Upgrade pip: `python3.10 -m pip install --upgrade pip`
- Instalar paquetes desde *requirements.txt*: `pip install -r requirements.txt`
- Desinstalar todos los paquetes: `pip freeze | xargs pip uninstall -y`
- Desactivar el entorno virtual: `deactivate`
- Eliminar le entorno virtual (opcional): `rm -rf venv`

En caso que si versión de Python no sea la 3.10, reemplazar con la versión correspondiente (revisar la versión instalada en su dispositivo). Sin embargo, debido a compatibilidades del resto de las librerías (ver archivo *requirements.txt*).

Si se desea correr el chatbot de forma local mediante `streamlit run main.py`, se debe instalar el entorno virtual con los requerimientos `requirements/requirements_local.txt`. El archivo `requirements.txt` en el directorio raiz se usa para el servidor de Streamlit.
