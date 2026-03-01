{
	for (i = 1; i <= length($2); i++) {
		code = substr($2, i, 1)
		codes[code] = 0
	}
}
END {
	for (code in codes) print code
}
