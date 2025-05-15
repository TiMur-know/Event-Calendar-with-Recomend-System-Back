import pytest
import numpy as np
from unittest.mock import patch, MagicMock
from app.utils.recomendation import RecommendationModel
from app import create_app  

@pytest.fixture
def app():
    app = create_app()  
    with app.app_context(): 
        yield app

@pytest.fixture
def mock_users_events():
    mock_event1 = MagicMock(id=1)
    mock_event2 = MagicMock(id=2)
    mock_user1 = MagicMock(id=10, events=[mock_event1])
    mock_user2 = MagicMock(id=20, events=[mock_event2])
    return [mock_user1, mock_user2], [mock_event1, mock_event2]

def test_prepare_data(app, mock_users_events):
    users, events = mock_users_events
    with patch("app.utils.recomendation.UserDetails.query") as mock_user_query, \
         patch("app.utils.recomendation.Event.query") as mock_event_query:

        mock_user_query.all.return_value = users
        mock_event_query.all.return_value = events

        model = RecommendationModel()
        user_ids, event_ids, matrix = model.prepare_data()

        assert user_ids == [10, 20]
        assert event_ids == [1, 2]
        assert matrix.shape == (2, 2)
        assert matrix[0][0] == 1  
        assert matrix[1][1] == 1  
        assert matrix[0][1] == 0
        assert matrix[1][0] == 0

@patch("app.utils.recomendation.RecommendationModel.prepare_data")
@patch("app.utils.recomendation.tf.keras.Model.fit")
@patch("app.utils.recomendation.tf.keras.models.Model")
def test_train_model(mock_model_class, mock_fit, mock_prepare_data, app):
    mock_prepare_data.return_value = (
        [10, 20], [1, 2], np.array([[1, 0], [0, 1]])
    )

    fake_model = MagicMock()
    mock_model_class.return_value = fake_model
    fake_model.fit.return_value = None

    model = RecommendationModel()
    model.train()

    assert model.model is not None
    fake_model.fit.assert_called_once()

def test_recommend_returns_ids(app, mock_users_events):
    users, events = mock_users_events
    with patch("app.utils.recomendation.UserDetails.query") as mock_user_query, \
         patch("app.utils.recomendation.Event.query") as mock_event_query:

        mock_user_query.all.return_value = users
        mock_event_query.all.return_value = events

        model = RecommendationModel()
        model.model = MagicMock()
        model.model.predict.return_value = np.array([[0.8], [0.3]])

        recommendations = model.recommend(user_id=10, top_n=1)
        assert isinstance(recommendations, list)
        assert recommendations[0] == 1  

def test_recommend_raises_if_not_trained(app):
    model = RecommendationModel()
    with pytest.raises(ValueError, match="Model is not trained yet."):
        model.recommend(user_id=1)

def test_recommend_raises_if_user_not_found(app, mock_users_events):
    users, events = mock_users_events
    with patch("app.utils.recomendation.UserDetails.query") as mock_user_query, \
         patch("app.utils.recomendation.Event.query") as mock_event_query:

        mock_user_query.all.return_value = users
        mock_event_query.all.return_value = events

        model = RecommendationModel()
        model.model = MagicMock()

        with pytest.raises(ValueError, match="User ID 99 not found."):
            model.recommend(user_id=99)
