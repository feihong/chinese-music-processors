upgrade:
	pip install --upgrade mitmproxy

proxy:
	mitmdump -w dumpfile --anticache

start:
	python runner.py parallel proxy browser

convert_to_sqlite:
	mitmdump -ns convert_to_sqlite.py -r dumpfile

process:
	python runner.py sequential convert_to_sqlite generate_metadata.coco generate_files.coco consolidate.coco

clean:
	rm assets/*; rm dumpfile
