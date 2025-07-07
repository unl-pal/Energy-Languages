compile:
	cp spectralnorm.java-2.java spectralnorm.java
	/usr/lib/jvm/java-8-openjdk-amd64/bin/javac -d . spectralnorm.java
measure:
	sudo modprobe msr
	sudo ../../RAPL/main "/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java spectralnorm 5500" Java spectral-norm

run:
	/usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java spectralnorm 5500

mem:
	/usr/bin/time -v /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java spectralnorm 5500

valgrind:
	valgrind --tool=massif --stacks=yes /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java spectralnorm 5500
