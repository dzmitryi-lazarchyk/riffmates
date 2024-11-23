from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.timezone import make_aware, datetime
from clubs.models import Member, Venue

def raises_an_error():
    raise ValueError()
class TestClubs(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            first_name="First", last_name="Last",
            date_of_birth=make_aware(datetime(1990, 12, 21))
        )

        self.UserModel = get_user_model()
        self.PASSWORD = "notsecure"
        self.user = self.UserModel.objects.create_user(username="testuser", password=self.PASSWORD)
        self.owner = self.UserModel.objects.create_user(username="owner", password=self.PASSWORD)

    def test_member_view(self):
        url = f'/clubs/member/{self.member.id}/'
        response = self.client.get(url)
        self.assertEqual(302, response.status_code) # Redirect to login page

        # Login user
        self.client.force_login(self.user)

        # Access view with logged in
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.member.id,
                         response.context['member'].id)
        self.assertIn(self.member.first_name,
                      str(response.content))

    def test_member_404(self):
        url = f'/clubs/member/11/'
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)  # Redirect to login page

        # Login user
        self.client.force_login(self.user)

        # Access view with logged in
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)

    def test_raises_an_error(self):
        with self.assertRaises(ValueError):
            raises_an_error()

    def test_add_edit_venue(self):
        self.client.login(username="owner",
                          password=self.PASSWORD)
        # Verify the page fetch works
        url = "/clubs/edit_venue/0/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

        # Create new venue
        data = {
            'name': 'TEstVenue',
            'description': 'Description'
        }
        response = self.client.post(url, data)
        self.assertEqual(302, response.status_code)

        # Validate the Venue was created
        venue = Venue.objects.last()
        self.assertEqual(data['name'], venue.name)
        self.assertEqual(data['description'], venue.description)
        self.assertTrue(
            self.owner.userprofile.venues_controlled.filter(
                id=venue.id).exists()
            )

        # Test editing venue
        url = f"/clubs/edit_venue/{venue.id}/"
        data['name'] = "Edited Name"
        response = self.client.post(url, data)

        self.assertEqual(302, response.status_code)
        venue = Venue.objects.first()
        self.assertEqual(data['name'], venue.name)

        # Verify that non-owner can't edit
        self.client.login(username="testuser", password=self.PASSWORD)
        response = self.client.post(url, data)
        self.assertEqual(404, response.status_code)
