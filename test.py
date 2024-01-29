from AuthApiClass import PermissionsRequester

requester = PermissionsRequester()

try:
    permissions = requester.get_permissions('sfi2201')
    print(permissions)
except Exception as e:
    print("fehler")
    print(f"Error: {e}")