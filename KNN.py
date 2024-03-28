def train_knn_models(ontology, k=5):
    """
    Treina modelos KNN para cada classe na ontologia.

    Args:
        ontology: Ontologia contendo os dados para treinamento dos modelos.
        k (int): Número de vizinhos a serem considerados no algoritmo KNN. O padrão é 5.

    Returns:
        dict: Dicionário de modelos KNN treinados para cada classe e propriedade.

    Esta função percorre cada classe na ontologia e cada instância dentro de cada classe,
    coletando os valores das propriedades de cada instância. Em seguida, treina um modelo
    KNN para cada propriedade de cada classe, usando os valores das propriedades como dados de treinamento.
    Os modelos treinados são armazenados em um dicionário e retornados.
    """
    knn_models = {}
    for class_name in ontology.classes():
        knn_models[class_name] = {}
        for instance in class_name.instances():
            for prop_name, prop_value in instance.get_properties():
                if prop_name not in knn_models[class_name]:
                    knn_models[class_name][prop_name] = []
                knn_models[class_name][prop_name].append(prop_value)

    for class_name, prop_dict in knn_models.items():
        for prop_name, prop_values in prop_dict.items():
            X = np.array(prop_values, dtype=float).reshape(-1, 1)
            knn_model = KNeighborsClassifier(n_neighbors=k)
            knn_model.fit(X)
            knn_models[class_name][prop_name] = knn_model

    return knn_models

def detect_anomalies(new_piece, knn_models):
    """
    Detecta anomalias em uma nova peça com base nos modelos KNN treinados.

    Args:
        new_piece (dict): Dados da nova peça a serem analisados.
        knn_models (dict): Dicionário de modelos KNN treinados.

    Returns:
        dict: Dicionário de anomalias detectadas para cada classe e propriedade.

    Esta função recebe dados de uma nova peça e os compara com os modelos KNN treinados
    para detectar anomalias. Para cada classe e propriedade na nova peça, calcula a distância
    para o modelo KNN correspondente. Se a distância for maior que 0.5, considera-se uma anomalia
    e é registrada no dicionário de anomalias, que é retornado.
    """
    anomalies = {}
    for class_name, prop_values in new_piece.items():
        anomalies[class_name] = {}
        for prop_name, prop_value in prop_values.items():
            knn_model = knn_models[class_name][prop_name]
            distance = knn_model.kneighbors(np.array([float(prop_value)]).reshape(1, -1))
            if distance > 0.5:
                anomalies[class_name][prop_name] = distance
    return anomalies

'''
hasParentID(?individuoA, ?childID) ^ hasID(?individuoB, ?parentID) ^ swrlb:equal(?childID, ?parentID) ^ hasName(?individuoA, ?nomeA) ^ hasName(?individuoB, ?nomeB) ^ swrlb:equal(?nomeA, ?nomeB) -> isParentOf(?individuoB, ?individuoA)
hasID(?x, "1") -> Web(?x)
'''