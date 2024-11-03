import InputParser


def normalizeTo1NF(tableArray, nonAtomicValues) -> bool:
    #Normalize to 1NF: 
    #Data Input: Any attributes that hold multivalued, non-atomic data --- {PromocodeUsed}, {DrinkIngredient}, {DrinkAllergen}, {FoodIngredient}, {FoodAllergen} 					
    #Approach: Create a separate relation for each multivalued attribute along with the primary key of the base relation. 					
    print("Non Atomic Values -- ", nonAtomicValues)

    for values in nonAtomicValues:
        tableName = "Evan Pozzo"
        # the indexes of the 4 2d arrays all line up to support the same tables
        # create a new table in tableArray to handle this non atomic value
        # epozzo fix candidateKeyArray
        primaryKeyArray = []
        candidateKeyArray = []
        keyConstraintsArray = []
        columnArray = []
        MVDArray = []
        
        # fill the new arrays with the new values before we create the new object
        for dependencies in tableArray[0].functionalDependencies:
            # search the array of dependencies
            if (values in dependencies.dependent):
                tableName = dependencies.determinant[0] + values + "Data"
                
                primaryKeyArray += dependencies.determinant
                columnArray += dependencies.determinant
                columnArray += dependencies.dependent
                keyConstraintsArray.append(InputParser.FunctionalDependency(dependencies.determinant, dependencies.dependent))

        # remove the old determinant from the first table
        tableArray[0].columns.remove(values)
  
        # loop through the functional dependencies and remove the one with the matching dependency
        for dependencies in tableArray[0].functionalDependencies:
            if (values in dependencies.dependent):
                tableArray[0].functionalDependencies.remove(dependencies)
        tableArray.append(InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray, MVDArray))

    return True

def normalizeTo2NF(tableArray) -> bool:
    #Normalize to 2NF: 
    #Data Input: The functional dependency set of each base relation. 
    #Approach: Create a separate relation for each partial functional dependency violation against the keys of the base relation. 
    for tables in tableArray:
        i = 0

        partialDependenciesAmount = 0

        for dependencies in tables.functionalDependencies:
            j = 0
            tableName = []
            primaryKeyArray = []
            candidateKeyArray = []
            keyConstraintsArray = []
            columnArray = []
            MVDArray = []

            # check for any determinants that are only part of the primary key
            if (dependencies.determinant != tables.primaryKey):
                # ensure this is not a candidate key
                if(dependencies.determinant not in tables.candidateKey):
                    partialDependenciesAmount += 1
                    
                    # we have located the partial dependency, now we must normalize it by creating a new table
                    #print(dependencies.determinant)
                    #print(dependencies.dependent)

                    tableName = dependencies.determinant[0] + dependencies.dependent[0] + "Data"
                    columnArray += dependencies.determinant
                    columnArray += dependencies.dependent
                    primaryKeyArray += dependencies.determinant
                    keyConstraintsArray.append(InputParser.FunctionalDependency(dependencies.determinant, dependencies.dependent))
                    tableArray.append([InputParser.Table(tableName, primaryKeyArray, candidateKeyArray, columnArray, keyConstraintsArray, MVDArray)])
                    print("New table: ", tableName)

                    # now we must remove the old data from their un-normalized positions
                    stillThere = False

                    # find and remove the partial functional dependency if the determinant and dependent match
                    for x in tables.functionalDependencies:
                        if (dependencies.determinant in x.determinant and dependencies.dependent in x.dependent):
                            tableArray[i].functionalDependencies.remove(x)
                        
                    # check if the old determinant is still in any functional dependencies
                    for x in tables.functionalDependencies:
                        if dependencies.determinant in x.determinant:
                            stillThere = True

                    # we have cycled through and determined this is no longer a part of the primary key - remove it 
                    if (stillThere == False):
                        print(dependencies.determinant, "   ---   ", tableArray[i].primaryKey)
                        tableArray[i].primaryKey.remove(dependencies.determinant)

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
