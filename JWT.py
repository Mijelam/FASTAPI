from jwt import encode,decode

def createToken(data:dict):
    token: str=encode(payload=data,key='Holi',algorithm='HS256')
    return token

def validateToken(token:str):
    data: dict=decode(token,key='Holi',algorithms=["HS256"])
    return data