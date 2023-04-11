import json
import time
import psutil
import os
import datetime

class ApplicationClassifiction:

    def __init__(self,fileName="applicationClassifiction.txt"):
        self.fileName=fileName;
        self.applicationClassifiction={}
        if os.path.exists(fileName):
            with open(self.fileName, 'r') as f:
                json_data = json.load(f)
                self.applicationClassifiction=json_data
                self.refreshRunningInfo()
        else:
            self.pids = psutil.pids()
            for pid in self.pids:
                process = None
                try:
                    process = psutil.Process(pid)
                    self.applicationClassifiction[process.name()]=[]
                    self.applicationClassifiction[process.name()].append("game")
                except Exception as e:
                    continue
            self.refreshStorage()

    def refreshStorage(self):
        with open(self.fileName, 'w') as f:
            json.dump(self.applicationClassifiction, f)

    def setClassifiction(self,name,classifictionList):
        self.applicationClassifiction[name]=classifictionList
        self.refreshStorage()

    def addClassifiction(self,name,classifiction):
        if name in self.applicationClassifiction:
            if classifiction not in self.applicationClassifiction[name]:
                self.applicationClassifiction[name].append(classifiction)
                self.refreshStorage()
        else:
            self.applicationClassifiction[name]=[]
            self.applicationClassifiction[name].append(classifiction)
            self.refreshStorage()

    def removeClassifiction(self,name,classifiction):
        if name in self.applicationClassifiction:
            if classifiction in self.applicationClassifiction[name]:
                self.applicationClassifiction[name].remove(classifiction)
                self.refreshStorage()

    def clearItem(self,name):
        if name in self.applicationClassifiction:
            self.applicationClassifiction.pop(name, None)
            self.refreshStorage()

    def resetClassifiction(self,name):
        if name in self.applicationClassifiction:
            self.applicationClassifiction[name]=[]
            self.applicationClassifiction[name].append("game")
            self.refreshStorage()

    def getAppListByType(self,classification):
        list=[]
        for ac in self.applicationClassifiction:
            if classification in self.applicationClassifiction[ac]:
                list.append(ac)
        return list

    def refreshRunningInfo(self):
        self.pids = psutil.pids()
        for pid in self.pids:
            process = None
            try:
                process = psutil.Process(pid)
                if process.name() not in self.applicationClassifiction:
                    self.applicationClassifiction[process.name()] = []
                    self.applicationClassifiction[process.name()].append("game")
            except Exception as e:
                continue
        self.refreshStorage()

