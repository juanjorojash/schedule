import subprocess
import pandas as pd
from pylatex import Document, Package, Command, PageStyle, Head, Foot, NewPage, NewLine,\
    TextColor,HorizontalSpace, VerticalSpace, \
    config
from pylatex.base_classes import Arguments, Environment
from pylatex.utils import NoEscape, bold, italic
import funciones as fun

activ = pd.read_csv("datos/actividades.csv")
horar = pd.read_csv("datos/horarios.csv")
usuar = pd.read_csv("datos/usuario.csv")

fun.analizar_horario(activ, horar)

class Schedule(Environment):
    """Custom LaTeX environment for the schedule package."""
    _latex_name = 'schedule'
    packages = [Package('schedule')]


def generar_horario(usuario,actividades,horarios):
    #Config
    config.active = config.Version1(row_heigth=1.5)
    #Geometry
    geometry_options = {
        "left": "2mm",
        "right": "2mm",
        "top": "5mm",
        "bottom": "5mm",
    }
    #Document options
    doc = Document(documentclass="article", \
                    fontenc=None, \
                    inputenc=None, \
                    lmodern=False, \
                    textcomp=False, \
                    page_numbers=False, \
                    indent=True, \
                    document_options=["landscape", "12pt", "dvipsnames"], \
                    geometry_options=geometry_options)
    #Packages
    doc.packages.append(Package(name="schedule", options=None))
    doc.packages.append(Package(name="fontawesome", options=None))
    #Preamble
    doc.preamble.append(NoEscape(r"""
\makeatletter
\def\@M@week{{Lunes} {Martes} {Miércoles} {Jueves} {Viernes} {Saturday} {Sunday}}
\makeatother
"""))
    doc.preamble.append(Command("CellHeight", "1.1cm"))
    doc.preamble.append(Command("CellWidth", "5cm"))
    doc.preamble.append(Command("TimeRange", NoEscape(r"7:30-20:00")))
    doc.preamble.append(Command("SubUnits", "30"))
    doc.preamble.append(Command("BeginOn", "Monday"))
    doc.preamble.append(Command("TextSize", NoEscape(r"\small")))
    doc.preamble.append(Command("FiveDay"))
    #define the appointments
    doc.preamble.append(Command("NewAppointment", ["curso", "blue!20!white", "black"]))
    doc.preamble.append(Command("NewAppointment", ["consu", "brown!20!white", "black"]))
    doc.preamble.append(Command("NewAppointment", ["admin", "cyan!20!white", "black"]))
    doc.preamble.append(Command("NewAppointment", ["inves", "green!20!white", "black"]))
    doc.preamble.append(Command("NewAppointment", ["libre", "dark", "black"]))
    doc.preamble.append(Command("NewAppointment", ["desca", "teal!20!white", "black"]))
    #Read data
    sem = str(usuario['semestre'].item())
    año = usuario['año'].item()
    doc.change_page_style("empty")
    titulo = usuario['titulo'].item()
    nombre = usuario['nombre'].item() 
    mail = usuario['mail'].item()
    doc.append(Command("centering"))
    doc.append(NoEscape(f'''\\large Horario del {fun.number_to_ordinals(sem)} semestre, {año}'''))
    doc.append(Command("par"))
    doc.append(Command("small"))
    doc.append(VerticalSpace("0.5cm"))
    doc.append(italic(NoEscape(f"{titulo} {nombre}")))
    #phone
    doc.append(HorizontalSpace("0.4cm"))
    doc.append(Command("faPhone"))
    doc.append(HorizontalSpace("0.2cm"))
    doc.append(NoEscape("8858-1419"))
    #mail
    doc.append(HorizontalSpace("0.4cm"))
    doc.append(Command("faEnvelope"))
    doc.append(HorizontalSpace("0.2cm"))
    doc.append(mail)

    with doc.create(Schedule()) as sched:

        # Iterate through horarios
        for __, row in horarios.iterrows():
            codigo = row['codigo']
            tipo = actividades[actividades['codigo'] == codigo]['tipo'].item()
            nombre = actividades[actividades['codigo'] == codigo]['nombre'].item()
            instancia = row['instancia']
            dia = row['día']
            inicio = row['inicio']
            horas = row['horas']
            ubicacion = row['ubicación']
            if pd.isna(ubicacion):
                ubicacion = ""
            tiempo = f"{inicio}-{(pd.to_datetime(inicio) + pd.Timedelta(hours=int(horas))).strftime('%H:%M')}"

            # Add appointment to the schedule
            match tipo:
                case "curso":
                    sched.append(Command(tipo, [NoEscape(nombre + r"\\" + codigo + r"\\ G" + str(instancia)),NoEscape(ubicacion),NoEscape(dia),NoEscape(tiempo)]))
                case "consu" | "admin":
                    sched.append(Command(tipo, [NoEscape(nombre),NoEscape(ubicacion),NoEscape(dia),NoEscape(tiempo)]))
                case "inves":
                    sched.append(Command(tipo, [NoEscape(r"Proyecto VIE.\\ Codigo:" + f"{codigo}"),NoEscape(ubicacion),NoEscape(dia),NoEscape(tiempo)]))
                case "desca":
                    sched.append(Command(tipo, [NoEscape(nombre),NoEscape(ubicacion),NoEscape(dia),NoEscape(tiempo)]))
    doc.append(Command("par"))
    doc.append(Command("raggedright"))
    doc.append(Command("footnotesize"))
    for __, row in actividades.iterrows():
        if row['tipo'] == "inves":
            codigo = row['codigo']
            nombre = row['nombre']
            doc.append(bold(NoEscape(f"Proyecto VIE. Codigo: ")))
            doc.append(NoEscape(codigo))
            doc.append(bold(NoEscape(f". Nombre: ")))
            doc.append(nombre)
            doc.append(VerticalSpace("0.2cm"))
            doc.append(NewLine())
    doc.generate_pdf(f"Horario-{sem}-{año}", clean=True, clean_tex=False, compiler='lualatex')

generar_horario(usuar,activ,horar)
