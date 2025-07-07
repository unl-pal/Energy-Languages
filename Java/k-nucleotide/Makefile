compile:

	/usr/lib/jvm/java-8-openjdk-amd64/bin/javac -d . -cp .:/usr/local/src/java-libs/fastutil-7.0.12.jar knucleotide.java

measure:
	sudo modprobe msr
	# NOTE: This path works only if input file exists
	sudo ../../RAPL/main "/usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp .:/usr/local/src/java-libs/fastutil-7.0.12.jar knucleotide 0 < knucleotide-input25000000.txt" Java k-nucleotide

run:
	
	/usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp .:/usr/local/src/java-libs/fastutil-7.0.12.jar knucleotide 0 < knucleotide-input25000000.txt

mem:
	/usr/bin/time -v /usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp .:/usr/local/src/java-libs/fastutil-7.0.12.jar knucleotide 0 < knucleotide-input25000000.txt

valgrind:
	
	valgrind --tool=massif --stacks=yes /usr/lib/jvm/java-8-openjdk-amd64/bin/java -cp .:/usr/local/src/java-libs/fastutil-7.0.12.jar knucleotide 0 < knucleotide-input25000000.txt
