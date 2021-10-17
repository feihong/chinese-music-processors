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

# Figure out how to do this with shell script instead
start:
	yarn start

proxy:
	mitmdump -w dumpfile --anticache

browser:
	$(BRAVE) -n --args --incognito --proxy-server=https://127.0.0.1:8080 https://streetvoice.com/megafeihong

clean:
	rm assets/* && rm dumpfile
