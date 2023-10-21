# CMSC495
This application is written in Python using the Streamlit framework. This tool is mostly a pet project, but the intent is for it to encompass multiple functions primarily used in the security industry.

# Docker
- From the root directory, run:
```
docker-compose -f Docker/docker-compose.yml up --build
```

# Cleanup
After making changes, you'll need to kill the container and rerun it in order for the updates to take. After you're done, I would suggest pruning in order to clear up space made by this process:
```
docker system prune -a
```
