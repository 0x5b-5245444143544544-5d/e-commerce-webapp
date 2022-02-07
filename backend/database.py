import dataset
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

from backend.config import config

class Database:
    def __init__(self) -> None:
        self.host = config['database']['host']
        self.database = config['database']['database']
        self.user = config['database']['user']
        self.password = config['database']['password']

        if not all([self.host, self.database, self.user, self.password]):
            print("Error! Some required configs weren't set, exiting!")
            raise SystemExit
        
        self.url = f"mysql://{self.user}:{self.password}@{self.host}/{self.database}"
        self.setup()
    
    def get(self) -> dataset.Database:
        """
        Returns the dataset connection object.
        """
        return dataset.connect(url=self.url)
    
    def setup(self) -> None:
        """
        Sets up required tables, if they don't exist yet.
        """
        engine = create_engine(self.url, connect_args=dict(host=self.host, port=3306))
        if not database_exists(engine.url):
            create_database(engine.url)
        
        db = self.get()

        if "items" not in db:
            items = db.create_table("items")
            items.create_column("item_name", db.types.text)
        
        if "cart" not in db:
            cart = db.create_table("cart")
            cart.create_column("item_id", db.types.integer)
            cart.create_column("user_id", db.types.integer)

        if "orders" not in db:
            orders = db.create_table("orders")
            orders.create_column("item_id", db.types.integer)
            orders.create_column("order_quantity", db.types.integer)
        
        if "user_info" not in db:
            user_info = db.create_table("user_info")
            user_info.create_column("email", db.types.text)
            user_info.create_column("password", db.types.text)
            user_info.create_column("is_seller", db.types.boolean)