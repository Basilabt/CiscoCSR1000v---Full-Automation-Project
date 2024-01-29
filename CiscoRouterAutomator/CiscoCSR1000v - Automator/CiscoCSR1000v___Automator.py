
from os import system, name
import os
import json
import requests
from enum import Enum


class enUserOption(Enum):
    get_root_resource_discovery = 1
    get_all_interfaces = 2 
    get_specific_interface = 3
    get_interfaces_status = 4
    allowed_methods = 5
    add_new_interface_with_post = 6
    add_new_interface_with_put = 7


class clsCiscoRouter:

     # Welcome To Cisco CSR1000v Router Automator
     # This Program Automates ietf-interfaces YANG Module Through Restfull APIs

    _url:str
    _payload:{}
    _headers:{} 
    _parameters:{}
    _userPass = ("nes470user" , "nes470passwd")
    _interfaceIP = "192.168.229.128"


    def __init__(self):
       requests.packages.urllib3.disable_warnings()
       self._url = ""
       self._payload = dict()
       self._headers = dict()
       self._parameters = dict()


    def runScript(self):
        self._printMenuOptions()
        userOption = self._readUserOption()
        self._performUserOption(userOption)
        pause = input("\n\n\t\t\t\t\t Press Enter to continue...")
        self._goBack()

    def _printMenuOptions(self):
        self._clearScreen()
        print("\n\n\n")
        print("\t\t\t\t\t------------------------------------")
        print("\t\t\t\t\t\t Cisco CSR1000v")
        print("\t\t\t\t\t------------------------------------")
        print("\t\t\t\t\t[1] GET Root Resource Discovery")
        print("\t\t\t\t\t[2] GET Interfaces")
        print("\t\t\t\t\t[3] GET Specific Interface")
        print("\t\t\t\t\t[4] GET Interfaces Status")
        print("\t\t\t\t\t[5] Allowed Methods")
        print("\t\t\t\t\t[6] Add New Interface With POST")
        print("\t\t\t\t\t[7] Add New Interface With PUT")



      
        

    def _readUserOption(self):
          print("\t\t\t\t\t------------------------------------")
          print("\t\t\t\t\t-> Please Enter Option: " , end="")
          option = int(input())
          return enUserOption(option)


    def _performUserOption(self, option: enUserOption):

        if option == enUserOption.get_root_resource_discovery:
            self._getRootResourceDiscovery()
            return 

        if option == enUserOption.get_all_interfaces:
            self._getInterfaces()
            return 

        if option == enUserOption.get_specific_interface:
            self._getSpecificInterface()
            return 

        if option == enUserOption. get_interfaces_status:
            self._getInterfacesStatus()
            return 

        if option == enUserOption.allowed_methods:
            self._discoverAllowedMethods()
            return


        if option == enUserOption.add_new_interface_with_post:
            self._addNewInterfaceWithPOST()
            return 

        if option == enUserOption.add_new_interface_with_put:
            self._addNewInterfaceWithPUT()
            return 




    def _getRootResourceDiscovery(self):
        self._url = "https://" + self._interfaceIP + "/" + ".well-known/host-meta"
        self._headers = { "Accept" : "application/json" }

        response = requests.get(self._url , auth = self._userPass , headers = self._headers , verify = False)

        self._printResponseResult(response)

    def _getInterfaces(self):
        self._url = "https://" + self._interfaceIP + "/" + "restconf/data/ietf-interfaces:interfaces"
        self._headers = { "Accept": "application/yang-data+json"}

        response = requests.get(self._url , auth = self._userPass , headers = self._headers , verify = False)

        self._printResponseResult(response)
        
    def _getSpecificInterface(self):
        print("\n\t\t\t\t\t Enter Interface Name: " , end = "")
        interfaceName = str(input())

        self._url = "https://" + self._interfaceIP + "/" + "restconf/data/ietf-interfaces:interfaces/interface=" + interfaceName
        self._headers = { "Accept": "application/yang-data+json"}

        
        response = requests.get(self._url , auth = self._userPass , headers = self._headers , verify = False)

        self._printResponseResult(response)

    def _getInterfacesStatus(self):
        self._url = "https://" + self._interfaceIP + "/" + "restconf/data/ietf-interfaces:interfaces"
        self._headers = { "Accept":"application/yang-data+json"}
        self._parameters = {"fields": "interface/name;interface/enabled"}

        response = requests.get(self._url , auth = self._userPass , headers = self._headers , params= self._parameters , verify = False)

        self._printResponseResult(response)

        return

    def _discoverAllowedMethods(self):

        self._url = "https://" + self._interfaceIP + "/" + "restconf/data/ietf-interfaces:interfaces"
        self._headers = {"Accept": "application/yang-data+json"}

        response = requests.options(self._url , auth = self._userPass , headers = self._headers , verify = False)

        self._printResonseResultWithoutText(response)

    def _addNewInterfaceWithPOST(self):
        
        newInterfaceData = {
             "ietf-interfaces:interface": {
             "name": "Huffman-Loopback69",
             "description": "Added By Me (Ahmad)",
             "type": "iana-if-type:softwareLoopback",
             "enabled": True,
             "ietf-ip:ipv4": {
                 "address": [
                                    {
                                    "ip": "69.69.69.0",
                                    "netmask": "255.255.255.0"
                                    }
                                ]
                             } ,
             "ietf-ip:ipv6": {}
                                        }
                           }
        
        print("\n\n\t\t\t\t\t Entre Interface Name: " , end = "")
        interfaceName = str(input())

        print("\n\n\t\t\t\t\t Entre Interface Description: " , end = "")
        description = str(input())

        print("\n\n\t\t\t\t\t Entre Interface IPv4: " , end = "")
        ipv4 = str(input())

        newInterfaceData['ietf-interfaces:interface']['name'] = interfaceName
        newInterfaceData['ietf-interfaces:interface']['description'] = description
        newInterfaceData['ietf-interfaces:interface']['ietf-ip:ipv4']['address'][0]['ip'] = ipv4


        self._url = "https://" + self._interfaceIP + "/" + "restconf/data/ietf-interfaces:interfaces" 
        self._headers = {"Accept": "application/yang-data+json" , "Content-Type":"application/yang-data+json"}

        response = requests.post(self._url , auth = self._userPass , data= json.dumps(newInterfaceData) , headers = self._headers , verify = False)

        self._printResponseResult(response)

    def _addNewInterfaceWithPUT(self): 
                
        newInterfaceData = { 
             "ietf-interfaces:interface": {
             "name": "Huffman-Loopback69",
             "description": "Added By Me (Ahmad)",
             "type": "iana-if-type:softwareLoopback",
             "enabled": True,
             "ietf-ip:ipv4": {
                 "address": [
                                    {
                                    "ip": "69.69.69.0",
                                    "netmask": "255.255.255.0"
                                    }
                                ]
                             } ,
             "ietf-ip:ipv6": {}
                                        }
                           }
        
        print("\n\n\t\t\t\t\t Entre Interface Name: " , end = "")
        interfaceName = str(input())

        print("\n\n\t\t\t\t\t Entre Interface Description: " , end = "")
        description = str(input())

        print("\n\n\t\t\t\t\t Entre Interface IPv4: " , end = "")
        ipv4 = str(input())

        newInterfaceData['ietf-interfaces:interface']['name'] = interfaceName
        newInterfaceData['ietf-interfaces:interface']['description'] = description
        newInterfaceData['ietf-interfaces:interface']['ietf-ip:ipv4']['address'][0]['ip'] = ipv4


        self._url = "https://" + self._interfaceIP + "/" + "restconf/data/ietf-interfaces:interfaces" + "/interface=" + interfaceName
        self._headers = {"Accept": "application/yang-data+json" , "Content-Type":"application/yang-data+json"}

        response = requests.put(self._url , auth = self._userPass , data= json.dumps(newInterfaceData) , headers = self._headers , verify = False)

        self._printResponseResult(response)

        
    def _goBack(self):
        self.runScript()




    def _printResponseResult(self,response):
        self._clearScreen()
        print("\n\n\n\n\t\t\t\t\t------------------------------------")
        print("\t\t\t\t\t\t Respone Results")
        print("\t\t\t\t\t------------------------------------")
        
        print("\n\n[+] URL: {}".format(response.url))
        print("[+] Status Code: {}".format(response.status_code))
        print("[+] Reason: {}".format(response.reason))
        print("[+] Time Elapsed: {}".format(response.elapsed))
        print("\n\n\n[+] Headers: {}".format(response.headers))
        print("\n\n\n[+] Text As Dict:\n {}".format(json.loads(response.text)))
        print("\n\n\n[+] Text AS JSON String:\n {}".format(response.text))


    def _printResonseResultWithoutText(self,response):
        self._clearScreen()
        print("\n\n\n\n\t\t\t\t\t------------------------------------")
        print("\t\t\t\t\t\t Respone Results")
        print("\t\t\t\t\t------------------------------------")
        
        print("\n\n[+] URL: {}".format(response.url))
        print("[+] Status Code: {}".format(response.status_code))
        print("[+] Reason: {}".format(response.reason))
        print("[+] Time Elapsed: {}".format(response.elapsed))
        print("\n\n\n[+] Headers: {}".format(response.headers))
        



    def _clearScreen(self): 
          if os.name == 'nt':  # For Windows
            print("\n\n" * 100)
          else:  # For other platforms (Unix/Linux/Mac)
            os.system('clear')




router = clsCiscoRouter()
router.runScript()