class TaskLists:
    def __init__(self):
        self.pids=[]
        self.task_dic={}
        self.pid_dic={}
        self.application_userTime={}

    def getProperty(slef,process, pro: str):
        try:
            ret = eval('process.' + pro)()
        except Exception as e:
            return ''
        return ret

    def refresh(self):
        self.pids=psutil.pids()
        self.task_dic={}
        self.pid_dic={}
        self.application_userTime = {}
        for pid in self.pids:
            process = None
            try:
                process=psutil.Process(pid)
                parent = self.getProperty(process, 'parent')

                if parent is str or parent is None:
                    parentName = ''
                else:
                    parentName = parent.name()

                userTime=process.cpu_times().user
                if process.name() in self.pid_dic:
                    self.pid_dic[process.name()].append(pid)
                    self.application_userTime[process.name()]+=userTime
                else:
                    self.pid_dic[process.name()]=[]
                    self.pid_dic[process.name()].append(pid)
                    self.application_userTime[process.name()] = userTime



                self.task_dic[pid]={
                    'pid':pid,
                    'name': process.name(),
                    'executionPath':self.getProperty(process, 'exe'),
                    'currentPath': self.getProperty(process,'cwd'),
                    'parentPid':process.ppid(),
                    'parentName':parentName,
                    'status': process.status(),
                    'userName': self.getProperty(process, 'username'),
                    'createTime': process.create_time(), # 进程创建时间
                    'executionTime': process.cpu_times(), # 执行时间
                    'userTime': userTime, # 用户使用时间
                    'memoryInfo': process.memory_info(), # 内存信息
                    'connections': process.connections() # 网络连接
                }
            except Exception as e:
                continue

    def refreshAll(self):
        self.pids=psutil.pids()
        self.task_dic={}
        self.pid_dic={}
        self.application_userTime = {}
        for pid in self.pids:
            process = None
            try:
                process=psutil.Process(pid)
                parent = self.getProperty(process, 'parent')
                if parent is str or parent is None:
                    parentName = ''
                else:
                    parentName = parent.name()

                userTime = process.cpu_times().user
                if process.name() in self.pid_dic:
                    self.pid_dic[process.name()].append(pid)
                    self.application_userTime[process.name()] += userTime
                else:
                    self.pid_dic[process.name()] = []
                    self.pid_dic[process.name()].append(pid)
                    self.application_userTime[process.name()] = userTime

                self.task_dic[pid]={
                    'pid':pid,
                    'name': process.name(),
                    'executionPath':self.getProperty(process, 'exe'),
                    'currentPath': self.getProperty(process,'cwd'),
                    'startCmd':self.getProperty(process, 'cmdline'),
                    'parentPid':process.ppid(),
                    'parentName':parentName,
                    'status': process.status(),
                    'userName': self.getProperty(process, 'username'),
                    'createTime': process.create_time(), # 进程创建时间
                    'terminal': self.getProperty(process, 'terminal'), # 终端
                    'executionTime': process.cpu_times(), # 执行时间
                    'userTime': userTime,  # 用户使用时间
                    'memoryInfo': process.memory_info(), # 内存信息
                    'openFiles': self.getProperty(process, 'open_files'), # 进程打开的文件
                    'connections': process.connections(), # 网络连接
                    'numThreads': process.num_threads(), # 线程数
                    'threads':self.getProperty(process, 'threads'), # 线程
                    'environ':self.getProperty(process, 'environ') # 环境变量
                }
            except Exception as e:
                continue
taskInfoManager=TaskLists()
applicationClassifiction=ApplicationClassifiction()
#########################################################################3
import telebot
import json

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

@bot.message_handler(commands=['start', 'help','hello'])
def send_welcome(message):
    print(message.text) # 消息的内容
    # print(message.entities) # 包含哪些命令
    for i in message.entities:
        print(i)
    bot.reply_to(message, "Howdy, how are you doing?")

@bot.message_handler(commands=['tasklist'])
def send_tasklist(message):
    taskInfoManager.refresh()
    # command=message.entities
    # print(message)
    # print(message.text)
    # print(len(message.text))
    # print(taskInfoManager.application_userTime)
    bot.reply_to(message, json.dumps(taskInfoManager.application_userTime, indent=4))

@bot.message_handler(commands=['taskDetail'])
def send_taskDetail(message):
    taskInfoManager.refresh()
    text=message.text
    applications=text[11:].strip().split(" ")
    result= {}
    for ap in applications:
        if ap.endswith(".exe") or ap in taskInfoManager.application_userTime:
            if ap in taskInfoManager.application_userTime:
                list=taskInfoManager.pid_dic[ap]
                for l in list:
                    result[ap + "-pid-" + str(l)] = {}
                    temp = taskInfoManager.task_dic[l]
                    result[ap + "-pid-" + str(l)]["pid"] = temp["pid"]
                    result[ap + "-pid-" + str(l)]["name"] = temp["name"]
                    result[ap + "-pid-" + str(l)]["status"] = temp["status"]
                    result[ap + "-pid-" + str(l)]["userTime"] = str(temp["userTime"])+' s'
                    result[ap + "-pid-" + str(l)]["createTime"] = datetime.datetime.fromtimestamp(temp["createTime"]).strftime('%Y-%m-%d %H:%M:%S')
        else:
            ap+='.exe'
            if ap in taskInfoManager.application_userTime:
                list = taskInfoManager.pid_dic[ap]
                for l in list:
                    result[ap +"-pid-"+str(l)] ={}
                    temp=taskInfoManager.task_dic[l]
                    result[ap +"-pid-"+str(l)]["pid"]=temp["pid"]
                    result[ap + "-pid-" + str(l)]["name"] = temp["name"]
                    result[ap + "-pid-" + str(l)]["status"] = temp["status"]
                    result[ap + "-pid-" + str(l)]["userTime"] = str(temp["userTime"])+' s'
                    result[ap + "-pid-" + str(l)]["createTime"] = datetime.datetime.fromtimestamp(temp["createTime"]).strftime('%Y-%m-%d %H:%M:%S')
    bot.reply_to(message, json.dumps(result,indent=4))

