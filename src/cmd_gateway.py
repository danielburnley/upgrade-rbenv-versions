import os
import subprocess

LOGFILE = open('/dev/null', 'w')

class CmdGateway:
    def change_directory(self, directory):
        os.chdir(directory)

    def create_branch(self):
        return subprocess.call(
            ["git", "checkout", "-b", "upgrade-ruby"]
        ) == 0

    def commit_ruby_version(self, ruby_version):
        return self.__git_add(".ruby-version") == 0 and self.__git_commit('Update Ruby to ' + ruby_version) == 0

    def bundle_update(self):
        return subprocess.call(
            ["bundle", "update"]
        ) == 0

    def commit_bundle_update(self):
        return self.__git_add("Gemfile.lock") == 0 and self.__git_commit("Run bundle update") == 0

    def run_tests(self):
        return subprocess.call(
            ["bundle", "exec", "rake"]
        ) == 0

    def __git_add(self, file):
        return subprocess.call(
            ["git", "add", file]
        )

    def __git_commit(self, message):
        return subprocess.call(
            ["git", "commit", "-m", message]
        )
