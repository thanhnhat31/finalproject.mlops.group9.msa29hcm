"""
Unit tests for Movie Rating Prediction API.

TODO: Complete the test cases below.

Run tests with:
    pytest tests/ -v
    pytest tests/ -v --cov=app --cov-report=html
"""

import pytest
from fastapi.testclient import TestClient

import app.main as main_module
from app.main import app

# Create test client
client = TestClient(app)
VALID_PAYLOAD = {"user_id": "user_196", "movie_id": "movie_242"}


class FakeModel:
    """Simple fake model to keep API tests deterministic."""

    def is_loaded(self):
        return True

    def predict_with_latency(self, user_id: str, movie_id: str):
        return 4.2, 12.34

    def get_info(self):
        return {
            "version": "test-version",
            "type": "SVD",
            "is_loaded": True,
            "path": "models/svd_model.pkl",
        }


@pytest.fixture(autouse=True)
def ensure_loaded_model():
    """Inject fake model for all tests to avoid external model dependency."""
    original = main_module.model
    main_module.model = FakeModel()
    yield
    main_module.model = original


# =============================================================================
# Health Check Tests (PROVIDED)
# =============================================================================
class TestHealthEndpoint:
    """Tests for the /health endpoint."""
    
    def test_health_check_returns_200(self):
        """Test that health endpoint returns 200 status code."""
        response = client.get("/health")
        assert response.status_code == 200
    
    def test_health_check_response_format(self):
        """Test that health response has correct format."""
        response = client.get("/health")
        data = response.json()
        
        assert "status" in data
        assert "model_loaded" in data
        assert isinstance(data["status"], str)
        assert isinstance(data["model_loaded"], bool)


# =============================================================================
# Root Endpoint Tests (PROVIDED)
# =============================================================================
class TestRootEndpoint:
    """Tests for the / endpoint."""
    
    def test_root_returns_200(self):
        """Test that root endpoint returns 200 status code."""
        response = client.get("/")
        assert response.status_code == 200
    
    def test_root_contains_api_info(self):
        """Test that root response contains API information."""
        response = client.get("/")
        data = response.json()
        
        assert "name" in data
        assert "version" in data
        assert "docs" in data


