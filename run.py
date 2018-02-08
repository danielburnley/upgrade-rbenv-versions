import sys
from src.cmd_gateway import CmdGateway
from src.file_gateway import FileGateway
from src.logger import Logger
from src.upgrade_ruby_version import UpgradeRubyVersion

def repos():
    repo_list = []
    with open('repos.txt', 'r') as file:
        repo_list = [repo.strip() for repo in file.readlines()]
    return repo_list

def get_ruby_version():
    ruby_version = ""
    try:
        ruby_version = sys.argv[1].strip()
    except IndexError:
        print("You must provide a ruby version!")
        raise RuntimeError
    return ruby_version

usecase = UpgradeRubyVersion(
    CmdGateway(),
    FileGateway(),
    Logger()
)

ruby_version = get_ruby_version()
print("Upgrading to ruby version: " + ruby_version)

for repo in repos():
    usecase.execute(repo, ruby_version)
