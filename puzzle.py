import requests
import sys, os, re;
from memrise import Memrise
class puzzle:

    s = requests.Session()
    def saveToFile(self, name, data, path):
        f = open(path + "/"  + name, 'w')
        f.write(str(data))
        f.close()


    def auth(self, login, password):
        url = 'https://puzzle-english.com/'

        data = { 'email': login, 'password': password, 'ajax_action':'ajax_common_signinUser', 'redirect_to': '/mobauth' }
        req =  self.s.post(url, data=data) # this will make the method "POST"

        print(req)



    def getData(self, text):
       data = text.split('\n')
       check = 0
       count = 1
       dicRus = {}
       dicEng = {}

       for string in data:
           result = re.findall(r"^\s+[^<{*]+", string)
           if (len(result) > 0):
               if (result[0].lstrip() != ""):
                   temp = result[0].lstrip()
                   if (check == 0):
                       dicEng[count] = temp.replace('&#039;', "'").replace('&quot;', "\"")

                       check = 1
                       continue
                   if(check == 1):
                       check = 0
                       dicRus[count] = temp.replace('&#039;', "'").replace('&quot;', "\"")
                       count  +=1


       print(dicEng)
       print (dicRus)
       return (dicEng, dicRus)

    def getUrlPhased(self, text):
        result = re.findall(r"\"audio\":\"(.+?)\/phrases_audio", text)
        return result[0].replace('\\', '')

    #https://images.puzzle-english.com/video/greatbig_story/valley_tombs/phrases_audio/1.mp3
    def work(self, login, password,  name, memriseLogin, memrisePassword, coloda):

        try:
            os.mkdir(name)
        except Exception:
            print("")

        self.auth(login, password);
        url = 'https://puzzle-english.com/video/'+name+'/print'
        print (url)
        book = self.s.get(url)
        (dicEng, dicRus) = self.getData (book.text)
        self.saveToFile("rus.txt", dicRus, name)

        self.saveToFile("eng.txt", dicEng, name)

        url = 'https://puzzle-english.com/video/'+name+'/work'
        urlPhased = self.s.get(url)



        string = self.getUrlPhased(urlPhased.text)
        i = 0
        while (i > -1):
            url = string + "/phrases_audio/" + str(i) + ".mp3"
            try:
                print(url)
                logo = self.s.get(url, stream=True)
                if (logo.status_code != 200):
                    break
                f = open(name + "/"  + str(i + 1) + ".mp3", 'wb')
                f.write(logo.content)
                f.close()
                i = i + 1
            except Exception as ex:
                print(ex)
                exit(0)

        memrise = Memrise()
        memrise.add(dicEng, dicRus, name, memriseLogin, memrisePassword, coloda)

