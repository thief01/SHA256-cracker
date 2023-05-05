import itertools
import string
import hashlib
import threading
import time
from multiprocessing import Process
from multiprocessing import Pool
# SuperFastPython.com
import math
from concurrent.futures import ProcessPoolExecutor

class Cracker:

    def __init__(self, passwordHash, passwordCount, charactersAtEnd):
        self.passwordHash = passwordHash
        self.passwordCount = passwordCount
        self.usingLettersSet = string.ascii_letters.strip()
        self.usingLettersSet = string.ascii_lowercase.strip()
        self.charactersCounts = len(self.usingLettersSet)
        self.combinations = self.charactersCounts**passwordCount
        self.charactersAtEnd = charactersAtEnd
        self.stopAllThreads = False
        self.checkedPasswords = 0
        self.crackedPassword = ""
        self.done = False

        self.dividersForRests = [0] * self.passwordCount
        for i in range(0,self.passwordCount):
            self.dividersForRests[i] = self.charactersCounts ** (i + 1)


    def StartCrackingNormal(self):
        self.CrackingLoop()

    def StartCrackingByMultiTasking(self, threads):

        thread = threading.Thread(target=self.LogLoop)
        thread.start()
        ths = []

        for i in range(0, threads):
            params = self.generateStartingParameters(i, threads)
            self.printsStatingPositions(params, i)
            tempThread = threading.Thread(target=self.CrackingLoop, args=(params,))
            tempThread.start()
            ths.append(tempThread)

        thread.join()

    def StartSimpleTask(self):
        self.CrackingLoop([0] * self.passwordCount)

    def TestPool(self, threadId, threads):
        args= self.generateStartingParameters(threadId, threads)
        self.CrackingLoop(args)


    def CrackingLoop(self, startingParameters: []):
        passwordIds = startingParameters
        rounds = 0

        for i in range(0, self.combinations):
            self.ComparePassword(self.GetPasswords(passwordIds))
            if self.crackedPassword:
                break

            rounds += 1
            self.checkedPasswords += 1
            passwordIds[0] += 1
            password = ""
            for j in range(0, len(passwordIds)):
                if passwordIds[j] >= len(self.usingLettersSet):
                    passwordIds[j] = 0
                    if j + 1 < len(passwordIds):
                        passwordIds[j + 1] += 1
    def StartReallyMultiThread(self, params: []):
        if __name__ == '__main__':
            # report a message
            print('Starting task...')
            # create the process pool
            with ProcessPoolExecutor(8) as exe:
                # perform calculations
                exe.map(cracker.ComparePassword, range(1, self.combinations))
            # report a message
            print('Done ALL COMBOSES.')

    def LogLoop(self):
        previousTime = time.perf_counter()
        while True:
            currentTime = time.perf_counter()
            execution_time = currentTime - previousTime
            if execution_time > 1:
                print(f"Combinations {self.checkedPasswords}/{self.combinations} Progress:" , str(self.checkedPasswords / self.combinations * 100) + "%")
                previousTime = time.perf_counter()
            if self.crackedPassword:
                break
    def TestLoop(self):
        previousTime = time.perf_counter()
        id = 0
        while True:
            currentTime = time.perf_counter()
            execution_time = currentTime - previousTime
            if execution_time > 0.00001:
                id += 1
                self.ComparePasswordWithNewRule(id)
                previousTime = time.perf_counter()
            if self.crackedPassword:
                break


    def GetPasswords(self, generatedParameters):
        text = ""
        for i in range(0, self.passwordCount):
            text += self.usingLettersSet[generatedParameters[i]]
        return text

    def ComparePasswordWithNewRule(self, combinationId):
        rests = [0] * self.passwordCount
        dividers = [0] * self.passwordCount
        toDivide = [0] * self.passwordCount

        previousRest = combinationId
        for i in reversed(range(0, len(self.dividersForRests))):
            rests[i] = previousRest % self.dividersForRests[i]
            dividers[i] = previousRest / self.dividersForRests[i]
            if i+1 < len(self.dividersForRests):
                if dividers[i] > 1:
                    dividers[i+1] = int(dividers[i])
                else:
                    dividers[i+1] = 0
            if i == 0:
                dividers[i] = rests[i]
            previousRest = rests[i]
        # print(combinationId)
        # print(self.dividersForRests)
        # print(rests)
        # print(dividers)
        print(self.GetPasswords(dividers))
        # self.crackedPassword = "XD"
        # self.done = False



    def ComparePassword(self, generatedPassword) -> bool:
        generatedPassword+= self.charactersAtEnd
        hash_object2 = hashlib.sha256(generatedPassword.encode())
        newHash = hash_object2.hexdigest()

        if newHash == self.passwordHash:
            self.stopAllThreads = True
            self.crackedPassword = generatedPassword
            print("Password got breaked:", generatedPassword)
            return True
        return False

    def ComparePasswordWithCurrent(self, generatedPassword):
        generatedPassword+= self.charactersAtEnd
        hash_object2 = hashlib.sha256(generatedPassword.encode())
        newHash = hash_object2.hexdigest()
        print(newHash)
        print(newHash == self.passwordHash)

    def generateStartingParameters(self, threadId, maxThreads) -> []:
        if threadId == 0:
            params = [0] * self.passwordCount
            return params
        params = [0] * (self.passwordCount-1)
        everyThread = self.charactersCounts / maxThreads
        everyThread = int(everyThread)
        lastParam = threadId * everyThread
        if threadId * everyThread >= self.charactersCounts:
            lastParam = self.charactersCounts-1
        params.append(lastParam)
        return params

    def printsStatingPositions(self, params, id):
        text = ""
        for i in range(0, len(params)):
            text += self.usingLettersSet[params[i]]
        print("Started with:", text, "at thread ID:", id)






# cracker = Cracker("08cf04af4d3b7e903cb15582d02b7fce682f867f04e9b9a82ea719f6e7ecad63", 3, "")
cracker = Cracker("8338482d1dc4f7d3447b41fa646b354c2dce447c3028d087561d856a2b99d47b", 6, "ia!")
# cracker.ComparePasswordWithCurrent("xdd")

cracker.StartCrackingByMultiTasking(10)


