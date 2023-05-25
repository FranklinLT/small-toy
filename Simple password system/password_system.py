import pickle
'[1]Youtube.com, 2021. [Online]. Available:' 
'https://www.youtube.com/watch?v=GXHVyjGhFuc. [Accessed: 28- Nov- 2021].'
import os
import time
import random
import math

def encrypt(password):
    """encrypt the password

    use time package to get the timestamp,
    use the last four digits as key to encrypt the password

    :param password: a string of password the users input
    :return:a string of encrypted password
    """
    key = str(time.time())[-5:-1]
    # get the key from timestamp, so every key is different
    pw = key + password
    # add key to password
    if len(key) != len(pw):
        for i in range(len(pw)):
            key+=key[i%4]
    key=key[0:len(pw)]
    L=[]
    for i in range(len(pw)):
        crypted = chr((ord(pw[i])+ord(key[i])-66)%95+33)
        L+=[crypted]
    crypted = ''.join(L)
    return crypted


def decrypt(encrypted_pw):
    """decrypt the password

    reverse the encryption process and delete the first four digits(key)

    :param encrypted_pw:a string of encrypted password which got from the local file
    :return:a string of decrypted password
    """

    crypted = encrypted_pw
    cryptkey = crypted[0:4]
    realkeylist = []
    realpw = []
    for i in cryptkey:
        realkeylist += chr(int((ord(i)+33)/2))
    realkey = ''.join(realkeylist)
    if len(realkey) != len(crypted):
        for i in range(len(crypted)):
            realkey += realkey[i%4]
    key=realkey[0:len(crypted)]
    for i in range(len(crypted)):
        for j in range(2):
            KeyPw = chr(95*j+ord(crypted[i])+33-ord(key[i]))
            if ord(KeyPw)>=33 and ord(KeyPw)<=126:
                realpw += [KeyPw]
    realpw = ''.join(realpw[4:])
    return realpw

def Password_input_and_storage():
    """store the input password

    This function can be called in function 'Function_choose'.
    In this function, function 'test2()' will be called to test the strength of users password,
    if the strength is weak, function 'PasswordGeneration()' will be called to suggust the users to replace their passwords.
    When storing account information, the password is encrypted with the function 'encrypt()'
    
    
    :param encrypted_pw: three string which the users input will be formated to Dictionarie{A:{B:C}}
    and the Dictionarie will be converted to binary form in 'Passwordsystem.txt' by the external 
    function 'pickle'.
    :return: none
    """

    while True:
        N = input('Please input a type of account you want to save:')
        with open('Passwordsystem.txt','rb') as f:
            dict = pickle.load(f)
        if N in dict:
            print('The type is already saved, please change to another one (eg:type(n))')
            continue
        A = input('Please input the account number you want to save:')
        P1 = input('Please input the corresponding password you want to save:')
        L1,L2 = test2(P1)
        if L2 <= 35:
            L3 = PasswordGeneration()
            print(L1,"\nThe system has generated a password for you:",L3)
            An = input('1.Replace with new password\n2.Still use the original password\n'
            '3.Change a new password to save(self)\n4.Back to the function menu\nPlease input your choice:')
            if An == '1':
                P1 = L3
            elif An == '2':
                print('You have used the original password')
            elif An == '3':
                continue
            elif An == '4':
                print('You have returned to the menu.')
                break
            else:
                print('Your input is unknown and has returned to the menu.')
                break
        else:
            print('The password strength is fine.')
        
        P2 = input('Please retype the password to verify:')
        if P1 == P2 :
            # the passwords are matched
            f = open('Passwordsystem.txt','rb')
            Dict = pickle.load(f)
            if list(Dict.keys()) == []:
                Dict = {'Administrator': {first_line: last_line}}
            if list(Dict.keys())[0] == 'Administrator':
                f.close()
                f = open('Passwordsystem.txt','wb+')
                print('Hi, welcome, free to use this new function.')
                P1 = encrypt(P1)
                # encrypt P1
                Dict = {N:{A:P1}}
                # store the account type, password and account as dictionary in dictionary
                pickle.dump(Dict,f)
                f.close()
                if f.closed == True:
                    print('Your password has saved successfully, you have returned to the menu.')
                    break
                else:
                    print('Your password has saved but the text has not closed, you have returned to the menu. please check.')
                    break
            else:
                f.close()
                f = open('Passwordsystem.txt','rb+')
                Dict = pickle.load(f)
                f.close()
                with open('Passwordsystem.txt','wb+') as f:
                    P1 = encrypt(P1)
                    Dict[N] = {A:P1}
                    pickle.dump(Dict,f)
                if f.closed == True:
                    print('Your password has saved successfully, you have returned to the menu.')
                    break
                else:
                    print('Your password has saved but the text has not closed, you have returned to the menu. Please check.')
                    break
        else:
            print('Sorry, the entered passwords do not match.')
            Answer1 = input("Want to try again?(Yes or No)")
            if Answer1 == 'yes' or Answer1 == 'Yes' or Answer1 == 'Y':
                continue
            elif Answer1 == 'No' or Answer1 == 'no' or Answer1 == 'N':
                print('You have returned to the menu. Thanks for use.')
                break
            else:
                print('Your input is unknown. You have returned to the menu. Thanks for use.')
                break



