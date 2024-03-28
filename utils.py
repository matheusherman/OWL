import re
from owlready2 import *
from conversor import *
from extract_and_insert import insert_data
from KNN import *
import numpy as np
from ftplib import FTP
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from pyod.models.knn import KNN
import matplotlib.pyplot as plt
import json

pattern_web = re.compile(r'web \(ID: (\d+); Position point:\(([^,]+),([^,]+),([^)]+)\); Position normal:\(([^,]+),([^,]+),([^)]+)\)')
pattern_corner = re.compile(r'corner \(ID: (\d+); Parent ID: (\d+); Radius: ([^ ]+) mm\)')
pattern_lightening_hole = re.compile(r'lightening hole \(ID: (\d+); Parent ID: (\d+); Outer diameter: ([^ ]+) mm; Clearance diameter: ([^ ]+) mm; Height: ([^ ]+) mm; Angle: ([^ ]+) degree; Bend radius: ([^ ]+) mm; Position point:\(([^,]+),([^,]+),([^)]+)\); Position normal:\(([^,]+),([^,]+),([^)]+)\)')
pattern_tooling_hole = re.compile(r'tooling hole \(ID: (\d+); Parent ID: (\d+); Diameter: ([^ ]+) mm; Position point:\(([^,]+),([^,]+),([^)]+)\); Position normal:\(([^,]+),([^,]+),([^)]+)\)')
pattern_attachment_hole = re.compile(r'attachment hole \(ID: (\d+); Parent ID: (\d+); Diameter: ([^ ]+) mm; Position point:\(([^,]+),([^,]+),([^)]+)\); Position normal:\(([^,]+),([^,]+),([^)]+)\)')
pattern_attachment_flange = re.compile(r'attachment flange \(ID: (\d+); Parent ID: (\d+); Width: ([^ ]+) mm; Length: ([^ ]+) mm; Bend radius: ([^ ]+) mm; Type: (.*?); Position point:\(([^,]+),([^,]+),([^)]+)\); Position normal:\(([^,]+),([^,]+),([^)]+)\)', re.DOTALL)
pattern_stiffening_flange = re.compile(r'stiffening flange \(ID: (\d+); Parent ID: (\d+); Width: ([^ ]+) mm; Length: ([^ ]+) mm; Bend radius: ([^ ]+) mm; Type: (.*?); Position point:\(([^,]+),([^,]+),([^)]+)\); Position normal:\(([^,]+),([^,]+),([^)]+)\)', re.DOTALL)
pattern_deformed_flange = re.compile(r'deformed flange \(ID: (\d+); Parent ID: (\d+); Deformation length: ([^ ]+) mm\)')
pattern_deformed_flange2 = re.compile(r'deformed flange \(ID: (\d+); Parent ID: (\d+)\)')
pattern_joggle = re.compile(r'joggle \(ID: (\d+); Parent ID: (\d+); Runout: ([^ ]+) mm; Runout Direction:\(([^,]+),([^,]+),([^)]+)\); Depth: ([^ ]+) mm; Depth Direction:\(([^,]+),([^,]+),([^)]+)\); Bend radius 1: ([^ ]+) mm; Bend radius 2: ([^ ]+) mm; Type: (.*?)\)', re.DOTALL)
pattern_twin_joggle = re.compile(r'twin joggle \(ID: (\d+); Parent ID: (\d+); Runout: ([^ ]+) mm; Runout Direction:\(([^,]+),([^,]+),([^)]+)\); Depth: ([^ ]+) mm; Depth Direction:\(([^,]+),([^,]+),([^)]+)\); Bend radius 1: 3 mm; Bend radius 2: 3 mm; Type: (.*?)\)', re.DOTALL)
pattern_bend_relief = re.compile(r'bend relief \(ID: (\d+); Parents IDs: 15, 7; Radius: ([^ ]+) mm\)')
pattern_stringer_cutout = re.compile(r'stringer cutout \(ID: (\d+); Parent ID: (\d+); Profile: \(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\)\n')
pattern_cutout = re.compile(r'cutout \(ID: (\d+); Parent ID: (\d+); Profile: \(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\(([^,]+),([^,]+),([^)]+)\)\)')
pattern_bead = re.compile(r'bead \(ID: (\d+); Parent ID: (\d+); Width: ([^ ]+) mm; Depth: ([^ ]+) mm\)')
pattern_lip = re.compile(r'lip \(ID: (\d+); Parent ID: (\d+); Width: ([^ ]+) mm; Length: ([^ ]+) mm\)')

