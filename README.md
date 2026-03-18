# Horario

Genera un horario en LaTeX/PDF usando PyLaTeX.

## Estructura

- `scripts/generate_schedule.py` — script principal
- `src/schedule/helpers.py` — funciones auxiliares
- `data/input/` — archivos CSV de entrada
- `output/pdf/` — PDFs generados
- `output/tex/` — archivos `.tex` generados

## Uso

```bash
python scripts/generate_schedule.py
```

## Entradas

- `data/input/activities.csv`
- `data/input/schedules.csv`
- `data/input/user.csv`
