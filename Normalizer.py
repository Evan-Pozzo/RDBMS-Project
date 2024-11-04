import InputParser
import FinalRelationGen

def normalizeTo1NF(tableArray, nonAtomicValues):
    #Normalize to 1NF: 
    #Data Input: Any attributes that hold multivalued, non-atomic data --- {PromocodeUsed}, {DrinkIngredient}, {DrinkAllergen}, {FoodIngredient}, {FoodAllergen} 					
    #Approach: Create a separate relation for each multivalued attribute along with the primary key of the base relation. 					
    print("Non Atomic Values -- ", nonAtomicValues)

    for values in nonAtomicValues:
        tableName = "Evan Pozzo"
        # the indexes of the 4 2d arrays all line up to support the same tables
        # create a new table in tableArray to handle this non atomic value
        primaryKeyArray = []
        candidateKeyArray = []
        keyConstraintsArray = []
        columnArray = []
        
        # fill the new arrays with the new values before we create the new object
        for dependencies in tableArray[0].functionalDependencies:
            # search the array of dependencies
            if (values in dependencies.dependent):
                tableName = values + "Data"
                
                primaryKeyArray += dependencies.determinant
                columnArray += dependencies.determinant
                columnArray += dependencies.dependent
                keyConstraintsArray.append(InputParser.FunctionalDependency(dependencies.determinant, dependencies.dependent, dependencies.MVD))

        # remove the old determinant from the first table
        tableArray[0].columns.remove(values)
  
        # loop through the functional dependencies and remove the one with the matching dependency
        for dependencies in tableArray[0].functionalDependencies:
            if (values in dependencies.dependent):
                tableArray[0].functionalDependencies.remove(dependencies)
        tableArray.append(InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray))
    
    print("\n------------- 1NF Results -------------\n")
    FinalRelationGen.printResult(tableArray)
    return tableArray

def normalizeTo2NF(tableArray):
    #Normalize to 2NF: 
    #Data Input: The functional dependency set of each base relation. 
    #Approach: Create a separate relation for each partial functional dependency violation against the keys of the base relation. 
    
    # will append to table array after done
    newTableArray = []
    for tables in tableArray:
        i = 0
        #print(tables.tableName)
        partialDependenciesAmount = 0
        checkDependencies = []
        j = 0
        for dependencies in tables.functionalDependencies:
            tableName = []
            primaryKeyArray = []
            candidateKeyArray = []
            keyConstraintsArray = []
            columnArray = []
            if(identifyPartialDependency(tables.primaryKey, tables.candidateKey, dependencies.determinant) == True):
                partialDependenciesAmount += 1
                # we have located the partial dependency, now we must normalize it by creating a new table
                tableName = dependencies.determinant[0] + dependencies.dependent[0] + "Data"
                columnArray += dependencies.determinant
                columnArray += dependencies.dependent
                primaryKeyArray += dependencies.determinant
                keyConstraintsArray.append(InputParser.FunctionalDependency(dependencies.determinant, dependencies.dependent, dependencies.MVD))
                skipped = 0
                if(len(newTableArray) > 0):
                    for newTables in newTableArray:
                        # if this table will have the same primary key as an already created table, just bundle them together
                        #print(newTables.tableName, newTables.primaryKey, primaryKeyArray)
                        if newTables.primaryKey == primaryKeyArray:
                            newTables.candidateKey = uniqueArrayAdd(newTables.candidateKey, candidateKeyArray)
                            newTables.columns = uniqueArrayAdd(newTables.columns, columnArray)
                            if keyConstraintsArray[0].determinant == newTables.functionalDependencies[0].determinant and keyConstraintsArray[0].dependent == newTables.functionalDependencies[0].dependent:
                                break
                            else:
                                newTables.functionalDependencies.append(keyConstraintsArray[0])
                                break
                        else:
                            skipped += 1
                else:
                    newTableArray.append(InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray))
                
                if skipped == len(newTableArray) and len(newTableArray) > 0:
                    newTableArray.append(InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray))


                #print("New table: ", tableName)
                
                # mark down the index of this FD so we can remove it later
                checkDependencies.append(j)

            j += 1
            
        # sort it high->low so they remain in the correct position when deleting
        checkDependencies = sorted(checkDependencies, reverse=True)
        # remove each partial FD
        for index in checkDependencies:
            tables.functionalDependencies.pop(index)

        toRemove = []
        for columns in tables.columns:
            #print("\tAttempting to remove: ", tables.tableName, columns)
            colExists = False
            for dependencies in tables.functionalDependencies:
                if ((columns not in dependencies.determinant) and (columns not in dependencies.dependent) and (columns not in tables.primaryKey)):
                    colExists = True
            if (colExists == True):
                #print("\t\tRemoved: ", columns)
                toRemove.append(columns)
                
        for columns in toRemove:
            tables.columns.remove(columns)

        #if (partialDependenciesAmount <= 0):
        #    print("No PFD violations. Table is already in 2NF.")
        
        checkTable(tableArray, i)
        i += 1

    if len(newTableArray) > 0:
        tableArray += newTableArray

    print("\n------------- 2NF Results -------------\n")
    FinalRelationGen.printResult(tableArray)
    return tableArray

