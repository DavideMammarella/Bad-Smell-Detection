# Bad Smell Detection
First project of [Knowledge Analysis & Management](https://search.usi.ch/en/courses/35263581/knowledge-analysis-management) college course<br>

## Prerequisites
- `Python 3` must be installed on your machine
- The libraries needed for the program to work are: `AST` (included in Python), `Owlready 2`, `rdflib`

## Download
You can download the compressed file from this page and extract 
it to a folder of your choice, alternatively you can download it directly 
from a terminal using the following commands:

```
git clone https://github.com/DavideMammarella/Bad-Smell-Detection.git
```

Access the application folder:
```
cd Bad-Smell-Detection/
```

## Run the application
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

## Access the results
### Output folder
All the files that will be generated as output will be available in the project folder <br>
- Execution of `Create the Ontology` command will create an ontology named `tree.owl` <br>
- Execution of `Populate the Ontology` command will populate `tree.owl`, generating a new ontology named `tree2.owl` <br>
- Finally, execution of `Find Bad Smells` command will generate a file named `log.txt` that contains the bad smells metrics
### Access files
- All ontologies, i.e. files with the extension `.owl`, can be opened with [Protegè](https://protege.stanford.edu) <br>
- It is advisable to open the `log.txt` file with a [Latex editor](https://www.overleaf.com/), as it contains bad smell metrics tables in Latex format

## Tests
All the scripts in the application have been tested. <br>
In order to reproduce the tests, it is necessary to access the application folder with the above command and execute the following command:
```
py.test
```