def extract_data_from_ontology(onto):
    """
    Extrai dados de uma ontologia e os retorna em um formato estruturado.

    Args:
        onto: Ontologia da qual os dados serão extraídos.

    Returns:
        dict: Dados extraídos da ontologia em um formato estruturado.
    """

    onto.load()
    prop_values_dict = {}

    for classe in onto.classes():
        if not list(classe.instances()):
            continue
        prop_values_dict[classe.name] = {}

        for individual in classe.instances():
            for prop in individual.get_properties():
                prop_value = getattr(individual, prop.python_name)
                if prop.python_name not in prop_values_dict[classe.name]:
                    prop_values_dict[classe.name][prop.python_name] = []
                prop_values_dict[classe.name][prop.python_name].append(prop_value)

    return prop_values_dict

def obter_dados_nova_peca(part_file_path):
    dados_peca = {}

    with open(part_file_path, 'r') as file:
        lines = file.readlines()

    for linha in lines:
        if re.match(pattern_web, linha):
            match = re.match(pattern_web, linha)
            dados_peca['Web'] = {
                'ID': match.group(1),
                'Position_Point_X': match.group(2),
                'Position_Point_Y': match.group(3),
                'Position_Point_Z': match.group(4),
                'Position_Normal_X': match.group(5),
                'Position_Normal_Y': match.group(6),
                'Position_Normal_Z': match.group(7)
            }
        elif re.match(pattern_corner, linha):
            match = re.match(pattern_corner, linha)
            dados_peca.setdefault('Corners', []).append({
                'ID': match.group(1),
                'Parent_ID': match.group(2),
                'Radius': match.group(3)
            })
        elif re.match(pattern_attachment_hole, linha):
            match = re.match(pattern_attachment_hole, linha)
            dados_peca.setdefault('Attachment_Holes', []).append({
                'ID': match.group(1),
                'Parent_ID': match.group(2),
                'Diameter': match.group(3),
                'Position_Point_X': match.group(4),
                'Position_Point_Y': match.group(5),
                'Position_Point_Z': match.group(6),
                'Position_Normal_X': match.group(7),
                'Position_Normal_Y': match.group(8),
                'Position_Normal_Z': match.group(9)
            })

    return dados_peca

def choose_file(root):
    """
    Abre uma janela de diálogo para permitir que o usuário escolha um arquivo.

    Args:
        root: Objeto raiz da interface gráfica onde a janela de diálogo será exibida.
    """
    root = tk.Tk().withdraw()
    file_path = filedialog.askopenfilename()
    directory, file_name = os.path.split(file_path)
    return file_path, directory, file_name

def save_ontology(arquivo_local, caminho_remoto):
    """
    Copia a ontologia salva localmente para um servidor remoto usando FTP.

    Args:
        arquivo_local: Nome/caminho do arquivo local da ontologia (por padrão a pasta do projeto atual).
        caminho_remoto: Caminho completo do servidor remoto em questão (hard coded).
    """

    with open('config.json') as f:
        config = json.load(f)

    hostname = config['hostname']
    port = config['port']
    username = config['username']
    password = config['password']

    ftp = FTP()
    ftp.connect(hostname, port)
    ftp.login(username, password)

    print(ftp.getwelcome())
    print(ftp.pwd())

    with open(arquivo_local, 'rb') as arquivo:
        ftp.storbinary('STOR ' + f'{caminho_remoto}', arquivo)
        print(f'{caminho_remoto}/{arquivo}')

    # Fecha AFR_Output conexão FTP
    ftp.quit()

    print("Arquivo copiado com sucesso para o servidor remoto via FTP.")

