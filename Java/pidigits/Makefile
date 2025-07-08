compile:
	cp pidigits.java-2.java pidigits.java
	javac pidigits.java

native:
	javac -h . GmpInteger.java
	gcc -I. \
	    -I/usr/lib/jvm/java-8-openjdk-amd64/include \
	    -I/usr/lib/jvm/java-8-openjdk-amd64/include/linux \
	    -L. -fPIC -shared -o libjgmplib.so jgmplib.c -lgmp

run:
	LD_LIBRARY_PATH=. /usr/lib/jvm/java-8-openjdk-amd64/bin/java \
	    -Djava.library.path=. \
	    pidigits 10000

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "LD_LIBRARY_PATH=. /usr/lib/jvm/java-8-openjdk-amd64/bin/java -Djava.library.path=. pidigits 10000" Java pidigits

mem:
	/usr/bin/time -v LD_LIBRARY_PATH=. /usr/lib/jvm/java-8-openjdk-amd64/bin/java -Djava.library.path=. pidigits 10000
