# Air Quality

El objetivo de este proyecto consiste en realizar predicciones de la calidad del aire en espacios interiores. La obtención de los datos se realiza con un sensor BME680 y una Raspberry Pi 3a+. Estos datos son almacenados en Firebase, desde donde se extraen y se utilizan para entrenar al modelo predictivo. 

### Instalación

Primero descargar el repositirio de git:

```
git clone https://github.com/jegalanl/air-quality.git
```

Es recomendable utilizar un entorno virtual durante el desarollo del proyecto.
Para instalar las librerias, que están en el archivo requirements.txt, se tiene que ejecutar el siguiente comando:

```
pip3 install -r requirements.txt
```

## TODO
* Extraer la información de la base de datos
* Entrenar el modelo
* Hacer predicciones
* Controlar el error y mejorarlo

## Hecho con

* [Python]
* [Firebase]
