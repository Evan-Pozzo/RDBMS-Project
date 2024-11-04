# Author: Evan Pozzo
# Date: 10/25/2024
# Purpose: COMP_SCI-5300-101, Programming Project: RDBMS Normalizer

import Normalizer
import InputParser
import FinalRelationGen

def main():

    # we will loop the program as long as the user has new tables to input
    while (True):
        isValid = True
        # tableArray is an array of Table objects
        # each table object has an array for  column names, primary key, candidate keys, and functionalDependency objects
        # each functionalDependency object has a determinant and a dependency array
        tableArray, highestNormalization, nonAtomicValuesArray = InputParser.takeInput1NF()
        if tableArray == "EXIT":
            isValid = False
            break

        FinalRelationGen.printResult(tableArray)

        if (isValid): # 1NF
            tableArray = Normalizer.normalizeTo1NF(tableArray, nonAtomicValuesArray)
            if (highestNormalization != "1NF" and isValid): # 2NF
                tableArray = Normalizer.normalizeTo2NF(tableArray)

                if (highestNormalization != "2NF" and isValid): # 3NF
                    tableArray = Normalizer.normalizeTo3NF(tableArray)
 
                    if (highestNormalization != "3NF" and isValid): # BCNF
                        tableArray = Normalizer.normalizeToBCNF(tableArray)

                        if (highestNormalization != "BCNF" and isValid): # 4NF 
                            tableArray = Normalizer.normalizeTo4NF(tableArray)

                            if (highestNormalization != "4NF" and isValid): # 5NF
                                tableArray = Normalizer.normalizeTo5NF(tableArray)

    print("\n\n-----------PROGRAM TERMINATED-----------\n\n")

    return

if __name__ == '__main__':
    main()