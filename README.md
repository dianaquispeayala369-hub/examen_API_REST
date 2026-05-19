# examen_API_REST

1. Creando carpeta y clonando repositorio

```bash
git config --global user.name "dianaquispeayala369-hub"
git config --global user.email "dianaquispeayala369@gmail.com"
# Clonando el proyecto
git clone https://github.com/dianaquispeayala369-hub/examen_API_REST.git
```
1.1 Abriendo Visual studio Code

```bash
cd examen_API_REST/
code .
```
1.2 uv gestor de paquetes

```bash
uv --version  # para ver la version actual uv
uv --help     #para ver el contenido del gestor uv

uv init       # inicializando el entorno
```
2. Configuracion del entorno

```bash
python -m venv .venv.

# Activando en git bash
source .venv/Scripts/activate
```
3. Instalar los modulos necesarios

```bash
pip install flask jinja2
```
4. Ejecutar API

```bash
python main.py
```