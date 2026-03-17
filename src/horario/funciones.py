def number_to_ordinals(number_str):
    match number_str:
        case "1" | "3":
            number_str += r"\textsuperscript{er}"
        case "2":
            number_str += r"\textsuperscript{do}"
        case "4" | "5" | "6":
            number_str += r"\textsuperscript{to}"
        case "7" | "10":
            number_str += r"\textsuperscript{mo}"
        case "8":
            number_str += r"\textsuperscript{vo}"
        case "9":
            number_str += r"\textsuperscript{no}"
    return number_str 

def analizar_horario(actividades, horarios):
    for __,row in actividades.iterrows():
        codigo = row['codigo']
        horas = row['horas'] * row['instancias']
        for __,row in horarios.iterrows():
            if row['codigo'] == codigo:
                instancia = row['instancia']
                horas = horas - row['horas']
        if horas == 0:
            print(f"Actividad {codigo} tiene todas sus horas asignadas en el horario.")
        else:
            print(f"Actividad {codigo} tiene {horas} horas sin asignar en el horario.")