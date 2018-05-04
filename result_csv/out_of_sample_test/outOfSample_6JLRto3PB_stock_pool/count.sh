for dir in $(find . -type d);do 
	find $dir -maxdepth 1 -type f | wc -l
done