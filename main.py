import json
from argparse import ArgumentParser
from Config import test_config, dev_config, prod_config, DBConnection
from Utils import Utility
from datetime import date

'''
1.Create two runtime argument env & user_args:
2.Environment prod/dev/test as mandatory.
        1.User will be restricted to choose either of env. Incase of test env, user need to give DB, Schema & table name to user_args.
        2.User_args as optional to take multiple values.
            1.This argument will take DB, table & schema name. If either of the value will be passed incase of either of the env. This should override the values of configuration. Error message in case of any of the value is not passed.
            2.Note: user_args is mandatory in case of test env.
'''
argparser = ArgumentParser()
argparser.add_argument('-e','--env',required=True, default='test',choices=['test', 'prod', 'dev'])
argparser.add_argument('-u', '--user_args', required=False)
args = vars(argparser.parse_args())

userArgs = json.loads(args['user_args'])
if args['env'] == 'test':
    try:
        dbname = userArgs[0]['dbname']
        table_name = userArgs[1]['table']
        schema_name = userArgs[2]['schema']
        print(dbname, table_name, schema_name)

    except Exception:

        print('user_args is mandatory in case of test environment.')
        exit(0)

print("Environment",args['env'])
#Arguments for test:  -e test -u [{\"dbname\":\"Employee\"},{\"table\":\"Accounts\"},{\"schema\":\"Payroll\"}]

'''
2.Create two DB in database as prod & dev respective configuration files.
'''

if(args['env']=='test'):
    default_config = test_config
elif(args['env']=='prod'):
    default_config = prod_config
elif(args['env']=='dev'):
    default_config = dev_config

'''
3.Create config package which initialize all the prod/dev/test configurations.
'''
conn = DBConnection()
my_conn = conn.connect(default_config)
print(default_config)
cursor = my_conn.cursor()
print('DB Init')

'''
4.Create DBConnection class template contains methods for select/insert/create table/export/import/other operations.
'''
class Template(DBConnection):
    def select(self, mycursor, query):
        mycursor.execute(query)
        return mycursor.fetchall()
    def create_table(self, mycursor):
        # Creating table as per requirement
        sql = '''CREATE TABLE IF NOT EXISTS PERSON(
           FIRST_NAME CHAR(20) NOT NULL,
           LAST_NAME CHAR(20),
           AGE INT,
           SEX CHAR(1),
           CREATION_TIME DATE
        )'''
        mycursor.execute(sql)
        print("Table created successfully........")
    def insert(self,mycursor,val):
        sql = "INSERT INTO PERSON VALUES " + val
        mycursor.execute(sql)
        print("Data inserted successfully........")

'''
5.Create utils package to have methods other than mentioned in previous tasks.
'''
class Util_Class(Utility):
    def uppercase(self, name):
        return name.upper()
    def lowercase(self, name):
        return name.lower()
    def length(self,name):
        return len(name)
"""
6.Create 3 classes by any name of person with in same family. Insert the person details into table as instance is created. Details are: first_name, last_name, age, sex, creation_time.
    1.Note: If the last name of a person will change then change all other’s last name also.
"""
class Class1(Template):

    def age(self, birthdate):
        today = date.today()
        age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
        return age

    def get_list(self, mycursor, age):
        sql = '''SELECT FIRST_NAME FROM PERSON WHERE AGE > '''  + str(age)
        mycursor.execute(sql)
        return mycursor.fetchall()

class Class2(DBConnection):
    def create_table(self, mycursor):
        # Creating table as per requirement
        sql = '''CREATE TABLE IF NOT EXISTS EMPLOYEE(
              EMP_NAME CHAR(20) NOT NULL,
              DOB DATE,
              SEX CHAR(1),
              MOBILE CHAR(10)
           )'''
        mycursor.execute(sql)
        print("New Schema Table created successfully........")

class Class3(Template):
    def update_last_name(self, mycursor, last_name):
        sql = '''UPDATE PERSON SET LAST_NAME = ''' + "\'" + last_name +"\'"
        print(sql)
        mycursor.execute(sql)
        print("Data updated successfully........")

util = Util_Class()
print(util.uppercase('raj'))
print(util.lowercase('Kumar'))
print(util.length('kshitij'))
# Write a query and execute it with cursor
query = 'SELECT * FROM PERSON'
obj = Template()
'''
7.Class1 & Class3 wants to go with default db operations. But, Class2 want's to have create_table operation in different schema.
'''
obj1 = Class1()
obj2 = Class3()
obj3 = Class2()
obj.create_table(cursor)
data = '("Kshitij","Apar",32, "M","10-12-2022")'
obj.insert(cursor,data)
result = obj.select(cursor,query)
obj3.create_table(cursor)
'''
8.Create a method to update the last_name Class3.
'''
obj2.update_last_name(cursor,"Gupta")
result = obj2.select(cursor,query)
print(result)
'''
9.Create a method to get the age of the person as per the dob given.
'''
person_age = obj1.age(date(2000, 1, 1))
'''
10.Create a method to get the list of the person first name whose age is greater than 18 years.
'''
print(obj1.get_list(cursor,person_age))


#Command to run program
# C:\codetech\Python\programs\venv\Scripts\python.exe C:/codetech/Python/programs/main.py -e dev -u [{\"dbname\":\"Employee\"},{\"table\":\"Accounts\"},{\"schema\":\"Human\"}]