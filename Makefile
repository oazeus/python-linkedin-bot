reqs:
	pipreqs --force .

company:
	python3 linkedin.py --keywords=${c} --page=${p} 

jobs:
	python3 linkedin.py --keywords=${c} 