def normalizeTo3NF(tableArray) -> bool:
    #print("\n------------- 3NF ------------- \n")
    #Normalize to 3NF: 
    #Data Input: The functional dependency set of each base relation. 
    #Approach: Create a separate relation for each transitive functional dependency violation against the keys of the base relation. 
    newTableArray = []
    for tables in tableArray:
        amount = 0
        j = 0
        checkDependencies = []
        for dependencies in tables.functionalDependencies:
            # check for transitive dependencies
            # ex: A -> B, B-> C
            # we will do this by checking for functional dependencies where the determinant is not a part of the primary key
            if searchArrayUnordered(dependencies.determinant, tables.primaryKey) == False:
                amount += 1
                primaryKeyArray = []
                candidateKeyArray = []
                keyConstraintsArray = []
                columnArray = []

                tableName = dependencies.determinant[0] + "Data"
                columnArray += dependencies.determinant
                columnArray += dependencies.dependent
                primaryKeyArray += dependencies.determinant
                keyConstraintsArray.append(InputParser.FunctionalDependency(dependencies.determinant, dependencies.dependent, dependencies.MVD))
                newTableArray.append(InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray))

                checkDependencies.append(j)
            j += 1

        checkDependencies = sorted(checkDependencies, reverse=True)

        # remove each TFD from the existing table
        for index in checkDependencies:
            for values in tables.functionalDependencies[index].determinant:
                tables.columns.remove(values)
            for values in tables.functionalDependencies[index].dependent:
                tables.columns.remove(values)
            tables.functionalDependencies.pop(index)
        # don't have to mess with the primary key because the value was already not inside the primary key
        #if (amount == 0):
        #    print("No TFD violations. Table is already in 3NF.")  

    if len(newTableArray) > 0:
        tableArray += newTableArray

    print("\n------------- 3NF Results -------------\n")
    FinalRelationGen.printResult(tableArray)
    return tableArray

def normalizeToBCNF(tableArray) -> bool:
    print("--------- BCNF ------------")
    #Normalize to BCNF: 
    #Data Input: The functional dependency set of each base relation. 
    #Approach: Create a separate relation for each BCNF functional dependency violation against the keys of the base relation. 

    newTableArray = []
    for tables in tableArray:
        BCNF1array = []
        BCNF2array = []
        amount = 0
        # check for instances where A -> B and B -> C
        for dependencies in tables.functionalDependencies:
            for dependecies2 in tables.functionalDependencies:
                # check if one relation's dependent is equal to another's determinant
                if dependencies.dependent == dependecies2.determinant:
                    # if these values are already at the same index then 
                    amount += 1
                    BCNF1array.append(dependencies.dependent)
                    BCNF2array.append(dependecies2.determinant)

        # create new tables for our found BCNF conflictions
        i = 0
        for values in BCNF1array: # loops over the dependents
            primaryKeyArray = []
            candidateKeyArray = []
            keyConstraintsArray = []
            columnArray = []
            MVD = False
            tableName = values[0] + "Data"
            columnArray += values
            columnArray += BCNF2array[i]
            primaryKeyArray += values
            for dependencies in tables.functionalDependencies:
                if BCNF2array[i] == dependencies.dependent and BCNF1array[i] == dependencies.determinant:
                    MVD = dependencies.MVD
                    break
            keyConstraintsArray.append(InputParser.FunctionalDependency(values, BCNF2array[i], MVD))
           
            newTableArray.append(InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray))
            i += 1
        
        # remove the old values
        i = 0
        # in a->b,b->c  we want to remove c
        for i in range(len(BCNF2array)): 
            tables.columns.remove(BCNF2array[i])
            j = 0
            for dependencies in tables.functionalDependencies:
                if BCNF2array[i] == dependencies.dependent and BCNF1array[i] == dependencies.determinant:
                    tables.functionalDependencies.pop(j)
                    break
                j += 1

        #if amount == 0:
        #    print("Table is already in BCNF")   

        if len(newTableArray) > 0:
            tableArray += newTableArray

    print("\n------------- BCNF Results -------------\n")
    FinalRelationGen.printResult(tableArray)
    return tableArray

