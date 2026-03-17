Main changes from the original DataSketch library:



rbo\_min\_hash.py:

 	-Slight modification of minhash.py

 	-Added rbo\_sim function to compute the RBO similarity

 	-Added \_hash\_rbo function to perform the hashing following RBOMinHash

 	-RBOMinHash class: slight modification of original MinHash class

 		-Modified \_\_init\_\_, update and copy methods

 		-jaccard method replaced by rbo method

&#x09;-Removed unused methods like ones involving GPU



utilities.py:

 	-Written from scratch

 	-Introduces 5 functions used in the examples:

 		-top\_keys

 		-encode\_ranking

 		-load\_rankings

&#x09;	-generate\_lists

&#x09;	-update\_json



examples/rbo\_min\_hash\_example.py:

 	-Slight modification of minhash\_examples.py

 	-Parameters are loaded from eg1\_parameters.json

 	-Dataset loaded from files in docs directory (files taken from 	https://github.com/rahularora/MinHash)



examples/ann\_example.py:

 	-Slight modification of minhash\_examples.py

 	-Used as an instance of the ANN problem

 	-Parameters are loaded from ann\_parameters.json

 	-Dataset loaded from files in docs directory (files taken from 	https://github.com/rahularora/MinHash)



examples/multi\_run\_experiment.py:

 	-Runs ann\_example.py multiple times, then computes:

 		-The average precision

 		-The average recall

 		-The average ratio between the RBO similarity and the probability of hash collision for two rankings



examples/multi\_query\_experiment.py:

 	-Runs ann\_example.py multiple times using different query files. The list of files to be queried is the 

&#x09;	parameter 'multi\_query' in the "ann\_parameters.json" file.

&#x09;-It prints the results in a txt file inside the "results" directory

&#x09;-It will create a subdirectory called "x neighbors", where x is the number of neighbors computed in the 

&#x09;	experiment, in which to save the results.



examples/both\_multi.py:

&#x09;-Runs ann\_example.py multiple times using different query files, then computes:

 		-The average precision

 		-The average recall

 		-The average ratio between the RBO similarity and the probability of hash collision for two rankings

 	-The list of files to be queried is the parameter 'multi\_query' in the "ann\_parameters.json" file.

&#x09;-It prints the results in a txt file inside the "results" directory

&#x09;-It will create a subdirectory called "x neighbors", where x is the number of neighbors computed in the

&#x09;	experiment, in which to save the results.







