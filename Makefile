


images/pinger.tar: slow_ping/Dockerfile
	S=C:/Users/giorgig/starter-kit/ahab/config/sonarqube PING_HOST=127.0.0.1 docker-compose -f slow-pinger-deploy.yml build
	docker save -o images/pinger.tar slow-ping:latest

run: images/pinger.tar slow-pinger-deploy.yml
	S=C:/Users/giorgig/starter-kit/ahab/config/sonarqube docker stack up --compose-file slow-pinger-deploy.yml pinger1
	docker stack services pinger1
	docker service ps pinger1_influxdb
	# docker service logs --tail 3 -f pinger1_influxdb
	#docker service logs pinger1_visualizer
	#docker service logs -f pinger1_slow_ping

all: run
	echo All done

clean:
	docker stack rm pinger1
	rm -f images/pinger.tar
	sleep 2
	docker stack services pinger1

status:
	docker service ps pinger1_slow_ping
	docker service ps pinger1_influxdb	
	@echo -n Mem usage:
	@docker stats --no-stream --format "table {{.MemPerc}}" | sed 's/[A-Za-z]*//g' | awk '{sum += $$1} END {print sum "%"}'