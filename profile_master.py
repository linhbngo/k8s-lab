import geni.rspec.pg as pg
from profile import return_param, return_numnodes

def install_docker(node):
    node.addService(pg.Execute(shell="sh", command="sudo bash /local/repository/install_docker.sh"))

def install_k8s(node):
    node.addService(pg.Execute(shell="sh", command="sudo swapoff -a"))

def install_k8s_manager(node):
    params = return_param()
    num_nodes = return_numnodes()
    node.addService(pg.Execute(shell="sh", command="sudo bash /local/repository/kube_manager.sh " + params.userid + " " + str(num_nodes)))

def install_helm(node):
    node.addService(pg.Execute(shell="sh", command="sudo bash /local/repository/install_helm.sh"))