def Password_retrieval():
    """retrieve all passwords or a specific password
    When this function is called, the users will be asked to verify administrator identity
    so that they can get the right of use. 

    The user can get all passwords or specific password after passig identity verification.
    The encrypted password is decrypted by function 'decrypt()' when the message is invoked.
    
    :param encrypted_pw:Files stored in binary form will be call by external function 'pickle' and will be
    transformed into a dictionary, the string in the dictionary will be orderly presentation to users.
    :return:the retrieved password(s)
    """

    code = input("Your administrator password: ")
    if code == last_line:
        Answer2 = input('Please choose a function below:\n1.Show all passwords\n2.Search for a specific password\nInput a function number:')
        if Answer2 == '1':
            with open ('Passwordsystem.txt','rb') as f:
                Dict = pickle.load(f)
            print('='*88)
            print('Type',' '*34,'Account number',' '*24,'Password')
            for s in Dict:
                if s == 'Administrator':
                    print("You currently have no account.")
                else:
                    s1 = list(Dict[s].keys())
                    if len(s) <= 40 :
                        if len(s1[0]) <= 40:
                            Dict[s][s1[0]]=decrypt(Dict[s][s1[0]])
                            print(s,' '*(38-len(s)),s1[0],' '*(38-len(s1[0])),Dict[s][s1[0]])
                        else:
                            Dict[s][s1[0]] = decrypt(Dict[s][s1[0]])
                            # decrypt the password in the local file
                            print(s,' '*(38-len(s)),s1[0],' ',Dict[s][s1[0]])
                    else:
                        Dict[s][s1[0]] = decrypt(Dict[s][s1[0]])
                        print(s,' ',s1[0],' ',Dict[s][s1[0]])
            print('='*88,'\nYou have returned to the menu. Thanks for use.')
        elif Answer2 == '2':
            f = open('Passwordsystem.txt','rb+')
            Dict = pickle.load(f)
            f.close()
            print('The type of your saved account are list below:')
            for i in Dict:
                if i == 'Administrator':
                    print("You currently have no account.")
                else:
                    print(i)
            n = input('Please input a type name listed above to get the account number and the password: ')
            try:
                m = Dict[n]
                l = list(m.keys())
                Dict[n][l[0]] = decrypt(Dict[n][l[0]])
                print('The name you choose is: ',n,'\nThe account number is: ',l[0],'\nThe password is: ',Dict[n][l[0]])
                print('You have returned to the menu. Thanks for use')
            except:
                print("I am sorry. You did not save the account '{0}' before.".format(n))
        else:
            Answer3 = ('You may write something wrong, try again? (Yes \ No)')
            if Answer3 == 'Yes':
                   Password_retrieval()
            elif Answer3 == 'No':
                print('Thanks to use. You have returned to the menu.')
            else:
                print('Your input is unknown, you have returned to the menu. Thanks to use.')
    else:
        print("The password is wrong, please enter it again.")
        Password_retrieval()


