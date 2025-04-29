
from encodings.punycode import T
from http.cookies import SimpleCookie
import os
import time
from tkinter.filedialog import asksaveasfilename
import json
import requests
import clsMenu

class VersionGetTool:
    def __init__(self):
        MainMenu = clsMenu.SimpleMenu(ShowIndex=True).addOption("WurstCN",self.WurstCN).addOption("MeteorCN",self.Meteor)
        MainMenu.addOption("刷新数据",self.RefreshInfo)
        MainMenu.ShowMenu()

    def RefreshInfo(self):
        MeteorDict = self.GetVersions("MeteorCN")
        WurstDict = self.GetVersions("WurstCN")
        if MeteorDict != {} and WurstDict != {}:
            with open("./versions.json","w+",encoding="utf-8") as f:
                Versions = {"WurstCN": WurstDict, "MeteorCN":MeteorDict}
                json.dump(Versions,f,ensure_ascii=False,indent=4)

    def Meteor(self):
        MeteorMenu = clsMenu.SimpleMenu(ShowIndex=True)
        with open("./versions.json","r",encoding="utf-8") as f:
            Datas:dict[list,list,list,list] = json.load(f)["MeteorCN"]
        for Version in Datas["Versions"]:
            MeteorMenu.addOption(Version,
                                 lambda index = Datas["Versions"].index(Version):self.ShowInfo(index,Datas) )
        MeteorMenu.addOption("返回上级菜单",MeteorMenu.Exit)

        MeteorMenu.ShowMenu()

    def WurstCN(self):
        WurstMenu = clsMenu.SimpleMenu(ShowIndex=True)
        with open("./versions.json","r",encoding="utf-8") as f:
            Datas:dict[list,list,list,list] = json.load(f)["WurstCN"]
        for Version in Datas["Versions"]:
            WurstMenu.addOption(Version,
                                lambda index = Datas["Versions"].index(Version):self.ShowInfo(index,Datas))
        WurstMenu.addOption("返回上级菜单",WurstMenu.Exit)

        WurstMenu.ShowMenu()
    
    def ShowInfo(self,index,Datas):
        InfoMenu = clsMenu.SimpleMenu(OneTime=True)
        InfoMenu.addOption(f"版本号:{Datas['Versions'][index]}")
        InfoMenu.addOption(f"更新时间:{Datas['UpdatedAt'][index]}")
        InfoMenu.addOption(f"下载次数:{Datas['DownloadCounts'][index]}")
        InfoMenu.addOption(f"下载地址:{Datas['DownloadUrls'][index]}")
        InfoMenu.addOption("下载",lambda:self.DownLoadFile(Datas["DownloadUrls"][index],Datas["Versions"][index]))
        InfoMenu.addOption("返回上级菜单",InfoMenu.Exit)
        InfoMenu.ShowMenu()

    def DownLoadFile(self,Url,name):
        os.system("cls")
        print("正在获取文件...")
        print(name,Url)
        filePath = asksaveasfilename(initialfile=f"{name}",
                                        defaultextension=".jar",
                                        filetypes=[("JAR files", "*.jar"), ("All files", "*.*")])
        if filePath == "":
            return
        with open(filePath, "wb") as f:
            f.write(requests.get(Url).content)
        print("保存成功")
        time.sleep(3)

    def GetVersions(self,Name):
        url = f'https://api.github.com/repos/dingzhen-vape/{Name}/releases/tags/ATV'
        response = requests.get(url)
        if response.status_code == 200:
            release = json.loads(response.content)["assets"]
            Versions = []
            DownloadCounts = []
            DownloadUrls = []
            UpdatedAt = []
            for version in release:
                Versions.append(version["name"])
                DownloadCounts.append(version["download_count"])
                DownloadUrls.append(version["browser_download_url"])
                UpdatedAt.append(version["updated_at"])
            os.system("cls")
            print("获取成功")
            time.sleep(3)
            return {"Versions":Versions,"UpdatedAt":UpdatedAt,"DownloadUrls":DownloadUrls,"DownloadCounts":DownloadCounts}
        else:
            os.system("cls")
            print("获取版本信息失败，请检查网络连接或者更换网络环境")
            print(response)
            print(response.content)
            time.sleep(5)

a = VersionGetTool()
