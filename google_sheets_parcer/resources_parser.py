import os
import git
import yaml
import csv
import re
import time
import gspread
from pydrive.auth import ServiceAccountCredentials
# import pdb; pdb.set_trace()


class Env:

    def __init__(self, name):
        self.name = name
        self.projects = []
        self.sum_metrics = None

    def get_project(self, name):
        for prj in self.projects:
            if prj.name == name:
                return prj
        prj = Project(name)
        self.projects.append(prj)
        return prj

    def calc(self):
        sum_min_CPU = 0
        sum_max_CPU = 0
        sum_min_MEM = 0
        sum_max_MEM = 0

        int_sum_min_CPU = 0
        int_sum_max_CPU = 0
        int_sum_min_MEM = 0
        int_sum_max_MEM = 0

        for prj in self.projects:
            sum_min_CPU += prj.sum_metrics.min_CPU
            sum_max_CPU += prj.sum_metrics.max_CPU
            sum_min_MEM += prj.sum_metrics.min_MEM
            sum_max_MEM += prj.sum_metrics.max_MEM
        self.sum_metrics = Calculator(sum_min_CPU, sum_max_CPU, sum_min_MEM, sum_max_MEM)

        for prj in self.projects:
            int_sum_min_CPU += prj.sum_metrics_int.min_CPU
            int_sum_max_CPU += prj.sum_metrics_int.max_CPU
            int_sum_min_MEM += prj.sum_metrics_int.min_MEM
            int_sum_max_MEM += prj.sum_metrics_int.max_MEM
        self.sum_metrics_int = Calculator(int_sum_min_CPU, int_sum_max_CPU, int_sum_min_MEM, int_sum_max_MEM)

    def __repr__(self):
        return "Env: {0}\n Projects: {1}".format(self.name, self.projects)


class Project:

    def __init__(self, name):
        self.name = name
        self.services = []
        self.sum_metrics = None

    def get_service(self, name):
        for srv in self.services:
            if srv.name == name:
                return srv
        srv = Service(name)
        self.services.append(srv)
        return srv

    def calc(self):
        sum_min_CPU = 0
        sum_max_CPU = 0
        sum_min_MEM = 0
        sum_max_MEM = 0

        int_sum_min_CPU = 0
        int_sum_max_CPU = 0
        int_sum_min_MEM = 0
        int_sum_max_MEM = 0

        for srv in self.services:
            sum_min_CPU += srv.sum_metrics.min_CPU
            sum_max_CPU += srv.sum_metrics.max_CPU
            sum_min_MEM += srv.sum_metrics.min_MEM
            sum_max_MEM += srv.sum_metrics.max_MEM
        self.sum_metrics = Calculator(sum_min_CPU, sum_max_CPU, sum_min_MEM, sum_max_MEM)

        for srv in self.services:
            int_sum_min_CPU += srv.sum_metrics_int.min_CPU
            int_sum_max_CPU += srv.sum_metrics_int.max_CPU
            int_sum_min_MEM += srv.sum_metrics_int.min_MEM
            int_sum_max_MEM += srv.sum_metrics_int.max_MEM
        self.sum_metrics_int = Calculator(int_sum_min_CPU, int_sum_max_CPU, int_sum_min_MEM, int_sum_max_MEM)

    def __repr__(self):
        return "\nProject: {0}\nServices: {1}".format(self.name, self.services)


