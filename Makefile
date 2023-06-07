run_api:
	uvicorn hatescan.api.model_api:app --reload

run_preprocess:
	python -c 'from hatescan.interface.main import preprocess; preprocess()'

run_train:
	python -c 'from hatescan.interface.main import train; train()'

run_evaluate:
	python -c 'from hatescan.interface.main import evaluate; evaluate()'

run_pred:
	python -c 'from hatescan.interface.main import pred; pred()'

run_all: run_preprocess run_train run_pred run_evaluate