def create_ontology(onto, file_name):
    """
    Cria uma nova ontologia estática a partir dos argumentos.

    Args:
        onto: Ontologia onde a estrutura será criada.
        file_name (str): Nome do arquivo para criação.
    """

    with onto:
        '''
        CLASSES
        '''

        class Product_Data(Thing):
            namespace = onto


        class Product_Features(Product_Data):
            namespace = onto


        class Base_Features(Product_Features):
            namespace = onto


        class Web(Base_Features):
            namespace = onto


        class Contact_Features(Product_Features):
            namespace = onto


        class Attachment_Flange(Contact_Features):
            namespace = onto


        class Attachment_Hole(Contact_Features):
            namespace = onto


        class Deformed_Flange(Contact_Features):
            namespace = onto


        class Deformed_Web(Contact_Features):
            namespace = onto


        class Joggle(Contact_Features):
            namespace = onto


        class Twin_Joggle(Contact_Features):
            namespace = onto


        class Part_Features(Product_Features):
            namespace = onto


        class Part_Area(Part_Features):
            namespace = onto


        class Part_Name(Part_Features):
            namespace = onto


        class Part_Perimeter(Part_Features):
            namespace = onto


        class Part_Thickness(Part_Features):
            namespace = onto


        class Part_Weight(Part_Features):
            namespace = onto


        class Refinement_Features(Product_Features):
            namespace = onto


        class Bead(Refinement_Features):
            namespace = onto


        class Bend_Relief(Refinement_Features):
            namespace = onto


        class Corner(Refinement_Features):
            namespace = onto


        class Cutout(Refinement_Features):
            namespace = onto


        class Lightening_Cutout(Refinement_Features):
            namespace = onto


        class Lightening_Hole(Refinement_Features):
            namespace = onto


        class Lip(Refinement_Features):
            namespace = onto


        class Stiffening_Flange(Refinement_Features):
            namespace = onto


        class Stringer_Cutout(Refinement_Features):
            namespace = onto


        class Tooling_Hole(Refinement_Features):
            namespace = onto


        '''
        DATA PROPERTIES
        '''


        class hasID(DataProperty):
            namespace = onto
            domain = onto.classes()
            range = [int]


        class hasParentID(DataProperty):
            namespace = onto
            range = [int]


        class hasPosition_Point_X(DataProperty):
            namespace = onto
            domain = [Web, Lightening_Hole, Tooling_Hole, Attachment_Hole, Attachment_Flange,  Stiffening_Flange]
            range = [float]


        class hasPosition_Point_Y(DataProperty):
            namespace = onto
            domain = [Web, Lightening_Hole, Tooling_Hole, Attachment_Hole, Attachment_Flange,  Stiffening_Flange]
            range = [float]


        class hasPosition_Point_Z(DataProperty):
            namespace = onto
            domain = [Web, Lightening_Hole, Tooling_Hole, Attachment_Hole, Attachment_Flange,  Stiffening_Flange]
            range = [float]


        class hasPosition_Normal_X(DataProperty):
            namespace = onto
            domain = [Web, Lightening_Hole, Tooling_Hole, Attachment_Hole, Attachment_Flange,  Stiffening_Flange]
            range = [float]


        class hasPosition_Normal_Y(DataProperty):
            namespace = onto
            domain = [Web, Lightening_Hole, Tooling_Hole, Attachment_Hole, Attachment_Flange,  Stiffening_Flange]
            range = [float]


        class hasPosition_Normal_Z(DataProperty):
            namespace = onto
            domain = [Web, Attachment_Hole]
            range = [float]
            
            
        class hasRunout(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle]
            range = [float]
            
            
        class hasRunout_Direction_X(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle]
            range = [float]
            
            
        class hasRunout_Direction_Y(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle]
            range = [float]
            
            
        class hasRunout_Direction_X(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle]
            range = [float]
            

        class hasWidth(DataProperty):
            namespace = onto
            domain = [Attachment_Flange, Stiffening_Flange]
            range = [float]


        class hasLength(DataProperty):
            namespace = onto
            domain = [Attachment_Flange, Stiffening_Flange]
            range = [float]


        class hasHeight(DataProperty):
            namespace = onto
            domain = [Lightening_Hole]
            range = [float]


        class hasLength(DataProperty):
            namespace = onto
            domain = [Lip, Bead, Twin_Joggle, Joggle,]
            range = [float]


        class hasBend_Radius(DataProperty):
            namespace = onto
            domain = [Attachment_Flange, Stiffening_Flange]
            range = [float]


        class hasBend_Radius_2(DataProperty):
            namespace = onto
            domain = [Attachment_Flange, Stiffening_Flange]
            range = [float]


        class hasBend_Radius_2(DataProperty):
            namespace = onto
            domain = [Attachment_Flange, Stiffening_Flange]
            range = [float]


        class hasRadius(DataProperty):
            namespace = onto
            domain = [Corner, Bend_Relief]
            range = [float]


        class hasDiameter(DataProperty):
            namespace = onto
            domain = [Attachment_Hole, Tooling_Hole]
            range = [float]


        class hasDeformation_Length(DataProperty):
            namespace = onto
            domain = [Deformed_Flange]
            range = [float]


        class hasOuter_Diameter(DataProperty):
            namespace = onto
            domain = [Lightening_Hole]
            range = [float]


        class hasClearance_Diameter(DataProperty):
            namespace = onto
            domain = [Lightening_Hole]
            range = [float]


        class hasAngle(DataProperty):
            namespace = onto
            domain = [Lightening_Hole]
            range = [float]


        class hasType(DataProperty):
            namespace = onto
            domain = [Stiffening_Flange, Attachment_Flange, Joggle, Twin_Joggle]
            range = [str]


        class hasProfile(DataProperty):
            namespace = onto
            domain = [Stringer_Cutout, Cutout]
            range = [str]


        class hasDepth(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle, Bead]
            range = [float]


        class hasDepth_Direction_X(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle, Bead]
            range = [float]


        class hasDepth_Direction_Y(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle, Bead]
            range = [float]


        class hasDepth_Direction_Z(DataProperty):
            namespace = onto
            domain = [Joggle, Twin_Joggle, Bead]
            range = [float]


        class hasName(DataProperty):
            namespace = onto
            range = [str]


        '''
        OBJECT PROPERTIES
        '''

        '''
        SEMANTIC RULES
        '''

    print("Ontology created!")
    onto.save(file=f'{file_name}.owl')
    save_ontology(f'{file_name}.owl', f'/{file_name}.owl')