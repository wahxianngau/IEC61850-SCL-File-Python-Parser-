#-------------------------------------------------------------------------------
# Name:        IEC61850 Tag Configurator
# Purpose:     To parse SCD File and Extract relevant 61850 Tags according
#              to Report Requirements
#
# Author:      10098468 Ngau Wah Xian
#
# Created:     29-06-2018
# Copyright:   (c) 10098468 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

#--------Global Variables------------------
import xml.etree.ElementTree as ET
namespaces = {'x':'http://www.iec.ch/61850/2003/SCL'}

#-----------Initialisation of XML Element Tree and variable declaration----------------
ReportControlStr = ""
PhysicalDeviceStr = ""
LogicalDeviceStr = ""
LogicalNodeStr = ""
FunctionalConstraintsStr = ""
DataObjectList = []
DataAttributeList = []
DataTypeList = []

SignalTagList = []

IECTagDict = {'ReportControlStr':'', 'PhysicalDeviceStr':'','LogicalDeviceStr':'','LogicalNodeStr':'','FunctionalConstraintsStr':'','DataObjectList':[],'DataAttributeList':[], 'DataTypeList':[]}
IECTagDictList = []

DBConfigDict = {}
DBConfigDictList = []

PrintEnable = 0
ReportControlEnable = 1
CSVPrintEnable = 1
FCDAEnable = 0
ReportNumberStr = "5"


#--------------CSV Creation--------------
csvFile = open('LGNG_61850_Signals_Tag Generator.csv', 'w')
csvFile.write("Report, Time Tag, Quality Tag, Signal Tag, Physical Device\n" )

#--------------XML Parsing--------------

DirectoryStr = 'LENGGENG_500_275_KV.scd' #For BBTU file
#DirectoryStr = 'C:\\Users\\10098468\\Documents\\Python\\IEC61850_Configurator\\GRNE_1611012226_AddBBHz2IEDA&C.xml' #For BBTU file

print "ET.parse(" + DirectoryStr + ")"
tree = ET.parse(DirectoryStr)
root = tree.getroot()


#---------Logical Device---------------------
def getLogicalDevice( PDElem, inst ):
    #print "Error in getLogicalDevice: PDElem, inst" + str(PDElem) + " | "+str(inst)
    LDElem = PDElem.find("x:AccessPoint/x:Server/x:LDevice/[@inst='" + inst +"']", namespaces)
    LogicalDevice = LDElem.get("inst")
    if PrintEnable == 1:
        print "--------------------------------------Logical Device-----------------------------------------"
    #print "Logical Device: " + LogicalDevice
    global LogicalDeviceStr
    LogicalDeviceStr = str(LogicalDevice)    #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    return LDElem

#----------Logical Node --------------------
def getLogicalNode(LDElem):
    global ReportControlStr

    for LNElem in LDElem:
        RCElems = []
        DSElem = []
        RCElems = LNElem.findall("x:ReportControl", namespaces)
        #print "RCElems: " + str(RCElems)
        if RCElems != []:     #If Logical Node contains Report, must have dataset
            #LogicalNodeStr = LNElem.get("lnClass")  #CHANGE!! get LNodes that contain Reports only     ????
            LNTypeStr = LNElem.get("lnType")
            lnClassStr = LNElem.get("lnClass") + LNElem.get("inst")

            for RCElem in RCElems:      #report Control Elements
