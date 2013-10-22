'''
Created on 2013-3-5

@author: rongyu zhou
'''
#coding:utf-8
import os, subprocess
import time
#from MySQLdb import DATETIME
from controller import APK


strJarPath = os.getcwd() + "\\gpc.jar"
strCfgPath = os.getcwd() + "\\crawler.conf "
queryOffset = 50


def GooglePlayCmd(cmd):
    cmdline = "java.exe -jar " +strJarPath+ " -f " + strCfgPath + cmd
    
    outRead = []
    process = subprocess.Popen(cmdline,stdout = subprocess.PIPE,shell = True)
    outRead += process.stdout.readlines()
    print outRead
    if outRead[0][0:4] == "GPE:":#google play error
        return outRead
   
    result = []
    for item in outRead:
        item = item[:-2]
        result.append(item.split(";"))
        
    return result[1:]

def DownloadApk(packageName):
    cmdline = "java.exe -jar " +strJarPath+ " -f " + strCfgPath + "download " + packageName
    process = subprocess.Popen(cmdline,stdout = subprocess.PIPE,shell = True)
    outRead = []
    while process.poll() is None:    
        outRead += process.stdout.readlines()
        time.sleep(1)     
    for item in outRead:
        if str(item).find("Downloaded!") != -1:
            return True
    return False

def GetPlaySubCategory(category):
    cmd = "list " + category
    subCategory = GooglePlayCmd(cmd)
    if not subCategory.__len__():
        return
    return subCategory   

def ListApkInformation(category,subCategory,startIndex):
    cmdline = "list -n " + str(queryOffset) +" -o " + str(startIndex) + " -s " + subCategory + " " + category
    # Title;Package;Creator;Price;Installation Size;Number Of Downloads
    
    apkList = GooglePlayCmd(cmdline) 
    if not apkList.__len__():
        return
    return apkList

def GetPlayRootCategory():
    categorites = GooglePlayCmd("categories")
    if not categorites.__len__():
        print "Category Error\n"
        return
    return categorites#ID;Name


if __name__ == '__main__':
    rootCategory = GetPlayRootCategory()
    if ( rootCategory ):
        for itemRoot in rootCategory:
            print itemRoot
            #itemRoot: id; name
            subCategory = GetPlaySubCategory(itemRoot[0])
            #subCategory: [[id; name]...]
            if (subCategory):
                nOffset = 0
                for itemSub in subCategory:
                    print itemSub
                    apkList = ListApkInformation(itemRoot[0], itemSub[0], nOffset)
                    
                    while (apkList):
                        if (apkList[0][0:7] == "GPE:200"):
                            #check google play block
                            tryCounts = 0  
                            while (apkList[0][0:7] == "GPE:200" and tryCounts < 3):
                                time.sleep(60)
                                apkList = ListApkInformation(itemRoot[0], itemSub[0], nOffset)
                                tryCounts +=1
                        
                        if (apkList[0][0:7] != "GPE:200"):
                            #iterat APK
                            for itemApk in apkList:
                                #print itemApk
                                apk = APK()
                                apk.package_name = itemApk[1]
                                apk.app_name = itemApk[0]
                                apk.size = int(itemApk[4])
                                apk.creator = itemApk[2]
                                #if ( not apk._isTrustedCreator(apk.creator) and not apk._checkApkExistApkInfo(apk.package_name,apk.app_name,apk.size) ):
                                #    apk._insertDB()
                            nOffset += queryOffset
                            time.sleep(10)
                            apkList = ListApkInformation(itemRoot[0], itemSub[0], nOffset)
                    print str(apkList)

'''
#thread way
if __name__ == '__main__':
    #[Category,subCategory ...]
    apkCategory = GetPlayRootCategory()()
    if not apkCategory.__len__():
        print "Error\n"
    else:
        threadList = []
        for item in range(1):
            print apkCategory[item]
            threadList.append(DownloadThread(apkCategory[item]))
            #threadList[item].setDaemon(True)
            threadList[item].start()
'''           