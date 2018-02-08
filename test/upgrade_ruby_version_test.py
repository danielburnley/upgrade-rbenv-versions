from src.upgrade_ruby_version import UpgradeRubyVersion

class CmdGatewaySpy:
    def __init__(self):
        self.changed_directory = False
        self.directory_changed_to = None
        self.branch_created = False
        self.ruby_version_commited = False
        self.bundle_updated = False
        self.bundle_update_commited = False
        self.tests_run = False
        self.tests_pass = True

    def change_directory(self, directory):
        self.changed_directory = True
        self.directory_changed_to = directory

    def create_branch(self):
        self.branch_created = True

    def commit_ruby_version(self):
        self.ruby_version_commited = True

    def bundle_update(self):
        self.bundle_updated = True

    def commit_bundle_update(self):
        self.bundle_update_commited = True

    def run_tests(self):
        self.tests_run = True
        return self.tests_pass

class FileGatewaySpy:
    def __init__(self):
        self.current_ruby_version = '2.4.2'
        self.ruby_version_updated = False
        self.new_ruby_version = None

    def get_ruby_version(self):
        return self.current_ruby_version

    def update_ruby_version(self, new_version):
        self.ruby_version_updated = True
        self.new_ruby_version = new_version

class LoggerSpy:
    def __init__(self):
        self.messages = []

    def log(self, message):
        self.messages.append(message)

class TestUpgradeRubyVersion:
    def setup_method(self, method):
        self.cmd_gateway = CmdGatewaySpy()
        self.file_gateway = FileGatewaySpy()
        self.logger = LoggerSpy()
        self.usecase = UpgradeRubyVersion(self.cmd_gateway, self.file_gateway, self.logger)

    def test_changes_directory_to_project_directory(self):
        self.usecase.execute('/foo/bar', '2.5.0')

        assert self.cmd_gateway.changed_directory
        assert self.cmd_gateway.directory_changed_to == '/foo/bar'

    def test_given_ruby_at_current_version_do_nothing(self):
        self.file_gateway.current_ruby_version = '2.5.0'
        self.usecase.execute('/foo/bar', '2.5.0')

        assert not self.file_gateway.ruby_version_updated

    def test_given_ruby_version_different_update_version(self):
        self.usecase.execute('/foo/bar', '2.5.0')

        assert self.file_gateway.ruby_version_updated == True
        assert self.file_gateway.new_ruby_version == '2.5.0'

    def test_given_ruby_version_different_change_branch_and_commit_change(self):
        self.usecase.execute('/foo/bar', '2.5.0')

        assert self.cmd_gateway.branch_created
        assert self.cmd_gateway.ruby_version_commited

    def test_given_ruby_version_different_run_bundle_update_and_commit(self):
        self.usecase.execute('/foo/bar', '2.5.0')

        assert self.cmd_gateway.bundle_updated
        assert self.cmd_gateway.bundle_update_commited

    def test_given_ruby_version_different_run_tests(self):
        self.usecase.execute('/foo/bar', '2.5.0')

        assert self.cmd_gateway.tests_run

    def test_given_ruby_at_current_version_log_path_to_project_and_nothing_to_do(self):
        self.file_gateway.current_ruby_version = '2.5.0'
        self.usecase.execute('/foo/bar', '2.5.0')

        assert self.logger.messages[0] == '/foo/bar\tNothing to do'

    def test_given_tests_pass_log_tests_pass(self):
        self.usecase.execute('/foo/bar', '2.5.0')

        assert self.logger.messages[0] == '/foo/bar\tPASS'

    def test_given_tests_fail_log_tests_fail(self):
        self.cmd_gateway.tests_pass = False
        self.usecase.execute('/foo/bar', '2.5.0')

        assert self.logger.messages[0] == '/foo/bar\tFAIL'
