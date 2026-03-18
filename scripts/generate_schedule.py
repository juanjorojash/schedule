from pathlib import Path
import sys

import pandas as pd
from pylatex import (
    Command,
    Document,
    HorizontalSpace,
    NewLine,
    Package,
    VerticalSpace,
    config,
)
from pylatex.base_classes import Environment
from pylatex.utils import NoEscape, bold, italic

BASE = Path(__file__).resolve().parents[1]
SRC = BASE / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from schedule import helpers as fun  # noqa: E402

DATA_DIR = BASE / "data" / "input"
OUTPUT_PDF_DIR = BASE / "output" / "pdf"
OUTPUT_TEX_DIR = BASE / "output" / "tex"


class Schedule(Environment):
    """Custom LaTeX environment for the schedule package."""

    _latex_name = "schedule"
    packages = [Package("schedule")]



def generate_schedule(user_df, activities_df, schedules_df):
    OUTPUT_PDF_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_TEX_DIR.mkdir(parents=True, exist_ok=True)

    config.active = config.Version1(row_heigth=1.5)
    geometry_options = {
        "left": "2mm",
        "right": "2mm",
        "top": "5mm",
        "bottom": "5mm",
    }
    doc = Document(
        documentclass="article",
        fontenc=None,
        inputenc=None,
        lmodern=False,
        textcomp=False,
        page_numbers=False,
        indent=True,
        document_options=["landscape", "12pt", "dvipsnames"],
        geometry_options=geometry_options,
    )
    doc.packages.append(Package(name="schedule", options=None))
    doc.packages.append(Package(name="fontawesome", options=None))
    doc.preamble.append(
        NoEscape(
            r"""
\makeatletter
\def\@M@week{{Lunes} {Martes} {Miércoles} {Jueves} {Viernes} {Saturday} {Sunday}}
\makeatother
"""
        )
    )
    doc.preamble.append(Command("CellHeight", "1.1cm"))
    doc.preamble.append(Command("CellWidth", "5cm"))
    doc.preamble.append(Command("TimeRange", NoEscape(r"7:30-19:00")))
    doc.preamble.append(Command("SubUnits", "30"))
    doc.preamble.append(Command("BeginOn", "Monday"))
    doc.preamble.append(Command("TextSize", NoEscape(r"\small")))
    doc.preamble.append(Command("FiveDay"))
    doc.preamble.append(Command("NewAppointment", ["curso", "blue!20!white", "black"]))
    doc.preamble.append(Command("NewAppointment", ["consu", "brown!20!white", "black"]))
    doc.preamble.append(Command("NewAppointment", ["admin", "cyan!20!white", "black"]))
    doc.preamble.append(Command("NewAppointment", ["inves", "green!20!white", "black"]))
    doc.preamble.append(Command("NewAppointment", ["libre", "dark", "black"]))
    doc.preamble.append(Command("NewAppointment", ["desca", "teal!20!white", "black"]))

    sem = str(user_df["semestre"].item())
    año = user_df["año"].item()
    doc.change_page_style("empty")
    titulo = user_df["titulo"].item()
    nombre = user_df["nombre"].item()
    mail = user_df["mail"].item()
    doc.append(Command("centering"))
    doc.append(NoEscape(f"\\large Horario del {fun.number_to_ordinals(sem)} semestre, {año}"))
    doc.append(Command("par"))
    doc.append(Command("small"))
    doc.append(VerticalSpace("0.5cm"))
    doc.append(italic(NoEscape(f"{titulo} {nombre}")))
    doc.append(HorizontalSpace("0.4cm"))
    doc.append(Command("faPhone"))
    doc.append(HorizontalSpace("0.2cm"))
    doc.append(NoEscape("8858-1419"))
    doc.append(HorizontalSpace("0.4cm"))
    doc.append(Command("faEnvelope"))
    doc.append(HorizontalSpace("0.2cm"))
    doc.append(mail)

    with doc.create(Schedule()) as sched:
        for __, row in schedules_df.iterrows():
            codigo = row["codigo"]
            tipo = activities_df[activities_df["codigo"] == codigo]["tipo"].item()
            nombre = activities_df[activities_df["codigo"] == codigo]["nombre"].item()
            instancia = row["instancia"]
            dia = row["día"]
            inicio = row["inicio"]
            horas = row["horas"]
            ubicacion = row["ubicación"]
            if pd.isna(ubicacion):
                ubicacion = ""
            tiempo = f"{inicio}-{(pd.to_datetime(inicio) + pd.Timedelta(hours=int(horas))).strftime('%H:%M')}"

            match tipo:
                case "curso":
                    sched.append(
                        Command(
                            tipo,
                            [
                                NoEscape(nombre + r"\\" + codigo + r"\\ G" + str(instancia)),
                                NoEscape(ubicacion),
                                NoEscape(dia),
                                NoEscape(tiempo),
                            ],
                        )
                    )
                case "consu" | "admin":
                    sched.append(Command(tipo, [NoEscape(nombre), NoEscape(ubicacion), NoEscape(dia), NoEscape(tiempo)]))
                case "inves":
                    sched.append(
                        Command(
                            tipo,
                            [NoEscape(r"Proyecto VIE.\\ Codigo:" + f"{codigo}"), NoEscape(ubicacion), NoEscape(dia), NoEscape(tiempo)],
                        )
                    )
                case "desca":
                    sched.append(Command(tipo, [NoEscape(nombre), NoEscape(ubicacion), NoEscape(dia), NoEscape(tiempo)]))

    doc.append(Command("par"))
    doc.append(Command("raggedright"))
    doc.append(Command("footnotesize"))
    for __, row in activities_df.iterrows():
        if row["tipo"] == "inves":
            codigo = row["codigo"]
            nombre = row["nombre"]
            doc.append(bold(NoEscape("Proyecto VIE. Codigo: ")))
            doc.append(NoEscape(codigo))
            doc.append(bold(NoEscape(". Nombre: ")))
            doc.append(nombre)
            doc.append(VerticalSpace("0.2cm"))
            doc.append(NewLine())

    output_base = OUTPUT_PDF_DIR / f"Schedule-{sem}-{año}"
    doc.generate_pdf(str(output_base), clean=True, clean_tex=False, compiler="lualatex")

    generated_tex = output_base.with_suffix(".tex")
    target_tex = OUTPUT_TEX_DIR / generated_tex.name
    if generated_tex.exists():
        generated_tex.replace(target_tex)


if __name__ == "__main__":
    activities = pd.read_csv(DATA_DIR / "activities.csv")
    schedules = pd.read_csv(DATA_DIR / "schedules.csv")
    user_df = pd.read_csv(DATA_DIR / "user.csv")
    fun.analyze_schedule(activities, schedules)
    generate_schedule(user_df, activities, schedules)
