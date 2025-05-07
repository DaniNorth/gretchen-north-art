import os
from dotenv import load_dotenv
from square import Square
from square.environment import SquareEnvironment

client = Square(
    environment=SquareEnvironment.SANDBOX, 
)
