compile:
	/usr/lib/jvm/java-8-openjdk-amd64/bin/javac -d . -cp .:/usr/local/src/java-libs/fastutil-7.0.12.jar knucleotide.java

measure:
	sudo modprobe msr
	cat knucleotide-input25000000.txt | sudo ../../RAPL/main "/usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp .:/usr/local/src/java-libs/fastutil-7.0.12.jar knucleotide 0" Java k-nucleotide

run:
	cat knucleotide-input25000000.txt | /usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp .:/usr/local/src/java-libs/fastutil-7.0.12.jar knucleotide 0

mem:
	/usr/bin/time -v sh -c 'cat knucleotide-input25000000.txt | /usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp .:/usr/local/src/java-libs/fastutil-7.0.12.jar knucleotide 0'

valgrind:
	valgrind --tool=massif --stacks=yes --log-file=massif.log /usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp .:/usr/local/src/java-libs/fastutil-7.0.12.jar knucleotide 0 < knucleotide-input25000000.txt
