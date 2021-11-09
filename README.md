# USI Bad Smell Detection
First project of [Knowledge Analysis & Management](https://search.usi.ch/en/courses/35263581/knowledge-analysis-management) college course. <br>

## Prerequisites
`Python 3` must be installed on your machine. <br>
The libraries needed for the program to work are: `AST` (included in Python), `Owlready 2`, `rdflib`

## Download
You can download the compressed file from this page and extract 
it to a folder of your choice, alternatively you can download it directly 
from a terminal using the following commands:

```
git clone https://github.com/DavideMammarella/Bad-Smell-Detection.git
```

## Access
Access the application folder:
```
cd Bad-Smell-Detection/
```
N.B. Check that the path to the project folder is correct

## Run the application:
#### Create the Ontology
```
python3 onto-creator.py
```
#### Populate the Ontology
```
python3 individ-creator.py
```
#### Find Bad Smells
```
python3 bad-smells.py
```

## How to access the results
### Output folder
All the files that will be generated as output will be available in the project folder <br><br>
Execution of `Create the Ontology` command will create an ontology named `tree.owl` <br>
Execution of `Populate the Ontology` command will populate `tree.owl`, generating a new ontology named `tree2.owl` <br>
Finally, execution of `Find Bad Smells` command will generate a file named `log.txt` that contains the metrics on the Bad Smells in Latex format.
### Access files
All ontologies, i.e. files with the extension `.owl`, can be opened with [Protegè](https://protege.stanford.edu) <br>
It is advisable to open the file with the `.txt` extension with a [Latex editor](https://www.overleaf.com/), as it contains the tables relating to Bad Smells in Latex format.