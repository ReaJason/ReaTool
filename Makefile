init:
	pip install -r requirements.txt

deploy:
	mkdir -p dist
	rm -rf dist
	mkdir -p dist/asserts
	cp asserts/* dist/asserts
	cp aria2c.exe dist/
	pyinstaller -F -i ./asserts/logo.ico -w -n ReaTool  main.py