install:
	yarn install

upgrade:
	pip install --user --upgrade mitmproxy

proxy:
	mitmdump -w dumpfile --anticache

browser:
	brave -n --args --incognito --proxy-server=https://127.0.0.1:8080 https://streetvoice.com/megafeihong

clean:
	rm assets/* && rm dumpfile
