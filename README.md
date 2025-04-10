# ✨ DevPilot
The development pilot guiding you from requirements to deployment.
_Pilot your entire software lifecycle from idea to release_

## Setup Instruction
- Clone the repo
- Create a virtual environment
- Install the requirements
- Install Docker Desktop
- Pull the Redis image using `docker pull redis`
- Run the Redis container using `docker run -p 6379:6379 redis` (Docker is used to store the state of the graph in Redis)
- Run the streamlit app using `streamlit run app.py`

## Workflow Graph
![](workflow_graph.png)

### TODO
- Fast API Integration
- Deploy as a docker on AWS