class Service:

    def __init__(self, name):
        self.name = name
        self.pods = []
        self.sum_metrics = None
        self.sum_metrics_int = None

    def get_pod(self, name):
        for pod in self.pods:
            if pod.name == name:
                return pod
        pod = Pod(name)
        self.pods.append(pod)
        return pod

    def calc(self):
        sum_min_CPU = 0
        sum_max_CPU = 0
        sum_min_MEM = 0
        sum_max_MEM = 0

        int_sum_min_CPU = 0
        int_sum_max_CPU = 0
        int_sum_min_MEM = 0
        int_sum_max_MEM = 0

        for pod in self.pods:
            sum_min_CPU += pod.sum_metrics.min_CPU
            sum_max_CPU += pod.sum_metrics.max_CPU
            sum_min_MEM += pod.sum_metrics.min_MEM
            sum_max_MEM += pod.sum_metrics.max_MEM

        for pod in self.pods:
            int_sum_min_CPU += pod.sum_metrics.min_CPU / pod.replicas
            int_sum_max_CPU += pod.sum_metrics.max_CPU / pod.replicas
            int_sum_min_MEM += pod.sum_metrics.min_MEM / pod.replicas
            int_sum_max_MEM += pod.sum_metrics.max_MEM / pod.replicas

        self.sum_metrics = Calculator(sum_min_CPU, sum_max_CPU, sum_min_MEM, sum_max_MEM)
        self.sum_metrics_int = Calculator(int_sum_min_CPU, int_sum_max_CPU, int_sum_min_MEM, int_sum_max_MEM)

    def __repr__(self):
        return "\nService: {0}\nPods: {1}".format(self.name, self.pods)


class Pod:

    def __init__(self, name):
        self.name = name
        self.containers = []
        self.replicas = None
        self.sum_metrics = None

    def add_container(self, cnt):
        # for cnt in self.containers:
        #     if cnt.name == name:
        #         return cnt
        self.containers.append(cnt)
        return cnt

    def calc(self):
        sum_min_CPU = 0
        sum_max_CPU = 0
        sum_min_MEM = 0
        sum_max_MEM = 0

        for cnt in self.containers:
            sum_min_CPU += self.none_checker(cnt.metrics.min_CPU) * self.replicas
            sum_max_CPU += self.none_checker(cnt.metrics.max_CPU) * self.replicas
            sum_min_MEM += self.none_checker(cnt.metrics.min_MEM) * self.replicas
            sum_max_MEM += self.none_checker(cnt.metrics.max_MEM) * self.replicas
        self.sum_metrics = Calculator(sum_min_CPU, sum_max_CPU, sum_min_MEM, sum_max_MEM)

    @staticmethod
    def none_checker(mtr):
        if mtr is None:
            return 0
        else:
            return mtr

    def __repr__(self):
        return "\nPod: {0} |Replicas: {2}\nContainers: {1}".format(self.name, self.containers, self.replicas)


class Container:

    def __init__(self, name, metrics):
        self.name = name
        self.metrics = metrics

    def __repr__(self):
        return "\nContainer: {0}\n \tMetrics: {1}".format(self.name, self.metrics)


class Metrics:

    def __init__(self):
        self.min_CPU = None
        self.max_CPU = None
        self.min_MEM = None
        self.max_MEM = None

    def __repr__(self):
        return "\n\t\tmin_CPU: {0} \n\t\tmax_CPU: {1} \n\t\tmin_MEM: {2} \n\t\tmax_MEM: {3}".format(self.min_CPU, self.max_CPU,
                                                                                  self.min_MEM, self.max_MEM)


class Calculator:

    def __init__(self, min_CPU, max_CPU, min_MEM, max_MEM):
        self.min_CPU = min_CPU
        self.max_CPU = max_CPU
        self.min_MEM = min_MEM
        self.max_MEM = max_MEM


class Summarizer:

    def __init__(self, envs):
        self.envs = envs

    def sum(self):
        for env in self.envs:
            for prj in env.projects:
                for srv in prj.services:
                    for pod in srv.pods:
                        pod.calc()
                    srv.calc()
                prj.calc()
            env.calc()


class Repository:

    def __init__(self, git_url):

        self.local_path = os.getcwd() + '/repo'
        self.git_url = git_url

        print("Cloning repo in {0}".format(self.local_path))

        try:
            git.Repo.clone_from(self.git_url, self.local_path)
        except git.exc.GitCommandError as err:
            print(err)

        self.repo = git.Repo(self.local_path)

        print("Active branch: {0}".format(self.repo.active_branch))
        print("- : {0}".format(self.repo))


