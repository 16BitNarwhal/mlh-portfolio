num_before=$(curl http://localhost:5000/api/timeline_post | jq length)
status_code=$(curl --write-out %{http_code} --silent --output /dev/null -X POST http://localhost:5000/api/timeline_post -d 'name=john&email=john%gmail.com&content=food')

if [[ "$status_code" -eq 200 ]]; then
	num_after=$(curl http://localhost:5000/api/timeline_post | jq length)
	if [ $after -gt $before ]; then
		echo "Success!"
		exit 0
	fi
fi

echo "Failed!"
exit 1
