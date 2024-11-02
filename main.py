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
            break
        
        if (isValid):
            Normalizer.normalizeTo1NF(tableArray, nonAtomicValuesArray)
            FinalRelationGen.printResult(tableArray)

        if (highestNormalization != "1NF" and isValid):
            InputParser.takeInput2NF()
            isValid = Normalizer.normalizeTo2NF(tableArray)
            FinalRelationGen.printResult(tableArray)

        elif (highestNormalization != "2NF" and isValid):
            InputParser.takeInput3NF()
            isValid = Normalizer.normalizeTo3NF(tableArray)
            FinalRelationGen.printResult(tableArray)

        elif (highestNormalization != "3NF" and isValid):
            InputParser.takeInputBCNF()
            isValid = Normalizer.normalizeToBCNF(tableArray)
            FinalRelationGen.printResult(tableArray)

        elif (highestNormalization != "BCNF" and isValid):
            InputParser.takeInput4NF()
            isValid = Normalizer.normalizeTo4NF(tableArray)
            FinalRelationGen.printResult(tableArray)

        elif (highestNormalization != "4NF" and isValid):
            InputParser.takeInput5NF()
            isValid = Normalizer.normalizeTo5NF(tableArray)
            FinalRelationGen.printResult(tableArray)

    print("\n\n-----------PROGRAM TERMINATED-----------\n\n")

    return

if __name__ == '__main__':
    main()