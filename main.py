import json
import sys
import os, pwd
from tqdm import tqdm
from time import sleep

# Comandos de configuração:
# 
# set default port 3000: Define a porta dos servidores Flask para 3000 como padrão.
# set default host 192.0.0.1: Define o host dos servidores Flask para 192.0.0.1 como padrão.
# 
# deactivate auto-install-depedencies: Desativa a instalação automática de dependencias do requirements.
# activate auto-install-dependencies: Ativa a instalação automática de dependencias do requirements.
# 
# deactivate auto-gitignore: Desativa a criação automática de um .gitignore.
# activate auto-gitignore: Ativa a criação automática de um .gitignore.
#
# Comandos de inicialização:
# 
# init HelloWorld: Inicia um novo projeto dentro da pasta HelloWorld.
#
# update HelloWorld: Caso a instalação automática de dependencias estiver ativada, esse comando ira instalar todas as
# dependencias pendentes. 
# 
# #

code_app = '''
# Bem vindo ao {}! 
# Aproveite seu projeto ao máximo.#

from flask import Flask, render_template

app = Flask(__name__, template_folder="templates", static_folder="public")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port={}, host="{}")
'''

code_html = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <title>FlaskJUMP</title>
</head>
<body>
    <h1>Bem vindo ao seu projeto!</h1>
    <p>Comece o código!</p>
