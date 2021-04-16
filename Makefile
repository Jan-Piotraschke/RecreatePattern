# Important for the development process
# ============================================================
# SHELL := /bin/bash




########################################################################################################################
# PYTHON                                                                                                             #
########################################################################################################################

# Setup the virtual environment. Recommended for development.
.PHONY: venv
venv:
	python3 -m venv venv && \
	source venv/bin/activate && \
	pip3 install -r requirements.txt