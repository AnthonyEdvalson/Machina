#Makefile

CC = clang++

tests : Event.h.gch Tests.o
	$(CC) Event.h.gch Tests.o -o tests


Event.h.gch : Event.h
	$(CC) -c Event.h

Tests.o : Tests.cpp
	$(CC) -c Tests.cpp

