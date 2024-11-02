import InputParser


def printResult(tableArray):

    for tables in tableArray:
        print(tables.tableName)
        print("\tPrimary Key: ", tables.primaryKey)
        print("\Candidate Keys: ", tables.candidateKey)

        for columns in tables.columns:
            print("\t", columns)
        print()
        i = 1
        for dependencies in tables.functionalDependencies:
            print("FD " + i + ")\t" + dependencies.determinant + " --> " + dependencies.dependent)
            i += 1

    return