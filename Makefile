.PHONY: main
main:
	echo "#!/usr/bin/env python3" > JackAnalyzer;
	cat JackAnalyzer.py >> JackAnalyzer;
	chmod +x ./JackAnalyzer;

.PHONY: zip
zip:
	zip project10.zip \
		Makefile \
		JackTokens.py \
		TokenNavigator.py \
		CompilationEngine.py \
		JackTokenizer.py \
		JackAnalyzer.py

.PHONY: clean
clean:
	rm -f JackAnalyzer;
	rm -f project10.zip;

.PHONY: format
format:
	tidy -xml -i -m test/ArrayTest/MainT.xml &> /dev/null;
	tidy -xml -i -m test/ArrayTest/Main.xml &> /dev/null;
	tidy -xml -i -m test/ExpressionLessSquare/MainT.xml &> /dev/null;
	tidy -xml -i -m test/ExpressionLessSquare/Main.xml &> /dev/null;
	tidy -xml -i -m test/ExpressionLessSquare/SquareT.xml &> /dev/null;
	tidy -xml -i -m test/ExpressionLessSquare/Square.xml &> /dev/null;
	tidy -xml -i -m test/ExpressionLessSquare/SquareGameT.xml &> /dev/null;
	tidy -xml -i -m test/ExpressionLessSquare/SquareGame.xml &> /dev/null;

.PHONY: test
test:
	./JackAnalyzer test/ArrayTest
	./JackAnalyzer test/ExpressionLessSquare