class Parser:
    """
    :param repo, folders
    :returns nested dict with metrics
    """

    def __init__(self, repo, to_check_folders, envs):
        self.repo_path = repo  # Local system path to repository
        self.required_files_path = []  # Array with all files from folders to check
        self.to_check_folders = to_check_folders
        self.envs = envs
        # todo git webhooks after commit

    def searcher(self, path):
        """
        function recursivelly searches all files from the given file path

        :param path: folder path
        :return: all files full path, from given folder
        """

        for file in os.listdir(path):
            file_path = str(path + '/' + file)

            if os.path.isdir(file_path):
                self.searcher(file_path)
            else:
                self.required_files_path.append(file_path)

        return self.required_files_path

    def search_required_folders(self, folders):
        """
        :param folders: folders required to check
        :return: all files full paths
        """

        for folder in folders:
            folder = self.repo_path + "/" + folder
            try:
                for file in os.listdir(folder):
                    file_path = str(folder + '/' + file)
                    if os.path.isdir(file_path):
                        self.searcher(file_path)
                    else:
                        self.required_files_path.append(file_path)
            except FileNotFoundError as err:
                print("Directory not found: {0}".format(err))
        return self.required_files_path

    def parse(self):

        required_files = self.search_required_folders(self.to_check_folders)
        self.fill_the_structure(required_files)  # Getting files from to_check_folders to parse

    def fill_the_structure(self, files):
        """
        :param files to parse
        :return: list of dicts for each env
        """
        files_parsed = 0
        files_failed_to_parse = 0
        for file in files:
            data = self.check_file_kind(file)
            if data:
                print("Checking file: {0}".format(file))
                # print("Data: {0}".format(data))
                self.parse_yaml(file, data)
                files_parsed+=1
        print("Files parsed: {0}".format(files_parsed))
        return self.envs

    def check_file_kind(self, file):
        if file.lower().endswith('.yaml'):
            with open(file, 'r') as stream:
                try:
                    for data in yaml.load_all(stream):
                        if data:
                            if data.get('kind', None) == 'Deployment':
                                return data
                            else:
                                return False
                except AttributeError as err:
                    print("=> Error parsing yaml file: {0} \n Error: {1}".format(file, err))
                    return False

                except yaml.YAMLError as err:
                    print("=> Error parsing yaml file: {0} \n Error: {1}".format(file, err))
                    return False
        else:
            return False

    def get_env(self, name):
        for env in self.envs:
            if env.name == name:
                return env
        env = Env(name)
        self.envs.append(env)
        return env

    def parse_yaml(self, file, data):
        env = self.get_env(file.split('/')[-2])
        # prj = env.get_project(file[(file.index('/deployment/') + len('/deployment/')):file.index("/" + env.name)])
        prj = env.get_project(file.split('/')[file.split('/').index('deployment') + 1])

        if data.get('metadata', {}).get('name', None):
            srv = prj.get_service(data['metadata']['name'])
            pod_replicas = data.get('spec', {}).get('replicas', None)
            if data.get('spec', {}).get('template', {}).get('metadata', {}).get('labels', {}).get('app', None):
                pod = srv.get_pod(data['spec']['template']['metadata']['labels']['app'])
                pod.replicas = pod_replicas
            else:
                pod = srv.get_pod(srv.name)
                pod.replicas = pod_replicas
                if data.get('spec', {}).get('template', {}).get('spec', {}).get('containers', None):
                    for container in data['spec']['template']['spec']['containers']:
                        metrics = Metrics()
                        if container.get('resources', None):
                            if container['resources'].get('requests', None):
                                metrics.min_CPU = container['resources']['requests'].get('cpu', 0)
                                metrics.min_MEM = container['resources']['requests'].get('memory', 0)
                            if container['resources'].get('limits', None):
                                metrics.max_CPU = container['resources']['limits'].get('cpu', 0)
                                metrics.max_MEM = container['resources']['limits'].get('memory', 0)

                        metrics.min_CPU = self.metric_recalculation(metrics.min_CPU)
                        metrics.max_CPU = self.metric_recalculation(metrics.max_CPU)
                        metrics.max_MEM = self.metric_recalculation(metrics.max_MEM)
                        metrics.min_MEM = self.metric_recalculation(metrics.min_MEM)

                        cnt = Container(container.get('name', None), metrics)
                        pod.add_container(cnt)

    def metric_recalculation(self, metric):
        if type(metric) is int:
            return metric
        if type(metric) is str:
            if 'm' in metric:
                return int(re.findall('\d+', str(metric))[0]) / 1000
            elif 'Gi' in metric:
                return int(re.findall('\d+', str(metric))[0]) * 1000
            elif 'Mi' in metric:
                return int(re.findall('\d+', str(metric))[0])
        if type(metric) is None:
            return int(0)


