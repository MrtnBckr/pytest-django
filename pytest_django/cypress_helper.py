import subprocess

import pytest
from django.conf import settings


class CypressTestApplication(object):
    """The cypress_test fixture

    This is the object that the ``cypress_test`` fixture initializes.
    The method ``run_test`` is returned by the fixture.
    """

    def __init__(self, url, config):
        self.url = url
        self.config = config
        self._base_command = settings.CYPRESS_RUN_COMMAND

        if not self._base_command:
            raise Exception("Path to cypress run has to be defined!")

    def run_test(self, spec: str, video: bool = False, env: dict = None) -> None:
        video_option = "true" if video else "false"
        command = "{} --config baseUrl={},video={} --spec '{}'".format(
            self._base_command, self.url, video_option, spec
        )

        if not env:
            env = {}
        env_option = ",".join(
            ["{}={}".format(key, value) for key, value in env.items()]
        )
        command += "--env {}".format(env_option)
        verbose = self.config.getoption("verbose") > 0

        try:
            output = subprocess.check_output([command], shell=True)
            if verbose:
                print(output.decode())
        except subprocess.CalledProcessError as error:
            pytest.fail(error.output)
