import socket
import json
import mysql.connector
import setting



with open("domains.txt") as input_file:
    domains = input_file.read().split()

    result = []
    for domain in domains:
        ip = socket.gethostbyname(domain)
            
        result.append({
            "name": domain,
            "ip": ip
        })

with open("domains.json", "w") as output_file:
    result_json = json.dumps(result, indent=4)
    output_file.write(result_json)
    
connection = mysql.connector.connect(
    host=setting.host,
    user=setting.user,
    password=setting.password,
    port=setting.port,
    # database=setting.db_name
)

cursor = connection.cursor()

cursor.execute("create database if not exists Internet")
cursor.execute("use Internet")
cursor.execute("""create table if not exists Domain (
    id int auto_increment primary key, 
    domain varchar(128) not null, 
    ip varchar(128) not null)""")

for i in result:
    cursor.execute("insert into Domain (domain, ip) VALUES (%s, %s)", (i["name"], i["ip"]))
    
connection.commit()
connection.close()
    

            