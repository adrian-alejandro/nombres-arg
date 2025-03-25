# nombres-arg: Nombres y Apellidos de Argentina

## Overview

### ES:
Colección de nombres históricos de Argentina, basado en los siguientes datasets del repositorio de datos público [Datos Argentina](https://www.datos.gob.ar/):
1) [Histórico de nombres](https://www.datos.gob.ar/dataset/otros-nombres-personas-fisicas/archivo/otros_2.1), perteneciente al recurso [Nombres de personas físicas](https://www.datos.gob.ar/dataset/otros-nombres-personas-fisicas). Fecha de última actualización: 27-Julio-2017

2) [Personas por apellido por provincia](https://datos.gob.ar/dataset/renaper-distribucion-apellidos-argentina/archivo/renaper_2.3), perteneciente al recurso [Distribución de apellidos en Argentina](https://datos.gob.ar/dataset/renaper-distribucion-apellidos-argentina). Fecha de última actualización: 21-Agosto-2022.

La finalidad de este repositorio de datos es disponibilizar sin repeticiones los nombres y apellidos de personas físicas en Argentina.

### EN:
Collection of historical names from Argentina, based on the following datasets from the public data repository [Datos Argentina](https://www.datos.gob.ar/):
1) [Historical Names](https://www.datos.gob.ar/dataset/otros-nombres-personas-fisicas/archivo/otros_2.1), part of the [Names of Natural Persons](https://www.datos.gob.ar/dataset/otros-nombres-personas-fisicas) resource. Last updated: July 27, 2017

2) [People by Last Name by Province](https://datos.gob.ar/dataset/renaper-distribucion-apellidos-argentina/archivo/renaper_2.3), part of the [Distribution of Last Names in Argentina](https://datos.gob.ar/dataset/renaper-distribucion-apellidos-argentina) resource. Last updated: August 21, 2022.

The purpose of this data repository is to make the first and last names of individuals in Argentina available without repetition.

## Installation

There are multiple alternatives for installing this package.

### Install from PyPI (Recommended)
**nombres-arg** is available on [PyPI](https://pypi.org/project/nombres-arg). It can be installed via pip as follows:

```bash
pip install nombres-arg
```

### Install from GitHub (Latest Version)
```bash
pip install git+https://github.com/adrian-alejandro/nombres-arg.git
```

### Install locally from Source
```bash
git clone https://github.com/adrian-alejandro/nombres-arg.git
cd nombres-arg
pip install .
```

### Install in editable mode (for development)
In case you would like to modify the package:
```bash
pip install -e .
```

## Usage

It's easy to import the lists of names and lastnames:

```python
from nombres_arg import NAMES
```

or

```python
from nombres_arg import LASTNAMES
```

## Feedback and/or Contribution

Please feel free to reach out for feedback and/or to contribute, either e-email or by raising an issue in the [gitHub repo](https://github.com/adrian-alejandro/nombres-arg).
