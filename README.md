#  CI/CD Pipeline & Cloud Deployment para Web App en Flask
Descripción: Proyecto integrador de DevOps donde contenericé una aplicación web desarrollada en Python/Flask y automaticé su despliegue en la nube.

Arquitectura y Tecnologías:

Código: Python y Flask.

Contenerización: Docker (creación de Dockerfile optimizado).

CI/CD: GitHub Actions (Pipeline para build, push a Docker Hub y despliegue automático).

Cloud: AWS EC2 (Servidor Ubuntu con configuración de Security Groups y SSH).

El proceso: Cada vez que se hace un push a la rama principal, un workflow de GitHub Actions construye la nueva imagen, la sube al Container Registry y se conecta por SSH al servidor de AWS para desplegar la nueva versión sin tiempo de inactividad (Zero Downtime).
