import os
import sys
import requests
import time
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename
import threading

event = threading.Event()

def download_file(url, client):
    try:
        response = requests.get(url)
    except requests.exceptions.SSLError:
        print('SSL证书错误，请检查网络连接（vpn）')
        for retry in range(1, 11):
            try:
                response = requests.get(url)
            except:
                print(f'失败,三秒后重试{retry}/10，检查网络连接（vpn）')
                time.sleep(3)
    if response.status_code == 200:
        print('链接成功(若未弹出对话框，请重开程序)')
        time.sleep(0.1)
        save_path = asksaveasfilename(initialfile=f"{client}.jar", defaultextension=".jar", filetypes=[("JAR files", "*.jar"), ("All files", "*.*")])
        time.sleep(0.1)
        if save_path:
            with open(save_path, "wb") as f:
                f.write(response.content)
            print('文件已保存到:', save_path)
        else:
            print('用户取消了文件保存操作')
    elif response.status_code == 404:
        print("链接不存在，请检查版本号是否正确,或该版本尚未更新，敬请期待")
    else:
        print('无法获取数据，状态码:', response.status_code)
        for retry in range(1, 11):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    print('链接成功')
                    download_file(url, client)
                    break
            except:
                print(f'失败,三秒后重试{retry}/10，检查网络连接（vpn）')
                time.sleep(3)

    event.set()  # 设置事件标志，表示下载完成

def main():
    def demain():
        version = input("请输入Minecraft版本号：")
        WurstUrl = f'https://github.com/dingzhen-vape/WurstCN/releases/download/ATV/Wurst-ClientCN-MC{version}.jar'
        MeteorUrl = f"https://github.com/dingzhen-vape/MeteorCN/releases/download/ATV/meteor-client-{version}.jar"
        Client = input("请输入客户端名称（Wurst输入1/Meteor输入2）：")
        if Client == "1":
            print("正在获取链接，请等待（github），可能需要一点时间...")
            root.after(0, download_file, WurstUrl, f"Wurst-ClientCN-MC{version}")
        elif Client == "2":
            print("正在获取链接，请等待（github），可能需要一点时间...")
            root.after(0, download_file, MeteorUrl, f"meteor-client-{version}")
        event.wait()
        print("程序即将退出")
        root.quit()  # 退出Tkinter主循环
        time.sleep(5)
        sys.exit()

    global root
    root = Tk()
    root.withdraw()
    threading.Thread(target=demain).start()
    root.mainloop()

if __name__ == "__main__":
    main()
