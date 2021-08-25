# coding: utf-8
"""
Base para desarrollo de modulos externos.
Para obtener el modulo/Funcion que se esta llamando:
     GetParams("module")

Para obtener las variables enviadas desde formulario/comando Rocketbot:
    var = GetParams(variable)
    Las "variable" se define en forms del archivo package.json

Para modificar la variable de Rocketbot:
    SetVar(Variable_Rocketbot, "dato")

Para obtener una variable de Rocketbot:
    var = GetVar(Variable_Rocketbot)

Para obtener la Opcion seleccionada:
    opcion = GetParams("option")


Para instalar librerias se debe ingresar por terminal a la carpeta "libs"
    
    pip install <package> -t .

"""

import requests
import base64

module = GetParams("module")

if module == "GetOCR":
    image_path = GetParams("image_path")
    path_type = GetParams("path_type")
    api_key = GetParams("api_key")
    result = GetParams("result")

if image_path.startswith("http"):
    image = {
        "source": {
            "imageUri": image_path
        }
    }

else:
    with open(image_path, 'rb') as image_file:
        img = image_file.read()
        content = base64.b64encode(img).decode()

    image = {
        "content": content
    }

body = {
    "requests": [
        {
            "image": image,
            "features": [
                {
                    "type": "TEXT_DETECTION"
                }
            ]
        }
    ]
}
body = json.dumps(body)

try:
    response = requests.post("https://vision.googleapis.com/v1/images:annotate?key={key}".format(key=api_key),
                             data=body)
    json_resp = response.json()
    
    if "error" in json_resp:
        SetVar(result, json_resp["error"]["message"])
        raise Exception(json_resp["error"]["message"])
    if "responses" in json_resp:
        texto = json_resp["responses"]
        SetVar(result, json.dumps(texto))

except Exception as e:
    PrintException()
    raise e
