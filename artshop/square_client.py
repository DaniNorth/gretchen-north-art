import os
from dotenv import load_dotenv
from square import Square
from square.environment import SquareEnvironment

load_dotenv()

# Will need to update once in production
client = Square(
    environment=SquareEnvironment.SANDBOX,
    token=os.environ.get("SQUARE_ACCESS_TOKEN")
)
