import mysql.connector

user_online = ""
user_id = ""
user_name = ""
id_du_mec = ""


def inscription():
    print("Votre pseudo")
    pseudo = input()
    print("Votre mot de passe")
    mdp = input()
    conn = mysql.connector.connect(user='c9AB91ZTWs', password='RbvnvmTKqv',
                                   host='remotemysql.com',  port="3306", database='c9AB91ZTWs')
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # Executing the SQL command
    cursor.execute("INSERT INTO `Users` VALUES (%s, %s,%s, %s,%s)",
                   (None, str(pseudo), str(mdp), "None", "None"))
    # Commit your changes in the database
    conn.commit()
    # Rolling back in case of error
    conn.rollback()
    # Closing the connection
    conn.close()


def connexion():
    print("Votre pseudo")
    utilisateur = input()
    print("Votre Mot de passe")
    password = input()
    conn = mysql.connector.connect(user='c9AB91ZTWs', password='RbvnvmTKqv',
                                   host='remotemysql.com',  port="3306", database='c9AB91ZTWs')
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # Executing the SQL command
    cursor.execute("SELECT * FROM `Users`")
    data = cursor.fetchall()
    for name in data:
        if name[1] == utilisateur:
            if name[2] == password:
                global user_online, user_name, user_id
                user_online = True
                user_name = name[1]
                user_id = str(name[0])
                conn.commit()
                # Rolling back in case of error
                conn.rollback()
                # Closing the connection
                conn.close()
                print("Bonjour " + str(user_name) +
                      " vous avez réussi votre connexion")
                return True


def choix_user():
    print("A qui envoyer un message ? (choissisez le chiffre apres le nom pour selectionner)")
    conn = mysql.connector.connect(user='c9AB91ZTWs', password='RbvnvmTKqv',
                                   host='remotemysql.com',  port="3306", database='c9AB91ZTWs')
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # Executing the SQL command
    cursor.execute("SELECT * FROM `Users`")
    data = cursor.fetchall()
    for name in data:
        print(str(name[1])+" id ("+str(name[0])+")")
        # Rolling back in case of error
    conn.rollback()
    # Closing the connection
    conn.close()
    selection = input()
    conn = mysql.connector.connect(user='c9AB91ZTWs', password='RbvnvmTKqv',
                                   host='remotemysql.com',  port="3306", database='c9AB91ZTWs')
    # Creating a cursor object using the cursor() method
    cursor = conn.cursor()
    # Executing the SQL command
    cursor.execute("SELECT * FROM `Users`")
    data = cursor.fetchall()

    for name in data:
        if str(name[0]) == str(selection):
            print("Vous avez choisis l'utilisateur prénommé "+str(name[1]))
            global id_du_mec
            id_du_mec = name[0]
            # Rolling back in case of error
            conn.rollback()
            # Closing the connection
            conn.close()
            return True
    return False


def state_conversation():
    print("Affichez la conversation avec cette personne ? 1")
    print("Envoyez un message à cette personne ? 2")
    print("Discuter avec quelqu'un d'autre ? 3")
    choix = input()
    if choix == '1':
            conn = mysql.connector.connect(user='c9AB91ZTWs', password='RbvnvmTKqv',
                                           host='remotemysql.com',  port="3306", database='c9AB91ZTWs')
            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()
            # Executing the SQL command
            cursor.execute("SELECT `message` FROM `Conversations` WHERE `id_emmeteur` = (%s) AND `id_recepteur` = (%s) OR `id_emmeteur` = (%s) AND `id_recepteur` = (%s) ", (
                user_id, id_du_mec, id_du_mec, user_id))
            data = cursor.fetchall()
            for i in data:
                print(i)
            # Commit your changes in the database
            conn.commit()
            # Rolling back in case of error
            conn.rollback()
            # Closing the connection
            conn.close()
    elif choix == '2':
            msg = input(str(user_name)+": ")
            conn = mysql.connector.connect(user='c9AB91ZTWs', password='RbvnvmTKqv',
                                           host='remotemysql.com',  port="3306", database='c9AB91ZTWs')
            # Creating a cursor object using the cursor() method
            cursor = conn.cursor()
            # Executing the SQL command
            cursor.execute("INSERT INTO `Conversations` VALUES (%s, %s,%s,%s)",
                           (None, user_id, id_du_mec, str(msg)))
            # Commit your changes in the database
            conn.commit()
            # Rolling back in case of error
            conn.rollback()
            # Closing the connection
            conn.close()
    elif choix == '3':
            return False


while (True):
    print("Voulez-vous vous creer un compte taper 1")
    print("Voulez-vous vous connecter taper 2")
    choix = input()
    if choix == '1':
        inscription()
    elif choix == '2':
        if connexion():
            while (True):
                if choix_user():
                    while (True):
                        if state_conversation() == False:
                            break
                        
