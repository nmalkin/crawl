appname = crawl

.PHONY: clean run

all: build run

run:
	docker run -it --rm --name $(appname) \
		-v $(PWD)/out:/usr/src/app/out \
		-v $(PWD)/whitelist.txt:/data/whitelist.txt \
		-v $(PWD)/blacklist.txt:/data/blacklist.txt \
		-v $(PWD)/complete.py:/usr/src/app/complete.py \
		--env START_URL \
		$(appname)

build:
	docker build -t $(appname) .

clean:
	rm -rf out && \
	docker rmi $(appname)

