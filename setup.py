from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
        '''
        this function will return the list of requirements
        '''
        requirement_lst=[]
        try:
            with open('requirement.txt','r') as file:
                lines=file.readlines() #read lines from file
                for line in lines:
                    requirement=line.strip()
                    if requirement and requirement!= '-e .':
                        requirement_lst.append(requirement) # ignore -e.
        except FileNotFoundError:
            print("requiremt file not found")
        return requirement_lst
print(get_requirements())

setup(
    name='mlproject',
    version='0.0.1',
    author='manjuunath',
    author_email='manju.r.k9446@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()

    )   