##                ReportControlStr = RCElem.get("rptID") #OLD REPORT ID
##                ReportControlStr = PhysicalDeviceStr + LogicalDeviceStr
                if PrintEnable == 1:
                    print "-----------------------------------Report Control:---------------------------------" + ReportControlStr
                DatSet = RCElem.get('datSet')
                #print "DatSet: " + str(DatSet)
                DSElem = LNElem.find("x:DataSet/[@name='" + DatSet +"']", namespaces)
                #print DSElem

                #------------------------------Print Report
                ReportControlStr = ""
                if RCElem.get("buffered") is not None:
                    if RCElem.get("buffered") == "true":
                        ReportControlStr = PhysicalDeviceStr + LogicalDeviceStr + "/" + lnClassStr + "$" + "BR" +"$" + RCElem.get("name") + "0" + ReportNumberStr
                    else:
                        ReportControlStr = PhysicalDeviceStr + LogicalDeviceStr + "/" + lnClassStr + "$" + "RP"+"$" + RCElem.get("name") + "0" + ReportNumberStr
                else:
                    ReportControlStr = PhysicalDeviceStr + LogicalDeviceStr + "/" + lnClassStr + "$" + "RP"+"$" + RCElem.get("name") + "0" + ReportNumberStr

                if DSElem != None:
                    getDataSetInfo(DSElem, LDElem, LNTypeStr, RCElem)

                else:
                    if PrintEnable == 1:
                        print "Error:Dataset Does Not Exist!"
                #print "Dataset found: " + str(DSElem.attrib)





    return

def getDataSetInfo(DSElem, LDElem, LNTypeStr, RCElem):
    #global LogicalDeviceStr
    global LogicalNodeStr

    global FunctionalConstraintsStr
    global DataObjectList



    for FCDAElem in DSElem:
        #to find proper Logical Node inside Physical Device itself (Local instead of DataTemplate)
        ldInst= FCDAElem.get('ldInst')
        prefix = FCDAElem.get('prefix')

        doNameList = []
        doName = FCDAElem.get('doName')
        fc = FCDAElem.get('fc')
        lnClass = FCDAElem.get('lnClass')
        lnInst = FCDAElem.get('lnInst')
        #print "doName: " + str(doName) + " | fc: " + str(fc) + " | lnClass: " + str(lnClass) + " | lnInst: " + str(lnInst) + " | prefix: " + str(prefix) + " | ldInst: " + str(ldInst)

        #---------------------------LogicalNodeString-------------------------------------------
        LogicalNodeStr = ""
        if prefix is not None:
            LogicalNodeStr = str(prefix)

        LogicalNodeStr = LogicalNodeStr + str(lnClass)
        if lnInst is not None:
            LogicalNodeStr = LogicalNodeStr + str(lnInst)  #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

        FunctionalConstraintsStr = str(fc)     #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        doNameList = processDoName(doName)  #%%seperated doName (delimited by .)
        DataObjectList = doNameList      #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        #print "LNTypeStr:" + LNTypeStr #%%%%%%%%%%%%%%%%%%%%%%%%%% PRINT %%%%%%%%%%%%%%%%%%%%%%%



        #print "-----------------------------------Logical Node:---------------------------------------------------------" + str(LogicalDeviceStr)

        if lnInst != None:
            LNTypeStr2 = getLNType(LDElem, lnClass, lnInst, ldInst, prefix) #%%Get the LNType Name to find it in data Templates  #local search for LN first
            getLNodeTypeElem(LNTypeStr2,doNameList, fc)
        else:  #for Regda
            getLNodeTypeElemR(doNameList, LNTypeStr,fc)

    return

def processDoName(doName):     #function to split strings according to delim .
    doNameListTmp = []
    if "." in str(doName):
        doNameListTmp = doName.split(".")
    else:
        doNameListTmp.append(doName)
    return doNameListTmp

def getLNType(LDElem, lnClass, lnInst, ldInst, prefix):
    #Find correct LDElem first
