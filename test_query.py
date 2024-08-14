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
    for i in range(count, size):
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
    script_file.write("{ time ldbadd -H ldap://192.168.40.19 -U administrator --password=qqqwww12! " + file_name + "_add.ldif; } 2>> result_add_data.txt\n")
    script_file.write(f"echo \"{file_name} is done!\" >> result_add_data.txt\n")
        
#======================Delete======================#

def createQueryForDelete(file_name, script_file, count, size):
    file = open(file_name+"_delete.ldif", 'w')
    for i in range(count, size):
        ldif = [
            f"dn: CN=user_{i},{domain_dn}",
            "changetype: delete",
            "\n"
        ]
        file.write("\n".join(ldif))
    file.close()
    script_file.write("{ time ldapmodify -H ldap://192.168.40.19 -x -D \"CN=administrator,CN=Users,DC=example,DC=tst\" -w qqqwww12! -f " + file_name + "_delete.ldif > /dev/null; } 2>> result_delete_data.txt\n" )
    script_file.write(f"echo \"{file_name} is done!\" >> result_delete_data.txt\n")

#=======================Update====================#

def createQueryForUpdate(file_name, script_file, count, size):
    file = open(file_name+"_update.ldif", 'w')
    for i in range(count, size):
        ldif = [
            f"dn: CN=user_{i},{domain_dn}",
            "changetype: modify",
            "replace: mail",
            f"mail: user{i}@{Domain}.mod",
            "\n"
        ]
        file.write("\n".join(ldif))
    file.close()
    script_file.write("{ time ldapmodify -H ldap://192.168.40.19 -x -D \"CN=administrator,CN=Users,DC=example,DC=tst\" -w qqqwww12! -f " + file_name + "_update.ldif > /dev/null; } 2>> result_update_data.txt\n")
    script_file.write(f"echo \"{file_name} is done!\" >> result_update_data.txt\n")

#=================Script================#

script_add_file = open("add_script.sh", 'w')
script_add_file.write("#!/bin/bash\n")
script_add_file.write("touch result_add_data.txt\n")
script_upd_file = open("upd_script.sh", 'w')
script_upd_file.write("#!/bin/bash\n")
script_upd_file.write("touch result_update_data.txt\n")
script_del_file = open("del_script.sh", 'w')
script_del_file.write("#!/bin/bash\n")
script_del_file.write("touch result_delete_data.txt\n")

сount_record = int(input("Write count records:"))
step = int(input("Write step:"))

for current_value in range(1,сount_record, step):
    fullName = FileName+"_"+str(current_value)+"-"+str(current_value+step-1 )
    createQueryForAdd( fullName, script_add_file, current_value, current_value+step )
    createQueryForUpdate( fullName, script_upd_file, current_value, current_value+step )
    createQueryForDelete( fullName, script_del_file, current_value, current_value+step )

print("LDAP requests have been created!")

script_add_file.write("nohup ./upd_script.sh\nexit")
script_add_file.close()
script_upd_file.write("nohup ./del_script.sh\nexit")
script_upd_file.close()
script_del_file.close()