class Printer:

    def __init__(self, envs):
        self.envs = envs

    def print(self):
        for env in envs:
            print("Env: " + env.name)
            for prj in env.projects:
                print("- Project: " + prj.name)
                for srv in prj.services:
                    print(" - Service: " + srv.name)
                    for pod in srv.pods:
                        print("  - Pod: " + pod.name)
                        print("    Replicas: {0}".format(pod.replicas))
                        for cnt in pod.containers:
                            print("   - Container: {0}".format(cnt.name))
                            print("     {0}".format(cnt.metrics))


class CSVPrinter(Printer):

    def __init__(self, envs):
        self.headers = ["Project", "Service", "Pod", "Summary", "Replicas", "Container", "min_CPU", "max_CPU",
                        "min_MEM", "max_MEM"]
        super(CSVPrinter, self).__init__(envs)

    def write_row(self, *arg):
        self.csv_env.append([*arg])

    def print_to_files(self):

        csv_files_dir = os.getcwd() + '/envs/'
        print("Printing to files to {0}".format(csv_files_dir))
        if not os.path.exists(csv_files_dir):
            os.makedirs(csv_files_dir)

        files = []
        env_names = []
        for env in self.envs:
            with open(csv_files_dir + env.name, "w") as file:
                writer = csv.DictWriter(file, self.headers)
                writer.writeheader()
                for row in self.print_env(env):
                    writer.writerow(dict(zip(self.headers, row)))
            files.append(csv_files_dir + env.name)
            env_names.append(env.name)
        return env_names, files

    def print_env(self, env):
        self.csv_env = []
        for prj in env.projects:
            for srv in prj.services:
                for pod in srv.pods:
                    for cnt in pod.containers:
                        self.write_row(prj.name, srv.name, pod.name, None, None, cnt.name,
                                       cnt.metrics.min_CPU, cnt.metrics.max_CPU, cnt.metrics.min_MEM, cnt.metrics.max_MEM)

                    self.write_row(prj.name, srv.name, pod.name, "by pod", pod.replicas, None,
                                    pod.sum_metrics.min_CPU, pod.sum_metrics.max_CPU, pod.sum_metrics.min_MEM, pod.sum_metrics.max_MEM)
                    self.write_row(None, None, None, None, None, None, None, None, None, None)

                self.write_row(prj.name, srv.name, None, "by service", None, None,
                                    srv.sum_metrics.min_CPU, srv.sum_metrics.max_CPU, srv.sum_metrics.min_MEM, srv.sum_metrics.max_MEM)
                self.write_row(prj.name, srv.name, None, "by service(integration)", None, None,
                                    srv.sum_metrics_int.min_CPU, srv.sum_metrics_int.max_CPU, srv.sum_metrics_int.min_MEM, srv.sum_metrics_int.max_MEM)

            self.write_row(None, None, None, None, None, None, None, None, None, None)
            self.write_row(prj.name, None, None, "by project", None, None,
                           prj.sum_metrics.min_CPU, prj.sum_metrics.max_CPU, prj.sum_metrics.min_MEM, prj.sum_metrics.max_MEM)
            self.write_row(prj.name, None, None, "by project(integration)", None, None,
                           prj.sum_metrics_int.min_CPU, prj.sum_metrics_int.max_CPU, prj.sum_metrics_int.min_MEM, prj.sum_metrics_int.max_MEM)
            self.write_row(None, None, None, None, None, None, None, None, None, None)

        self.write_row(None, None, None, None, None, None, None, None, None, None)
        self.write_row(None, None, None, "Total", None, None,
                       env.sum_metrics.min_CPU, env.sum_metrics.max_CPU, env.sum_metrics.min_MEM, env.sum_metrics.max_MEM)
        self.write_row(None, None, None, "Total(integration)", None, None,
                       env.sum_metrics_int.min_CPU, env.sum_metrics_int.max_CPU, env.sum_metrics_int.min_MEM, env.sum_metrics_int.max_MEM)

        return self.csv_env

    def print(self):
        for env in envs:
            return env.name, self.print_env(env)

    def print_by_env(self, env):
        return env.name, self.print_env(env)


