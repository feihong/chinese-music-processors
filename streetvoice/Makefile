UNAME := $(shell uname)

ifeq ($(UNAME),Darwin)
  BRAVE := open -a "Brave Browser"
else
  BRAVE := brave
endif

install:
	yarn install

upgrade:
	pip install --user --upgrade mitmproxy

proxy:
	mitmdump -w dumpfile --anticache

browser:
	$(BRAVE) -n --args --incognito --proxy-server=https://127.0.0.1:8080 https://streetvoice.com/megafeihong

start:
	python runner.py parallel proxy browser

convert_to_sqlite:
	mitmdump -ns convert_to_sqlite.py -r dumpfile

process:
	python runner.py sequential convert_to_sqlite generate_metadata.coco generate_files.coco consolidate.coco

clean:
	rm assets/* && rm dumpfile
