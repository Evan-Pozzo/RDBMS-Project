
#I am going to represent the functional dependencies as a 2d array of dependency objects
class FunctionalDependency:
    def __init__(self, determinant, dependent):
        self.determinant = determinant # left hand side
        self.dependent = dependent # right hand side

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
        return tableName, 0, 0, 0, 0
    
    keyConstraintsArray = []

    columnStr = input("Input the list of Columns: \n")
    primaryKeyStr = input("Input the primary key: \n")
    candidateKeyStr = input("Input any candidate keys: \n")
    amount = int(input("How many functional dependencies are there?: \n"))

    # create an array of each string we input
    # we will parse these into objects later
    for i in range(amount):
        keyConstraintsStr = input("FD" + (i+1) + ") ")
        keyConstraintsArray.append(keyConstraintsStr)
        
    if (primaryKeyStr != ""):
        primaryKeyStr = primaryKeyStr.replace('{', '')
        primaryKeyStr = primaryKeyStr.replace('}', '')
        primaryKeyArray = primaryKeyStr.split(', ')
    else:
        print("-----------------------ERROR: NO PRIMARY KEY INPUTTED-----------------------")
        return 0
    
    if (candidateKeyStr != ""):
        candidateKeyStr = candidateKeyStr.replace('{', '')
        candidateKeyStr = candidateKeyStr.replace('}', '')
        candidateKeyArray = candidateKeyStr.split(', ')
    else:
        candidateKeyArray = []

    highestNormalization = input("Input the highest normal form you wish to achieve: \n")   

    # parse the inputted strings into arrays
    columnArray = columnStr.split(', ')
    keyConstraintsArray, nonAtomicValuesArray, MVDarray = parseConstraints(keyConstraintsArray)
    
    tableArray = [Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray)]

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

    dependent = 0
    determinant = 0

    for values in keyConstraintsArray:
        #left side
        determinant = values[:values.find(" -->")]
        #right side
        # check if arrow is -->> or -->
        if (values.find("-->") > -1):
            if (values.find("-->>") > -1):
                dependent = values[:values.find("-->> ")+5]
            else:
                dependent = values[:values.find("--> ")+4]


        keyConstraintsArray.append(FunctionalDependency(dependent, determinant))

        print()

    i = 0

    for constraints in keyConstraintsArray:
        if (constraints.find("(a non-atomic attribute)") > -1):
            constraints = constraints.replace(" (a non-atomic attribute)", "")
            # replace the non parsed value with the parsed value
            keyConstraintsArray[i] = constraints 
           
            #isolate the dependant value
            if (constraints.find("--> ") > -1):
                constraints = constraints[constraints.find("--> ")+4:]
                nonAtomicValuesArray.append(constraints)

        # might need to change how i do this
        if (constraints.find("(a MVD)") > -1): 
            constraints = constraints.replace(" (a MVD)", "")
            # replace the non parsed value with the parsed value
            keyConstraintsArray[i] = constraints 

            #isolate the dependant value
            if (constraints.find("-->> ") > -1):
                constraints = constraints[constraints.find("-->> ")+5:]
                MVDarray.append(constraints)

        i += 1


    return keyConstraintsArray, nonAtomicValuesArray, MVDarray