def Password_update():
        """remove or update a specific account/password
        
        When this function is called, the users will be asked to verify administrator identity
        so that they can get the right of use. 

        The user can remove and update the saved passwords and account numbers after passig identity verification.
        When changing an account or password, the user will also need to correctly enter the previous 
        password to gain access to the change.

        While changing the password, function 'test2()' will be called to test the strength of users password,
        if the strength is weak, function 'PasswordGeneration()' will be called to suggust the users to replace their passwords.
        When storing new account information, the new password is encrypted with the function 'encrypt()'

        :param encrypted_pw:Files stored in binary form will be call by external function 'pickle' and will be
        transformed into a dictionary, the string which represent the account tpyes will be given to the users to 
        help them make the choice.

        While update the new information, three string which the users input will be formated to Dictionarie{A:{B:C}}
        and the Dictionarie will be converted to binary form in 'Passwordsystem.txt' by the external 
        function 'pickle'.

        :return:
        """

        while True:
            code = input("Your administrator password: ")
            if code == last_line:
                Answer4 = input('Please choose a function below:\n1.Remove specific password\n2.Update account or password\nInput the function number:')
                if Answer4 == '1':
                    with open ('Passwordsystem.txt','rb+') as f:
                        Dict = pickle.load(f)
                    print('The type of your saved account are list below:')
                    for i in Dict:
                        if i == 'Administrator':
                            print("You currently have no account.")
                        else:
                            print(i)
                    D = input('Please input the specific account name to remove it:')
                    try:
                        Dict.pop(D)
                        with open ('Passwordsystem.txt','wb+') as f:
                            pickle.dump(Dict,f)
                            print('The account has been removed, you have returned to the menu. Thanks for use.')
                            break
                    except:
                        print("I am sorry. You did not save the account '{0}' before.".format(D))
                        break
                elif Answer4 == '2':
                    Answer5 = input('1.Change the account number\n2.Change the password\nInput the function number:')
                    if Answer5 == '1':
                        with open ('Passwordsystem.txt','rb+') as f:
                            Dict = pickle.load(f)
                        print('The type of your saved account are list below:')
                        for i in Dict:
                            if i == 'Administrator':
                                print("You currently have no account.")
                            else:
                                print(i)
                        D = input('Choose a account name to change its account number:')
                        try:
                            T = input('Please input previous account number to complete authentication:')
                            AU = list(Dict[D].keys())
                            if T == AU[0]:
                                New = input('You have passed the authentication, please input a new accout number to replace it:')
                                Dict[D] = {New:Dict[D][AU[0]]}
                                with open ('Passwordsystem.txt','wb+') as f:
                                    pickle.dump(Dict,f)
                                print('Your account number has changed, you have returned to the menu. Thanks for use.')
                                break
                            else:
                                print('You have not passed the authentication, you have returned to the menu. Please check.')
                                break
                        except:
                            print("I am sorry. You did not save the account '{0}' before.".format(D))
                            break
                    elif Answer5 == '2':
                        with open ('Passwordsystem.txt','rb+') as f:
                            Dict = pickle.load(f)
                        print('The type of your saved account are list below:')
                        for i in Dict:
                            if i == 'Administrator':
                                print("You currently have no account.")
                            else:
                                print(i)
                        D = input('Choose a account name to change its password:')
                        try:
                            T = input('Please input previous password to complete authentication:')
                            AU = list(Dict[D].keys())
                            if T == decrypt(Dict[D][AU[0]]):
                                New = input('You have passed the authentication, please input a new password to replace it:')
                                L1,L2 = test2(New)
                                if L2 <= 35:
                                    L3 = PasswordGeneration()
                                    print(L1,"\nThe system has generated a password for you:",L3)
                                    A = input('1.Replace with new password\n2.Still use the original password\n'
                                    '3.Change a new password to save(self)\n4.Back to the function menu\nPlease input your choice:')
                                    if A == '1':
                                        New = L3
                                    elif A == '2':
                                        print('You have used the original password')
                                    elif A == '3':
                                        continue
                                    elif A == '4':
                                        print('You have returned to the menu.')
                                        break
                                    else:
                                        print('Your input is unknown and has returned to the menu.')
                                        break
                                else:
                                    print('The new password strenth is fine.')
                                    break
                                New = encrypt(New)
                                Dict[D] = {AU[0]:New}
                                with open ('Passwordsystem.txt','wb+') as f:
                                    pickle.dump(Dict,f)
                                    print('Your password has changed, you have returned to the menu. Thanks for use.')
                                    break
                            else:
                                print('You has not passed the authentication, you have returned to the menu. Please check.')
                                break
                        except:
                            print("I am sorry. You did not save the account '{0}' before.".format(D))
                            break
            else:
                print("The password is wrong, you have returned to the menu. Please check.")
                break



def PasswordGeneration():
    """generate a password

    Be called in other functions.
    If the input password is tested to be weak, this function will be called.

    :return: a 8-digit string of random password
    """

    base = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM@#_^*%/.+:;="
    newpw = [i for i in base]
    random.shuffle(newpw)
    return ''.join(random.sample(newpw,8))

def PasswordGeneration1():
    """generate a password

    generate a password, the number of digit is decided by the users
    Exist as an independent function for users to choose.

    :return: a string of random password
    """

    while True:
        n = input('Please enter the number of digits you want for the password:')
        try:
            int(n)
        except Exception:
            print('Your input is not a integer,want to try again?\n1.Re-enter\n2.Back to menu.')
            A = input('Please input your choice:')
            if A == '1':
                continue
            elif A == '2':
                print('You have returned to the menu.')
                break
            else:
                print('Your input is unknown, you have returned to the menu.')
                break
        else:
            n = int(n)
            if 32> n > 0:
                base = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM@#_^*%/.+:;="
                newpw = [i for i in base]
                random.shuffle(newpw)
                P = ''.join(random.sample(newpw,n))
                print('The password is: ',P,'\nYou have returned to the menu. Thanks for use.')
                break
            else:
                P = input('Please input a positive integer(no larger than 32), input 1 to retry or input 0 to quit:')
                if P == '1':
                    continue
                elif P == '0':
                    print('You have returned to the menu.')
                    break
                else:
                    print('The input is unknow. You have returned to the menu.')
                    break
    
        

