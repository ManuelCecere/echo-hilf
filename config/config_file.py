import os
from dotenv import load_dotenv

# Load credentials.env file if exists
env_path = "config/credentials.env"
load_dotenv(dotenv_path=env_path)


# Define your configuration as class properties
class Config:
    OPENAI_KEY = os.getenv("OPENAI_KEY")  # No default value


config_obj = Config()
print(config_obj)












