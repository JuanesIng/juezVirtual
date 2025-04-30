#Plataforma de Programación Competitiva con Django + Judge0

Este proyecto es una API desarrollada con **Django REST Framework** que permite crear problemas de programación, evaluar soluciones usando **Judge0 vía RapidAPI**, y gestionar submissions con feedback automático.

---

## Características

- Crear problemas con descripción, inputs/outputs, y ejemplos.
- Añadir testcases (visibles y ocultos).
- Recibir submissions de usuarios.
- Evaluar código automáticamente usando Judge0.
- Base de datos PostgreSQL.
- Dockerizado para desarrollo simple.

---

##Requisitos

- Docker y Docker Compose
- RapidAPI key de [Judge0](https://rapidapi.com/judge0-official/api/judge0-ce/)

---

### 1. Clona el repositorio

```bash
git clone https://github.com/JuanesIng/juezVirtual.git
cd juezVirtual
