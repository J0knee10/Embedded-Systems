# Makefile for helloworld

# Macro def
CC = gcc
CFLAGS = -Wall
OBJECTS = hello-main.o hello-funct1.o

#default target is first target declared
all: helloworld

#linking rule does not matter compiling or linking first, it makes a dependency graph
helloworld: $(OBJECTS)
	$(CC) $(CFLAGS) -o helloworld $(OBJECTS)

#Compiling rule
hello-main.o: hello-main.c hello.h
	$(CC) $(CFLAGS) -c hello-main.c

hello-funct1.o: hello-funct1.c hello.h
	$(CC) $(CFLAGS) -c hello-funct1.c

# Clean rule
clean:
	rm -f *.o helloworld


