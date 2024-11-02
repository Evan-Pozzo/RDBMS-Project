import InputParser


def normalizeTo1NF(tableArray, nonAtomicValues) -> bool:
    #Normalize to 1NF: 
    #Data Input: Any attributes that hold multivalued, non-atomic data --- {PromocodeUsed}, {DrinkIngredient}, {DrinkAllergen}, {FoodIngredient}, {FoodAllergen} 					
    #Approach: Create a separate relation for each multivalued attribute along with the primary key of the base relation. 					
    
    for values in nonAtomicValues:
        print(values)
        
        # the indexes of the 4 2d arrays all line up to support the same tables
        # create a new table in tableArray to handle this non atomic value
        tableName = tableArray[0] + values + "data"
        # epozzo fix candidateKeyArray
        primaryKeyArray = candidateKeyArray = keyConstraintsArray = columnArray =[]
        
        # fill the new arrays with the new values before we create the new object
        for dependencies in tableArray.functionalDependencies:
            # search the array of dependencies
            if (dependencies.dependent.find(values) > -1):
                primaryKeyArray.append(dependencies.determinant)
                columnArray.append(dependencies.determenant, dependencies.dependent)
                keyConstraintsArray.append(InputParser.FunctionalDependency(dependencies.dependent, dependencies.determinant))

        # remove the old determinant from the first table
        tableArray[0].columns.remove(values)
        tableArray[0].primaryKeyArray.remove(values)

        # loop through the functional dependencies and remove the one with the matching dependency
        for dependencies in tableArray.functionalDependencies:
            if (dependencies.dependent.find(values) > -1):
                tableArray[0].functionalDependencies.remove(values)

        tableArray.append(InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray))

    return True

def normalizeTo2NF(tableArray) -> bool:
    #Normalize to 2NF: 
    #Data Input: The functional dependency set of each base relation. 
    #Approach: Create a separate relation for each partial functional dependency violation against the keys of the base relation. 
    for tables in tableArray:
        i = 0

        partialDependenciesAmount = 0

        for dependencies in tableArray.functionalDependencies:
            j = 0
            tableName = primaryKeyArray = candidateKeyArray = keyConstraintsArray = columnArray = []

            # check for any determinants that are only part of the primary key
            if (dependencies.determinant != tables.primaryKey):
                # ensure this is not a candidate key
                if(tables.candidateKey.find(dependencies.determinant) == -1):
                    partialDependenciesAmount += 1
                    
                    # we have located the partial dependency, now we must normalize it by creating a new table
                    tableName = dependencies.determinant + dependencies.dependent + "data"
                    columnArray.append(dependencies.determinant, dependencies.dependent)
                    primaryKeyArray.append(dependencies.determinant)
                    keyConstraintsArray.append(InputParser.FunctionalDependency(dependencies.determinant, dependencies.dependent))
                    tableArray.append([InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray)])

                    # now we must remove the old data from their un-normalized positions

                    # check if the old determinant is still needed in the new primary key: if not then remove it
                    tableArray[i].primaryKey.remove(dependencies.determinant)

                    # check for all instances of 
                    for values in tableArray.functionalDependencies:
                        if (values.dependent.find(dependencies.determinant) > -1):
                            tableArray[0].functionalDependencies.remove(values)
                        


            j+= 1
        i += 1
        if (partialDependenciesAmount <= 0):
            print("No PFD violations. Table is already in 2NF.")

    return

def normalizeTo3NF(tableArray) -> bool:
    #Normalize to 3NF: 
    #Data Input: The functional dependency set of each base relation. 
    #Approach: Create a separate relation for each transitive functional dependency violation against the keys of the base relation. 
    return

def normalizeToBCNF(tableArray) -> bool:
    #Normalize to BCNF: 
    #Data Input: The functional dependency set of each base relation. 
    #Approach: Create a separate relation for each BCNF functional dependency violation against the keys of the base relation. 
    return

def normalizeTo4NF(tableArray) -> bool:
    #Normalize to 4NF: 
    #Data Input: The multi-valued functional dependency set of each base relation. 
    #Approach: Create a separate relation for each MVD violation.     
    return

def normalizeTo5NF(tableArray) -> bool:
    #Normalize to 5NF: 
    #Data Input: User provided data instances for each base relation. 
    #Approach: Decompose each base relation into its sub-relation projection if a non-trivial join dependency is identified. 
    return
