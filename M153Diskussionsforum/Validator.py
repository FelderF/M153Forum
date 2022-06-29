class Validator(object):
    """description of class"""
    #not used
    def isString(self,stringToTest):        
        return True
    
    #tests if input is empty, returns false if it is empty, true otherwise
    def isNotEmpty(self,input):
        if input:
            return True
        else:
            return False
    
    def has_numbers(self,inputString):
        return any(char.isdigit() for char in inputString)

    def isValidPassword(self, password):  
        #min 12 characters, at least one lowercase, uppercase, number. Each test writes error and returns false if something is wrong
        #test if at leas 12 characters and maximum 99
        length = len(password)
        if (lentgh >12 or length <100):
            validLength = True
        #test if on lowercase
        for c in password:
            if c.islower():
                hasLowercase = True
        #test if one uppercase
        for c in password:
            if c.isupper():
                hasUppercase = True
        #test if contains a number
        hasNumber = has_number(password)
        #write errors if something is wrong and return false, true otherwise
        if not(validLength):
            print("The length of the password is wrong, must be between 3 and 15 characters. Your has", len(password), "characters")
        if not(hasLowercase):
            print("The password must contain at least 1 lowercase letter")
        if not(hasUppercase):
            print("The password must contain at least 1 uppercase letter")
        if not(hasNumber):
            print("The password must contain at least 1 number")
        if(validLength and hasLowercase and hasUppercase and hasNumber):
            return True
        else:
            return False
    
    def isVaildUsername(self,username):
        #between 3 and 15 characters, all characters allowed, else write error message and return false
        length = len(username)
        if (length <3):
            print("The username is to short, must be at least 3 characters")
            return False
        elif (length>15):
            print("The username is to long, maximum 15 characters allowed")
            return False      
        #check if not already in use, else write error message and return false
        return True
    

