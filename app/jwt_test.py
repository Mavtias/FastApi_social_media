from jose import jwt
from datetime import datetime, timedelta

# Configuración
SECRET_KEY = "4a6d9b8e2f7a1c3d6f5b8e4a9c2e3f7d4a5b9e6c7f1a3d2b5c8e7f9b1c4d6e2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1  # Ajusta el tiempo de expiración para probar

# Crear un token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Verificar un token
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError as e:
        print(f"Error al decodificar el token: {e}")
        return None

# Prueba del flujo
if __name__ == "__main__":
    # Datos del token
    token_data = {"user_id": 9}

    # Crear el token
    token = create_access_token(token_data)
    print(f"Token generado: {token}")

    # Verificar el token
    decoded_payload = verify_access_token(token)
    if decoded_payload:
        print(f"Token decodificado: {decoded_payload}")
    else:
        print("El token no es válido.")
