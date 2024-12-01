import tempfile
from base64 import b64decode
import io

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils.timezone import make_aware, datetime
from django.core.management import call_command

from clubs.models import Member, Venue


def raises_an_error():
    raise ValueError()


class TestClubs(TestCase):
    def setUp(self):
        self.member = Member.objects.create(first_name="First", last_name="Last",
                                            date_of_birth=make_aware(datetime(1990, 12, 21)))

        self.UserModel = get_user_model()
        self.PASSWORD = "notsecure"
        self.user = self.UserModel.objects.create_user(username="testuser", password=self.PASSWORD)
        self.owner = self.UserModel.objects.create_user(username="owner", password=self.PASSWORD)
        self.user_staff = self.UserModel.objects.create_user(username="user_staff", password=self.PASSWORD,
                                                             is_staff=True)
        self.admin = self.UserModel.objects.create_superuser(username="admin", password=self.PASSWORD)

        # Base64 encoded version of a single pixel GIF image
        image = "R0lGODdhAQABAIABAP///wAAACwAAAAAAQABAAACAkQBADs="
        self.image = b64decode(image)

    def test_member_view(self):
        url = f'/clubs/member/{self.member.id}/'
        response = self.client.get(url)
        self.assertEqual(302, response.status_code)  # Redirect to login page

        # Login user
        self.client.force_login(self.user)

        # Access view with logged in
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(self.member.id, response.context['member'].id)
        self.assertIn(self.member.first_name, str(response.content))

    def test_member_404(self):
        url = '/clubs/member/11/'
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
        self.client.login(username="owner", password=self.PASSWORD)
        # Verify the page fetch works
        url = "/clubs/edit_venue/0/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

        # Create new venue
        data = {'name': 'TEstVenue', 'description': 'Description'}
        response = self.client.post(url, data)
        self.assertEqual(302, response.status_code)

        # Validate the Venue was created
        venue = Venue.objects.last()
        self.assertEqual(data['name'], venue.name)
        self.assertEqual(data['description'], venue.description)
        self.assertTrue(self.owner.userprofile.venues_controlled.filter(id=venue.id).exists())

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

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_add_edit_venue_picture(self):
        file = SimpleUploadedFile('test.gif', self.image)
        data = {'name': "TestName", "description": "Description", "picture": file, }
        self.client.login(username="owner", password=self.PASSWORD)
        url = "/clubs/edit_venue/0/"
        response = self.client.post(url, data)

        self.assertEqual(302, response.status_code)
        venue = Venue.objects.first()
        self.assertIsNotNone(venue.picture)

    def test_add_edit_member(self):
        file = SimpleUploadedFile('test.gif', self.image)
        data = {
            'first_name': "First",
            'last_name': "Last",
            'date_of_birth': make_aware(datetime(1994, 11, 21)),
            'description': "Description",
            'picture': file
        }
        url = "/clubs/add_edit_member/0/"

        response = self.client.get(url)
        self.assertEqual(302, response.status_code)

        # verify fetching page works
        self.client.login(username="owner", password=self.PASSWORD)
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

        # Create member
        response = self.client.post(url, data)
        self.assertEqual(302, response.status_code)

        # Validate member was created
        member = Member.objects.last()
        self.owner = self.UserModel.objects.get(id=self.owner.id)
        self.assertEqual(data['first_name'], member.first_name)
        self.assertEqual(data['last_name'], member.last_name)
        self.assertEqual(data['description'], member.description)
        self.assertEqual(data['date_of_birth'], member.date_of_birth)
        self.assertIsNotNone(member.picture)
        self.assertTrue(
            self.owner.userprofile.member_profile.id == member.id
        )

        # Edit member as user
        data['last_name'] = "Last_new"
        file = SimpleUploadedFile('test1.gif', self.image)
        data['picture'] = file
        url = f"/clubs/add_edit_member/{member.id}/"
        response = self.client.post(url, data)

        self.assertEqual(302, response.status_code)
        member = Member.objects.last()
        self.assertEqual(data['last_name'], member.last_name)

        # Verify that admins can edit
        self.client.login(username="admin",
                          password=self.PASSWORD)
        url = f"/clubs/add_edit_member/{member.id}/"
        file = SimpleUploadedFile('test2.gif', self.image)
        data['picture'] = file
        data['first_name'] = "Edited by admin Name"
        response = self.client.post(url, data)
        self.assertEqual(302, response.status_code)
        member = Member.objects.last()
        self.assertEqual(data['first_name'], member.first_name)

        # Verify that staff can edit
        self.client.login(username="user_staff",
                          password=self.PASSWORD)
        url = f"/clubs/add_edit_member/{member.id}/"
        file = SimpleUploadedFile('test3.gif', self.image)
        data['picture'] = file
        data['description'] = "Staff\'s description"
        response = self.client.post(url, data)
        self.assertEqual(302, response.status_code)
        member = Member.objects.last()
        self.assertEqual(data['description'], member.description)

        # Verify that non-user can't edit
        self.client.login(username="testuser", password=self.PASSWORD)
        url = f"/clubs/add_edit_member/{member.id}/"
        file = SimpleUploadedFile('test4.gif', self.image)
        data['picture'] = file
        data['first_name'] = "Non-user name"
        response = self.client.post(url, data)
        self.assertEqual(404, response.status_code)

    def test_members(self):
        for i in range(1, 10):
            Member.objects.create(
                first_name=f"First{i}",
                last_name=f"Last{i}",
                date_of_birth=datetime(1995, 1, i)
            )

        url = "/clubs/members/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.context['members']))
        self.assertTrue(response.context['page'].has_next())
        self.assertFalse(response.context['page'].has_previous())

        url = "/clubs/members/?per_page=10"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(10, len(response.context['members']))
        self.assertFalse(response.context['page'].has_next())
        self.assertFalse(response.context['page'].has_previous())

        url = "/clubs/members/?per_page=5&page=2"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.context['members']))
        self.assertFalse(response.context['page'].has_next())
        self.assertTrue(response.context['page'].has_previous())

        url = "/clubs/members/?per_page=-1"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(5, len(response.context['members']))
        self.assertTrue(response.context['page'].has_next())
        self.assertFalse(response.context['page'].has_previous())

class TestMembersCommand(TestCase):
    def setUp(self):
        self.member = Member.objects.create(
            first_name="First",
            last_name="Last",
            date_of_birth=datetime(1990, 1, 1)
        )

    def test_command(self):
        output = io.StringIO()
        call_command("members", stdout=output)
        self.assertIn("First", output.getvalue())

        for i in range(1, 10):
            Member.objects.create(
                first_name=f"First{i}",
                last_name=f"Last{i}",
                date_of_birth=datetime(1995, 1, i)
            )

        output = io.StringIO()
        call_command("members", stdout=output, date_of_birth="1995-01-5")
        num_of_members = len(output.getvalue().strip().split('\n'))
        self.assertEqual(5, num_of_members)


