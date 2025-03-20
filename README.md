# nombres-arg: Nombres y Apellidos de Argentina

Colección de nombres históricos de Argentina, basado en los siguientes datasets del repositorio de datos público [Datos Argentina](https://www.datos.gob.ar/):
1) [Histórico de nombres](https://www.datos.gob.ar/dataset/otros-nombres-personas-fisicas/archivo/otros_2.1), perteneciente al recurso [Nombres de personas físicas](https://www.datos.gob.ar/dataset/otros-nombres-personas-fisicas). Fecha de última actualización: 27-Julio-2017

2) [Personas por apellido por provincia](https://datos.gob.ar/dataset/renaper-distribucion-apellidos-argentina/archivo/renaper_2.3), perteneciente al recurso [Distribución de apellidos en Argentina](https://datos.gob.ar/dataset/renaper-distribucion-apellidos-argentina). Fecha de última actualización: 21-Agosto-2022.

La finalidad de este repositorio de datos es disponibilizar sin repeticiones los nombres y apellidos de personas físicas en Argentina.

Fecha de última actualización: 20-Marzo-2025.

PENDING TO DO:
- Thorough check of names and cleaning rules
- Remove all-number names and other cleaning rules
- Update data README file
- Fix execution issue, as currently the script runs with the following workaround: `PYTHONPATH=$(pwd) python scripts/preprocess_data.py`
- See if execution time can be further reduced
- Improve code comments
