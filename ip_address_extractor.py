#-------------------------------------------------------------------------------
# Name:        IP Address Extractor
# Purpose:     To Extract IP Addresses held by IEDs usin
#
# Author:      10098468 Ngau Wah Xian
#
# Created:     06-07-2018
# Copyright:   (c) 10098468 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import xml.etree.ElementTree as ET
csvFile = open('IP_Addresses_output.csv', 'w')
csvFile.write("No, IED, IP Address \n")

def main():
    DirectoryStr = 'GRNE_1611012226.scd' #For BBTU file
    #DirectoryStr = 'C:\\Users\\10098468\\Documents\\Python\\IEC61850_Configurator\\GRNE_1611012226_AddBBHz2IEDA&C.xml'
    tree = ET.parse(DirectoryStr)
    root = tree.getroot()
    namespaces = {'x':'http://www.iec.ch/61850/2003/SCL'}

    CommElem = root.find("x:Communication", namespaces)
    SubnetElems = CommElem.findall("x:SubNetwork", namespaces)

    i=1
    for SubnetElem in SubnetElems:
        for ConnectedAP in SubnetElem.findall("x:ConnectedAP", namespaces):
            IEDNameStr = ConnectedAP.get("iedName")
            IPAddElem = ConnectedAP.find("x:Address/x:P/[@type='IP']", namespaces)
            if IPAddElem is not None:
                IPAddStr = IPAddElem.text
                print str(i)+","+IEDNameStr + "," + IPAddStr
                csvFile.write(str(i)+","+IEDNameStr + "," + IPAddStr + "\n")
                i+=1

    csvFile.close()

if __name__ == '__main__':
    main()