# =============================================================================
# TODO 1: Prediction Endpoint Tests
# =============================================================================
class TestPredictEndpoint:
    """Tests for the /predict endpoint."""
    
    # -------------------------------------------------------------------------
    # TODO: Implement test_predict_valid_input
    # -------------------------------------------------------------------------
    # Requirements:
    # - Send POST request to /predict with valid user_id and movie_id
    # - Assert status code is 200
    # - Assert response contains "predicted_rating"
    # - Assert predicted_rating is between 1.0 and 5.0
    
    def test_predict_valid_input(self):
        """Test prediction with valid input."""
        # TODO: Implement this test
        #
        # response = client.post(
        #     "/predict",
        #     json={"user_id": "196", "movie_id": "242"}
        # )
        # assert response.status_code == 200
        # data = response.json()
        # assert "predicted_rating" in data
        # assert 1.0 <= data["predicted_rating"] <= 5.0
        response = client.post(
            "/predict",
            json=VALID_PAYLOAD
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert "predicted_rating" in data
        assert 1.0 <= data["predicted_rating"] <= 5.0
    
    # -------------------------------------------------------------------------
    # TODO: Implement test_predict_response_format
    # -------------------------------------------------------------------------
    # Requirements:
    # - Assert response contains all required fields:
    #   user_id, movie_id, predicted_rating, model_version
    
    def test_predict_response_format(self):
        """Test that prediction response has correct format."""
        # TODO: Implement this test
        #
        # response = client.post(
        #     "/predict",
        #     json={"user_id": "196", "movie_id": "242"}
        # )
        # data = response.json()
        # 
        # assert "user_id" in data
        # assert "movie_id" in data
        # assert "predicted_rating" in data
        # assert "model_version" in data
        response = client.post(
            "/predict",
            json=VALID_PAYLOAD
        )
        assert response.status_code == 200, response.text
        data = response.json()

        assert "user_id" in data
        assert "movie_id" in data
        assert "predicted_rating" in data
        assert "model_version" in data
    
    # -------------------------------------------------------------------------
    # TODO: Implement test_predict_missing_user_id
    # -------------------------------------------------------------------------
    # Requirements:
    # - Send request without user_id
    # - Assert status code is 422 (Validation Error)
    
    def test_predict_missing_user_id(self):
        """Test prediction with missing user_id."""
        # TODO: Implement this test
        #
        # response = client.post(
        #     "/predict",
        #     json={"movie_id": "242"}  # Missing user_id
        # )
        # assert response.status_code == 422
        response = client.post(
            "/predict",
            json={"movie_id": "242"}
        )
        assert response.status_code == 422
    
    # -------------------------------------------------------------------------
    # TODO: Implement test_predict_missing_movie_id
    # -------------------------------------------------------------------------
    # Requirements:
    # - Send request without movie_id
    # - Assert status code is 422 (Validation Error)
    
    def test_predict_missing_movie_id(self):
        """Test prediction with missing movie_id."""
        # TODO: Implement this test
        response = client.post(
            "/predict",
            json={"user_id": "196"}
        )
        assert response.status_code == 422
    
    # -------------------------------------------------------------------------
    # TODO: Implement test_predict_empty_body
    # -------------------------------------------------------------------------
    # Requirements:
    # - Send request with empty JSON body
    # - Assert status code is 422 (Validation Error)
    
    def test_predict_empty_body(self):
        """Test prediction with empty request body."""
        # TODO: Implement this test
        #
        # response = client.post("/predict", json={})
        # assert response.status_code == 422
        response = client.post("/predict", json={})
        assert response.status_code == 422


# =============================================================================
# TODO 2: Edge Case Tests (BONUS)
# =============================================================================
class TestEdgeCases:
    """Edge case tests."""
    
    def test_predict_unknown_user(self):
        """Test prediction with unknown user ID."""
        # The model should still return a prediction (with default rating)
        # or handle gracefully
        # TODO: Implement this test
        response = client.post(
            "/predict",
            json={"user_id": "unknown_user_999999", "movie_id": "movie_242"}
        )
        assert response.status_code == 200, response.text
        assert 1.0 <= response.json()["predicted_rating"] <= 5.0
    
    def test_predict_unknown_movie(self):
        """Test prediction with unknown movie ID."""
        # TODO: Implement this test
        response = client.post(
            "/predict",
            json={"user_id": "user_196", "movie_id": "unknown_movie_999999"}
        )
        assert response.status_code == 200, response.text
        assert 1.0 <= response.json()["predicted_rating"] <= 5.0
    
    def test_predict_special_characters_in_id(self):
        """Test prediction with special characters in IDs."""
        # TODO: Implement this test
        response = client.post(
            "/predict",
            json={"user_id": " user-196 ", "movie_id": "movie_242"}
        )
        assert response.status_code == 200


# =============================================================================
# TODO 3: Model Info Endpoint Tests
# =============================================================================
class TestModelInfoEndpoint:
    """Tests for the /model/info endpoint."""
    
    def test_model_info_returns_200(self):
        """Test that model info endpoint returns 200."""
        response = client.get("/model/info")
        assert response.status_code == 200
    
    def test_model_info_contains_version(self):
        """Test that model info contains version."""
        # TODO: Implement this test
        response = client.get("/model/info")
        data = response.json()
        assert "version" in data


# =============================================================================
# Batch Prediction Tests (BONUS)
# =============================================================================
class TestBatchPredictEndpoint:
    """Tests for the /predict/batch endpoint (BONUS)."""
    
    def test_batch_predict_multiple_items(self):
        """Test batch prediction with multiple items."""
        # TODO: Implement this test (BONUS)
        response = client.post(
            "/predict/batch",
            json={
                "predictions": [
                    {"user_id": "user_196", "movie_id": "movie_242"},
                    {"user_id": "user_186", "movie_id": "movie_302"},
                ]
            }
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data["total_count"] == 2
        assert len(data["predictions"]) == 2
    
    def test_batch_predict_empty_list(self):
        """Test batch prediction with empty list."""
        # TODO: Implement this test (BONUS)
        response = client.post("/predict/batch", json={"predictions": []})
        assert response.status_code == 422


# =============================================================================
# Run tests
# =============================================================================
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
