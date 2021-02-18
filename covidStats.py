import requests, json, time, datetime, asyncio




#country that has all the covid stats
class country:
    def __init__(self, code):
        self.code = code
        self.setInfo(code)
        self.setCovidStats(code)
        self.setDeltas(code)
        
    def setInfo(self, code):
        r = requests.get('https://restcountries.eu/rest/v2/alpha/' + code)
        data = r.text
        j = json.loads(data)
        self.name = j['translations']['es'] #change language here
        self.pop = j['population']

    def setCovidStats(self, code):
        with requests.Session() as s:
            r = s.get('https://covid19-api.org/api/status/' + self.code)
            data = r.text
            j = json.loads(data)
            self.cases = j['cases']
            self.casesWeighted =int((self.cases*100000)/self.pop)
            self.deaths = j['deaths']
            self.recovered = j['recovered']

    def setDeltas(self, code):
        with requests.Session() as s:   
            r = s.get('https://covid19-api.org/api/status/' + code + '?date=' + getDate14DaysAgo())
            data = r.text
            j = json.loads(data)
            self.weeklyCases = self.cases - j['cases']
            self.weeklyCasesWeighted = int((self.weeklyCases*100000)/self.pop)

    def getData(self):
        l = list(vars(self).values())
        l.remove(self.code)
        l.remove(self.pop)
        return l

#gets date from 14 days ago
def getDate14DaysAgo():
    currentDate = datetime.datetime.now()
    deltaDays = datetime.timedelta(days = 14)
    weekOldDate = currentDate - deltaDays
    return str(weekOldDate)[0:10]

     
