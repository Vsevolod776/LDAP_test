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
             "unicodePwd:: " + base64.b64encode(f'"{UserPass}"'.encode('UTF-16LE')).decode('UTF-8'),
             "\n"
        ]
        file.write("\n".join(ldif))
    file.close()
    script_file.write("time ldbadd -H ldap://192.168.40.19 -U administrator --password=qqqwww12! " + file_name + "_add.ldif"+"\n")
    print("\nCreate users file - done!")
        
#======================Delete======================#

def createQueryForDelete(file_name, script_file, count, size):
    file = open(file_name+"_delete.ldif", 'w')
    for i in range(count, count + size):
        ldif = [
            f"dn: CN=user_{i},{domain_dn}",
            "changetype: delete",
            "\n"
        ]
        file.write("\n".join(ldif))
    file.close()
    script_file.write("time ldbadd -H ldap://192.168.40.19 -U administrator --password=qqqwww12! " + file_name + "_delete.ldif"+"\n")
    print("\nFile for delete users - done!")


#=======================Update====================#

def createQueryForUpdate(file_name, script_file, count, size):
    file = open(file_name+"_update.ldif", 'w')
    for i in range(count, count + size):
        ldif = [
            f"dn: CN=user_{i},{domain_dn}",
            "changetype: modify",
            "replace: mail",
            f"mail: user{i}@{Domain}.mod",
            "\n"
        ]
        file.write("\n".join(ldif))
    file.close()
    script_file.write("time ldbadd -H ldap://192.168.40.19 -U administrator --password=qqqwww12! " + file_name + "_update.ldif"+"\n")
    print("\nFile for delete users - done!")

#=================Script================#

def createScriptFile( file, file_name ):


    file.close()

TestArray = [1000, 4000, 20000, 25000, 50000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000,
             100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000,
             100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000, 100000]

init_value = 1

script_add_file = open("add_script.sh", 'w')
script_add_file.write("#!/bin/bash \n")
script_upd_file = open("upd_script.sh", 'w')
script_upd_file.write("#!/bin/bash \n")
script_del_file = open("del_script.sh", 'w')
script_del_file.write("#!/bin/bash \n")

for value in TestArray:
    fullName = FileName+"_"+str(init_value)+"-"+str(init_value+value-1)
    createQueryForAdd( fullName, script_add_file, init_value, value )
    createQueryForUpdate( fullName, script_upd_file, init_value, value )
    createQueryForDelete( fullName, script_del_file, init_value, value )
    init_value += value

script_add_file.close()
script_upd_file.close()
script_del_file.close()