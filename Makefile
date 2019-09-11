all:build

build:
	gcc server.c -o server
	gcc client.c -o client

clean:
	rm -f server client

run-collect:
	python3 ./alg/SockCollector.py $(alg)

run-feeder:
	python3 ./alg/$(alg).py