##    LNElem = LDElem.find("x:LN/[@lnClass='"+lnClass+"'][@inst='"+lnInst+"']", namespaces)
    if prefix is None:
        #print "getLNType: No Prefix"
        PDElem = root.find("x:IED/[@name='"+PhysicalDeviceStr+"']", namespaces)
        LDElem = PDElem.find("x:AccessPoint/x:Server/x:LDevice/[@inst='" + ldInst +"']", namespaces)
        LNElem = LDElem.find("x:LN/[@lnClass='"+lnClass+"'][@inst='"+lnInst+"']", namespaces)
    else:
        PDElem = root.find("x:IED/[@name='"+PhysicalDeviceStr+"']", namespaces)
        LDElem = PDElem.find("x:AccessPoint/x:Server/x:LDevice/[@inst='" + ldInst +"']", namespaces)
        LNElem = LDElem.find("x:LN/[@lnClass='"+lnClass+"'][@inst='"+lnInst+"'][@prefix='"+prefix+"']", namespaces)
        if LNElem is None:
            #print "getLNType: No element found with Prefix"
            LNElem = LDElem.find("x:LN/[@lnClass='"+lnClass+"'][@inst='"+lnInst+"']", namespaces)
    LNTypeStr = LNElem.get('lnType')  #used to find LNType, in conjunction with doName
    return LNTypeStr

# lnTypeSTR="REGS_REGD_LLN0"
# lnClass="LLN0"
def getLNodeTypeElemR(doNameList, LNTypeStr, fc):
    global DataAttributeList
    global DataTypeList
    #print "in getLNodeTypeElemR, doNameList: "+str(doNameList)
    LNodeTypeElem = root.find("x:DataTypeTemplates/x:LNodeType/[@id='"+LNTypeStr+"']", namespaces)
    #print "LNodeTypeElem" + str(LNodeTypeElem.tag)
    #print "doName: " + str(doName)
    DOElem = LNodeTypeElem.find("x:DO/[@name='"+doNameList[0]+"']", namespaces)
    DOTypeStr = DOElem.get("type")

    if len(doNameList) == 2:
        #traverse twice
        DOTypeElem = root.find("x:DataTypeTemplates/x:DOType/[@id='"+DOTypeStr+"']", namespaces)
        SDOElem = DOTypeElem.find("x:SDO/[@name='"+doNameList[1]+"']", namespaces)
        DOTypeStr = SDOElem.get("type")

    DOTypeElem = root.find("x:DataTypeTemplates/x:DOType/[@id='"+DOTypeStr+"']", namespaces)
    DAElems = DOTypeElem.findall("x:DA/[@fc='"+fc+"']", namespaces)

    for DA in DAElems:
        DataAttributeList = []
        DataTypeList = []
        DAElem = DA
        #print "DA RegDa:" + str(DA.attrib)
        DAStr = DA.get("name")
        DATypeStr = DA.get("bType")
        DataAttributeList.append(DAStr)    #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        DataTypeList.append(DATypeStr)

        if(DAElem.get('bType')=="Struct"):
            DATypeStr = DAElem.get('type')
            DATypeElem2 = root.find("x:DataTypeTemplates/x:DAType/[@id='"+DATypeStr+"']", namespaces)
            #print "inside bType 1"
            for BDAElem in DATypeElem2:

                #To get rid of existing text in DataAttribList
                DataAttributeList = []
                DataTypeList = []
                DataAttributeList.append(DAStr)
                DataTypeList.append(DATypeStr)

                BDANameStr = BDAElem.get("name")
                BDANTypeStr = BDAElem.get("bType")
                DataAttributeList.append(BDANameStr)
                DataTypeList.append(BDANTypeStr)
                if (BDAElem.get("bType")=="Struct"):
                    BDATypeStr = BDAElem.get("type")
                    DATypeElem3 = root.find("x:DataTypeTemplates/x:DAType/[@id='"+BDATypeStr+"']", namespaces)
                    #print "inside bType 2"
                    for BDAElem in DATypeElem3:
                        BDANameStr = BDAElem.get("name")
                        BDANTypeStr = BDAElem.get("bType")
                        DataAttributeList.append(BDANameStr)
                        DataTypeList.append(BDANTypeStr)
                        TagPrinter()
                else:
                    TagPrinter()
        else:
            TagPrinter()


