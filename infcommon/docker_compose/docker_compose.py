import os
import subprocess


class DockerComposeService(object):
    def __init__(self, base_dir, docker_compose_file_name):
        self.BASE_DIR = base_dir or os.environ['DOCKER_COMPOSE_ETC']
        self.DEFAULT_DOCKER_COMPOSE_FILE_NAME = docker_compose_file_name or 'docker-compose.yml'

    def container_names(self):
        container_names = os.listdir(self.BASE_DIR)
        container_names.append('*')
        return container_names

    def restart_process(self, name):
        self.stop_process(name)
        self._start_process(name)

    def _start_process(self, name):
        docker_compose_file_name = self.DEFAULT_DOCKER_COMPOSE_FILE_NAME
        subprocess.call('cd {base_dir}/{name} && docker-compose -f {dc_file_name} up -d'.format(base_dir=self.BASE_DIR,
                                                                                                name=name,
                                                                                                dc_file_name=docker_compose_file_name),
                        shell=True)

    def stop_process(self, name):
        docker_compose_file_name = self.DEFAULT_DOCKER_COMPOSE_FILE_NAME
        subprocess.call('cd {base_dir}/{name} && docker-compose -f {dc_file_name} stop && docker-compose -f {dc_file_name} rm -f'.format(base_dir=self.BASE_DIR,
                                                                                                                                         name=name,
                                                                                                                                         dc_file_name=docker_compose_file_name),
                        shell=True)

    def process_status(self, name):
        docker_compose_file_name = self.DEFAULT_DOCKER_COMPOSE_FILE_NAME
        subprocess.call('cd {base_dir}/{name} && docker-compose -f {dc_file_name} ps'.format(base_dir=self.BASE_DIR,
                                                                                             name=name,
                                                                                             dc_file_name=docker_compose_file_name),
                        shell=True)

    def log_for(self, grep_pattern=None):
        log_path = '/var/log/docker.log'

        try:
            if grep_pattern is None:
                subprocess.call('tail -f {log_path}'.format(log_path=log_path), shell=True)
            else:
                subprocess.call('tail -f {log_path} | grep {grep_pattern}'.format(log_path=log_path,
                                                                                  grep_pattern=grep_pattern),
                                shell=True)
        except KeyboardInterrupt:
            pass
