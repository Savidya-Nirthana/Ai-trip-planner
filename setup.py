from setuptools import setup, find_packages
from typing import List

def get_requirements()->List[str]:
    """
    This function will return the list of requirements
    """

    reqiurements_list: List[str] = []

    try:
        with open("requirements.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                requirement = line.strip()

                if requirement and requirement != "-e .":
                    reqiurements_list.append(requirement)
    except FileNotFoundError:
        print("Requirement.txt file not found")

    return reqiurements_list


print(get_requirements())
    

setup(
    name="ai_trip_planner",
    version="0.0.1",
    description="AI Trip Planner",
    author="Savidya Perera",
    author_email="snirthana5@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
    