@bot.message_handler(commands=['task'])
def send_task(message):
    taskInfoManager.refresh()
    text=message.text
    applications=text[5:].strip().split(" ")
    result=""
    for ap in applications:
        if len(ap)>1:
            if ap.endswith(".exe") or ap in taskInfoManager.application_userTime:
                if ap in taskInfoManager.application_userTime:
                    result=result+ap+": "+json.dumps(taskInfoManager.application_userTime[ap])+" s\n"
            else:
                ap+='.exe'
                if ap in taskInfoManager.application_userTime:
                    result=result+ap+": "+json.dumps(taskInfoManager.application_userTime[ap])+" s\n"
    bot.reply_to(message, result)

@bot.message_handler(commands=['getType'])
def send_getType(message):
    applicationClassifiction.refreshRunningInfo()
    text = message.text
    applications = text[8:].strip().split(" ")
    result=""
    for app in applications:
        if app in applicationClassifiction.applicationClassifiction:
            result = result + "The type of " + app + " includes: "
            result = result + ', '.join(applicationClassifiction.applicationClassifiction[app])
    bot.reply_to(message, result)

@bot.message_handler(commands=['setTypes'])
def send_getType(message):
    applicationClassifiction.refreshRunningInfo()
    text = message.text
    info = text[9:].strip().split(" ")
    result=""
    name=info[0]
    if name in applicationClassifiction.applicationClassifiction:
        info.pop(0)
        applicationClassifiction.setClassifiction(name,info)
        result = result + "The type of " + name + " includes: "
        result = result + ', '.join(applicationClassifiction.applicationClassifiction[name])
    bot.reply_to(message, result)

@bot.message_handler(commands=['addType'])
def send_addType(message):
    applicationClassifiction.refreshRunningInfo()
    text = message.text
    applications = text[8:].strip().split(" ")
    result=""
    name = applications[0]
    if len(applications)>1:
        if name in applicationClassifiction.applicationClassifiction:
            applicationClassifiction.addClassifiction(name,applications[1])
            result = result + "The type of " + name + " includes: "
            result = result + ', '.join(applicationClassifiction.applicationClassifiction[name])
    bot.reply_to(message, result)

@bot.message_handler(commands=['removeType'])
def send_removeType(message):
    applicationClassifiction.refreshRunningInfo()
    text = message.text
    applications = text[11:].strip().split(" ")
    result=""
    name = applications[0]
    if len(applications)>1:
        if name in applicationClassifiction.applicationClassifiction:
            if applications[1] in applicationClassifiction.applicationClassifiction[name]:
                applicationClassifiction.removeClassifiction(name,applications[1])
                result = result + "The type of " + name + " includes: "
                result = result + ', '.join(applicationClassifiction.applicationClassifiction[name])
    bot.reply_to(message, result)

@bot.message_handler(commands=['getInfoByType'])
def send_getInfoByType(message):
    applicationClassifiction.refreshRunningInfo()
    taskInfoManager.refresh()
    text = message.text
    applications = text[14:].strip().split(" ")
    result= {}
    type = applications[0]
    if type:
        list=applicationClassifiction.getAppListByType(type)
        for app in list:
            if app in taskInfoManager.application_userTime:
                result[app]=taskInfoManager.application_userTime[app]
    bot.reply_to(message, json.dumps(result, indent=4))

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
