import requests
import json
import base64
import time


class API(object):
    
    def __init__(self):
        self.url = "https://dev.sighthoundapi.com/v1/recognition?objectType=vehicle,licenseplate"
        self.headers = {"Content-Type": "application/json", "X-Access-Token": "wbpDL7Slz7j1yTyBqxPAFmQofOrMoPKL3QfW"}
        
    def get_data(self):
        img_data = base64.b64encode(open("car.jpg", "rb").read()).decode()
        data = json.dumps({"image": img_data})
        endpoint= requests.post(self.url, headers=self.headers, data=data)
        data = endpoint.json()
        return data
    
    def data_extraction(self):
        print('evts')
        data = self.get_data()
        if data.get('objects', False):
             car_object_list = []
             for i in range(len(data['objects'])):
               result= {}
               vehicle_annotation = data["objects"][i]["vehicleAnnotation"]
               result["make"] = vehicle_annotation['attributes']['system']['make']['name']
               result["model"] = vehicle_annotation['attributes']['system']['model']['name']
               result["color"] = vehicle_annotation['attributes']['system']['color']['name'].capitalize()
               if vehicle_annotation.get('licenseplate', False):
                   license_plate = vehicle_annotation["licenseplate"]['attributes']['system']['string']['name']
                   try:
                       int(license_plate[0:2])
                       result["license_plate"] = vehicle_annotation["licenseplate"]['attributes']['system']['string']['name']
                   except:
                       pass
                    
               car_object_list.append(result)
             print(car_object_list)
             self.post_data(car_object_list)
             return car_object_list
           
        else:
            return False
        
    def post_data(self, car_object_list):
        print("post_data")
        fecth = requests.post('http://192.168.1.106:5555', json = car_object_list)
        return True
        # fecth = requests.post('http://192.168.1.102:5555', json = car_object_list)
        # fecth = requests.post('http://192.168.43.102:5555', json = car_object_list)
        # print(fecth.json())
        # time.sleep(1)
        
        
         
        