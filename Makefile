say_hello:
	echo "hello world"

docker:
	docker build -t cf-app .
	docker tag cf-app ronbckbn/cf_app
	docker push ronbckbn/cf_app

docker_base:
	docker build -t cf_base -f Dockerfile_base .
	docker tag cf_base ronbckbn/cf_base
	docker push ronbckbn/cf_base
# test:
# 	python3 manager.py test
# lambda:
# 	virtualenv lambda_handler/v-env
# 	source ~/development/stride-core/lambda_handler/v-env/bin/activate
# 	cd lambda_handler/v-env/lib/python3.7/site-packages/ && zip -r9 ~/development/stride-core/lambda_handler/stride_function.zip .
# 	cd ~/development/stride-core/lambda_handler && zip -g stride_function.zip lambda_function.py
# 	cd ~/development/stride-core/lambda_handler && aws lambda update-function-code --function-name stride-balance-update --zip-file fileb://stride_function.zip
# activate:
# 	source ~/env/stride/bin/activate