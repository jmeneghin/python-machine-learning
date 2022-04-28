#!/usr/bin/python3

##########################################################################################################################################################
# Neural Net Runner                                                                                                                                    ###
#                                                                                                                                                      ###
# nn_runner.py -f <Tab delimited input file (e.g. saved from Excel)>                                                                                   ###
#                                                                                                                                                      ###
# An Implementation of an MLPClassifier in Python.                                                                                                     ###
#                                                                                                                                                      ###
# This script takes any tab delimited file, where the first column contains the known categories, and the rest of the columns contain any numeric data ###
# to be used as input into the Multi-Layer Perceptron.\n\nAn MLPClassifier is an implementation of a Multi-Layer Perceptron Classifier,                ###
# which is a feedforward artificial neural network that maps the input dataset to a set of output classes.                                             ###
#                                                                                                                                                      ###
# The confusion matrix helps you look at the errors in more detail. If we were just classifying True/False here,                                       ###
# then the matrix would show correct answers on the diagonal (true positives and true negatives,                                                       ###
# and then false positives and false negatives on the other corners.                                                                                   ###
#                                                                                                                                                      ###
# The example I used to play with this script is a tab delimited file with tetranucleotided counts for 3201 MAGs (Meta-Genome Assembled Genomes),      ###
# that have been classified into five known species of bacteria. In this case, the five column totals show the actual number of members for each       ###
# species in the set, and the row totals show the species reported by the Perceptron. In this type of case, it could show whether particular           ###
# pairs of species are getting mixed up more than others                                                                                               ###
#                                                                                                                                                      ###
# If you'd like to play with tetranucleotide statistics, please see get_kmer_frequencies.py, a script I wrote that takes a fasta file,                 ###
# calculates the tetranucleotides and writes them to a tab delimited file.                                                                             ###
#                                                                                                                                                      ###
# Jennifer Meneghin                                                                                                                                    ###
# 4/27/2022                                                                                                                                            ###
##########################################################################################################################################################

import sys, getopt
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix

def accuracy(confusion_matrix):
    diagonal_sum = confusion_matrix.trace()
    sum_of_all_elements = confusion_matrix.sum()
    return diagonal_sum/sum_of_all_elements

def getDataFrame(argv):
    msg_txt = """\n\nnn_runner.py -f <Tab delimited input file (e.g. saved from Excel)>\n\nAn Implementation of an MLPClassifier in Python.\n\nThis script takes any tab delimited file, where the first column contains the known categories, and the rest of the columns contain any numeric data to be used as input into the Multi-Layer Perceptron.\n\nAn MLPClassifier is an implementation of a Multi-Layer Perceptron Classifier, which is a feedforward artificial neural network that maps the input dataset to a set of output classes.\n\nThe confusion matrix helps you look at the errors in more detail. The column totals show the actual number of members for each group in the set, and the row totals show the group reported by the Perceptron.\n\nJennifer Meneghin 4/27/2022\n\n"""
    in_file = "file.txt"
    try:
        opts, args = getopt.getopt(argv,"hf:",["ffile="])
    except getopt.GetoptError:
        print("\nNot a valid argument or value")
        print(msg_txt)
        sys.exit(2)        
    for opt, arg in opts:
        if opt == "-h":
            print(msg_txt)
            sys.exit()
        elif opt in ("-f", "--ffile"):
            in_file = arg
    try:
        fullDataSet = pd.read_csv(in_file, sep='\t')
    except FileNotFoundError:
        print("\nNot a valid argument or value -- File Not Found Error")
        print(msg_txt)
        sys.exit(3)                
    return fullDataSet
    
def main(argv):
    fullDataSet = getDataFrame(argv)

    print("Importing data set...")
    #This converts text data to numeric categories. Answer is in 1st column.
    fullDataSet.iloc[:,0] = LabelEncoder().fit_transform(fullDataSet.iloc[:,0])

    #If N = number of rows and test_size = 0.2 then 0.2xN = number of rows in test set. Rest are in training set.
    #Rows chosen for test and training are randomized
    print("Splitting data into training and testing sets...")
    train_set, test_set = train_test_split(fullDataSet, test_size = 0.2, random_state = 21)

    print("Splitting both training and testing data into X (input data) and Y (known answers)...")
    X_train = train_set.iloc[:,1:].values
    Y_train = train_set.iloc[:,0].values 
    X_test = test_set.iloc[:,1:].values  
    Y_test = test_set.iloc[:,0].values   

    print("Running the MLP Classifier...")
    #Multi-Layer Perceptron Classifier -- this is a feedforward artificial neural network that maps input data to a set of output classes.
    classifier = MLPClassifier(                   
    activation='relu',     
    #activation='identity', #Possible Activation functions.
    #activation='logistic',
    #activation='tanh',
    alpha=0.0001,
    batch_size='auto',
    beta_1=0.9,
    beta_2=0.999,
    early_stopping=False,
    epsilon=1e-08,
    #hidden_layer_sizes=(100,),
    hidden_layer_sizes=(150,100,50),
    learning_rate='constant',
    max_fun=15000,
    #max_iter=200,
    max_iter=300,
    momentum=0.9,
    n_iter_no_change=10,
    nesterovs_momentum=True,
    power_t=0.5,
    random_state=None,
    shuffle=True,
    solver='adam',
    tol=0.0001,
    validation_fraction=0.1,
    verbose=True,
    warm_start=False,
    learning_rate_init=.001
    )
    try:
        classifier.fit(X_train,Y_train)
    except ValueError:
        print("\nNon-numeric value found in datafile. Please fix your data and try again.\n")
        sys.exit(4)                

    y_prediction = classifier.predict(X_test)
    cm = confusion_matrix(y_prediction, Y_test)
    print("Confusion Matrix = ")
    print(cm)
    print("Calculating the accuracy of the MLP Classifier...")
    print("Accuracy of MLPClassifier = ", accuracy(cm))
    
if __name__ == "__main__":
    main(sys.argv[1:])

