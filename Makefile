reqs:
	pipreqs --force .

company:
	python3 ./scripts/linkedin.py --keywords=${c} --page=${p} 

jobs:
	python3 ./scripts/jobs.py --keywords=${c} 

fb_posts:
	python3 ./scripts/fb_posts.py --keywords=${c} 