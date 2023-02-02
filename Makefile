IMG := johanneswuerbach/markdown-inline-mermaid

build-test-image:
	docker build -t $(IMG) .

test: build-test-image
	docker run --rm -it -v $(PWD):/app $(IMG) pytest -v
