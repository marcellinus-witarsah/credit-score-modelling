#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = credit-score-modeling
PYTHON_VERSION = 3.12.4
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################


## Install Python Dependencies
.PHONY: requirements
requirements:
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	
## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8 and black (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 credit_score_modelling
	isort --check --diff --profile black credit_score_modelling
	black --check --config pyproject.toml credit_score_modelling

## Format source code with black
.PHONY: format
format:
	black --config pyproject.toml credit_score_modelling

## Set up python interpreter environment
.PHONY: create_environment
create_environment:
	
	conda create --name $(PROJECT_NAME) python=$(PYTHON_VERSION) -y
	
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"


## Create a ipykernel
.PHONY: create_ipykernel
create_ipykernel: requirements
	$(PYTHON_INTERPRETER) -m pip install ipykernel
	$(PYTHON_INTERPRETER) -m ipykernel install --user --name $(PROJECT_NAME) --display-name "$(PROJECT_NAME) (Python $(PYTHON_VERSION))"

	@echo ">>> ipykernel created"

## Create a documentation using numpydoc format
.PHONY: pyment_generate_doc
pyment_generate_doc: 
	pyment -w -o $(DOC_FORMAT) $(PYTHON_FILE)

	@echo ">>> $(DOC_FORMAT) documentation generated"

	
## Update requirements.text
.PHONY: update_requirements
update_requirements: 
	echo '-e .' >requirements.txt
	pip-chill >> requirements.txt

	@echo ">>> requirements.txt updated"


#################################################################################
# MODELLING			                                                            #
#################################################################################

## Data Preprocessing
.PHONY: data_preprocessing
data_preprocessing: 
	$(PYTHON_INTERPRETER) credit_score_modelling/data_preprocessing.py

	@echo ">>> Data preprocessing completed"


## Train model
.PHONY: train
train: 
	$(PYTHON_INTERPRETER) credit_score_modelling/modeling/train.py

	@echo ">>> Training completed"


## Evaluation
.PHONY: eval
eval:
	$(PYTHON_INTERPRETER) credit_score_modelling/modeling/evaluate.py
	
	echo '## Model Train Metrics' > report.md
	cat ./reports/train_metrics.json >> report.md
	echo '\n' >> report.md
	
	echo '## Train Calibration Plot' >> report.md
	echo '![Train Calibration Plot](./reports/figures/train_calibration_curve.png)' >> report.md
	
	echo '## Model Test Metrics' >> report.md
	cat ./reports/test_metrics.json >> report.md
	echo '\n' >> report.md
	
	echo '## Test Calibration Plot' >> report.md
	echo '![Test Calibration Plot](./reports/figures/test_calibration_curve.png)' >> report.md
	
	cml comment create report.md
	@echo '>>> Model evaluation completed'


#################################################################################
# DEPLOYMENT                                                                    #
#################################################################################
.PHONY: hf-login
hf-login:
	pip install -U "huggingface_hub[cli]"
	huggingface-cli login --token $(HF) --add-to-git-credential

.PHONY: push-hub
push-hub:
	huggingface-cli upload marcellinus-witarsah/credit-score-app ./app --repo-type=space --commit-message="Sync App files"
	huggingface-cli upload marcellinus-witarsah/credit-score-app ./models /models --repo-type=space --commit-message="Sync Model"
	huggingface-cli upload marcellinus-witarsah/credit-score-app ./credit_score_modelling /credit_score_modelling --repo-type=space --commit-message="Sync Personal Python Package"
	huggingface-cli upload marcellinus-witarsah/credit-score-app ./requirements.txt /requirements.txt --repo-type=space --commit-message="Sync Python Dependencies"
	huggingface-cli upload marcellinus-witarsah/credit-score-app ./pyproject.toml /pyproject.toml --repo-type=space --commit-message="Sync for Install Personal Python Package"

.PHONY: deploy
deploy: hf-login push-hub

#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


## Make Dataset
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) credit_score_modelling/dataset.py


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
