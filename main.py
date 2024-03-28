from utils import *

# Specify the path for ontology creation
onto, onto_path, onto_directory, onto_file_name = None, None, None, None
part_file_path, part_directory, part_file_name  = None, None, None
current_path = os.getcwd()

def main():
    """
    Função principal responsável por gerenciar a interface gráfica e as interações do usuário.

    A função cria uma janela de interface gráfica com botões para várias operações, como criar uma ontologia,
    inserir dados em uma ontologia, carregar uma ontologia existente, visualizar uma peça, converter um arquivo
    .stp em .txt, testar uma anomalia e fechar o programa.

    Cada botão está associado a uma função específica que executa a operação correspondente quando acionada.

    A função principal utiliza a biblioteca Tkinter para criar a interface gráfica e gerenciar os eventos do usuário.

    O programa continua em execução até que o usuário feche a janela da interface gráfica.

    """

    global onto

    '''
    CRIA UMA ONTOLOGIA
    '''
    def criar():
        nome_ontologia = simpledialog.askstring("Nome da Ontologia", "Digite o nome da ontologia:")
        if nome_ontologia:
            messagebox.showinfo("Sucesso", f"Criando ontologia {nome_ontologia}.owl")
            create_ontology(get_ontology(f'IP{nome_ontologia}.owl'), nome_ontologia)
            messagebox.showinfo("Sucesso", f"Ontologia criada e salva como {nome_ontologia}.owl")
        else:
            messagebox.showerror("Erro", "Nenhum nome foi digitado!")

    '''
    INSERE UMA PEÇA NA ONTOLOGIA ESCOLHIDA
    '''
    def inserir():
        global onto
        if onto is None:
            messagebox.showinfo("Selecione", f"Selecione a ontologia!")
            onto_path, onto_directory, onto_name = choose_file(root)
            if not onto_name.endswith('.owl'):
                messagebox.showerror("Erro", "O arquivo selecionado não é um arquivo .owl!")
                return

            onto = get_ontology(f'file://{onto_path}')

        onto.load()
        messagebox.showinfo("Selecione", f"Selecione a Peça .STP que deseja inserir!")
        part_path, part_directory, part_file_name = choose_file(root)
        if not part_file_name.endswith('.stp') and not part_file_name.endswith('.txt'):
            messagebox.showerror("Erro", "O arquivo selecionado não é um arquivo .stp nem .txt!")
            return

        if part_file_name.endswith('.stp'):
            part_path, part_directory, part_file_name = AFR_conversion(part_directory, part_file_name)

        insert_data(onto, part_path)
        onto.save(file=f'{onto_name}')
        save_ontology(f'{onto_name}', f'Público/{onto_name}')
        messagebox.showinfo("Sucesso", f"Arquivos inseridos na ontologia e salva como {onto_name}")

    '''
    CARREGA UMA ONTOLOGIA
    '''
    def carregar_onto():
        global onto, onto_path, onto_directory, onto_file_name
        messagebox.showinfo("Selecione", f"Selecione a ontologia!")
        onto_path, onto_directory, onto_file_name = choose_file(root)
        if not onto_file_name.endswith('.owl'):
            messagebox.showerror("Erro", "O arquivo selecionado não é um arquivo .owl!")
            return  # Sai da função inserir() se o arquivo não tiver a extensão .owl

        onto = get_ontology(f'file://{onto_path}')
        onto.load()
        messagebox.showinfo("Sucesso", "Ontologia carregada")
        return onto_path, onto_directory, onto_file_name

    '''
    ABRE A VISUALIZAÇÃO 3D DE UMA PEÇA
    '''
    def visualizar_peca():
        #open_file_dialog()
        messagebox.showinfo("Sucesso", "Peça selecionada!")

    '''
    CONVERTER O STP EM TXT
    '''
    def converter():
        global part_file_name, part_file_path, peca_directory
        messagebox.showwarning("Selecione", "Seleciona a Peça para conversão!")
        file_path, directory, file_name = choose_file(root)
        if not file_name.endswith('.stp'):
            messagebox.showerror("Erro", "O arquivo selecionado não é um arquivo .stp!")
            return
        part_file_path, part_directory, part_file_name = AFR_conversion(directory, file_name)
        messagebox.showinfo("Sucesso", "Peça Convertida para txt!")
        return part_file_path, part_directory, part_file_name

    '''
    SELECIONA UMA PEÇA E TESTA UMA ANOMALIA COMPARANDO COM INFORMAÇÕES DA ONTOLOGIA
    '''
    def testar():
        global part_file_name, part_file_path, part_directory
        try:
            onto.load()
            converter()
            obter_dados_nova_peca(part_file_path)

        except AttributeError:
            carregar_onto()
            testar()

    '''
    ENCERRA O PROGRAMA
    '''
    def fechar_janela():
        root.destroy()

    root = tk.Tk()
    root.title("Menu")
    root.geometry("300x250")

    # Botões para cada opção
    btn_criar = tk.Button(root, text="Criar Ontologia", command=criar)
    btn_criar.pack()

    btn_inserir = tk.Button(root, text="Coletar Dados", command=inserir)
    btn_inserir.pack()

    btn_carregar_onto = tk.Button(root, text="Carregar Ontologia", command=carregar_onto)
    btn_carregar_onto.pack()

    btn_visualizar_onto = tk.Button(root, text="Visualizar Peça", command=visualizar_peca)
    btn_visualizar_onto.pack()

    btn_converter_peca = tk.Button(root, text="Converter STEP para TXT", command=converter)
    btn_converter_peca.pack()

    btn_testar = tk.Button(root, text="Testar Anomalia", command=testar)
    btn_testar.pack()

    # Botão para fechar a janela
    btn_fechar = tk.Button(root, text="Fechar", command=fechar_janela)
    btn_fechar.config(bg="red", fg="white")
    btn_fechar.pack()

    root.mainloop()

if __name__ == "__main__":
    main()