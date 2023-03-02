__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

from datetime import datetime
import models

def search(argument):
    products_found = []
    argument = argument.lower()
    query = models.product.select()
    for item in query:
        words_in_name = 0
        words_in_desc = 0
        for word in item.name.lower().split():
            for words in argument.lower().split():
                if words == word:
                    words_in_name += 1
        for word in item.description.lower().split():
            for words in argument.lower().split():
                if words == word:
                    words_in_desc += 1
        if words_in_name > 0 or words_in_desc > 0:
            products_found.append(item)
    return products_found

def view_user_products(user_id):
    query = models.user.get_by_id(user_id)
    return query.inventory

def view_products_for_tag(tag_id):
    tag_id = models.tag.get_by_id(tag_id)
    query = models.product.select()
    result = []
    for item in query:
        for t in item.tags:
            if tag_id == t:
                result.append(item)
    return result

def add_product_to_users_stockroom(user_id, product):
    user = models.user.get_by_id(user_id)
    current_owned = []
    for item in user.inventory:
        current_owned.append(item)
    current_owned.append(product)
    user.inventory = current_owned
    user.save()
    return None

def update_stock(product_id, new_quantity):
    product = models.product.get_by_id(product_id)
    product.quantity = new_quantity
    product.save()
    return None

def buy_product(product_id, buyer_id, quantity):
    product = models.product.get_by_id(product_id)
    buyer = models.user.get_by_id(buyer_id)
    if product.quantity >= quantity:
        product.quantity -= quantity
        product.save()
        transaction = models.transaction.create(product=product, user_buyer=buyer, quantity=quantity, timestamp=datetime.now())
        transaction.save()
        return True
    else:
        return False

def remove_product(product_id):
    product = models.product.get_by_id(product_id)
    product.delete_instance()
    return None

def test_database():
    def users():
        chad = models.user(name = "Chad Chaddington", adress = "Chadstreet 1", bilinfo = "NL12 CHAD 1234 5678 90")
        chad.save()
        game_meneer = models.user(name = "Game Meneer", adress = "Gamestreet 1", bilinfo = "NL12 GAME 1234 5678 90")
        game_meneer.save()
        pro_gamer = models.user(name = "Pro Gamer", adress = "Progamestreet 1", bilinfo = "NL12 GAMR 1234 5678 90")
        pro_gamer.save()

        razer_naga = models.product.select().where(models.product.name == "Razer Naga gaming mouse")[0]
        steelseries_arctis = models.product.select().where(models.product.name == "Steelseries Arctis 7 gaming headset")[0]
        razer_blackwidow = models.product.select().where(models.product.name == "Razer Blackwidow gaming keyboard")[0]

        chad.inventory = [razer_naga]
        chad.save()
        game_meneer.inventory = [steelseries_arctis]
        game_meneer.save()
        pro_gamer.inventory = [razer_naga, steelseries_arctis, razer_blackwidow]
        pro_gamer.save()
    
    def products():
        razer_naga = models.product(name = "Razer Naga gaming mouse", description = "Gaming mouse with 12 programmable buttons", ppu = 69.95, quantity = 10, for_sale = True)
        razer_naga.save()
        steelseries_arctis = models.product(name = "Steelseries Arctis 7 gaming headset", description = "Gaming headset with 7.1 surround sound", ppu = 99.95, quantity = 5, for_sale = True)
        steelseries_arctis.save()
        razer_blackwidow = models.product(name = "Razer Blackwidow gaming keyboard", description = "Gaming keyboard with mechanical keys", ppu = 149.95, quantity = 2, for_sale = True)
        razer_blackwidow.save()
        samsung = models.product(name = "Samsung Galaxy S20", description = "Smartphone with 8GB RAM", ppu = 699.95, quantity = 1, for_sale = True)
        samsung.save()

        expensive = models.tag.select().where(models.tag.tag=="expensive")
        amazing = models.tag.select().where(models.tag.tag=="amazing")
        worth_it = models.tag.select().where(models.tag.tag=="worth it")
        cool = models.tag.select().where(models.tag.tag=="cool")
        pro = models.tag.select().where(models.tag.tag=="pro")
        necessary = models.tag.select().where(models.tag.tag=="necessary")

        razer_naga.tags = [expensive, amazing, worth_it, cool]
        razer_naga.save()
        steelseries_arctis.tags = [amazing, worth_it, cool, pro]
        steelseries_arctis.save()
        razer_blackwidow.tags = [cool, pro, necessary]
        razer_blackwidow.save()
        samsung.tags = [expensive, amazing, worth_it, cool, pro, necessary]
        samsung.save()

    def tags():
        models.tag.create(tag = "expensive")
        models.tag.create(tag = "amazing")
        models.tag.create(tag = "worth it")
        models.tag.create(tag = "cool")
        models.tag.create(tag = "pro")
        models.tag.create(tag = "necessary")

    tags()
    products()
    users()

def testings():
    models.delete_tables()
    models.create_tables()
    test_database()

    search_result = search("gameng mouse")
    for item in search_result:
        print("test search: ", item.name)

    result = view_user_products(1)
    for item in result:
        print("users products: ", item.name)

    new_result = view_products_for_tag(3)
    print ("tag has been found in", new_result)
    for item in new_result:
        print("search for product by tag: ", item.name)

    buy_product(3, 2, 1)

    samsung = models.product.get_by_id(4)
    add_product_to_users_stockroom(1, samsung)

    chad = models.user.get_by_id(1)
    for item in chad.inventory:
        print("chad inventory: ", item.name)

testings()


