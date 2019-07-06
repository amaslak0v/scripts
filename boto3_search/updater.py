#!/usr/bin/env python3
# install aws-cli and enter credentials

import boto3
import yaml
from collections import defaultdict


class AWS():

    def __init__(self):
        self.ec2 = boto3.resource('ec2')
        self.ec2info = self.get_ec2info()

    def get_ec2info(self):
        ec2info = defaultdict()
        running_ec2_instances = self.ec2.instances.filter(
            Filters=[{
                'Name': 'instance-state-name',
                'Values': ['running']
            }])
        for instance in running_ec2_instances:
            for tag in instance.tags:
                if 'Name' in tag['Key']:
                    name = tag['Value']
            ec2info[instance.id] = {
                "Name": name,
                "Type": instance.instance_type,
                "State": instance.state["Name"],
                "Public-IP": instance.public_ip_address,
                "Internal-IP": instance.private_ip_address}
        return ec2info

    # def print_all_instances(self):
    #     print("=> Getting all ec2 instances")
    #     for instance_id, instance in self.ec2info.items():
    #         print(instance_id)
    #         for k, v in instance.items():
    #             print("{0}: {1}".format(k, v))
    #
    # def print_jumphosts(self):
    #     print("=> Searching for ec2 instances with public IP")
    #     for instance_id, instance in self.ec2info.items():
    #         if not instance.get("Public-IP") == None:
    #             for k, v in instance.items():
    #                 print("{0}: {1}".format(k, v))

    def find_cluster_instances(self, names):
        cluster_info = defaultdict()
        for name in names:
            print("=> Searching for : {}".format(name))
            for instance_id, instance in self.ec2info.items():
                if instance["Name"] == name:
                    cluster_info[instance_id] = {
                        "Name": name,
                        "Internal-IP": instance["Internal-IP"],
                        "Public-IP": instance["Public-IP"]}
        return cluster_info


class Cluster:

    def __init__(self, file):
        self.file = file
        self.config = self.parse_config()
        self.name = self.config["SSH"]["jump_host"]["name"]
        self.search_instances = self.get_instances_names_for_cluster()
        self.info = defaultdict()

    def get_instances_names_for_cluster(self):
        if self.name == 'qa-0':
            search_instanses = ['QA-0-Core-SDP-QA', 'QA-0-Core-k8s-NGP-QA']
        elif self.name == 'qa-1':
            search_instanses = ['QA-1-Core-SDP-QA', 'QA-1-Core-k8s-NGP-QA']
        elif self.name == 'qa-2':
            search_instanses = ['QA-2-Core-SDP-QA', 'QA-2-Core-k8s-NGP-QA']
        elif self.name == 'qa-4':
            search_instanses = ['QA-4-Core-SDP-Dev', 'QA-4-Core-k8s-NGP-Dev']
        return search_instanses

    def parse_config(self):
        with open(self.file, 'r') as stream:
            try:
                yaml_file = yaml.safe_load(stream)
                return yaml_file
            except yaml.YAMLError as exc:
                print(exc)
                return None

    def update_config(self):
        print("=> Updating {} config".format(self.name))
        core_internal_ip = []
        jumphost_public_ip = self.config["SSH"]["jump_host"]["ip"]

        for cluster_name, cluster_info in self.info.items():
            if cluster_info["Public-IP"]:
                jumphost_public_ip = cluster_info["Public-IP"]
            else:
                core_internal_ip.append(cluster_info["Internal-IP"])

        if self.config["SSH"]["jump_host"]["ip"] != jumphost_public_ip:
            print("=> Changing Jumphost IP to {}".format(jumphost_public_ip))
            self.config["SSH"]["jump_host"]["ip"] = jumphost_public_ip

        if core_internal_ip != self.config["SSH"]["core"]["ips"]:
            print("=> Changing Core IPs to:")
            print(core_internal_ip)
            self.config["SSH"]["core"]["ips"] = core_internal_ip

        stream = open(self.file, 'w')
        yaml.safe_dump(self.config, stream, default_flow_style=False)

    def print_config(self, *args):
        print(self.name)
        print(self.info)

    def print_info(self):
        for cluster_name, cluster_info in self.info.items():
            for k, v in cluster_info.items():
                print("{0}: {1}".format(k, v))


def main():

    # Change Cluster.get_instances_names_for_cluster if instances names in AWS changed.

    aws = AWS()
    cluster = Cluster('config-cluster.yaml')
    cluster.info = aws.find_cluster_instances(cluster.search_instances)
    cluster.update_config()


if __name__ == '__main__':
    main()
