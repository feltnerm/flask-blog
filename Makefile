.PHONY: all less coffee

all: 	clean less coffee

clean:
	rm -rf apps/static/css/*.css
	rm -rf apps/static/js/*.js
less:
	lessc apps/static/less/style.less apps/static/css/style.css

coffee:
	coffee -b -l --compile --output apps/static/js/ apps/static/coffee/*.coffee

watch:
	coffee -wlbc -o apps/static/js/ apps/static/coffee/*.coffee
	
social_queue: 
	coffee -lbc -o apps/social_queue/ apps/social_queue/
