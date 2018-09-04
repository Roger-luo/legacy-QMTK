import yaml

with open('test.yml', 'r') as f:
    envs = yaml.load(f)

envs['nparticles']


