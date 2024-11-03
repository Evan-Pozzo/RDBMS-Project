
#I am going to represent the functional dependencies as a 2d array of dependency objects
class FunctionalDependency:
    def __init__(self, determinant, dependent, MVD=False):
        self.determinant = determinant # left hand side
        self.dependent = dependent # right hand side
        self.MVD = MVD

class Table:
    def __init__(self, name, primaryKeyArray, candidateKeyArray, columnsArray, functionalDependenciesArray, MVDArray):
        self.tableName = name
        self.primaryKey = primaryKeyArray
        self.candidateKey = candidateKeyArray
        self.columns = columnsArray 
        self.functionalDependencies = functionalDependenciesArray # array of FunctionalDependency objects
        self.MVD = MVDArray

def takeInput1NF():
    # take the input from the user
    tableName = input("Input the name of the table or input EXIT to end the program: \n")
    if tableName == "EXIT":
        return tableName, 0, 0, 0
    
    keyConstraintsArray = []

    columnStr = input("Input the list of Columns: \n")
    primaryKeyStr = input("Input the primary key: \n")
    candidateKeyStr = input("Input any candidate keys: \n")
    amount = int(input("How many functional dependencies are there?: \n"))
    
    # create an array of each string we input
    # we will parse these into objects later
    for i in range(amount):
        keyConstraintsStr = input("FD" + str(i+1) + ") ")
        # remove the ', ' for all but the last item
        if(i < (amount - 1)):
            keyConstraintsStr = keyConstraintsStr[:-2]
        keyConstraintsArray.append(keyConstraintsStr)

    columnArray = columnStr.split(', ')
        
    if (primaryKeyStr != "{{}}"):
        primaryKeyStr = primaryKeyStr.replace('{', '')
        primaryKeyStr = primaryKeyStr.replace('}', '')
        primaryKeyArray = primaryKeyStr.split(', ')
    else:
        print("-----------------------ERROR: NO PRIMARY KEY INPUTTED-----------------------")
        return 0
    
    if (candidateKeyStr != "{{}}"):
        candidateKeyStr = candidateKeyStr.replace('{', '')
        candidateKeyStr = candidateKeyStr.replace('}', '')
        candidateKeyArray = candidateKeyStr.split(', ')
    else:
        candidateKeyArray = []

    highestNormalization = input("Input the highest normal form you wish to achieve: \n")   
    parsedkeyConstraintsArray = []
    parsedkeyConstraintsArray, nonAtomicValuesArray, MVDarray = parseConstraints(keyConstraintsArray)
    
    tableArray = [Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, parsedkeyConstraintsArray, MVDarray)]

    return tableArray, highestNormalization, nonAtomicValuesArray, MVDarray

def takeInput2NF():
    return

def takeInput3NF():
    return

def takeInputBCNF():
    return

def takeInput4NF():
    return

def takeInput5NF():
    return

# parse the inputted key constraints
def parseConstraints(keyConstraintsArray):
    # 2d list of FunctionalDependency Objects
    parsedKeyConstraints = [] # epozzo fix this

    nonAtomicValuesArray = []
    MVDarray = []


    classConstraintsArray = []

    # parse the dependent and determinant values in the functional dependencies
    for values in keyConstraintsArray:
        MVD = False
        dependent = []
        determinant = []

        #left side
        temp = values[:values.find(" -->")]
        if(temp.find('{') > -1):
            temp = temp.replace('{', '')
            temp = temp.replace('}', '')
            determinant = temp.split(', ')
        else:
            determinant = [temp]    

        # check for any MVDs
        if (values.find("(a MVD)") > -1):
            temp = values.replace(" (a MVD)", "")
            MVD = True
            values = temp

        # check for any non atomic values
        if (values.find("(a non-atomic attribute)") > -1):
            temp = values.replace(" (a non-atomic attribute)", "")
            temp = temp[temp.find("--> ")+4:]
            nonAtomicValuesArray.append(temp)
            dependent = [temp]
        #right side

        elif (values.find("-->") > -1):
            if (values.find("-->>") > -1):
                temp = values[values.find("-->> ")+5:]

                if(temp.find('{') > -1):
                    temp = temp.replace('{', '')
                    temp = temp.replace('}', '')
                    dependent = temp.split(', ')
                elif(temp.find(" | ") > -1):
                    dependent = temp.split(" | ")
                    MVDarray += temp
                else:
                    dependent = [temp]

            else:
                temp = values[values.find("--> ")+4:]
                if(temp.find('{') > -1):
                    temp = temp.replace('{', '')
                    temp = temp.replace('}', '')
                    dependent = temp.split(', ')
                elif(temp.find(" | ") > -1):
                    dependent = temp.split(" | ")
                else:
                    dependent = [temp]
        else:
            print("------------------ERROR '-->' NOT FOUND------------------")
            return
           



        classConstraintsArray.append(FunctionalDependency(determinant, dependent, MVD))

    return classConstraintsArray, nonAtomicValuesArray, MVDarray