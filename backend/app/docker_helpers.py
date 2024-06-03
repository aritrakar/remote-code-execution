import docker
import time
import os
import logging
import concurrent.futures

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def build_image_if_not_exists(client, image_name: str, path: str="../"):
    """
    Build a Docker image if it does not already exist.

    This function checks if a Docker image with the specified name already exists.
    If the image does not exist, it builds the image using the provided path.

    Args:
        client (docker.DockerClient): The Docker client instance.
        image_name (str): The name of the Docker image to check or build.
        path (str): The path to the Dockerfile and context for building the image. Default is "../".

    Returns:
        None
    """
    try:
        client.images.get(image_name)
        logging.info(f"Image '{image_name}' already exists. Skipping build.")
    except docker.errors.ImageNotFound:
        logging.info(f"Building image '{image_name}'...")
        client.images.build(path=path, dockerfile="Dockerfile.executor", tag=image_name, rm=True)
        logging.info("Image built")

def clean_existing_container(client, container_name: str):
    """
    Remove an existing Docker container if it exists.

    This function checks if a Docker container with the specified name already exists.
    If the container exists, it stops and removes the container.

    Args:
        client (docker.DockerClient): The Docker client instance.
        container_name (str): The name of the Docker container to check and remove.

    Returns:
        None
    """
    try:
        existing_container = client.containers.get(container_name)
        existing_container.stop()
        existing_container.remove()
        logging.info(f"Removed existing container '{container_name}'")
    except docker.errors.NotFound:
        logging.info(f"No existing container '{container_name}' found. Proceeding.")

def cleanup_container(container):
    """
    Stop and remove a Docker container.

    This function stops and removes the specified Docker container.

    Args:
        container (docker.models.containers.Container): The Docker container instance to stop and remove.

    Returns:
        None
    """
    container.stop()
    container.remove()
    logging.info("Container stopped and removed")

def execute_code_in_container(client, image_name: str, container_name: str, code: str):
    """
    Execute code inside a Docker container and return the output, execution time, and memory usage.

    This function runs a specified code string inside a Docker container, captures the output,
    measures the execution time, and calculates the memory usage. It also handles container cleanup.

    Args:
        client (docker.DockerClient): The Docker client instance.
        image_name (str): The name of the Docker image to use.
        container_name (str): The name of the Docker container to create.
        code (str): The code to execute inside the Docker container.

    Returns:
        tuple: A tuple containing the output (str), time taken (float), memory usage (int), and exit code (int).
    """
    container = client.containers.run(image=image_name, name=container_name, detach=True, tty=True, command="/bin/sh")
    logging.info(f"Container created: {container.id}")
    # time.sleep(2)  # Give the container some time to initialize

    # Escape double quotes in the code string to ensure it works correctly in the command
    code_escaped = code.replace('"', '\\"')
    
    # Measure the start time
    start_time = time.time()

    exec_result = container.exec_run(f'python -c "{code_escaped}"', stdout=True) # stderr cannot be True because detach=True
    output = exec_result.output.decode()
    
    # Measure the end time
    end_time = time.time()

    # Calculate the time taken
    time_taken = end_time - start_time

    # Get memory usage
    stats = container.stats(stream=False)
    memory_usage = stats['memory_stats']['usage']

    # Check for errors
    exit_code = exec_result.exit_code

    logging.info(f"Code executed. Time taken: {time_taken:.2f}s, Memory usage: {memory_usage} bytes. Exit code: {exit_code}")
    logging.info(f"Output: {output}")

    # Use a background thread to handle container cleanup
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    executor.submit(cleanup_container, container)

    return output, time_taken, memory_usage, exit_code

def setup_docker_environment():
    """
    Set up the Docker environment by initializing the Docker client, building the image if it doesn't exist,
    and cleaning any existing container with the specified name.

    Returns:
        tuple: A tuple containing the Docker client (docker.DockerClient), image name (str), and container name (str).
    """
    client = docker.from_env()
    image_name = "code_executor"
    container_name = "test_container"
    
    logging.info("Initialized client")
    build_image_if_not_exists(client, image_name, path="../code_executor")
    clean_existing_container(client, container_name)
    
    return client, image_name, container_name
