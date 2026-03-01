import pytest


class TestSignupForActivity:
    def test_signup_success(self, client, reset_activities):
        """Test successful signup for an activity"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity_name = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "Signed up" in result["message"]
        assert email in result["message"]
    
    def test_signup_duplicate_prevention(self, client, reset_activities):
        """Test that duplicate signups are prevented"""
        # Arrange
        email = "michael@mergington.edu"  # Already signed up for Chess Club
        activity_name = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "already signed up" in result["detail"]
    
    def test_signup_activity_not_found(self, client, reset_activities):
        """Test signup fails when activity doesn't exist"""
        # Arrange
        email = "student@mergington.edu"
        activity_name = "NonexistentActivity"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "Activity not found" in result["detail"]
    
    def test_signup_updates_participant_list(self, client, reset_activities):
        """Test that signup actually adds participant to the activity"""
        # Arrange
        email = "testnewstudent123@mergington.edu"
        activity_name = "Art Club"
        
        # Act
        client.post(f"/activities/{activity_name}/signup?email={email}")
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert email in activities[activity_name]["participants"]
    
    def test_signup_new_student_in_different_activity(self, client, reset_activities):
        """Test that a new student can sign up for a different activity"""
        # Arrange
        email = "brandnewstudent@mergington.edu"
        activity_name = "Drama Club"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]


class TestUnregisterFromActivity:
    def test_unregister_success(self, client, reset_activities):
        """Test successful unregistration from an activity"""
        # Arrange
        email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 200
        result = response.json()
        assert "Unregistered" in result["message"]
    
    def test_unregister_not_registered(self, client, reset_activities):
        """Test unregister fails when student isn't registered"""
        # Arrange
        email = "notregistered@mergington.edu"
        activity_name = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 400
        result = response.json()
        assert "not signed up" in result["detail"]
    
    def test_unregister_activity_not_found(self, client, reset_activities):
        """Test unregister fails when activity doesn't exist"""
        # Arrange
        email = "student@mergington.edu"
        activity_name = "NonexistentActivity"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/unregister?email={email}"
        )
        
        # Assert
        assert response.status_code == 404
        result = response.json()
        assert "Activity not found" in result["detail"]
    
    def test_unregister_removes_participant(self, client, reset_activities):
        """Test that unregister actually removes participant from activity"""
        # Arrange
        email = "michael@mergington.edu"
        activity_name = "Chess Club"
        
        # Act
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        activities_response = client.get("/activities")
        activities = activities_response.json()
        
        # Assert
        assert email not in activities[activity_name]["participants"]
    
    def test_unregister_then_signup_again(self, client, reset_activities):
        """Test that a student can re-signup after unregistering"""
        # Arrange
        email = "james@mergington.edu"  # Already in Basketball Team
        activity_name = "Basketball Team"
        
        # Act
        client.delete(f"/activities/{activity_name}/unregister?email={email}")
        signup_response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        
        # Assert
        assert signup_response.status_code == 200
        activities_response = client.get("/activities")
        activities = activities_response.json()
        assert email in activities[activity_name]["participants"]
