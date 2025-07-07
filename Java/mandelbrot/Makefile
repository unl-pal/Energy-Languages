compile:
	cp mandelbrot.java-2.java mandelbrot.java
	/usr/lib/jvm/java-8-openjdk-amd64/bin/javac -d . mandelbrot.java

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "/usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp . mandelbrot 16000" Java mandelbrot

run:
	/usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp . mandelbrot 16000

mem:
	/usr/bin/time -v /usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp . mandelbrot 16000

valgrind:
	valgrind --tool=massif --stacks=yes /usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp . mandelbrot 16000
