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
      "EUR": "0.1",
      "USD": "0.0133"
    },
    "USD": {
      "RUB": "0.3",
      "EUR": "0.0124"
    },
    "ARO": {
      "RUB": "0.3",
      "EUR": "1.3"
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