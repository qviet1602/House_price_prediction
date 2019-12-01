import json

class Business:

    def __init__(self, business_id, business_name, rating, categories, address, city, state, zipcode):
        self.business_id = business_id
        self.business_name = business_name
        self.rating = rating
        self.categories = categories
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode


    def get_business_id(self):
        if self.business_id is None:
            return ""
        return self.business_id

    def get_business_name(self):
        if self.business_name is None:
            return ""
        self.business_name = self.business_name.replace('\'', '\'\'')
        return self.business_name

    def get_rating(self):
        if self.rating is None:
            return ""
        return self.rating

    def get_categories(self):
        if self.categories is None:
            return ""
        self.categories = self.categories.replace('\'', '\'\'')
        return self.categories

    def get_address(self):
        if self.address is None:
            return ""
        self.address = self.address.replace('\'', '\'\'')
        return self.address

    def get_city(self):
        if self.city is None:
            return ""
        self.city = self.city.replace('\'', '\'\'')
        return self.city

    def get_state(self):
        if self.state is None:
            return ""
        return self.state

    def get_zipcode(self):
        if self.zipcode is None:
            return ""
        return self.zipcode


def get_business_info():
    businesses = []
    with open("business.json", "r") as json_file:
        for line in json_file:
            line = line.rstrip("\n")
            json_line = json.loads(line)
            business_id = json_line['business_id']
            business_name = json_line['name']
            rating = json_line['stars']
            address = json_line['address']
            city = json_line['city']
            state = json_line['state']
            zipcode = json_line['postal_code']
            categories = json_line['categories']

            new_business = Business(business_id, business_name, rating, categories, address, city, state, zipcode)

            businesses.append(new_business)

    return businesses

def create_sql_file():
    business_list = get_business_info()
    sql_file = open("business_insert.sql", "a")
    for each in business_list:
        if each.get_city() == "" or each.get_state() == "" or each.get_zipcode() == "":
            continue

        zipcode_id_select = "(SELECT id from zipcode where zip_code='" + each.get_zipcode() + "')"
        insert_statement = "INSERT INTO business(business_id, name, categories, rating, address, zipcode_id)" \
                           "VALUES ('" + each.get_business_id() + "','" + each.get_business_name() + "','" + each.get_categories() \
                           + "','" + str(each.get_rating()) + "','" + each.get_address() + "'," \
                           + zipcode_id_select + ");"
        sql_file.write(insert_statement)
        sql_file.write("\n")

    sql_file.close()

create_sql_file()
