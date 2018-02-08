class UpgradeRubyVersion:
    def __init__(self, cmd_gateway, file_gateway, logger):
        self.cmd_gateway = cmd_gateway
        self.file_gateway = file_gateway
        self.logger = logger

    def execute(self, path_to_project, ruby_version):
        self.cmd_gateway.change_directory(path_to_project)
        if ruby_version == self.file_gateway.get_ruby_version():
            self.logger.log(path_to_project + '\tNothing to do')
            return
        if not self.cmd_gateway.create_branch():
            self.logger.log(path_to_project + '\tError: Branch creation failed')
            return
        self.file_gateway.update_ruby_version(ruby_version)
        if not self.cmd_gateway.commit_ruby_version(ruby_version):
            self.logger.log(path_to_project + '\tError: Ruby version commit failed')
            return
        if not self.cmd_gateway.bundle_update():
            self.logger.log(path_to_project + '\tError: Bundle update failed')
            return
        if not self.cmd_gateway.commit_bundle_update():
            self.logger.log(path_to_project + '\tError: Bundle update commit failed')
            return
        tests_passed = self.cmd_gateway.run_tests()
        if tests_passed:
            self.logger.log(path_to_project + '\tPASS')
        else:
            self.logger.log(path_to_project + '\tFAIL')
