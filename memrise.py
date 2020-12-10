import requests
import re
import json

class Memrise:

    def add(self, dicEng, dicRus, name, login, password, coloda):
        s = requests.Session()
        headers = {
             'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
             'Host': 'www.memrise.com'


        }

        #url = 'https://memr.com/'

        url = 'https://www.memrise.com/login/'
        temp = s.get(url, headers = headers)
        result = re.findall(r"csrfmiddlewaretoken\" value=\"(.+?)\"\>" , temp.text)
        print (result[0])

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
           'Upgrade-Insecure-Requests': '1',
            'Referer': 'https://www.memrise.com/login/'

        }
        print(s.cookies.get_dict())
        data = { 'username': login, 'password': password, 'csrfmiddlewaretoken':result[0], 'next': "" }
        req =  s.post(url, data=data, headers=headers) # this will make the method "POST"

        if (coloda[-1] =='/'):
            coloda = coloda[:-1]

        url = coloda + '/edit'

        print (url)
        temp = s.get(url, headers = headers)
        result = re.findall(r"csrftoken: \"(.+?)\"" , temp.text)
        token = result[0]

        result = re.findall(r"data-pool-id=\"(.+?)\"\>" , temp.text)
        pool = result[0]


        result = re.findall(r"data-course-id=\"(.+?)\"" , temp.text)
        course = result[0]
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
            'Upgrade-Insecure-Requests': '1',
            'Referer': url,
            'Host': 'www.memrise.com',
                      'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-CSRFToken':token,
            'X-Requested-With': 'XMLHttpRequest'

        }


        url = 'https://www.memrise.com/ajax/level/add/'
        data = { 'kind': 'things', 'course_id': course, 'pool_id':pool}
        req =  s.post(url, data=data, headers=headers) # this will make the method "POST"

        print (req.text)
        result = re.findall(r"edit\/\#l\_(.+)\"" , req.text)
        level = result[0]


        url = 'https://www.memrise.com/ajax/level/set_title/'
        data = { 'level_id':level, "new_val":name}
        req =  s.post(url, data=data, headers=headers) # this will make the method "POST"


        length = len(dicEng)

        for id in range(1, length+1):
            url = 'https://www.memrise.com/ajax/level/thing/add/'
            string = {"1":dicEng[id], "2":dicRus[id]}
            print (str(string))
            data = { 'columns':json.dumps(string), "level_id":level}
            req =  s.post(url, data=data, headers=headers)

            print (req.text)
            js = json.loads(req.text)
            print(js['thing']['id'])
            url = 'https://www.memrise.com/ajax/thing/cell/upload_file/'
            files = {'f': open(name + "/" + str(id) + ".mp3", 'rb')}
            data = { 'thing_id':js['thing']['id'], "cell_id":3, "cell_type":'column', }
            req =  s.post(url, data=data, files=files, headers=headers)
            print (req.text)