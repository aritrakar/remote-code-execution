from docker_helpers import setup_docker_environment, execute_code_in_container

# Test the setup_docker_environment function
def test_setup_docker_environment():
    client, image_name, container_name = setup_docker_environment()
    assert client is not None
    assert image_name == "code_executor"
    assert container_name == "test_container"

# Test the execute_code_in_container function
def test_execute_code_in_container():
    client, image_name, container_name = setup_docker_environment()
    code = "print('Hello, Docker!')"
    output = execute_code_in_container(client, image_name, container_name, code)
    assert output == "Hello, Docker!\n"

# Test the execute_code_in_container function with an error
def test_execute_code_in_container_error():
    client, image_name, container_name = setup_docker_environment()
    code = "print('Hello, Docker!')\nundefined_variable"
    output = execute_code_in_container(client, image_name, container_name, code)
    assert "NameError" in output
    assert "undefined_variable" in output
    assert "Hello, Docker!" in output
    assert "Traceback" in output
    assert "Error" in output

test_setup_docker_environment()
test_execute_code_in_container()
test_execute_code_in_container_error()
