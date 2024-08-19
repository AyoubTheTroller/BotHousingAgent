from test.container.test_services_container import ServicesTestContainer
from pytest_asyncio import fixture
import pytest
from app.service.mongodb.dao.search_params.search_params_dao import SearchParamsDAO
from app.scraping.model.search_params import SearchParams
from app.service.mongodb.dao_controller_service import DaoControllerService

@fixture
def services_test_container(event_loop):
    container = ServicesTestContainer()
    container.wire(modules=[__name__])
    container.core.init_resources()
    yield container
    container.unwire()

@pytest.mark.asyncio
class TestDAOs:

    async def test_add_and_get_search_params(self,services_test_container):
        
        dao_controller_service: DaoControllerService = services_test_container.services.dao_controller_service()
        
        # Get the SearchParamsDAO from DaoControllerService
        search_params_dao: SearchParamsDAO = dao_controller_service.get_dao('scraping', 'search_params')

        # Define a set of search parameters
        search_params = SearchParams(
            location="Trento",
            search_type="room_for_rent",
            max_price=250,
            min_rooms=2
        )

        # Add the search parameters to the database
        hash_id = await search_params_dao.add_search_params(search_params)

        # Retrieve the search parameters by hash ID
        retrieved_search_params = await search_params_dao.get_by_hash_id(hash_id)

        # Assertions
        assert retrieved_search_params is not None
        assert retrieved_search_params.location == search_params.location
        assert retrieved_search_params.search_type == search_params.search_type
        assert retrieved_search_params.min_price == search_params.min_price

    async def test_adding_duplicate_search_params(self,services_test_container):
        dao_controller_service: DaoControllerService = services_test_container.services.dao_controller_service()
        
        # Get the SearchParamsDAO from DaoControllerService
        search_params_dao: SearchParamsDAO = dao_controller_service.get_dao('scraping', 'search_params')

        # Define a set of search parameters
        search_params = SearchParams(
            location="Trento",
            search_type="home_for_sale",
            min_price=500000,
            max_price=1000000,
            min_rooms=3,
            max_rooms=5,
            bathrooms=2,
            furnished=False
        )

        # Add the search parameters to the database
        first_hash_id = await search_params_dao.add_search_params(search_params)

        # Add the same search parameters again to check for duplicates
        second_hash_id = await search_params_dao.add_search_params(search_params)

        # Assertions to ensure both IDs are the same, meaning no duplicate entry
        assert first_hash_id == second_hash_id

        # Check that only one document exists
        document_count = await search_params_dao.count_documents({"hash_id": first_hash_id})
        assert document_count == 1
