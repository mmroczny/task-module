import requests
import json
import datetime

class TaskExecutor:
    

    def __init__(self, taskType, taskName, limit = 10):
        self.logs = []
        self.taskType = taskType
        self.taskName = taskName
        self.limit = limit
        self.current_task_id = None


    def __sendLogs(self, logsToSend):

        url = 'http://192.168.1.50:8080/api/v1/tasks/logs'
        x = requests.post(url = url, json= {"logs": logsToSend})
        print(logsToSend)
        print(x)
        print(x.content)

    
    def __downloadTasks(self):

        url= f'http://192.168.1.50:8080/api/v1/tasks/tasks-for-processing?taskType={self.taskType}&taskName={self.taskName}&limit={self.limit}'  # noqa: E501
        getTasks = requests.get(url=url).json()
        
        taskList = []

        for task in getTasks:
            taskList.append((task['uuid'], task['name'],
                            json.loads(task['taskData'])))
    
        return taskList
        

    def __sendRemamingLogs(self):
        if self.logs != []:
            self.__sendLogs(self.logs)   
        self.logs = []     

    def __addLog(self, msg, level, taskId, immidiate = False):
        

        logOccurred = datetime.datetime.utcnow().isoformat() + "Z"

        self.logs.append({
            "taskId": self.current_task_id,
            "logType": level,
            "logContent": msg,
            "logOccurredAt": logOccurred,
        })
        if immidiate:
            self.__sendRemamingLogs()


    def logDebug(self, msg, immidiate = False):
        self.__addLog(msg, 'DEBUG', immidiate)
    def logInfo(self, msg, immidiate = False):
        self.__addLog(msg, 'INFO', immidiate)
    def logWarning(self, msg, immidiate = False):
        self.__addLog(msg, 'WARNING', immidiate)
    def logError(self, msg, immidiate = False):
        self.__addLog(msg, 'ERROR', immidiate)
    def logSuccess(self, msg, immidiate = False):
        self.__addLog(msg, 'SUCCESS', immidiate)

    def __markAsStarted(self):
        startUrl = 'http://192.168.1.50:8080/api/v1/tasks/started'  # noqa: E501
        requests.post(url = startUrl, json= {"tasks": [{"taskId": self.current_task_id}]})
        



    def __markAsFinished(self, stat):
        finUrl = 'http://192.168.1.50:8080/api/v1/tasks/finished'
        requests.post(url = finUrl, json= {'tasks': [{"taskId": self.current_task_id, "taskStatus": stat}]})

        
    def __ok(self):
        self.__markAsFinished("OK")

    def __nok(self):
        self.__markAsFinished("KO")

    def __exception(self, exception):
        self.logError(str(exception))
        self.__markAsFinished("KO")

    def __triggerOneTask(self, task):
        taskData = task[2]
        self.current_task_id = task[0]
        self.__markAsStarted()
        try:
            wynik = self.processTask(taskData)
            if wynik is True:
                self.__ok()
            else:
                self.__nok()
        except Exception as e:
            self.__exception(e)
        self.__sendRemamingLogs()


    def run(self):
        tasks = self.__downloadTasks()
        for task in tasks:
            self.__triggerOneTask(task)
        
    def processTask(self, taskData):
        raise Exception("Overwrite this method!")



