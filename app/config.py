from pydantic import BaseSettings

# creating env variables
class Settings(BaseSettings):
    database_password : str = "localhost"
    database_username : str = "postgress"
    secret_key:str = "23298wudsiajkh"

settings = Settings()