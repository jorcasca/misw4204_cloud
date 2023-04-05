from flask_restful import Resource
import requests

def validadorRutas():
    urls = [
        'http://localhost:5003/rutas',
        'http://localhost:5004/rutas',
        'http://localhost:5005/rutas'
    ]
    resultados = []
    for url in urls:
        respuesta = requests.get(url)
        resultados.append(respuesta) 

    print(resultados[0].status_code)
        
    if resultados[0].json()==resultados[1].json()==resultados[2].json():
        if resultados[0].status_code==200:
            print("Microservicios /rutas estan funcionando")
            #requests.post('http://localhost:5002/log',json={"mensaje":"Microservicios /rutas estan funcionando"})
            return resultados[0].json()
        else:
            print("Falla general de los microservicios")
           # requests.post('http://localhost:5002/log',json={"mensaje":"Falla general de los microservicios"})
            return 'Todos los servicios han fallado (1)', 404
    elif resultados[0].json()==resultados[1].json()!=resultados[2].json():
        if resultados[0].status_code==200:
            print("Microservicio ms3/rutas no esta funcionando")
            #requests.post('http://localhost:5002/log',json={"mensaje":"Microservicio ms3/rutas no esta funcionando"})
            return resultados[0].json()
        else:
            print("Microservicio ms1 y ms2/rutas no esta funcionando")
            #requests.post('http://localhost:5002/log',json={"mensaje":"Microservicio ms1 y ms2/rutas no esta funcionando"})
            return resultados[2].json()
        
    elif resultados[0].json()==resultados[2].json()!=resultados[1].json():
        if resultados[0].status_code==200:
            print('Microservicio ms2/rutas no esta funcionando')
            #requests.post('http://localhost:5002/log',json={"mensaje":"Microservicio ms2/rutas no esta funcionando"})
            return resultados[0].json()
        else:
            print("Microservicio ms1 y ms3/rutas no esta funcionando")
            #requests.post('http://localhost:5002/log',json={"mensaje":"Microservicio ms1 y ms3/rutas no esta funcionando"})
            return resultados[1].json()
    elif resultados[1].json()==resultados[2].json()!=resultados[0].json():
        if resultados[1].status_code==200:
            print("Microservicio ms1/rutas no esta funcionando")
            #requests.post('http://localhost:5002/log',json={"mensaje":"Microservicio ms1/rutas no esta funcionando"})
            return resultados[1].json()
        else:
            print("Microservicio ms2 y ms3/rutas no esta funcionando")
            #requests.post('http://localhost:5002/log',json={"mensaje":"Microservicio ms2 y ms3/rutas no esta funcionando"})
            return resultados[0].json()
    else:
        #requests.post('http://localhost:5002/log',json={"mensaje":"Falla general de los microservicios"})
        return 'Todos los servicios han fallado', 404

class VistaRuta(Resource):

    def get(self):
        return validadorRutas()
    
# class VistaLog(Resource):
#     def post(self):
#         print(request.json["mensaje"])
#         registrar_log.delay(request.json["mensaje"],datetime.utcnow())
#         return "ok", 200 
    