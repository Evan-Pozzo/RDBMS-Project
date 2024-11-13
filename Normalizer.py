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
    totalpartialDependenciesAmount = 0
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
                # check if there are any transitive dependencies to carry over to the new table
                l = 0
                for dependencies2 in tables.functionalDependencies:
                    #print("new TFD?", dependencies2.determinant, dependencies.dependent)
                    if searchArrayUnordered(dependencies2.determinant, dependencies.dependent):
                        #print("adding new TFD")
                        keyConstraintsArray.append(InputParser.FunctionalDependency(dependencies2.determinant, dependencies2.dependent, dependencies2.MVD))
                        # mark down the index of this FD for later removal
                        #print("appending: ", l)
                        checkDependencies.append(l)
                    l += 1
                skipped = 0

                # check over the tables we already know we will add
                if(len(newTableArray) > 0):
                    for newTables in newTableArray:
                        # if this table will have the same primary key as an already created table, just bundle them together
                        #print(newTables.tableName, newTables.primaryKey, primaryKeyArray)
                        if newTables.primaryKey == primaryKeyArray:
                            newTables.candidateKey = uniqueArrayAdd(newTables.candidateKey, candidateKeyArray)
                            newTables.columns = uniqueArrayAdd(newTables.columns, columnArray)
                            # check if this is the same FD as another table
                            if keyConstraintsArray[0].determinant == newTables.functionalDependencies[0].determinant and keyConstraintsArray[0].dependent == newTables.functionalDependencies[0].dependent:
                                break
                            else:
                                for FDs in keyConstraintsArray:
                                    newTables.functionalDependencies.append(FDs)
                                break
                        else:
                            skipped += 1

                # this is the first new table
                else:
                    newTableArray.append(InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray))
                # add in our final table that has checked through all the new tables
                if skipped == len(newTableArray) and len(newTableArray) > 0:
                    newTableArray.append(InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray))

                
                # mark down the index of this FD so we can remove it later
                checkDependencies.append(j)

            j += 1
            
        # sort it high->low so they remain in the correct position when deleting
        checkDependencies = sorted(checkDependencies, reverse=True)
        #remove duplicates
        test = []
        for nums in checkDependencies:
            if nums not in test:
                test.append(nums)
        checkDependencies = test       
        # remove each partial FD
        for index in checkDependencies:
            #print(checkDependencies)
            #print(tables.tableName, "REMOVING : ", tables.functionalDependencies[index].determinant, tables.functionalDependencies[index].dependent)

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
            #print(tables.tableName, " TO REMOVE ", columns)
            tables.columns.remove(columns)
        
        #checkTable(tableArray, i)
        totalpartialDependenciesAmount += partialDependenciesAmount
        i += 1

    if len(newTableArray) == 0:
        print("\n\n-----------Tables are already in 2NF-----------\n\n")
    else:
        tableArray += newTableArray
        # ensure the tables are correct
        for i in range(len(tableArray)):
            checkTable(tableArray, i)
        print("\n------------- 2NF Results -------------\n")
        FinalRelationGen.printResult(tableArray)

    return tableArray

def normalizeTo3NF(tableArray) -> bool:
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
                print("LOCATED TFD: ", tables.tableName, dependencies.determinant, dependencies.dependent, tables.primaryKey)
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
                # check for columns and functional dependencies that need to be switched around
        k = 0
        for newTables in newTableArray:
            #print(newTables.columns)

            m = 0
            # if we have duplicate values across multiple tables
            for newTables2 in newTableArray:
                # dont search the same tables over each other
                if newTables.tableName != newTables2.tableName:
                    # loop over every column value
                    for values in newTables2.columns:
                        if values in newTables.columns:
                            # only remove this value if it is not in the primary key
                            if values not in newTables2.primaryKey and values not in newTables.primaryKey:
                                # remove this value from the already existing new table
                                if (values in newTableArray[k].columns):
                                    print(newTableArray[k].tableName, " : Removing from columns: ", values)
                                    newTableArray[k].columns.remove(values)
                                for s in range(len(newTableArray[k].functionalDependencies)):
                                    if values in newTableArray[k].functionalDependencies[s].dependent:
                                        print("Removing from FD: ", values)
                                        newTableArray[k].functionalDependencies[s].dependent.remove(values)
                m += 1
            k += 1

        # remove each TFD from the existing table
        for index in checkDependencies:
            for values in tables.functionalDependencies[index].determinant:
                for newTables in newTableArray:
                    if values not in newTables.primaryKey:
                        #print("1 REMOVE from ", tables.tableName, values, tables.columns)
                        tables.columns.remove(values)
                        break
            for values in tables.functionalDependencies[index].dependent:
                #print("REMOVE from ", tables.tableName, values, tables.columns)
                tables.columns.remove(values)
            tables.functionalDependencies.pop(index)

        # remove values of the transitive dependency from the original FD
        for newTables in newTableArray:
            z = 0
            # check every value of this dependent against the functional dependency of the new table 
            fakeFD = []
            for dependents in tables.functionalDependencies[0].dependent:
                #print("? ", dependents, newTables.functionalDependencies[0].dependent)
                if dependents in newTables.functionalDependencies[0].dependent:
                    #print(tables.tableName," REMOVED ", dependents, " FROM ", tables.functionalDependencies[0].dependent)
                    fakeFD.append(dependents)

            for values1 in fakeFD:
                if values1 not in tables.columns:
                    #print("2 REMOVE from ", tables.tableName, values1, tables.functionalDependencies[0].dependent, tables.columns)
                    tables.functionalDependencies[0].dependent.remove(values1)
            z += 1

        # don't have to mess with the primary key because the value was already not inside the primary key
        #if (amount == 0):
        #    print("No TFD violations. Table is already in 3NF.")  


    if len(newTableArray) == 0:
        print("\n\n-----------Tables are already in 3NF-----------\n\n")
    else:
        tableArray += newTableArray
        for y in range(len(tableArray)):
            checkTable(tableArray, y)
        print("\n------------- 3NF Results -------------\n")
        FinalRelationGen.printResult(tableArray)
    return tableArray

