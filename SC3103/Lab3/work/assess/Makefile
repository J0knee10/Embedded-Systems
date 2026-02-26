# Makefile for assessment

# Macros
cc = gcc
CFLAGS = -Wall
OBJ = mathlib.o
DEBUGFLAG = -g
PROFFLAG = -pg

# default target
all: printFact printMulti printFact-d printFact-p

# build main obj
mathlib.o: mathlib.c mathlib.h
	$(CC) $(PROFFLAG) $(DEBUGFLAG) $(CFLAGS) -c mathlib.c

# build main files
printFact.o: printFact.c mathlib.h
	$(CC) $(PROFFLAG) $(DEBUGFLAG) $(CFLAGS) -c printFact.c

printMulti.o: printMulti.c mathlib.h
	$(CC) $(CFLAGS) -c printMulti.c

# the linking
printFact: printFact.o $(OBJ)
	$(CC) printFact.o $(OBJ) -o printFact

printMulti: printMulti.o $(OBJ)
	$(CC) printMulti.o $(OBJ) -o printMulti

# debug build
printFact-d: printFact.o $(OBJ)
	$(CC) $(DEBUGFLAG) printFact.o $(OBJ) -o printFact-d

#prof enabled
printFact-p: printFact.o $(OBJ)
	$(CC) $(PROFFLAG) printFact.o $(OBJ) -o printFact-p

clean:
	rm -f *.o printFact printMulti printFact-d printFact-p gmon.out
