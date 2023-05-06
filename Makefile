init:
	pip install -r requirements.txt

# build application
b:
	rm -rf dist build *.spec && mkdir -p dist/asserts
	cp asserts/* dist/asserts && cp aria2c.exe aria2c.html dist/
	pyinstaller -F -i ./asserts/logo.ico -w -n ReaTool  main.py
