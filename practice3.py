import telebot
import json
import time
import psutil
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

@bot.message_handler(commands=['task'])
def send_tasklist(message):
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

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()
