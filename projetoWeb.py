import os
import subprocess
import shutil
import requests

def create_and_open_project():
    # Diretório base para os projetos
    base_directory = r"C:/dev/projects"

    # Certifique-se de que o diretório base existe
    os.makedirs(base_directory, exist_ok=True)

    # Solicitar o nome do projeto
    project_name = input("Nome do projeto: ").strip()

    # Caminho completo do novo projeto
    project_path = os.path.join(base_directory, project_name)

    # Verificar se o projeto já existe
    if os.path.exists(project_path):
        print(f"O projeto '{project_name}' já existe em: {project_path}")
        # Perguntar ao usuário se deseja substituir o projeto
        resposta = input("Deseja substituir o projeto? (Sim/SIM/s/s ou Não/NAO/n/n): ").strip().lower()

        if resposta in ['sim', 's']:
            # Excluir o diretório existente
            shutil.rmtree(project_path)
            print(f"O projeto '{project_name}' foi excluído.")
            # Criar o novo diretório do projeto
            os.makedirs(project_path)
            print(f"Novo projeto '{project_name}' criado em: {project_path}")
        else:
            print("Projeto não foi substituído. Saindo.")
            return
    else:
        # Criar o diretório do projeto, se não existir
        os.makedirs(project_path)
        print(f"Projeto '{project_name}' criado em: {project_path}")

    # Abrir o diretório no VS Code usando o arquivo .cmd
    try:
        subprocess.run([r"C:\Users\betot\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd", project_path], check=True)
        print(f"Abrindo o projeto '{project_name}' no VS Code...")
    except FileNotFoundError:
        print("Erro: O comando 'code' não foi encontrado. Certifique-se de que o VS Code está instalado e configurado corretamente.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao abrir o projeto no VS Code: {e}")

    # Perguntar ao usuário se o repositório será público ou privado
    visibility = input("O repositório será público ou privado? (público/privado): ").strip().lower()
    if visibility == "público" or visibility == "publico":
        is_private = False
    elif visibility == "privado" or visibility == "privado":
        is_private = True
    else:
        print("Opção inválida. Usando repositório público por padrão.")
        is_private = False

    # Criar o repositório no GitHub
    create_github_repo(project_name, is_private)

def create_github_repo(repo_name, is_private):
    # Verificando se o token de autenticação foi encontrado
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Erro: Token de autenticação não encontrado. Defina a variável de ambiente 'GITHUB_TOKEN'.")
        return
    else:
        print("Token encontrado com sucesso!")

    # Dados para a criação do repositório
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {token}"}
    data = {
        "name": repo_name,
        "description": f"Repositório do projeto {repo_name}",
        "private": is_private  # Define a privacidade do repositório com base na escolha do usuário
    }
    
    # Fazendo a requisição para a API do GitHub
    response = requests.post(url, headers=headers, json=data)
    
    # Verificar se o repositório foi criado com sucesso
    if response.status_code == 201:
        print(f"Repositório '{repo_name}' criado no GitHub!")
    else:
        print(f"Erro ao criar repositório: {response.json().get('message', 'Desconhecido')}")

if __name__ == "__main__":
    create_and_open_project()
