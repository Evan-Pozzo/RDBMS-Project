import InputParser


def printResult(tableArray):
    for tables in tableArray:
        print(tables.tableName)
        print("\tPrimary Key: ", tables.primaryKey)
        print("\tCandidate Keys: ", tables.candidateKey)

        for columns in tables.columns:
            print("\t - ", columns)
        print()
        i = 1
        for dependencies in tables.functionalDependencies:

            print("\tFD " + str(i) + ")\t", end = '')
            print(dependencies.determinant, end = "")
            print(" --> ", end ="")
            print(dependencies.dependent, end = "")
            print()
            i += 1
    print("\n---------------- DONE ----------------\n")
    return