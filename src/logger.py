class Logger:
    def __init__(self):
        self.file = open('ruby-upgrade.log', 'w')

    def log(self, message):
        self.file.write(message + '\n')
