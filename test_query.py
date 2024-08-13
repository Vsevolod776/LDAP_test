#===========CHANGE==========================================
Domain    = "example.tst"   # Именование домена            =
UserPref  = "user_"         # Префикс пользователя         =
UserPass  = "qqqwww12!"     # Пароль пользователей         =
FileName  = "users"         # Имя файла                    =
#===========CHANGE==========================================

import base64

domain_dn = "CN=Users"
for a in Domain.split("."):
    domain_dn += f",DC={a}"

#======================Create======================#

def createQueryForAdd(file_name, script_file, count, size):
    file = open(file_name+"_add.ldif", 'w')
    for i in range(count, count + size):
        ldif = [
            f"dn: CN=user_{i},{domain_dn}",
             "objectClass: top",
             "objectClass: person",
             "objectClass: organizationalPerson",
             "objectClass: user",
            f"cn: user_{i}",
             "sn: logon",
            f"givenName: Test{i}",
            f"displayName: Test Logon{i}",
            f"userPrincipalName: user_{i}@{Domain}",
            f"sAMAccountName: user_{i}",
             "userAccountControl: 512",
             f"mail: user_{i}@{Domain}"
             "unicodePwd:: " + base64.b64encode(f'"{UserPass}"'.encode('UTF-16LE')).decode('UTF-8')
        ]
        file.write("\n".join(ldif))
    file.close()
    script_file.write("{ time ldbadd -H ldap://192.168.40.19 -U administrator --password=qqqwww12! " + file_name + "_add.ldif } > result_add_data.txt\n")
    script_file.write(f"echo \"{file_name} is done!\" > result_add_data.txt\n")
    print(f"\nFile {file_name}_add.ldif - done!")
        
#======================Delete======================#

def createQueryForDelete(file_name, script_file, count, size):
    file = open(file_name+"_delete.ldif", 'w')
    for i in range(count, count + size):
        ldif = [
            f"dn: CN=user_{i},{domain_dn}",
            "changetype: delete"
        ]
        file.write("\n".join(ldif))
    file.close()
    script_file.write("{ time ldapmodify -H ldap://192.168.40.19 -x -D \"CN=administrator,CN=Users,DC=example,DC=tst\" -f " + file_name + "_delete.ldif > /dev/null -w qqqwww12! } > result_delete_data.txt\n" )
    script_file.write(f"echo \"{file_name} is done!\" > result_delete_data.txt\n")
    print(f"\nFile {file_name}_delete.ldif - done!")

#=======================Update====================#

def createQueryForUpdate(file_name, script_file, count, size):
    file = open(file_name+"_update.ldif", 'w')
    for i in range(count, count + size):
        ldif = [
            f"dn: CN=user_{i},{domain_dn}",
            "changetype: modify",
            "replace: mail",
            f"mail: user{i}@{Domain}.mod"
        ]
        file.write("\n".join(ldif))
    file.close()
    script_file.write("{ time ldapmodify -H ldap://192.168.40.19 -x -D \"CN=administrator,CN=Users,DC=example,DC=tst\" -f " + file_name + "_update.ldif > /dev/null -w qqqwww12! } > result_update_data.txt\n")
    script_file.write(f"echo \"{file_name} is done!\" > result_update_data.txt\n")
    print(f"\nFile {file_name}_update.ldif - done!")

#=================Script================#

TestArray = [1000, 4000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000, 5000,     #50k
             10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, #150k
             10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, #250k
             10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, #350k
             10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, #450k
             10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, #550k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #700k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #850k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #1m
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #1m150k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #1m300k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #1m450k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #1m600k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #1m750k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #1m900k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #2m50k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #2m200k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #2m350k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #2m500k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #2m650k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #2m800k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #2m950k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #3m100k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #3m250k
             15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, 15000, #3m400k
            ]

init_value = 1

script_add_file = open("add_script.sh", 'w')
script_add_file.write("#!/bin/bash\n")
script_add_file.write("touch result_add_data.txt\n")
script_upd_file = open("upd_script.sh", 'w')
script_upd_file.write("#!/bin/bash\n")
script_upd_file.write("touch result_update_data.txt\n")
script_del_file = open("del_script.sh", 'w')
script_del_file.write("#!/bin/bash\n")
script_del_file.write("touch result_delete_data.txt\n")

for value in TestArray:
    fullName = FileName+"_"+str(init_value)+"-"+str(init_value+value-1)
    createQueryForAdd( fullName, script_add_file, init_value, value )
    createQueryForUpdate( fullName, script_upd_file, init_value, value )
    createQueryForDelete( fullName, script_del_file, init_value, value )
    init_value += value

script_add_file.close()
script_upd_file.close()
script_del_file.close()