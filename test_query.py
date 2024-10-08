#===========CHANGE==========================================
#Domain    = "test-example.tst"   # Именование домена            =
UserPref  = "user_"         # Префикс пользователя         =
UserPass  = "qqqwww12!"     # Пароль пользователей         =
FileName  = "users"         # Имя файла                    =
#===========CHANGE==========================================

Domain = input("Write you domain name:")
ip = input("Write DC ip:")
DC1, DC2 = Domain.rsplit('.', 1)

import base64

domain_dn = "CN=Users"
for a in Domain.split("."):
    domain_dn += f",DC={a}"

#=======================Update====================#

def queryModifyAfterAdd(file_name, script_file, count, size):
    file = open(file_name+"_add_update.ldif", 'w')
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

def queryModifyBeforeDelete(file_name, script_file, count, size):
    file = open(file_name+"_del_update.ldif", 'w')
    for i in range(count, size):
        ldif = [
            f"dn: CN=user_{i},{domain_dn}",
            "changetype: modify",
            "replace: mail",
            f"mail: Yser{i}@{Domain}.mod",
            "\n"
        ]
        file.write("\n".join(ldif))
    file.close()

#======================Read======================#

def queryRead(file_name, script_file, count, size):
    file = open(file_name+"_update.ldif", 'w')
    for i in range(count, size):
        ldif = [
            f"dn: {domain_dn}",
            "uid: user_{i}",
            "\n"
        ]
        file.write("\n".join(ldif))
    file.close()

#======================Create======================#
def createQueryForAdd(file_name, script_file, count, size):
    file = open(file_name+"_add.ldif", 'w')
    readQuery = open(file_name + "_read_after_add.sh", 'w')
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
             f"mail: user_{i}@{Domain}",
             "unicodePwd:: " + base64.b64encode(f'"{UserPass}"'.encode('UTF-16LE')).decode('UTF-8'),
             "\n"
        ]
        file.write("\n".join(ldif))
        readQuery.write(f"ldapsearch -H ldap://{ip} -x -D \"CN=administrator,CN=Users,DC={DC1},DC={DC2}\" -w qqqwww12! -b \"DC={DC1},DC={DC2}\" \"(cn=user_{i})\"\n")
    file.close()
    #add
    script_file.write(f"{{ time ldbadd -H ldap://{ip} -U administrator --password=qqqwww12! " + file_name + "_add.ldif; } 2>> result_add.txt | tr '\\n' ' '\n")
    script_file.write(f"echo \"{file_name} is done!\" >> result_add.txt\n")
    #read
    script_file.write( f"chmod +x {file_name}_read_after_add.sh\n")
    script_file.write( f"{{ time ./{file_name}_read_after_add.sh >/dev/null; }} 2>> result_add_read.txt\n" )
    script_file.write( f"echo \"{file_name} is done!\" >> result_add_read.txt\n")
    #update
    queryModifyAfterAdd(file_name, script_file, count, size)
    script_file.write(f"{{ time ldapmodify -H ldap://{ip} -x -D \"CN=administrator,CN=Users,DC={DC1},DC={DC2}\" -w qqqwww12! -f " + file_name + "_add_update.ldif > /dev/null; } 2>> result_add_update.txt | tr '\\n' ' '\n")
    script_file.write(f"echo \"{file_name} is done!\" >> result_add_update.txt\n\n")
        
#======================Delete======================#

def createQueryForDelete(file_name, script_file, count, size):
    file = open(file_name+"_delete.ldif", 'w')
    readQuery = open(file_name + "_read_before_delete.sh", 'w')
    for i in range(count, size):
        ldif = [
            f"dn: CN=user_{i},{domain_dn}",
            "changetype: delete",
            "\n"
        ]
        file.write("\n".join(ldif))
        readQuery.write(f"ldapsearch -H ldap://{ip} -x -D \"CN=administrator,CN=Users,DC={DC1},DC={DC2}\" -w qqqwww12! -b \"DC={DC1},DC={DC2}\" \"(cn=user_{i})\"\n")
    file.close()
    #update
    queryModifyBeforeDelete(file_name, script_file, count, size)
    script_file.write( f"{{ time ldapmodify -H ldap://{ip} -x -D \"CN=administrator,CN=Users,DC={DC1},DC={DC2}\" -w qqqwww12! -f " + file_name + "_del_update.ldif > /dev/null; } 2>> result_delete_update.txt | tr '\\n' ' '\n")
    script_file.write( f"echo \"{file_name} is done!\" >> result_delete_update.txt\n")
    #read
    script_file.write( f"chmod +x {file_name}_read_before_delete.sh\n")
    script_file.write( f"{{ time ./{file_name}_read_before_delete.sh >/dev/null; }} 2>> result_delete_read.txt\n")
    script_file.write( f"echo \"{file_name} is done!\" >> result_delete_read.txt\n")
    #delete
    script_file.write(f"{{ time ldapmodify -H ldap://{ip} -x -D \"CN=administrator,CN=Users,DC={DC1},DC={DC2}\" -w qqqwww12! -f " + file_name + "_delete.ldif > /dev/null; } 2>> result_delete.txt | tr '\\n' ' '\n" )
    script_file.write(f"echo \"{file_name} is done!\" >> result_delete.txt\n\n")

#=================Script================#
script_add_file = open("add.sh", 'w')
script_add_file.write("#!/bin/bash\n")
script_add_file.write("touch result_add.txt\n")
script_add_file.write("touch result_add_read.txt\n")
script_add_file.write("touch result_add_update.txt\n")
#=====================================================#
script_del_file = open("delete.sh", 'w')
script_del_file.write("#!/bin/bash\n")
script_del_file.write("touch result_delete_update.txt\n")
script_del_file.write("touch result_delete_read.txt\n")
script_del_file.write("touch result_delete.txt\n")

сount_record = int(input("Write count records:"))
init_value = int(input("Write start value (Exp user_1, user_1000):"))
step = int(input("Write step:"))

for current_value in range(init_value,сount_record, step):
    fullName = FileName+"_"+str(current_value)+"-"+str(current_value+step-1 )
    createQueryForAdd( fullName, script_add_file, current_value, current_value+step )

print("LDAP requests for add have been created!")

for current_value in range(init_value,сount_record, step):
    fullName = FileName + "_" + str(current_value) + "-" + str(current_value + step - 1)
    createQueryForDelete(fullName, script_del_file, current_value, current_value + step)

print("LDAP requests for delete have been created!")

script_add_file.write("nohup ./delete.sh\nexit")
script_add_file.close()
script_del_file.close()