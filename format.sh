#!/bin/sh

case $1 in
	rime)
		cat | sed 's/<>//g; s/ | //g'
		;;
	algebra)
		cat | sed 's/<>//g; s/ | //g' | sed -E 's/(.+)\t(.+)/- xform|^\2$|\1|/'
		;;
	plover)
		echo "{"
		cat | sed 's/ | /\//g; s/<>//g' |
			sed -E 's/(.+)\t(.+)/"\2": "\1",/' |
			sed -E '$ s/,$//' |
			perl -pe 's/: "(?!(\{.+\}|=))/: "{&/g;' |
			sed -E 's/: "\{&(.+)"/: "\{\&\1}"/'
		echo "}"
		;;
esac
