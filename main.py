# Author: Evan Pozzo
# Date: 10/25/2024
# Purpose: COMP_SCI-5300-101, Programming Project: RDBMS Normalizer

import Normalizer
import InputParser
import FinalRelationGen
import numpy as np

def main():

    # we will loop the program as long as the user has new tables to input
    while (True):
        isValid = True
        # tableArray is an array of Table objects
        # each table object has an array for  column names, primary key, candidate keys, and functionalDependency objects
        # each functionalDependency object has a determinant and a dependency array
        tableArray, highestNormalization, nonAtomicValuesArray, MVDarray = InputParser.takeInput1NF()
        if tableArray == "EXIT":
            isValid = False
            break

        FinalRelationGen.printResult(tableArray)

        if (isValid):
            tableArray = Normalizer.normalizeTo1NF(tableArray, nonAtomicValuesArray)
            print("\n------------- 1NF Results -------------\n")
            FinalRelationGen.printResult(tableArray)

        if (highestNormalization != "1NF" and isValid):
            tableArray = Normalizer.normalizeTo2NF(tableArray)
            print("\n------------- 2NF Results -------------\n")
            FinalRelationGen.printResult(tableArray)

            if (highestNormalization != "2NF" and isValid):
                tableArray = Normalizer.normalizeTo3NF(tableArray)
                print("\n------------- 3NF Results -------------\n")
                FinalRelationGen.printResult(tableArray)

                if (highestNormalization != "3NF" and isValid):
                    tableArray = Normalizer.normalizeToBCNF(tableArray)
                    print("\n------------- BCNF Results -------------\n")
                    FinalRelationGen.printResult(tableArray)

                    if (highestNormalization != "BCNF" and isValid):
                        tableArray = Normalizer.normalizeTo4NF(tableArray)
                        print("\n------------- 4NF Results -------------\n")
                        FinalRelationGen.printResult(tableArray)

                        if (highestNormalization != "4NF" and isValid):
                            tableArray = Normalizer.normalizeTo5NF(tableArray)
                            print("\n------------- 5NF Results -------------\n")
                            FinalRelationGen.printResult(tableArray)

    print("\n\n-----------PROGRAM TERMINATED-----------\n\n")

    return

if __name__ == '__main__':
    main()