class CSVImporter:
    def __init__(self, credentials):

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        self.credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials, scope)
        self.gc = gspread.authorize(self.credentials)

    def create_sheet(self, sh_name, mail):
        
        self.sh = self.gc.create(sh_name)
        self.sh.share('mail', perm_type='user', role='writer')
        return self.sh

    def calculate_env_size(self, metrics):
        rows = len(metrics)
        cols = len(metrics[0])
        print("rows: {0} \ncolumns: {1}".format(rows, cols))
        return rows, cols

    def import_env(self, sheet_key, env_name, metrics, mail):

        print("Updating env: {0}".format(env_name))

        try:
            sheet = self.gc.open_by_key(sheet_key)
            print("Opening sheet: {0}".format(sheet.title))
        except Exception:
            print("Creating new sheet: {0}".format(sheet.title))
            sheet = self.create_sheet(sheet_key, mail)

        rows, cols = self.calculate_env_size(metrics)

        try:
            sheet.del_worksheet(sheet.worksheet(env_name))
        except gspread.exceptions.WorksheetNotFound:
            print("Creating new worksheet: {0}".format(env_name))

        wsh = sheet.add_worksheet(title=env_name, rows=rows, cols=cols)

        self.update_by_cell(wsh, metrics)

    def update_by_cell(self, wsh, metrics):

        if self.credentials.access_token_expired:
            print("Refreshing token")
            self.gc.login()

        for row_i, row in enumerate(metrics):
            print(row_i, row)
            for col_i, cell in enumerate(row):
                print(row_i + 1, col_i + 1, cell)
                wsh.update_cell(row_i + 1, col_i + 1, cell)
                time.sleep(1)

    def update_wsh(self, wsh, metrics):

        cell_list = []
        for row_i, row in enumerate(metrics):
            for col_i, value in enumerate(row):
                print(row_i + 1, col_i + 1, value)
                cellToUpdate = wsh.cell(row_i + 1, col_i + 1)
                cellToUpdate.value = value
                cell_list.append(cellToUpdate)

        # print("cell_list:")
        # print(cell_list)
        wsh.update_cells(cell_list)


if __name__ == '__main__':

    # todo argparse

    # Execution parameters
    repo_url = 'git@github.com:amaslakou/saas-app-deployment.git'
    to_check_folders = ["folder1", "folder2", "folder3"]
    google_sheet_key = '1b34X*****************'
    credentials_importer = os.getcwd() + '/service_account.json'
    mail = 'YOUR_MAIL_ADDR@gmail.com'

    # Downloading repository
    repo = Repository(repo_url)
    repository = repo.local_path

    # Parse required folders, create envs structure
    envs = []
    parser = Parser(repo.local_path, to_check_folders, envs)
    parser.parse()

    if not envs:
        print("No metrics found")
        exit()
    else:
        printer = Printer(envs)
        printer.print()

    # Add sum values in envs structure
    summarizer = Summarizer(envs)
    summarizer.sum()

    csv_printer = CSVPrinter(envs)

    # Prints CSV to local files
    csv_printer.print_to_files()

    # Authenticate in Google
    print(credentials_importer)

    # Writing envs to Google Sheets
    for env in envs:
        env_name, env_metrics = csv_printer.print_by_env(env)
        csv_importer = CSVImporter(credentials_importer)
        csv_importer.import_env(google_sheet_key, env_name, env_metrics, mail)