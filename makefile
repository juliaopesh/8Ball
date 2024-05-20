CC = clang
CFLAGS = -std=c99 -Wall -pedantic -fPIC
#LDFLAGS = -shared
# For ssh ; PYTHON_INCLUDE = /usr/include/python3.11
LDFLAGS = -shared -L/Library/Frameworks/Python.framework/Versions/3.11/lib
PYTHON_INCLUDE = /Library/Frameworks/Python.framework/Versions/3.11/include/python3.11
LD_LIBRARY_PATH_EXPORT = export LD_LIBRARY_PATH=$(shell pwd)
TEST_FILE = A3Test3.py

# Target: phylib.o
phylib.o: phylib.c
	$(CC) $(CFLAGS) -c phylib.c -o phylib.o

# Target: libphylib.so
libphylib.so: phylib.o
	$(CC) $(LDFLAGS) -o libphylib.so phylib.o -lm

# Target: phylib_wrap.c and phylib.py
phylib_wrap.c phylib.py: phylib.i
	swig -python phylib.i

# Target: phylib_wrap.o
phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I$(PYTHON_INCLUDE) -o phylib_wrap.o

# Target: _phylib.so
_phylib.so: phylib_wrap.o libphylib.so
	$(CC) $(LDFLAGS) -o _phylib.so phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib

# Target: clean
clean:
	rm -f phylib.o libphylib.so phylib_wrap.c phylib.py phylib_wrap.o _phylib.so

# Target: all
all: _phylib.so

# Target: run
run: _phylib.so
	$(LD_LIBRARY_PATH_EXPORT); python3.11 $(TEST_FILE)

# Target: run_server 
run_server: _phylib.so
	$(LD_LIBRARY_PATH_EXPORT); python3.11 server.py 58267
