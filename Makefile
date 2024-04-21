.PHONY: main
main:
	echo "#!/usr/bin/env python3" > JackAnalyzer;
	cat JackAnalyzer.py >> JackAnalyzer;
	chmod +x ./JackAnalyzer;

.PHONY: zip
zip:
	zip project10.zip \
		Makefile \
		CompilationEngine.py \
		JackTokenizer.py \
		JackAnalyzer.py

.PHONY: clean
clean:
	rm -f JackAnalyzer;
	rm -f project10.zip;

.PHONY: test
test:
	echo "hello world"
