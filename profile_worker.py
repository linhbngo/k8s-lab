import geni.rspec.pg as pg

def install_docker(node):
    node.addService(pg.Execute(shell="sh", command="sudo bash /local/repository/install_docker.sh"))

def install_k8s(node):
    node.addService(pg.Execute(shell="sh", command="sudo swapoff -a"))

def install_k8s_worker(node):
    node.addService(pg.Execute(shell="sh", command="sudo bash /local/repository/kube_worker.sh"))