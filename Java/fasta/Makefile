compile:
	cp fasta.java-5.java fasta.java
	/usr/lib/jvm/java-8-openjdk-amd64/bin/javac -d . fasta.java

measure:
	sudo modprobe msr
	sudo ../../RAPL/main "/usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp . fasta 25000000" Java fasta

run:
	/usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp . fasta 25000000

mem:
	/usr/bin/time -v /usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp . fasta 25000000

valgrind:
	valgrind --tool=massif --stacks=yes /usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp . fasta 25000000
