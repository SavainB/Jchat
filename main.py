import mysql.connector
import rsa
user_private_key = ""
user_online = ""
user_id = ""
user_name = ""
id_du_mec = ""
key_publique_du_mec = ""


def inscription():
    pseudo = input("| Taper votre pseudo : ")
    print("+--------------------------------------------+")
    mdp= input("| Taper votre mot de passe : ")
    print("+--------------------------------------------+")
    key = (rsa.gen_rsa_keypair(128))
    public_key = (key[0][0], key[0][1])
    conn = mysql.connector.connect(user='c9AB91ZTWs', password='RbvnvmTKqv',
                                   host='remotemysql.com',  port="3306", database='c9AB91ZTWs')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO `Users` VALUES (%s, %s,%s, %s,%s)",
                   (None, str(pseudo), str(mdp), str(key), str(public_key)))
    conn.commit()
    conn.rollback()
    conn.close()
    print("| vous avez réussi votre inscription")


def connexion():
    utilisateur = input("| Taper votre pseudo : ")
    print("+--------------------------------------------+")
    password = input("| Taper votre mot de passe : ")
    print("+--------------------------------------------+")
    conn = mysql.connector.connect(user='c9AB91ZTWs', password='RbvnvmTKqv',
                                   host='remotemysql.com',  port="3306", database='c9AB91ZTWs')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `Users`")
    data = cursor.fetchall()
    for name in data:
        if name[1] == utilisateur:
            if name[2] == password:
                global user_online, user_name, user_id, user_private_key
                user_online = str(name[3])
                user_name = name[1]
                user_id = str(name[0])
                user_private_key = str(name[3])
                print("| Clé privée ["+user_private_key+"]")
                conn.commit()
                conn.rollback()
                conn.close()
                print("+----------------------------------------------------------+")
                print("|| Bonjour [" + str(user_name) +
                      "] vous avez réussi votre connexion")
                print("+----------------------------------------------------------+")
                return True
    print("+----------------------------------------------------------+")
    print("|| Votre mot de passe ou votre nom d'utilisateur est incorrect")
    print("+----------------------------------------------------------+")


def choix_user():
    print("+----------------------------------------------------------+")
    print("| Taper l'id de la personne dont vous voulez communiquer   |")
    print("+----------------------------------------------------------+")
    conn = mysql.connector.connect(user='c9AB91ZTWs', password='RbvnvmTKqv',
                                   host='remotemysql.com',  port="3306", database='c9AB91ZTWs')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `Users`")
    data = cursor.fetchall()
    print("+----------------------------------------------------------+")
    for name in data:
        print("| "+str(name[1])+" id ["+str(name[0])+"]")
    print("+----------------------------------------------------------+")
    conn.rollback()
    conn.close()
    selection = input("| Votre séléction : ")
    conn = mysql.connector.connect(user='c9AB91ZTWs', password='RbvnvmTKqv',
                                   host='remotemysql.com',  port="3306", database='c9AB91ZTWs')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM `Users`")
    data = cursor.fetchall()
    for name in data:
        if str(name[0]) == str(selection):
            print("+----------------------------------------------------------+")
            print(
                "Vous avez choisis l'utilisateur prénommé ["+str(name[1])+"]")
            print("+----------------------------------------------------------+")
            global id_du_mec, key_publique_du_mec
            id_du_mec = name[0]
            key_publique_du_mec = name[4]
            conn.rollback()
            conn.close()
            return True
    return False


def state_conversation():
    print("+----------------------------------------------------------+")
    print("| Affichez la conversation avec cette personne ? Taper [1] |")
    print("+----------------------------------------------------------+")
    print("| Envoyez un message à cette personne ?          Taper [2] |")
    print("+----------------------------------------------------------+")
    print("| Discuter avec quelqu'un d'autre ?              Taper [3] |")
    print("+----------------------------------------------------------+")
    choix = input("| Votre séléction : ")
    if choix == '1':
        conn = mysql.connector.connect(user='c9AB91ZTWs', password='RbvnvmTKqv',
                                       host='remotemysql.com',  port="3306", database='c9AB91ZTWs')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM `Conversations`")
        data = cursor.fetchall()
        print("+----------------------------------------------------------+")
        for message in data:
            if str(message[1]) == user_id and str(message[1]) == id_du_mec or str(message[2]) == user_id or str(message[1]) == id_du_mec:
                msg_chiffrer = eval(message[3])
                
                print("Le message chiffrer ["+str(msg_chiffrer)+"]")
                user_private_key = eval(user_online)
                dec = rsa.rsa_dec(msg_chiffrer, user_private_key)
                print("Le message déchiffrer : "+str(dec))
        print("+----------------------------------------------------------+")
        conn.commit()
        conn.rollback()
        conn.close()
    elif choix == '2':
        msg = input(str(user_name)+": ")
        while (len(msg) > 17):
            print("+----------------------------------------------------------+")
            print(
                "|| Pour une raison de sécurité, nous avons décider de limiter à au max 16 charactere")
            msg = input(str(user_name)+": ")
            print("+----------------------------------------------------------+")
        enc = rsa.rsa_enc(msg, eval(key_publique_du_mec))
        conn = mysql.connector.connect(user='c9AB91ZTWs', password='RbvnvmTKqv',
                                       host='remotemysql.com',  port="3306", database='c9AB91ZTWs')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO `Conversations` VALUES (%s, %s,%s,%s)",
                       (None, user_id, id_du_mec, str(enc)))
        conn.commit()
        conn.rollback()
        conn.close()
    elif choix == '3':
        return False


while (True):
    print("+--------------------------------------------+")
    print("| Voulez-vous vous creer un compte Taper [1] |")
    print("+--------------------------------------------+")
    print("| Voulez-vous vous connecter       Taper [2] |")
    print("+--------------------------------------------+")
    choix = input("| Votre séléction : ")
    print("+--------------------------------------------+")
    if choix == '1':
        inscription()
    elif choix == '2':
        if connexion():
            while (True):
                if choix_user():
                    while (True):
                        if state_conversation() == False:
                            break