def getLNodeTypeElem(LNTypeStr,doNameList, fc):
    global DataAttributeList
    #print "in getLNodeTypeElem, doNameList and LNType: "+str(doNameList) + " | " + str(LNTypeStr)
    LNodeTypeElem = root.find("x:DataTypeTemplates/x:LNodeType/[@id='"+LNTypeStr+"']", namespaces)      #Remember to use namespaces for every node
    #print LNodeTypeElem.attrib
    #if doNameList has one element = go straight , if 2 then traverse 2 times
    DOElem = LNodeTypeElem.find("x:DO/[@name='"+doNameList[0]+"']",namespaces)
    DOTypeStr = DOElem.get("type")
    #print "DOTypeStr" + str(DOTypeStr)
    if len(doNameList) == 2:
        #traverse twice
        DOTypeElem = root.find("x:DataTypeTemplates/x:DOType/[@id='"+DOTypeStr+"']", namespaces)
        SDOElem = DOTypeElem.find("x:SDO/[@name='"+doNameList[1]+"']", namespaces)
        DOTypeStr = SDOElem.get("type")

    DOTypeElem2 = root.find("x:DataTypeTemplates/x:DOType/[@id='"+DOTypeStr+"']", namespaces)
    DAElems = DOTypeElem2.findall("x:DA/[@fc='"+fc+"']", namespaces)

    for DA in DAElems:
        DataAttributeList = []
        DAElem = DA
        DAStr = DAElem.get("name")
        DataAttributeList.append(DAStr)

        if(DAElem.get('bType')=="Struct"):
            DATypeStr = DAElem.get('type')
            DATypeElem2 = root.find("x:DataTypeTemplates/x:DAType/[@id='"+DATypeStr+"']", namespaces)
            #print "inside bType 1"
            for BDAElem in DATypeElem2:

                #To get rid of existing text in DataAttribList
                DataAttributeList = []
                DataAttributeList.append(DAStr)

                BDANameStr = BDAElem.get("name")
                DataAttributeList.append(BDANameStr)
                if (BDAElem.get("bType")=="Struct"):
                    BDATypeStr = BDAElem.get("type")
                    DATypeElem3 = root.find("x:DataTypeTemplates/x:DAType/[@id='"+BDATypeStr+"']", namespaces)
                    #print "inside bType 2"
                    for BDAElem in DATypeElem3:
                        BDANameStr = BDAElem.get("name")
                        DataAttributeList.append(BDANameStr)
                        TagPrinter()
                else:
                    TagPrinter()
        else:
            TagPrinter()

    #return DAElems

def TagPrinter():
    #Generate String
    global IECTagDictList
    global IECTagDict
    global SignalTagList
    IECTagDict2 = {'ReportControlStr':'', 'PhysicalDeviceStr':'','LogicalDeviceStr':'','LogicalNodeStr':'','FunctionalConstraintsStr':'','DataObjectList':[],'DataAttributeList':[]}

    #IECTagDictList = []
    if CSVPrintEnable == 0:
        OutputStr = ""
        if ReportControlEnable == 1:
            OutputStr = ReportControlStr + "&"
        OutputStr = OutputStr + PhysicalDeviceStr + "/" + PhysicalDeviceStr+LogicalDeviceStr+"/"+LogicalNodeStr+"$"+FunctionalConstraintsStr
        #---OutputStr = OutputStr + PhysicalDeviceStr+ LogicalDeviceStr+"/"+LogicalNodeStr+"$"+FunctionalConstraintsStr #New driver
        for DataObjectStr in DataObjectList:
            OutputStr = OutputStr+ "$" + DataObjectStr
        for DataAttributeStr in DataAttributeList:
            OutputStr = OutputStr + "$" + DataAttributeStr

        print OutputStr

    else:   #print CSV - wait for everything to come in first
        #put everything into dictionary {'ReportControlStr','PhysicalDeviceStr','LogicalDeviceStr','LogicalNodeStr','FunctionalConstraintsStr','DataObjectList','DataAttributeList'}
        IECTagDict2['ReportControlStr'] = ReportControlStr
        IECTagDict2['PhysicalDeviceStr'] = PhysicalDeviceStr
        IECTagDict2['LogicalDeviceStr'] = LogicalDeviceStr
        IECTagDict2['LogicalNodeStr'] = LogicalNodeStr
        IECTagDict2['FunctionalConstraintsStr'] = FunctionalConstraintsStr
        IECTagDict2['DataObjectList'] = DataObjectList
        IECTagDict2['DataAttributeList'] = DataAttributeList
        IECTagDict2['DataTypeList'] = DataTypeList

        if IECTagDictList == []:
            #print "first insert: " + str(len(IECTagDictList))
            IECTagDictList.append(IECTagDict2)
            #print "len after first insert: " +  str(len(IECTagDictList))
        elif IECTagDictList[-1]['DataObjectList'] == IECTagDict2['DataObjectList'] and IECTagDictList[-1]['LogicalNodeStr'] == IECTagDict2['LogicalNodeStr']:
            #print IECTagDict2['DataObjectList'] + "inserted as it is the same as previous Data Object" + str(IECTagDictList[-1]['DataObjectList'])
            IECTagDictList.append(IECTagDict2)
            #print "length after insert: " + str(len(IECTagDictList))
        else:
            #print "----------------------------not the same ----------------------------------"
            #Initialisation:


            printTagCommand()

            del IECTagDictList[:] #delete everything in the list
            IECTagDictList.append(IECTagDict2)
        return

