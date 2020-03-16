import json
import time

class CollectionFactory:
    def __init__(self):
        self.collections = {}

    def add(self, entity):
        code = entity['code']
        if code not in self.collections:
            self.collections[code] = Collection(entity)
        self.collections[code].add_data(entity)

    def to_json(self):
        for c in self.collections:
            payload = self.collections[c]
            if payload.granularity == 'world':
                payload.indicator('casConfirmes', 'Cas confirmés')
                payload.indicator('paysTouches', 'Pays Touches')
                payload.indicator('deces', 'Sujets décédés')

            if payload.granularity == 'country':
                payload.indicator('casConfirmes', 'Cas confirmés')
                payload.indicator('deces', 'Sujets décédés')

            if payload.granularity == 'region':
                payload.indicator('casConfirmes', 'Cas confirmés')
                payload.indicator('deces', 'Sujets décédés')

            if payload.granularity == 'departement':
                payload.indicator('casConfirmes', 'Cas confirmés')
                payload.indicator('reanimation', 'Sujets en réanimation')
                payload.indicator('deces', 'Sujets décédés')
                payload.indicator('victimes', 'Informations sur les victimes')
            delattr(payload, '_data')
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Collection:
    def __init__(self, entity):
        self._data = {}
        self.indicators = {}
        self.name = entity['nom']
        self.code = entity['code']
        self.granularity = None
        self._granularity(entity)
        
        
    def add_data(self, entity):
        # remove object identification
        del entity['nom']
        del entity['code']
        
        # entity date
        date = entity['date']
        del entity['date']

        self._data[date] = entity
    
    def _granularity(self, entity):
        if entity['code'] == 'FRA':
            self.code = 'COUNTRY-FRA'
            self.granularity = 'country'
        if entity['code'] == 'WORLD':
            self.granularity = 'world'
        elif entity['code'].startswith('REG-'):
            self.granularity = 'region'
        elif entity['code'].startswith('DEP-'):
            self.granularity = 'departement'
    
    def indicator(self, name, description):
        g = Graph(name)
        for date in sorted(self._data, reverse = True):
            if name in self._data[date]:
                g.add_data(self._data)
                self.indicators[name] = {'date': date, 'description': description, 'value': self._data[date][name], 'source': self._data[date]['source'], 'graph': g }
                return
        self.indicators[name] = {'date': time.strftime('%Y-%M-%d'), 'description': description, 'value': None, 'source': "Pas d'information" }

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)

class Graph:
    def __init__(self, name):
        self.name = name
        self.data = []

    def add_data(self, payload):
        name = self.name
        for date in sorted(payload):
            if name in payload[date]:
                if type(payload[date][name]) == list: 
                    value = len(payload[date][name])
                else: 
                    value = payload[date][name]
                self.data.append({'t': date, 'y': value})
