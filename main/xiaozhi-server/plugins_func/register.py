from config.logger import setup_logging
from enum import Enum

TAG = __name__

logger = setup_logging()


class ToolType(Enum):
    NONE = (1, "After calling the tool, do no other operations")
    WAIT = (2, "Call the tool and wait for the function to return")
    CHANGE_SYS_PROMPT = (3, "Modify the system prompt words and switch roles or responsibilities")
    SYSTEM_CTL = (
        4,
        "System control, which affects the normal dialogue process, such as exiting, playing music, etc., needs to pass the conn parameter",
    )
    IOT_CTL = (5, "IOT device control, you need to pass the conn parameter")
    MCP_CLIENT = (6, "MCP client")

    def __init__(self, code, message):
        self.code = code
        self.message = message


class Action(Enum):
    ERROR = (-1, "mistake")
    NOTFOUND = (0, "function not found")
    NONE = (1, "Do nothing")
    RESPONSE = (2, "Reply directly")
    REQLLM = (3, "After calling the function, request llm to generate a reply")

    def __init__(self, code, message):
        self.code = code
        self.message = message


class ActionResponse:
    def __init__(self, action: Action, result=None, response=None):
        self.action = action  # action type
        self.result = result  # result of action
        self.response = response  # Direct reply content


class FunctionItem:
    def __init__(self, name, description, func, type):
        self.name = name
        self.description = description
        self.func = func
        self.type = type


class DeviceTypeRegistry:
    """Device type registry, used to manage IOT device types and their functions"""

    def __init__(self):
        self.type_functions = {}  # type_signature -> {func_name: FunctionItem}

    def generate_device_type_id(self, descriptor):
        """Generate type ID from device capability description"""
        properties = sorted(descriptor["properties"].keys())
        methods = sorted(descriptor["methods"].keys())
        # Use a combination of properties and methods as a unique identifier for a device type
        type_signature = (
            f"{descriptor['name']}:{','.join(properties)}:{','.join(methods)}"
        )
        return type_signature

    def get_device_functions(self, type_id):
        """Get all functions corresponding to the device type"""
        return self.type_functions.get(type_id, {})

    def register_device_type(self, type_id, functions):
        """Register device types and their functions"""
        if type_id not in self.type_functions:
            self.type_functions[type_id] = functions


# Initialization function registration dictionary
all_function_registry = {}


def register_function(name, desc, type=None):
    """Decorator for registering functions into function registration dictionary"""

    def decorator(func):
        all_function_registry[name] = FunctionItem(name, desc, func, type)
        logger.bind(tag=TAG).debug(f"Function '{name}' has been loaded and can be registered for use")
        return func

    return decorator


def register_device_function(name, desc, type=None):
    """Decorator that registers device-level functions into the function registration dictionary"""

    def decorator(func):
        logger.bind(tag=TAG).debug(f"Device function '{name}' has been loaded")
        return func

    return decorator


class FunctionRegistry:
    def __init__(self):
        self.function_registry = {}
        self.logger = setup_logging()

    def register_function(self, name, func_item=None):
        # If func_item is provided, register directly
        if func_item:
            self.function_registry[name] = func_item
            self.logger.bind(tag=TAG).debug(f"Function '{name}' is directly registered successfully")
            return func_item

        # Otherwise search from all_function_registry
        func = all_function_registry.get(name)
        if not func:
            self.logger.bind(tag=TAG).error(f"Function '{name}' not found")
            return None
        self.function_registry[name] = func
        self.logger.bind(tag=TAG).debug(f"Function '{name}' registered successfully")
        return func

    def unregister_function(self, name):
        # Unregister function to check whether it exists
        if name not in self.function_registry:
            self.logger.bind(tag=TAG).error(f"Function '{name}' not found")
            return False
        self.function_registry.pop(name, None)
        self.logger.bind(tag=TAG).info(f"Function '{name}' logged out successfully")
        return True

    def get_function(self, name):
        return self.function_registry.get(name)

    def get_all_functions(self):
        return self.function_registry

    def get_all_function_desc(self):
        return [func.description for _, func in self.function_registry.items()]
