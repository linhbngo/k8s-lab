import geni.portal as portal
import geni.rspec.pg as pg
import geni.rspec.igext as IG
import profile_master, profile_worker

pc = portal.Context()

pc.defineParameter( "n", 
                   "Number of nodes (2 or more)", 
                   portal.ParameterType.INTEGER, 2 )
pc.defineParameter( "userid", 
                   "CloudLab user ID to deploy K8s from (should be your CloudLab ID. Defaulted to none", 
                   portal.ParameterType.STRING, 'none' )
pc.defineParameter( "corecount", 
                   "Number of cores in each node.  NB: Make certain your requested cluster can supply this quantity.", 
                   portal.ParameterType.INTEGER, 2 )
pc.defineParameter( "ramsize", "MB of RAM in each node.  NB: Make certain your requested cluster can supply this quantity.", 
                   portal.ParameterType.INTEGER, 2048 )
pc.defineParameter("storage", "GB of storage for each node",
                   portal.ParameterType.INTEGER, 500)
pc.defineParameter("disk_image", "Disk Image for each node",
                   portal.ParameterType.ENUM, 
                   "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU22-64-STD"
                   [
                      "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU18-64-STD",
                      "urn:publicid:IDN+emulab.net+image+emulab-ops:UBUNTU20-64-STD",
                      "urn:publicid:IDN+utah.cloudlab.us+image+emulab-ops:UBUNTU18-64-A-OSCP-T",
                      "urn:publicid:IDN+utah.cloudlab.us+image+emulab-ops:UBUNTU22-64-ARM"
                   ]
                   )

params = pc.bindParameters()

def return_param():
    return params

request = pc.makeRequestRSpec()

tourDescription = \
"""
This profile provides the template for Docker and Rancher/RKE2 Kubernetes installed on Ubuntu 22.04
"""

#
# Setup the Tour info with the above description and instructions.
#  
tour = IG.Tour()
tour.Description(IG.Tour.TEXT,tourDescription)
request.addTour(tour)

prefixForIP = "192.168.1."
link = request.LAN("lan")

num_nodes = params.n
storage = params.storage
disk_image = params.disk_image

def return_numnodes():
    return num_nodes

for i in range(num_nodes):
  if i == 0:
    node = request.XenVM("head")
    bs_landing = node.Blockstore("bs_image", "/image")
    bs_landing.size = storage
  else:
    node = request.XenVM("worker-" + str(i))
  node.cores = params.corecount
  node.ram = params.ramsize
  bs_landing = node.Blockstore("bs_" + str(i), "/image")
  bs_landing.size = storage
  node.routable_control_ip = "true" 
  node.disk_image = disk_image
  iface = node.addInterface("if" + str(i))
  iface.component_id = "eth1"
  iface.addAddress(pg.IPv4Address(prefixForIP + str(i + 1), "255.255.255.0"))
  link.addInterface(iface)
  
  # install Docker
  profile_master.install_docker()
  profile_worker.install_docker()
  # install Kubernetes
  profile_master.install_k8s()
  profile_worker.install_k8s()
  
  if i == 0:
    # install Kubernetes manager
    profile_master.install_k8s_manager()
    # install Helm
    profile_master.install_helm()
  else:
    profile_worker.install_k8s_worker()
    
pc.printRequestRSpec(request)
