from flask import Flask, render_template
from database.utils import get_num_schedules, get_schedules
import argparse

# argument parser for password
parser = argparse.ArgumentParser(description='Supply the password.')
parser.add_argument('-p',
            dest='password',
            required=True,
            type=str,
            help='the rds password')
args = parser.parse_args()

# create flask app object
app = Flask(__name__)


@app.route('/')
def home():
	
	# get the number of schedules in the database
	num_schedules = get_num_schedules(args.password)
	
	# get a list of schedules
	schedules = get_schedules(args.password, num_schedules=100)
	
	return render_template('home.html', num_schedules=num_schedules, schedules=schedules)

if __name__ == '__main__':
	app.run()