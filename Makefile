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

run_local_build:
	docker build --tag=${GCR_IMAGE}:dev .

run_local_run:
	docker run -e PORT=8000 -p 8000:8000 --env-file .env ${GCR_IMAGE}:dev

run_local_docker:
	run_local_build run_local_run

run_GCR_build:
	docker build --platform linux/amd64 -t ${GCR_REGION}/${GCP_PROJECT}/${GCR_IMAGE}:prod .

run_GCR_push:
	docker push ${GCR_REGION}/${GCP_PROJECT}/${GCR_IMAGE}:prod

run_GCR_deploy:
	gcloud run deploy --image ${GCR_REGION}/${GCP_PROJECT}/${GCR_IMAGE}:prod --memory ${GCR_MEMORY} --region ${GCP_REGION} --env-vars-file .env.yaml

run_GCR_all:
	run_GCR_build run_GCR_push run_GCR_deploy
