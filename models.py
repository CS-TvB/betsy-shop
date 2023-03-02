# Models go here
from peewee import *

db = SqliteDatabase('betsy_shop.db')

class tag(Model):
    tag = CharField(unique=True)
    
    class Meta:
        database = db

class product(Model):
    name = CharField()
    description = CharField()
    ppu = FloatField(constraints=[Check("ppu >= 0")])
    quantity = IntegerField(constraints=[Check("quantity >= 0")])
    tags = ManyToManyField(tag)
    
    class Meta:
        database = db
        indexes = (
        (("name", "description"), True),
        )

class user(Model):
    name = CharField()
    adress = CharField()
    bilinfo = CharField()
    inventory = ManyToManyField(product)
    
    class Meta:
        database = db

class transaction(Model):
    product = ForeignKeyField(product)
    user_buyer = ForeignKeyField(user)
    quantity = IntegerField(constraints=[Check("quantity > 0")])
    timestamp = DateTimeField()
    
    class Meta:
        database = db

def create_tables():
    with db:
        db.create_tables([user, product, tag, transaction, product.tags.get_through_model(), user.inventory.get_through_model()])

def delete_tables():
    with db:
        db.drop_tables([user, product, tag, transaction, product.tags.get_through_model(), user.inventory.get_through_model()])
