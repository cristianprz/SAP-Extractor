import os

def validate_material(material):
    if not isinstance(material, str) or not material.strip():
        raise ValueError("Material must be a non-empty string.")
    return True

def validate_quantity(quantity):
    if not isinstance(quantity, (int, float)) or quantity < 0:
        raise ValueError("Quantity must be a non-negative number.")
    return True

def validate_unit(unit):
    if not isinstance(unit, str) or not unit.strip():
        raise ValueError("Unit must be a non-empty string.")
    return True

def validate_bom_data(data):
    if not isinstance(data, tuple) or len(data) != 9:
        raise ValueError("BOM data must be a tuple with 9 elements.")
    validate_material(data[1])  # Material
    validate_quantity(data[4])   # Quantity_Base
    validate_material(data[5])   # Item
    validate_material(data[6])   # Component
    validate_quantity(data[7])    # Quantity
    validate_unit(data[8])        # Unit_Component
    return True

def validate_environment():
    """Validate SAP environment setup"""
    try:
        if "SAPNWRFC_HOME" not in os.environ:
            raise EnvironmentError("SAPNWRFC_HOME environment variable not set")

        sapnwrfc_home = os.environ["SAPNWRFC_HOME"]
        if not os.path.isdir(sapnwrfc_home):
            raise EnvironmentError(f"SAPNWRFC_HOME directory does not exist: {sapnwrfc_home}")

        lib_dir = os.path.join(sapnwrfc_home, "lib")
        if not os.path.isdir(lib_dir):
            raise EnvironmentError(f"lib directory not found in SAPNWRFC_HOME: {lib_dir}")

        required_dlls = ["icuuc57.dll", "icudt57.dll", "icuin57.dll"]
        for dll in required_dlls:
            if not os.path.isfile(os.path.join(lib_dir, dll)):
                raise EnvironmentError(f"Required DLL not found: {dll}")

        return True

    except Exception as e:
        print(f"Environment validation failed: {e}")
        return False