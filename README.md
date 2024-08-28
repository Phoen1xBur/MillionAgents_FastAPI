<h1>MillionAgents_FastAPI</h1>

<h2>Installation</h2>
Clone project
<pre>
git clone https://github.com/Phoen1xBur/MillionAgents_FastAPI.git
cd MillionAgents_FastAPI
</pre>
And if you need, create virtual environments
<pre>
python3 -m venv venv
. venv/bin/activate
</pre>
Install pypi package from requirements
<pre>pip install -r requirements.txt</pre>
<h3>Debian/Ubuntu</h3>
Install linux package libmagic1 for python-magic 
<pre>sudo apt-get install libmagic1</pre>

<h2>Configurate & Start application</h2>
Edit the .env file for your postgres connection and upgrade DB next command:
<pre>alembic upgrade head</pre>
Last step: run server!
<pre>uvicorn src.main:app --reload --host 127.0.0.1 --port 80</pre>
