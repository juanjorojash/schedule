# Horario

Genera un horario en LaTeX/PDF usando PyLaTeX.

## Estructura

- `scripts/generar_horario.py` — script principal
- `src/horario/funciones.py` — funciones auxiliares
- `data/input/` — archivos CSV de entrada
- `output/pdf/` — PDFs generados
- `output/tex/` — archivos `.tex` generados

## Uso

```bash
python scripts/generar_horario.py
```

## Entradas

- `data/input/actividades.csv`
- `data/input/horarios.csv`
- `data/input/usuario.csv`
