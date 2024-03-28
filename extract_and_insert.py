import re
import utils


# PEGA OS DADOS DA PEÇA ATUAL E CHAMA A FUNCAO DE INSERIR INSTANCIA
def insert_data(onto, file_path):
    """
    Coleta os dados de uma peça e insere em uma ontologia com base nos padrões encontrados em um arquivo.

    Args:
        onto: Ontologia onde os dados serão inseridos.
        file_path (str): Caminho completo do arquivo contendo os dados a serem inseridos.
    """


    with open(file_path, 'r') as file:
        lines = file.readlines()

    last_deformation_length = None

    for line in lines:
        if re.match(utils.pattern_web, line):
            match = re.match(utils.pattern_web, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasPosition_Point_X': float(data[1]),
                'hasPosition_Point_Y': float(data[2]),
                'hasPosition_Point_Z': float(data[3]),
                'hasPosition_Normal_X': float(data[4]),
                'hasPosition_Normal_Y': float(data[5]),
                'hasPosition_Normal_Z': float(data[6])
            }
            insert_instance(onto, "Web", **data_dict)

        elif re.match(utils.pattern_corner, line):
            match = re.match(utils.pattern_corner, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasRadius': float(data[2])
            }
            insert_instance(onto, 'Corner', **data_dict)

        elif re.match(utils.pattern_lightening_hole, line):
            match = re.match(utils.pattern_lightening_hole, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasOuter_Diameter': float(data[2]),
                'hasClearance_Diameter': float(data[3]),
                'hasHeight': float(data[4]),
                'hasAngle': float(data[5]),
                'hasBend_Radius': float(data[6]),
                'hasPosition_Point_X': float(data[7]),
                'hasPosition_Point_Y': float(data[8]),
                'hasPosition_Point_Z': float(data[9]),
                'hasPosition_Normal_X': float(data[10]),
                'hasPosition_Normal_Y': float(data[11]),
                'hasPosition_Normal_Z': float(data[12])
            }
            insert_instance(onto, 'Lightening_Hole', **data_dict)

        elif re.match(utils.pattern_tooling_hole, line):
            match = re.match(utils.pattern_tooling_hole, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasDiameter': float(data[2]),
                'hasPosition_Point_X': float(data[3]),
                'hasPosition_Point_Y': float(data[4]),
                'hasPosition_Point_Z': float(data[5]),
                'hasPosition_Normal_X': float(data[6]),
                'hasPosition_Normal_Y': float(data[7]),
                'hasPosition_Normal_Z': float(data[8])
            }
            insert_instance(onto, "Tooling_Hole", **data_dict)

        elif re.match(utils.pattern_attachment_hole, line):
            match = re.match(utils.pattern_attachment_hole, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasDiameter': float(data[2]),
                'hasPosition_Point_X': float(data[3]),
                'hasPosition_Point_Y': float(data[4]),
                'hasPosition_Point_Z': float(data[5]),
                'hasPosition_Normal_X': float(data[6]),
                'hasPosition_Normal_Y': float(data[7]),
                'hasPosition_Normal_Z': float(data[8])
            }
            insert_instance(onto, 'Attachment_Hole', **data_dict)

        elif re.match(utils.pattern_attachment_flange, line):
            match = re.match(utils.pattern_attachment_flange, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasWidth': float(data[2]),
                'hasLength': float(data[3]),
                'hasBend_Radius': float(data[4]),
                'hasType': str(data[5]),
                'hasPosition_Point_X': float(data[6]),
                'hasPosition_Point_Y': float(data[7]),
                'hasPosition_Point_Z': float(data[8]),
                'hasPosition_Normal_X': float(data[9]),
                'hasPosition_Normal_Y': float(data[10]),
                'hasPosition_Normal_Z': float(data[11])
            }
            insert_instance(onto, "Attachment_Flange", **data_dict)

        elif re.match(utils.pattern_stiffening_flange, line):
            match = re.match(utils.pattern_stiffening_flange, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasWidth': float(data[2]),
                'hasLength': float(data[3]),
                'hasBend_Radius': float(data[4]),
                'hasType': str(data[5]),
                'hasPosition_Point_X': float(data[6]),
                'hasPosition_Point_Y': float(data[7]),
                'hasPosition_Point_Z': float(data[8]),
                'hasPosition_Normal_X': float(data[9]),
                'hasPosition_Normal_Y': float(data[10]),
                'hasPosition_Normal_Z': float(data[11])
            }
            insert_instance(onto, 'Stiffening_Flange', **data_dict)

        elif re.match(utils.pattern_deformed_flange, line):
            match = re.match(utils.pattern_deformed_flange, line)
            if match:
                data = match.groups()
                last_deformation_length = float(data[2])
                data_dict = {
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasDeformation_length': float(data[2])
                }
            else:
                match = re.match(utils.pattern_deformed_flange2, line)
                data = match.groups()
                data_dict = {
                    'hasID': int(data[0]),
                    'hasParentID': int(data[1]),
                    'hasDeformation_length': last_deformation_length
                }
            insert_instance(onto, 'Deformed_Flange', **data_dict)

        elif re.match(utils.pattern_joggle, line):
            match = re.match(utils.pattern_joggle, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasRunout': float(data[2]),
                'hasRunout_Direction_X': float(data[3]),
                'hasRunout_Direction_Y': float(data[4]),
                'hasRunout_Direction_Z': float(data[5]),
                'hasDepth': float(data[6]),
                'hasDepth_Direction_X': float(data[7]),
                'hasDepth_Direction_Y': float(data[8]),
                'hasDepth_Direction_Z': float(data[9]),
                'hasBend_Radius_1': float(data[10]),
                'hasBend_Radius_2': float(data[11]),
                'hasType': str(data[12])
            }
            insert_instance(onto, 'Joggle', **data_dict)

        elif re.match(utils.pattern_twin_joggle, line):
            match = re.match(utils.pattern_twin_joggle, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasRunout': float(data[2]),
                'hasRunout_Direction_X': float(data[3]),
                'hasRunout_Direction_Y': float(data[4]),
                'hasRunout_Direction_Z': float(data[5]),
                'hasDepth': float(data[6]),
                'hasDepth_Direction_X': float(data[7]),
                'hasDepth_Direction_Y': float(data[8]),
                'hasDepth_Direction_Z': float(data[9]),
                'hasBend_Radius_1': float(data[10]),
                'hasBend_Radius_2': float(data[11]),
                'hasType': str(data[12])
            }
            insert_instance(onto, 'Twin_Joggle', **data_dict)

        elif re.match(utils.pattern_bend_relief, line):
            match = re.match(utils.pattern_bend_relief, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]).split(','),  # Convert comma-separated parents to a list
                'hasRadius': float(data[2])
            }
            insert_instance(onto, "Bend_Relief", **data_dict)

        elif re.match(utils.pattern_stringer_cutout, line):
            match = re.match(utils.pattern_stringer_cutout, line)
            data = match.groups()
            points = []
            for i in range(0, 18, 3):
                points.append((float(data[i]), float(data[i + 1]), float(data[i + 2])))
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasProfile': points
            }
            insert_instance(onto, "Stringer_Cutout", **data_dict)

        elif re.match(utils.pattern_cutout, line):
            match = re.match(utils.pattern_cutout, line)
            data = match.groups()
            points = []
            for i in range(0, 18, 3):
                points.append((float(data[i]), float(data[i + 1]), float(data[i + 2])))
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasProfile': points
            }
            insert_instance(onto, "Cutout", **data_dict)

        elif re.match(utils.pattern_bead, line):
            match = re.match(utils.pattern_bead, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasWidth': float(data[2]),
                'hasDepth': float(data[3])
            }
            insert_instance(onto, "Bead", **data_dict)

        elif re.match(utils.pattern_lip, line):
            match = re.match(utils.pattern_lip, line)
            data = match.groups()
            data_dict = {
                'hasID': int(data[0]),
                'hasParentID': int(data[1]),
                'hasWidth': float(data[2]),
                'hasLength': float(data[3])
            }
            insert_instance(onto, 'Lip', **data_dict)


# INSERE UMA INSTÂNCIA NA ONTOLOGIA COM OS DADOS DA PEÇA
def insert_instance(onto, class_name, **kwargs):
    """
    Insere instâncias de uma classe específica na ontologia.

    Args:
        onto: Ontologia onde as instâncias serão inseridas.
        class_name (str): Nome da classe na qual as instâncias serão inseridas.
        **kwargs: Argumentos nomeados representando propriedades e seus valores para as instâncias AFR_Output serem inseridas.
    """

    # Obtém AFR_Output classe correspondente na ontologia
    target_class = getattr(onto, class_name, None)

    if target_class is None:
        print(f"Classe '{class_name}' não encontrada na ontologia.")
        return

    # Cria uma nova instância da classe alvo
    new_instance = target_class()

    # Itera sobre os argumentos nomeados e define as propriedades das instâncias
    print(kwargs.items())
    for prop_name, value in kwargs.items():
        if hasattr(new_instance, prop_name):
            prop = getattr(new_instance, prop_name)
            prop.append(value)
        else:
            print(f"Propriedade '{prop}' não encontrada na classe '{class_name}'.")

    print(f"Instância inserida na ontologia: {new_instance}")
