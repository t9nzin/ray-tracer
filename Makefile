CXX      ?= c++
CXXFLAGS ?= -std=c++17 -O3 -Wall -Wextra -pthread

raytracer: main.cpp *.h
	$(CXX) $(CXXFLAGS) -o $@ main.cpp

run: raytracer
	./raytracer

clean:
	rm -f raytracer test.ppm

.PHONY: run clean
