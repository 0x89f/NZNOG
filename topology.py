import requests
import re
from flask import Flask, jsonify, render_template
url = "http://192.168.100.130:8181/restconf/operational/network-topology:network-topology/topology/bgp-example-linkstate-topology"
auth = requests.auth.HTTPBasicAuth('admin', 'admin')
response = requests.get(url, auth=auth)
rjson = response.json()
topology_raw = rjson['topology']

def toMKG(x):

    '''

    Function to convert Bandwidth to readable units

    '''
    x = float(x*8)
    if x >= 1000000000 : 
        return str(round(x/1000000000,4)) + " Gbps"
    
    elif x >= 1000000 : 
        return str(round(x/1000000,4)) + " Mbps"

    elif x >= 1000 : 
        return str(round(x/1000,4)) + " Kbps"
   
    else :
        return str(x) + " bps"


def get_topology():


  '''

  Function to get topology information - nodes and links in dictionary of lists format

  nodes is a list of nodes - each item a dictionary of attribute(key)/values 
  links is a list of links - each item a dictionary of attribute(key)/values 

  '''
  #Initialization of Topology dictionary, List of Nodes/Links and system_id to name binding
  topology = {} 
  nodes = [] 
  links = [] 
  bind_name_id = {} #

  for i in topology_raw[0]['node'] : 
     k = {}
     name = k['id'] =  i['l3-unicast-igp-topology:igp-node-attributes']['name']
     k['loopback_ip'] =  i['l3-unicast-igp-topology:igp-node-attributes']['router-id'][0]
     k['net'] =  i['l3-unicast-igp-topology:igp-node-attributes']['isis-topology:isis-node-attributes']['net'][0]
     identity =  i['l3-unicast-igp-topology:igp-node-attributes']['isis-topology:isis-node-attributes']['iso']['iso-system-id']
     bind_name_id[identity] = name
     nodes.append(k)




  for i in topology_raw[0]['link'] : 
     k = {}
     link_id = i['link-id']
     s = r'[\d]+\.[\d]+\.[\d]+\.?[\d]*'
     j = re.findall(s,link_id)
     k['source'] = bind_name_id[j[0]]
     k['target'] = bind_name_id[j[1]]
     k['source_linknet'] = j[2]
     k['target_linknet'] = j[3]
     k['te-metric'] =  i['l3-unicast-igp-topology:igp-link-attributes']['isis-topology:isis-link-attributes']['ted']['te-default-metric']
     bandwidth_list =  i['l3-unicast-igp-topology:igp-link-attributes']['isis-topology:isis-link-attributes']['ted']['unreserved-bandwidth']

     k['unreserved-bw-p0'] =  toMKG(bandwidth_list[1]['bandwidth'])
     k['unreserved-bw-p1'] =  toMKG(bandwidth_list[0]['bandwidth'])
     k['unreserved-bw-p2'] =  toMKG(bandwidth_list[3]['bandwidth'])
     k['unreserved-bw-p3'] =  toMKG(bandwidth_list[2]['bandwidth'])
     k['unreserved-bw-p4'] =  toMKG(bandwidth_list[5]['bandwidth'])
     k['unreserved-bw-p5'] =  toMKG(bandwidth_list[4]['bandwidth'])
     k['unreserved-bw-p6'] =  toMKG(bandwidth_list[7]['bandwidth'])
     k['unreserved-bw-p7'] =  toMKG(bandwidth_list[6]['bandwidth'])

     links.append(k)
     
  topology['nodes'] = nodes
  topology['links'] = links
  return topology 


# intialize a web app
app = Flask(__name__)

# define index route to return topology.html
@app.route("/")
def index():
    # Render 'topology.html' in template folder
    return render_template("topology.html")


# API to get topology data
@app.route("/api/topology")
def topology_api():

    return jsonify(get_topology())

if __name__ == "__main__":
    app.run()

