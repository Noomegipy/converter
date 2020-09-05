Test application for covert currencies

#### How to run:
docker-compose up -d

will run build from repo + run redis

###API EXAMPLES
____________________________________
####Add courses for currency

curl --request POST \
  --url 'http://0.0.0.0:5000/database?merge=1' \
  --header 'content-type: application/json' \
  --data '{
	"currencies": {
		"RUB": {
			"EUR": "0.9"
		},
		"USD": {
			"AED": "0.33"
		},
		"AED": {
			"RUB": 12
		}
	}
}'

This method also returns data after saving.
____________________________________
####Get all saved currencies and courses

curl --request GET \
  --url 'http://0.0.0.0:5000/database?merge=1'
  
___________________________________
####Convert amount

curl --request GET \
  --url 'http://0.0.0.0:5000/convert?from=RUB&to=USD&amount=100'