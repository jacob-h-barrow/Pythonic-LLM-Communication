import subprocess
import sys
import multiprocessing
import time 
import os
import json

class ProblemManager:
    def __init__(self, problemNumber, studentCode = "", username="jb2396"):
        self.q = multiprocessing.Queue()
        self.queue = []
        self.file = "./files/swapFiles/temp_problem_" + str(problemNumber) + "_" + username
        self.problemNumber = str(problemNumber)
        self.studentCode = studentCode
        
    def correctSyntax(self):
        if subprocess.run(["pyflakes", self.file], capture_output=True).returncode != 0:
            return False
        return True
    
    def testSyntax(self):
        with open(self.file, "w") as writer:
            writer.write("import sys\nimport json\n")
            writer.write(self.studentCode)
            writer.write("\nprint(check(*json.loads(sys.argv[1])))")
       
        if self.correctSyntax() == True:
            memory, cpu = self.runMultiThread()
            os.remove(self.file)
            if len(self.queue):
                return memory, cpu, sorted(self.queue, key = lambda x: x[0])
        return False

    def getInfo(self):
        first2Lines = open("/proc/meminfo", "r")
        return int(first2Lines.readline().split()[1]) - int(first2Lines.readline().split()[1])
                    
    def testCode(self, idx, data, testCase):
        ### data -> answer, memoryLimit
        ### testCase -> input: list always
        data = data.split()
        _ans = data[0]
        _timeout = int(data[1])
        try:
            response = subprocess.run(["python3", self.file, json.dumps(testCase)], capture_output=True, timeout=_timeout).stdout.decode().strip()
            print(response, _ans)
        except:
            response = "Timed Out"

        if response == "Timed Out":
            self.q.put([idx, response])
        else:
            self.q.put([idx, response == _ans])
        
    def runMultiThread(self):
        baseline = self.getInfo()
        mem = []
        startTime = time.time()

        with open("./files/problems/problem_" + self.problemNumber) as f:
            answers = f.read().strip().split("\n")

        with open("./files/testCases/testCase_" + self.problemNumber) as f:
            testCases = json.loads(f.read())
        
        for idx in range(len(answers)):
            exec('p{a} = multiprocessing.Process(target = {b}, args = {c})'.format(a = str(idx), b='self.testCode', c = (idx, answers[idx], testCases[idx],)))
            exec('p{a}.start()'.format(a=idx))
                 
        for idx in range(len(answers)):
            exec('p{a}.join()'.format(a=idx))
            mem.append(abs(self.getInfo()-baseline))

        while self.q.empty() is False:
            self.queue.append(self.q.get())

        return sum(mem)/len(mem), time.time() - startTime
    
    def isCorrect(self):
        result = self.testSyntax()
        if result == False:
            return False

        for caseIdx in range(len(result[-1])):
            if result[-1][caseIdx][1] == False:
                # Returns testCase that fails
                return caseIdx

        # Returns (memoryLoad, cpuLoad)
        return result[:-1]


#test = ProblemManager(sys.argv[1], sys.argv[2])
with open(sys.argv[2]) as f:
    code = f.read()

test = ProblemManager(sys.argv[1], code)
print(test.testSyntax())
print(test.isCorrect())
