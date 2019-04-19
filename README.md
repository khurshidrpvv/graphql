1. Install memcached for caching `sudo apt-get install memcached`
2. Clone `git clone https://github.com/khurshidrpvv/graphql.git`
3. `cd graphql`
4. create virtual evn  
    `virtualenv -p python3.6 .`  
    `source bin/activate`  
5. Install project dependencies  
  `pip install -r requirements.txt`
6. Start server `python manage.py runserver`  
7. `http://localhost:8000/graphql`