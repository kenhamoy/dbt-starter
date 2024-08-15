.PHONY: clean dev venv help
.DEFAULT_GOAL := help
-include .env

help: ## List Make Commands
	@awk -F ':.*?## ' '/^[a-zA-Z]/ && NF==2 {printf "\033[36m  %-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install:  ## Setup dev environment
	poetry install --with dev
	python setup.py
	@echo """Don't forget to install your dbt package use 'poetry add <dbt_adapter>'"""
	poetry shell