def test1():
    """test the strength of the input password

    Exist as an independent function for users to choose.
    The users input a string of password, then the function will test its strength
    based on the password entropy formula.

    :return: the evaluation of the password strength
    """

    s = input('Please input the password you want to test:')
    u = len(list(s))
    o = len(set(s))
    i = math.log2(u**o)
    print('Based on the password entropy formula, you password strength is :',i)
    if i <= 23:
        print('Your password is weak, the system recommends you to reset. You have returned to the menu.')
    elif 23 < i <= 50:
        print('The safety level is medium. You have returned to the menu.')
    else:
        print('The safety level is strong. You have returned to the menu.')


def test2(s):
    """test the strength of the input password

    When the users input or update a new password, this function will be called
    to test the password strength.

    :param s: a string of password that the users have inputted
    :return: the evaluation of the password strength
    """

    u = len(list(s))
    o = len(set(s))
    i = math.log2(u**o)
    if i <= 35:
        return ('Your password is weak, the system recommends you to reset.',i)
    if 35 < i <= 50:
        return ('The safety level is medium.',i)
    else:
        return ('The safety level is strong.',i)
#test2(Ab12)

def function_choose():
    """choose a function and call it

    :return: the corresponding function that the user has chosen
    """

    while True:
        print('='*48)
        M = input('(If this is the first time you use this system, please just input call function 1)\n1.Password Input and Storage\n2.Password Retrieval\n3.Password Update\n'
                '4.Password Generation\n5.Password strength analysis\nEnter 0 to exit\nChoose a function number or input other things to quit:')
        if M == '1':
            Password_input_and_storage()
        elif M == '2':
            Password_retrieval()
        elif M == '3':
            Password_update()
        elif M == '4':
            PasswordGeneration1()
        elif M == '5':
            test1()
        elif M == '0':
            print('Thanks for use.')
            break
        else:
            print('Your input is unknown.')
            continue


def main():
    """the menu of the program

    Open the file 'Passwordsystem.txt' which stored all passwords,
    if the file is empty, add the administrator account&password into it; if the file doesn't exist,
    creat a new one. Then call the function_choose().

    :return:none
    """

    print('-'*80)
    print('Welcome to our password system, it has input/storage/update/retrieval function.')
    f = 'Passwordsystem.txt'
    if os.path.exists(f):
        sz = os.path.getsize(f)
        if not sz:
            with open ('Passwordsystem.txt','wb+') as v:
                Dict = {'Administrator':{first_line:last_line}}
                pickle.dump(Dict,v)
            function_choose()
        else:
            function_choose()
    else:
        with open ('Passwordsystem.txt','wb+') as v:
            Dict = {'Administrator':{first_line:last_line}}
            pickle.dump(Dict,v)
        function_choose()


def setup_administrator():
    """set up the administrator account and password

       When the users retrieve or update the password, this function will be called
       to verify the authenticity of the action. Once the administrator account has
       been set up, the users couldn't change it unless deleting the file 'users' to
       set up a new one.

    :return:none
    """

    print('You do not have a account yet\nYou can create a administrator account')
    administrator_name = input(" username: ")
    administrator_password = input(" password: ")
    administrator_password2 = input("verify your administrator_password: ")
    while True:
        if administrator_password == administrator_password2:
            fo.write(administrator_name)
            fo.write("\n")
            fo.write(administrator_password)
            fo.close()
            print("your login information is reserved:", "login name:", administrator_name, "your password:",
                  administrator_password)
            break
        else:
            administrator_password = input("the password is not matching, please try again: ")
            administrator_password2 = input("verify your administrator_password: ")



"""
The program will excecute from here.
If no administrator account is found, the program will call the setup function to set up a new one.
After setting up the administrator account, the program will go to the main page.
"""

fo = open("users.txt", "a")
fo.close()
fo = open("users.txt", "r+")
line = fo.read()
# open the local file 'users' where stored the administrator account
if len(line) == 0:
    setup_administrator()
    # if no administrator account is found, call the setup function to set up a new one
    fo = open("users.txt", "r+")
    lines = fo.readlines()
    first_line = lines[0]
    last_line = lines[1]
    fo.close()
    main()
else:
    fo = open("users.txt", "r+")
    lines = fo.readlines()
    first_line = lines[0]
    last_line = lines[1]
    fo.close()
    main()

















