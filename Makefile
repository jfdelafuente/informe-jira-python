.PHONY: help install install-dev test lint format clean run-etl extract-bugs extract-delivs process-bugs process-delivs validate

help:  ## Muestra este mensaje de ayuda
	@echo "Comandos disponibles:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Instala las dependencias del proyecto
	pip install -r requirements.txt

install-dev:  ## Instala las dependencias de desarrollo
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

install-package:  ## Instala el paquete en modo editable
	pip install -e .

test:  ## Ejecuta los tests
	pytest tests/ -v

test-cov:  ## Ejecuta los tests con coverage
	pytest tests/ -v --cov=src/jira_etl --cov-report=html --cov-report=term

lint:  ## Verifica el código con flake8 y mypy
	flake8 src/ scripts/ --max-line-length=100 --exclude=__pycache__,*.pyc,.git
	mypy src/

format:  ## Formatea el código con black e isort
	black src/ scripts/ tests/
	isort src/ scripts/ tests/

format-check:  ## Verifica el formato sin modificar archivos
	black --check src/ scripts/ tests/
	isort --check-only src/ scripts/ tests/

clean:  ## Limpia archivos temporales y cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov/ dist/ build/

validate:  ## Valida el entorno antes de ejecutar
	python scripts/validate_environment.py

extract-bugs:  ## Extrae bugs desde Jira
	python scripts/extract_bugs.py

extract-delivs:  ## Extrae deliveries desde Jira
	python scripts/extract_deliveries.py

process-bugs:  ## Procesa los bugs extraídos (ETL)
	python scripts/process_bugs.py

process-delivs:  ## Procesa las deliveries extraídas (ETL)
	python scripts/process_deliveries.py

run-etl:  ## Ejecuta el pipeline ETL completo
	python scripts/run_full_etl.py

quick-test:  ## Test rápido: valida entorno y ejecuta un pequeño test
	python scripts/validate_environment.py --skip-jira
	@echo "✓ Entorno validado correctamente"

setup:  ## Setup inicial: crea directorios y valida configuración
	@echo "Configurando entorno..."
	@python -c "from src.jira_etl.config import Config; Config.create_directories(); print('✓ Directorios creados')"
	@test -f .env || (cp .env.example .env && echo "⚠ Archivo .env creado. Por favor configúralo.")
	@echo "✓ Setup completado"

show-config:  ## Muestra la configuración actual
	@python -c "from src.jira_etl.config import Config; \
		print('Configuración:'); \
		print(f'  JIRA_HOST: {Config.JIRA_HOST}'); \
		print(f'  JIRA_USER: {Config.JIRA_USER or \"<no configurado>\"}'); \
		print(f'  Input dir: {Config.INPUT_DIR}'); \
		print(f'  Output dir: {Config.OUTPUT_DIR}');"

# Alias comunes
init: setup  ## Alias para setup
run: run-etl  ## Alias para run-etl
check: lint  ## Alias para lint
fmt: format  ## Alias para format
