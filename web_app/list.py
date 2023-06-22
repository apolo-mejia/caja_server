class listas:
    def __init__(self):
        # self.key_list = key_list
        self.dato = {'key_list':'mano_soporte', 'name':'Marcas de soportes','data':[('def','Llevar lista'),('fag','FAG'),('ina','INA'),('skf','SKF'),
        ('snr','SNR'),('ntn','NTN'),('koy','KOYO'),('nsk','NSK'),('smt','SEALMASTER'),('lbt','LINK BELT'),('oth','Other..')]}
        
    def datalist(self):
        list = self.dato['data']
        for key in self.dato['data']:
    #        list.append( key , dato )
            print(key)
        return list