import json

class data:
    data=[]

    def read(self):
        with open('data/data.json','r') as file:
            data = json.load(file)
            self.data=data['results']
    def getPeriodo(self):
        periodos = []
        for row in self.data:
            periodo = row['Periodo']
            if periodo not in periodos:
                periodos.append(periodo)
        return periodos

    def getEntidad(self):
        entidades = []
        for row in self.data:
            entidad = row['Entidad_Federativa']
            if entidad not in entidades:
                entidades.append(entidad)
        return entidades
        
    def getDatos(self, Periodo, Entidad_Federativa):
        infoGpoEdad = []
        for row in self.data:
            opc1 = row['Periodo']
            opc2 = row['Entidad_Federativa']
            if opc1 == Periodo and opc2 == Entidad_Federativa:
                infoGpoEdad.append([periodoI,entidadI,row['Sexo']])
        return infoGpoEdad