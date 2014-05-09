from __future__ import print_function
from pprint import pprint
from jinja2 import Environment, FileSystemLoader
import json
import requests

ROOT = "https://192.168.56.101:8003/"

def read_config(cfg_filename):
    with open(cfg_filename) as cfg_f:
        cfg = json.loads(cfg_f.read())

    return cfg['pi-web-agent']['system']['actions']

def time_actions(actions):
    action_times = {}
    for action, attrs in actions.iteritems():
        action_url = "".join([ROOT, attrs['url']])
        dt = requests.get(action_url, verify=False).elapsed.total_seconds()
        action_times[attrs['title']] = dt

    return action_times

def main():
    actions = read_config("/Users/argyris/Desktop/config.cfg")
    action_times = time_actions(actions)
    #pprint(json.dumps(action_times))

    env = Environment(loader=FileSystemLoader(searchpath='templates'))
    template = env.get_template('results.html')

    with open("rendered.html", "w") as fout:
        fout.write(template.render(action_times=action_times))

if __name__ == "__main__":
    main()
