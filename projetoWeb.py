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
        resposta = input("Deseja substituir o projeto? (s ou n): ").strip().lower()

        if resposta in ['sim', 's']:
            # Excluir o diretório existente
            shutil.rmtree(project_path)
            print(f"O projeto '{project_name}' foi excluído.")
        else:
            print("Projeto não foi substituído. Saindo.")
            return

    # Perguntar se o repositório será público ou privado
    visibility = input("O repositório será público ou privado? (público/privado): ").strip().lower()
    if visibility in ["público", "publico"]:
        is_private = False
    elif visibility in ["privado", "privado"]:
        is_private = True
    else:
        print("Opção inválida. Usando repositório público por padrão.")
        is_private = False

    # Criar o repositório no GitHub
    print("Criando repositório no GitHub...")
    repo_ssh_url = create_github_repo(project_name, is_private)

    if not repo_ssh_url:
        print("Erro ao criar repositório no GitHub. Saindo...")
        return

    # Clonar o repositório para o diretório do projeto
    try:
        subprocess.run(["git", "clone", repo_ssh_url, project_path], check=True)
        print(f"Repositório '{project_name}' clonado com sucesso em {project_path}")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao clonar o repositório: {e}")
        return

    # Abrir o diretório no VS Code usando o arquivo .cmd
    try:
        subprocess.run([r"C:\Users\AlmavivA\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd", project_path], check=True)
        print(f"Abrindo o projeto '{project_name}' no VS Code...")
    except FileNotFoundError:
        print("Erro: O comando 'code' não foi encontrado. Certifique-se de que o VS Code está instalado e configurado corretamente.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao abrir o projeto no VS Code: {e}")

def create_github_repo(repo_name, is_private):
    # Verificando se o token de autenticação foi encontrado
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Erro: Token de autenticação não encontrado. Defina a variável de ambiente 'GITHUB_TOKEN'.")
        return None

    # Dados para a criação do repositório no GitHub
    url = "https://api.github.com/user/repos"
    headers = {"Authorization": f"token {token}"}
    data = {
        "name": repo_name,
        "description": f"Repositório do projeto {repo_name}",
        "private": is_private  # Define a privacidade do repositório
    }
    
    # Fazendo a requisição para a API do GitHub
    response = requests.post(url, headers=headers, json=data)
    
    # Verificar se o repositório foi criado com sucesso
    if response.status_code == 201:
        print(f"Repositório '{repo_name}' criado no GitHub!")
        # Solicitar a chave SSH do repositório
        repo_ssh_url = input(f"Agora, insira a chave SSH do repositório GitHub (geralmente no formato git@github.com:usuario/{repo_name}.git): ").strip()
        return repo_ssh_url
    else:
        print(f"Erro ao criar repositório: {response.json().get('message', 'Desconhecido')}")
        return None

if __name__ == "__main__":
    create_and_open_project()