def printTagCommand():
    ReportControlTag = ""
    TimeTag = ""
    QualityTag = ""
    SignalTag = ""
    FCDATag = ""
    SignalTagList = []
    FCDAList = []
    #1. Create ReportControl Tag
    ReportControlTag = IECTagDictList[-1]['ReportControlStr']

    for IECTag in IECTagDictList:
        #print "IECTag" + str(IECTag)
        #2. Create time Tag
        if IECTag['DataAttributeList'][-1] == "t":   #if last character is t
            #---TimeTag = IECTag['PhysicalDeviceStr'] + "/" + IECTag['PhysicalDeviceStr']+IECTag['LogicalDeviceStr']+"/"+IECTag['LogicalNodeStr']+"$"+IECTag['FunctionalConstraintsStr']
            TimeTag = IECTag['PhysicalDeviceStr'] + IECTag['LogicalDeviceStr']+"/"+IECTag['LogicalNodeStr']+"$"+IECTag['FunctionalConstraintsStr']
            for DataObjectStr in IECTag['DataObjectList']:
                TimeTag = TimeTag+ "$" + DataObjectStr
            for DataAttributeStr in IECTag['DataAttributeList']:
                TimeTag = TimeTag + "$" + DataAttributeStr

        #3. Create Quality Tag
        elif IECTag['DataAttributeList'][-1] == "q":
            #---QualityTag = IECTag['PhysicalDeviceStr'] + "/" + IECTag['PhysicalDeviceStr']+IECTag['LogicalDeviceStr']+"/"+IECTag['LogicalNodeStr']+"$"+IECTag['FunctionalConstraintsStr']
            QualityTag = IECTag['PhysicalDeviceStr'] + IECTag['LogicalDeviceStr']+"/"+IECTag['LogicalNodeStr']+"$"+IECTag['FunctionalConstraintsStr']
            for DataObjectStr in IECTag['DataObjectList']:
                QualityTag = QualityTag+ "$" + DataObjectStr
            for DataAttributeStr in IECTag['DataAttributeList']:
                QualityTag = QualityTag + "$" + DataAttributeStr

        elif IECTag['DataAttributeList'][-1] == "stSeld":
            print "stSeld Detected"
        #4. Create Signal Tags and FCDA Tag
        else:
            #---SignalTag = IECTag['PhysicalDeviceStr'] + "/" + IECTag['PhysicalDeviceStr']+IECTag['LogicalDeviceStr']+"/"+IECTag['LogicalNodeStr']+"$"+IECTag['FunctionalConstraintsStr']
            #SignalTag = IECTag['PhysicalDeviceStr'] + "/" + IECTag['LogicalDeviceStr']+"/"+IECTag['LogicalNodeStr']+"$"+IECTag['FunctionalConstraintsStr']
            SignalTag = IECTag['PhysicalDeviceStr'] + IECTag['LogicalDeviceStr']+"/"+IECTag['LogicalNodeStr']+"$"+IECTag['FunctionalConstraintsStr']

            FCDATag =  IECTag['PhysicalDeviceStr']+IECTag['LogicalDeviceStr']+"/"+IECTag['LogicalNodeStr']
            #B01AF34CLD0/GGIO10/Alm5/stVal[ST]

            cnt = 0
            for DataObjectStr in IECTag['DataObjectList']:
                SignalTag = SignalTag+ "$" + DataObjectStr
                if cnt ==0:
                    FCDATag = FCDATag+ "/" + DataObjectStr
                    cnt+=1
                else:
                    FCDATag = FCDATag+ "." + DataObjectStr

            cnt = 0
            for DataAttributeStr in IECTag['DataAttributeList']:
                SignalTag = SignalTag + "$" + DataAttributeStr
                if cnt == 0:
                    FCDATag = FCDATag + "/" + DataAttributeStr
                    cnt+=1
                else:
                    FCDATag = FCDATag + "." + DataAttributeStr

            FCDATag = FCDATag + "[" + IECTag['FunctionalConstraintsStr'] + "]"

            SignalTagList.append(SignalTag)
            FCDAList.append(FCDATag)


    #5. Join Up to become CSV
    i = 0
    for SigTag in SignalTagList:
        if FCDAEnable ==1:
            print ReportControlTag + "," + TimeTag + "," + QualityTag + "," + SigTag + "," + FCDAList[i]
            csvFile.write(ReportControlTag + "," + TimeTag + "," + QualityTag + "," + SigTag + "," + FCDAList[i] + "\n")
            i += 1
        else:
            print ReportControlTag + "," + TimeTag + "," + QualityTag + "," + SigTag
            csvFile.write(ReportControlTag + "," + TimeTag + "," + QualityTag + "," + SigTag + "," + IECTag['PhysicalDeviceStr'] + "\n")

