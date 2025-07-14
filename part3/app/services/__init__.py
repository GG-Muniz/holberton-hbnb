from app.services.facade import HBnBFacade

# Create a single shared facade instance
# The facade will automatically use the appropriate repository based on REPOSITORY_TYPE environment variable
facade = HBnBFacade()