#EPOZZO REDO
def normalizeToBCNF(tableArray) -> bool:
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


    if len(newTableArray) == 0:
        print("\n\n-----------Tables are already in BCNF-----------\n\n")
    else:
        tableArray += newTableArray
        for j in range(len(tableArray)):
            checkTable(tableArray, j)
        print("\n------------- BCNF Results -------------\n")
        FinalRelationGen.printResult(tableArray)
    return tableArray

def normalizeTo4NF(tableArray):
    #Normalize to 4NF: 
    #Data Input: The multi-valued functional dependency set of each base relation. 
    #Approach: Create a separate relation for each MVD violation.     
    newTableArray = []
    for tables in tableArray:
        i = 0
        primaryKeyArray = []
        candidateKeyArray = []
        keyConstraintsArray = []
        columnArray = []
        
        # loop over every functional dependency
        x = 0
        for dependencies in tables.functionalDependencies:
            # check if this dependency has an mvd
            if dependencies.MVD == True:

                tableName = dependencies.dependent[0] + "Data"
                # now we will create the new table with the first MVD dependent
                columnArray.append(dependencies.dependent[0])
                columnArray += dependencies.determinant
                primaryKeyArray += dependencies.determinant
                keyConstraintsArray.append(InputParser.FunctionalDependency(dependencies.determinant, [dependencies.dependent[0]]))
                newTableArray.append(InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray))
                
                primaryKeyArray = []
                candidateKeyArray = []
                keyConstraintsArray = []
                columnArray = []
                tableName = dependencies.dependent[1] + "Data"
                # now we will create the new table with the second MVD dependent
                columnArray.append(dependencies.dependent[1])
                columnArray += dependencies.determinant
                primaryKeyArray += dependencies.determinant
                keyConstraintsArray.append(InputParser.FunctionalDependency(dependencies.determinant, [dependencies.dependent[1]]))
                newTableArray.append(InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray))

                tables.columns.remove(dependencies.dependent[1])
                tables.columns.remove(dependencies.dependent[0])
                tables.functionalDependencies.pop(x)
                x += 1
            i += 0
            

    if len(newTableArray) == 0:
        print("\n\n-----------Tables are already in 4NF-----------\n\n")
    else:
        tableArray += newTableArray
        for j in range(len(tableArray)):
            checkTable(tableArray, j)
        for i in range(len(tableArray)):
            for j in range(len(tableArray[i].functionalDependencies)):
                tableArray[i].functionalDependencies[j].MVD = False

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

    # there is a partial dependency if the left side of the FD is only part of or not at all in the primary key
    if (partiallyInPrimaryKey == True and isInCandidateKey == False and (len(primaryKey) > len(functionalDependency))):
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
    #print(len(tableArray), index)
    #if len(tableArray[index].columns) == 0:
        #print("Deleting: ", tableArray[index].columns)
        #tableArray.pop(index)
        #return tableArray

    # check if it needs a new primary key
    if (len(tableArray[index].primaryKey) == 0):
        newKey = []
        for dependencies in tableArray[index].functionalDependencies:
            if(dependencies.determinant not in newKey):
                newKey += dependencies.determinant

        tableArray[index].primaryKey = newKey
        #print("new primary key: ", tableArray[index].primaryKey)
        return tableArray
    
    # ensure all the values in the FDs are in the columns
    uniqueVals = []
    for FDs in tableArray[index].functionalDependencies:
        for dependencies in FDs.dependent:
            if dependencies not in uniqueVals:
                uniqueVals.append(dependencies)
        for determinants in FDs.determinant:
            if determinants not in uniqueVals:
                uniqueVals.append(determinants)

    tableArray[index].columns = uniqueVals
    return tableArray

def uniqueArrayAdd(array1, array2):
    for values in array2:
        if values not in array1:
            array1.append(values)
    return array1