</body>
</html>
"""

code_ignore = """
__pycache__/
*.env
venv/
"""

class CLI:
    def __init__(self):
        self.commands = {
            '-help': self.help_cli,
            'set': self.set,
            'deactivate': self.deactivate,
            'activate': self.activate,
            'init': self.init_project
        }

        self.config_flaskjump = json.load(open('config.flaskjump.json', 'r'))

        try:
            os.mkdir(f'{pwd.getpwuid(os.getuid()).pw_dir}/FlaskJUMP-Projects')
        except:
            pass

        self.config_flaskjump['@default-directory'] = f'{pwd.getpwuid(os.getuid()).pw_dir}/FlaskJUMP-Projects'

        # print('\n\033[47;30m FlaskJUMP \033[m\n')

        for c, cmd in enumerate(sys.argv):
            if cmd == __file__:
                continue

            try:
                self.commands[cmd]
            except KeyError as err:
                print(err)
                print(f'\033[31m❌: {cmd} não é reconhecido como um comando do FlaskJUMP.\033[m')
                return
            else:
                self.commands[cmd](sys.argv[1:])
                exit()

    def help_cli(self, cmd):
        print('OK...')
        pass


    def save_changes(self):
        with open('config.flaskjump.json', 'w') as config:
            json.dump(self.config_flaskjump, config,indent=4)


    def set(self, cmd):
        for c, cd in enumerate(cmd):
            if len(cmd) <= 1:
                print('\033[32m🔎 Digite -help para ver a lista e comandos!\033[m')

            if cd == 'set':
                continue

            if cd == 'default':
                if len(cmd) == 2:
                    print('\033[32m🔎 Digite -help para ver a lista de comandos em "set default"!\033[m')
                    return

                if cmd[c+1] == 'port':
                    self.config_flaskjump['@default-port'] = int(cmd[c+2])
                    print(f'\033[32m✅: Porta foi alterada para {cmd[c+2]}\033[m')
                elif cmd[c+1] == 'host':
                    self.config_flaskjump['@default-host'] = cmd[c+2]
                    print(f'\033[32m✅: Host foi alterado para {cmd[c+2]}\033[m')
                else:
                    print(f'\033[31m❌: {cmd+1} não é reconhecido como um parâmetro do comando {cmd} do FlaskJUMP.\033[m')
                    return
                self.save_changes()
                exit()
            else:
                print(f'\033[31m❌: {cd} não é reconhecido como um comando do FlaskJUMP.\033[m')
                return


    def activate(self, cmd):
        for c, cd in enumerate(cmd):
            if len(cmd) == 1:
                print('\033[32m🔎 Digite -help para ver a lista e comandos!\033[m')

            if cd == 'activate':
                continue

            if cd == 'auto-install-dependencies':
                if self.config_flaskjump['@auto-install-dependencies']:
                    print(f'\033[32m✅: Instalação automática de dependencias já está ativado!\033[m')
                else:
                    self.config_flaskjump['@auto-install-dependencies'] = True
                    print(f'\033[32m✅: Instalação automática de dependencias foi ativado!\033[m')
                    self.save_changes()
            elif cd == 'auto-gitignore':
                if self.config_flaskjump['@auto-gitignore']:
                    print(f'\033[32m✅: .gitignore automático já está ativado!\033[m')
                else:
                    self.config_flaskjump['@auto-install-dependencies'] = True
                    print(f'\033[32m✅: .gitignore automático foi ativado!\033[m')
                    self.save_changes()
            else:
                print(f'\033[31m❌: {cd} não é reconhecido como um parâmetro do comando {cd} FlaskJUMP.\033[m')
                return


    def deactivate(self, cmd):
        for c, cd in enumerate(cmd):
            if len(cmd) == 1:
                print('\033[32m🔎 Digite -help para ver a lista e comandos!\033[m')

            if cd == 'deactivate':
                continue

            if cd == 'auto-install-dependencies':
                if not self.config_flaskjump['@auto-install-dependencies']:
                    print(f'\033[32m✅: Instalação automática de dependencias já está desativado!\033[m')
                else:
                    self.config_flaskjump['@auto-install-dependencies'] = False
                    print(f'\033[32m✅: Instalação automática de dependencias foi desativado!\033[m')
                    self.save_changes()
            elif cd == 'auto-gitignore':
                if not self.config_flaskjump['@auto-gitignore']:
                    print(f'\033[32m✅: .gitignore automático já está desativado!\033[m')
                else:
                    self.config_flaskjump['@auto-gitignore'] = False
                    print(f'\033[32m✅: .gitignore automático foi desativado!\033[m')
                    self.save_changes()
            else:
                print(f'\033[31m❌: {cd} não é reconhecido como um parâmetro do comando {cd} FlaskJUMP.\033[m')
                return

            
    def init_project(self, name):
        print('\n\033[47;30m FlaskJUMP \033[m\n')

        init = Init(name[1])
        print('\033[32m🔧: Obtendo configurações...\033[m')
        list_create = [init.createProject, init.createFolders, init.createFiles]
        list_name = ['Criando projeto', 'Criando pastas', 'Criando arquivos']

        with tqdm(total=100) as tq:
            for i in range(3):
                sleep(0.5)
                res = list_create[i]()
                tq.set_description_str(list_name[i])
                if not res:
                    return
                else:
                    tq.update(33.33)

            tq.close()

        print('\n🛠: Projeto criado com sucesso!')
        print(f'\033[32mAcesse "{self.config_flaskjump["@default-directory"]}/{name[1]}" para iniciar o seu desenvolvimento.\033[m')


class Init:
    def __init__(self, project_name):
        self.configs = json.load(open('config.flaskjump.json', 'r'))

        self.auto_install_dependencies = self.configs['@auto-install-dependencies']
        self.auto_gitignore = self.configs['@auto-gitignore']
        self.default_port = self.configs['@default-port']
        self.default_host = self.configs['@default-host']
        self.root_directory = self.configs['@default-directory']
        
        self.project_name = project_name

    
    def createProject(self):
        try:
            os.mkdir(f'{self.root_directory}/{self.project_name}')
        except:
            print('\033[31m❌: Esse projeto já existe ou um erro desconhecido ocorreu.\033[m')
            return False
        else:
            return True

    def createFolders(self):
        list_folder = ['public', 'templates', 'routes']
        for folder in list_folder:
            try:
                os.mkdir(f'{self.root_directory}/{self.project_name}/{folder}')
                if folder == 'public':
                    os.mkdir(f'{self.root_directory}/{self.project_name}/{folder}/css')
                    os.mkdir(f'{self.root_directory}/{self.project_name}/{folder}/js')
            except:
                print(f'\033[32m❌: Ocorreu um erro inesperado ao criar a pasta "{folder}"')
                return False
            else:
                continue

        return True

    def createFiles(self):
        with open(f'{self.root_directory}/{self.project_name}/app.py', 'w') as app:
            c = code_app.format(self.project_name, self.default_port, self.default_host)
            app.write(c)

        with open(f'{self.root_directory}/{self.project_name}/templates/index.html', 'w') as html:
            html.write(code_html.strip())

        if self.auto_gitignore:
            with open(f'{self.root_directory}/{self.project_name}/.gitignore', 'w') as ignore:
                ignore.write(code_ignore.strip())

        if self.auto_install_dependencies:
            code_requirements = f"""
            flask
            werkzeug
            """

            with open(f'{self.root_directory}/{self.project_name}/requirements.txt', 'w') as req:
                req.write(code_requirements.strip())

        return True

line = CLI()