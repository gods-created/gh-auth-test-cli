from unittest import IsolatedAsyncioTestCase
from services import api_handler
from faker import Faker

class ApiHandlerTests(IsolatedAsyncioTestCase):
    async def asyncSetUp(self) -> None:
        self.faker = Faker()
    
    async def test_service(self):
        url = self.faker.url()
        response = await api_handler(url=url)
        self.assertFalse(response)
    
    async def asyncTearDown(self) -> None:
        return super().tearDown()