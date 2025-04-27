from rest_framework.test import APITestCase
from . import models
from users.models import User


class TestAmenities(APITestCase):

    NAME = "Amenity test"
    DESC = "Amenity des"
    URL = "/api/v1/rooms/amenities/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_all_amenities(self):

        response = self.client.get(self.URL)
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "The status code isn't 200",
        )
        self.assertIsInstance(
            data,
            list,
        )
        self.assertEqual(
            len(data),
            1,
        )
        self.assertEqual(
            data[0]["name"],
            self.NAME,
        )
        self.assertEqual(
            data[0]["description"],
            self.DESC,
        )

    def test_create_amenity(self):

        new_amenity_name = "New Amenity"
        new_amenity_desc = "New Amenity Des"

        response = self.client.post(
            self.URL,
            data={
                "name": new_amenity_name,
                "description": new_amenity_desc,
            },
        )
        data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            "Status code is not 200",
        )
        self.assertEqual(
            data["name"],
            new_amenity_name,
            f"name is not '{new_amenity_name}'",
        )
        self.assertEqual(
            data["description"],
            new_amenity_desc,
            f"name is not '{new_amenity_desc}'",
        )

        response = self.client.post(self.URL)
        data = response.json()

        self.assertEqual(response.status_code, 400, "Status Code 400 required")
        self.assertIn("name", data)


class TestAmenity(APITestCase):
    NAME = "Amenity test"
    DESC = "Amenity des"
    URL = "/api/v1/rooms/amenities/1"
    EMPTY_URL = "/api/v1/rooms/amenities/2"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.NAME,
            description=self.DESC,
        )

    def test_amenity_not_count(self):
        response = self.client.get(self.EMPTY_URL)
        self.assertEqual(response.status_code, 404, "No status code 404")

    def test_get_amenity(self):
        response = self.client.get(self.URL)
        self.assertEqual(response.status_code, 200, "No status code 200")

        data = response.json()
        self.assertEqual(data["name"], self.NAME, "name is not valid")
        self.assertEqual(data["description"], self.DESC, "description is not valid")

    # code challenge
    def test_update_amenity(self):
        updated_amenity_name = "Updated Amenity"
        updated_amenity_desc = "Updated Amenity Des"
        ## is_valid()
        # update name
        response = self.client.put(
            self.URL,
            data={
                "name": updated_amenity_name,
            },
        )
        data = response.json()
        # check status code
        self.assertEqual(
            response.status_code,
            200,
            "No status code 200",
        )
        # check if name data is updated
        self.assertEqual(data["name"], updated_amenity_name, "name is not updated")

        # update description
        response = self.client.put(
            self.URL,
            data={
                "description": updated_amenity_desc,
            },
        )
        data = response.json()
        self.assertEqual(
            data["description"], updated_amenity_desc, "description is not updated"
        )

        ## is not valid
        response = self.client.put(
            self.URL,
            data={
                "name": "",
            },
        )
        # print(response)
        self.assertEqual(response.status_code, 400, "Status code 400 required")

    def test_delete_amenity(self):
        response = self.client.delete(self.URL)
        self.assertEqual(response.status_code, 204, "No status code 204")


class TestRooms(APITestCase):

    def setUp(self):
        # * create a user
        user = User.objects.create(username="test")
        user.set_password("123")
        user.save()
        self.user = user

    def test_create_room(self):

        response = self.client.post("/api/v1/rooms/")

        self.assertEqual(
            response.status_code, 403, "Status code 403 (forbidden) required"
        )

        # no need username and password
        self.client.force_login(self.user)
        # self.client.login(
        #     username="test",
        #     password="123",
        # )

        response = self.client.post("/api/v1/rooms/")
        print(response.json())