def main():

    i = 1

    for PDElem in root.findall("x:IED", namespaces):       #B01AF34C , B03F90AVR3,  [@name='B01AF34C']    D02AF34C
        PhysicalDevice = PDElem.get('name')
        #print str(i) + "PhysicalDevice: " + PhysicalDevice
        global PhysicalDeviceStr
        PhysicalDeviceStr = str(PhysicalDevice)    #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
        if PrintEnable == 1:
            print "=====================================PhysicalDevice=======================================" +str(i) + ": "+PhysicalDeviceStr
        i+=1

        #---------Logical Device--------------------- FOR LD0, MEAS, CTRL from here, make function
            #----------Logical Node--------------------------

        #-----------------General-----------------
        RCAvaiLDList = []
        #print "Error: main: before findall"
        LDElemsInPDElem = PDElem.findall("x:AccessPoint/x:Server/x:LDevice",namespaces)


        for LDElemInPDElem in LDElemsInPDElem:
            #print "Error: main: inside first for"
            for LNode_LDChild in LDElemInPDElem:     #LDChild = LNode
                #print "Error: main: inside second for"
                if LNode_LDChild.find("x:ReportControl", namespaces) is not None:
                    RCAvaiLD = LDElemInPDElem.get('inst')
                    if RCAvaiLDList == []:
                        RCAvaiLDList.append(RCAvaiLD)
                    elif RCAvaiLD != RCAvaiLDList[-1]:
                        RCAvaiLDList.append(RCAvaiLD)

        #print "Error:Main: RCAvaiLDList: " + str(RCAvaiLDList) + str(len(RCAvaiLDList))
        if len(RCAvaiLDList) != 0:
            for element in RCAvaiLDList:
                LDElem = getLogicalDevice(PDElem, str(element))
                getLogicalNode(LDElem)
    printTagCommand()
    csvFile.close()

if __name__ == '__main__':
    main()
