class FileGateway:
    def get_ruby_version(self):
        return open('.ruby-version', 'r').read().strip()

    def update_ruby_version(self, new_version):
        with open('.ruby-version', 'w') as f:
            f.write(new_version + '\n')
