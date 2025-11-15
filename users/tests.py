from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date
from .models import UserProfile

class UserProfileModelTest(TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            first_name='John',
            last_name='Doe'
        )
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            bio="I love cooking Italian food",
            location="New York",
            birth_date=date(1990, 5, 15),
            favorite_cuisine="Italian"
        )
    
    def test_user_profile_creation(self):
        """Test user profile creation with valid data"""
        self.assertEqual(self.user_profile.user, self.user)
        self.assertEqual(self.user_profile.bio, "I love cooking Italian food")
        self.assertEqual(self.user_profile.location, "New York")
        self.assertEqual(self.user_profile.birth_date, date(1990, 5, 15))
        self.assertEqual(self.user_profile.favorite_cuisine, "Italian")
        self.assertTrue(isinstance(self.user_profile, UserProfile))
    
    def test_user_profile_str_representation(self):
        """Test string representation of user profile"""
        expected_str = "testuser's Profile"
        self.assertEqual(str(self.user_profile), expected_str)
    
    def test_user_profile_with_minimal_data(self):
        """Test user profile creation with minimal required data"""
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpassword'
        )
        profile2 = UserProfile.objects.create(user=user2)
        
        self.assertEqual(profile2.user, user2)
        self.assertEqual(profile2.bio, "")
        self.assertEqual(profile2.location, "")
        self.assertIsNone(profile2.birth_date)
        self.assertEqual(profile2.favorite_cuisine, "")
    
    def test_user_profile_one_to_one_relationship(self):
        """Test one-to-one relationship with User"""
        # Each user should have only one profile
        profile_count = UserProfile.objects.filter(user=self.user).count()
        self.assertEqual(profile_count, 1)
        
        # Test accessing profile from user (reverse relationship)
        self.assertEqual(self.user.userprofile, self.user_profile)
    
    def test_user_profile_optional_fields(self):
        """Test that optional fields can be blank"""
        user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='testpassword'
        )
        profile3 = UserProfile.objects.create(
            user=user3,
            bio="",  # Empty bio
            location="",  # Empty location
            favorite_cuisine=""  # Empty favorite cuisine
        )
        
        self.assertEqual(profile3.bio, "")
        self.assertEqual(profile3.location, "")
        self.assertEqual(profile3.favorite_cuisine, "")
        self.assertIsNone(profile3.birth_date)
    
    def test_user_deletion_cascades_to_profile(self):
        """Test that deleting a user also deletes the profile"""
        user_id = self.user.id
        profile_id = self.user_profile.id
        
        # Delete the user
        self.user.delete()
        
        # Check that profile is also deleted
        with self.assertRaises(UserProfile.DoesNotExist):
            UserProfile.objects.get(id=profile_id)
        
        # Check that user is deleted
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=user_id)
