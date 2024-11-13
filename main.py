# Author: Evan Pozzo
# Date: 10/25/2024
# Purpose: COMP_SCI-5300-101, Programming Project: RDBMS Normalizer

import Normalizer
import InputParser
import FinalRelationGen

def main():

    # we will loop the program as long as the user has new tables to input
    isValid = True

    while (True):
        # tableArray is an array of Table objects
        # each table object has an array for  column names, primary key, candidate keys, and functionalDependency objects
        # each functionalDependency object has a determinant and a dependency array
        tableArray, highestNormalization, nonAtomicValuesArray = InputParser.takeInput1NF()
        if tableArray == "EXIT":
            isValid = False
            break

        FinalRelationGen.printResult(tableArray)
        # ensure we were given a valid normalization level
        if(highestNormalization == "1NF" or highestNormalization == "2NF" or highestNormalization == "3NF" or highestNormalization == "BCNF" or highestNormalization == "4NF" or highestNormalization == "5NF"):
            isValid = True
        else:
            isValid = False
            print("Enter a valid highest normalization value")
            break
        
        if (isValid): # 1NF
            if(len(nonAtomicValuesArray) > 0):
                tableArray = Normalizer.normalizeTo1NF(tableArray, nonAtomicValuesArray)
            else:
                print("\n\n-----------Table is already in 1NF-----------\n\n")
                
            if (highestNormalization != "1NF"): # 2NF
                tableArray = Normalizer.normalizeTo2NF(tableArray)

                if (highestNormalization != "2NF"): # 3NF
                    tableArray = Normalizer.normalizeTo3NF(tableArray)
 
                    if (highestNormalization != "3NF"): # BCNF
                        tableArray = Normalizer.normalizeToBCNF(tableArray)

                        if (highestNormalization != "BCNF"): # 4NF 
                            tableArray = Normalizer.normalizeTo4NF(tableArray)

                            if (highestNormalization != "4NF"): # 5NF
                                tableArray = Normalizer.normalizeTo5NF(tableArray)
            if(isValid):
                print("-----------FINAL OUTPUT-----------\n")
                FinalRelationGen.printResult(tableArray)


    print("\n\n-----------PROGRAM TERMINATED-----------\n\n")
    
    return

if __name__ == '__main__':
    main()