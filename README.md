# en-la-nube

Piezas de identidad de **Wasiluk Yasinsky & Asociados**.

| Carpeta | Qué hay |
|---|---|
| `tarjeta/` | Tarjeta virtual (`index.html`, lista para subir a wayauy.com/tarjeta/), vista previa `tarjeta.png` y un contacto `.vcf` por persona |
| `membrete/` | `Hoja membretada.docx` en blanco y `Presupuesto (modelo).docx`, con sus PDF de muestra |
| `herramientas/` | Generadores. Los datos del estudio están en `datos.py`: se cambian ahí y se regenera |

```bash
pip install segno python-docx
python3 herramientas/tarjeta.py
python3 herramientas/membrete.py
```
