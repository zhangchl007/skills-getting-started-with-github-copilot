import pytest


class TestGetActivities:
    def test_get_all_activities_success(self, client, reset_activities):
        """Test successful retrieval of all activities"""
        # Arrange
        expected_activity_names = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Soccer Team",
            "Basketball Team",
            "Art Club",
            "Drama Club",
            "Math Olympiad",
            "Debate Club"
        ]
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert len(activities) == 9
        assert all(name in activities for name in expected_activity_names)
    
    def test_activities_have_required_fields(self, client, reset_activities):
        """Test that each activity has required fields"""
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_data in activities.items():
            assert all(field in activity_data for field in required_fields)
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)
    
    def test_participants_list_format(self, client, reset_activities):
        """Test that participants are stored as a list of strings"""
        # Arrange
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_data in activities.values():
            assert isinstance(activity_data["participants"], list)
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)
    
    def test_activity_has_initial_participants(self, client, reset_activities):
        """Test that activities have initial participants loaded"""
        # Arrange
        
        # Act
        response = client.get("/activities")
        activities = response.json()
        
        # Assert
        assert response.status_code == 200
        chess_club = activities["Chess Club"]
        assert len(chess_club["participants"]) >= 1
        assert "michael@mergington.edu" in chess_club["participants"]