def normalizeTo4NF(tableArray):
    #Normalize to 4NF: 
    #Data Input: The multi-valued functional dependency set of each base relation. 
    #Approach: Create a separate relation for each MVD violation.     
    newTableArray = []
    for tables in tableArray:
        amount = 0
        i = 0
        MVDindex = []
        primaryKeyArray = []
        candidateKeyArray = []
        keyConstraintsArray = []
        columnArray = []
        
        # loop over every functional dependency
        for dependencies in tables.functionalDependencies:
            # check if this dependency has an mvd
            if dependencies.MVD == True:
                amount += 1
                MVDindex.append(i)

                tableName = dependencies.dependent[1] + "Data"
                # we will create the new table with the second MVD dependent
                columnArray.append(dependencies.dependent[1])
                columnArray += dependencies.determinant
                primaryKeyArray += dependencies.determinant
                keyConstraintsArray.append(InputParser.FunctionalDependency(dependencies.determinant, [dependencies.dependent[1]]))
                newTableArray.append(InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray))
            i += 0
        #if amount == 0:
        #    print("Table is already in 4NF") 

        # now we must remove the located MVDs
        # a -> b | > c we remove c
        for dependencies in keyConstraintsArray:
            tables.columns.remove(dependencies.dependent[0])

        MVDindex = sorted(MVDindex, reverse=True)
        # delete the second value in each MVD
        for index in MVDindex:
            tables.functionalDependencies[index].dependent.pop(1)

    if len(newTableArray) > 0:
        tableArray += newTableArray

    print("\n------------- 4NF Results -------------\n")
    FinalRelationGen.printResult(tableArray)
    return tableArray

def normalizeTo5NF(tableArray):
    #Normalize to 5NF: 
    #Data Input: User provided data instances for each base relation. 
    #Approach: Decompose each base relation into its sub-relation projection if a non-trivial join dependency is identified. 
    
    print("\n------------- 5NF Results -------------\n")
    FinalRelationGen.printResult(tableArray)
    return tableArray

def identifyPartialDependency(primaryKey, candidateKey, functionalDependency) -> bool:
    #print("Checking: ", functionalDependency, primaryKey, candidateKey)

    partiallyInPrimaryKey = searchArrayUnordered(functionalDependency, primaryKey)
    isInCandidateKey = searchArrayUnordered(functionalDependency, candidateKey)

    if partiallyInPrimaryKey == True and isInCandidateKey == False and (len(primaryKey) > len(functionalDependency)):
        #print("Found")
        return True
    else:
        return False
    
# return if the unordered elements of the subArray are inside the Array
def searchArrayUnordered(subArray, Array):
    amount = 0
    if len(subArray) > len(Array):
        return False
    
    # check if all the values of subArray are in Array
    for values in subArray:
        if values in Array:
            amount += 1

    # if the amount is the same, then all values have been found
    if amount == len(subArray):
        return True
    else:
        return False
    
# check if a table still exists after normalization
# alter it as needed or delete it
def checkTable(tableArray, index):
    # if there are no items left then delete this table
    #print("Checking: ", tableArray[index].tableName, tableArray[index].primaryKey)
    if len(tableArray[index].columns) == 0:
        #print("Deleting: ", tableArray[index].columns)
        tableArray.pop(index)
        return tableArray
    
    # check if it needs a new primary key
    if (len(tableArray[index].primaryKey) == 0):
        newKey = []
        for dependencies in tableArray[index].functionalDependencies:
            if(dependencies.determinant not in newKey):
                newKey += dependencies.determinant

        tableArray[index].primaryKey = newKey
        #print("new primary key: ", tableArray[index].primaryKey)
        return tableArray
    
    return tableArray

def uniqueArrayAdd(array1, array2):
    for values in array2:
        if values not in array1:
            array1.append(values)
    return array1