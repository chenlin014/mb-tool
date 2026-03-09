BEGIN {
	if (len == "") len = 2
}
length($2) >= len {
	for (i = 1; i+len-1 <= length($2); i++) {
		seq = substr($2, i, len)
		seq_freq[seq]++
	}
}
END {
	for (seq in seq_freq) print seq, seq_freq[seq]
}
