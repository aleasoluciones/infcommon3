from infcommon.factory import Factory
from infcommon.docker_compose.docker_compose import DockerComposeService


def docker_compose_service(base_dir=None, docker_compose_file_name=None):
        return Factory.instance('docker_compose_service', lambda: DockerComposeService(base_dir, docker_compose_file_name))
