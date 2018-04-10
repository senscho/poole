# kill $(ps aux | grep jekyll | awk '{print $2}')
jekyll serve --config _config.yml,_local.yml &
osascript -e 'tell application "Safari" to make new document with properties {URL: "http:localhost:4000"}' &