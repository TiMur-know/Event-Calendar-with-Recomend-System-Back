import tensorflow as tf
import numpy as np
from app.models.user_details import UserDetails
from app.models.event import Event
from app.database import db

class RecommendationModel:
    def __init__(self):
        self.model = None

    def prepare_data(self):
        """
        Prepare training data from UserDetails and Events.
        """
        users = UserDetails.query.all()
        events = Event.query.all()

        user_ids = [user.id for user in users]
        event_ids = [event.id for event in events]

        user_event_matrix = np.zeros((len(user_ids), len(event_ids)))

        for user in users:
            for event in user.events:
                user_event_matrix[user_ids.index(user.id)][event_ids.index(event.id)] = 1

        return user_ids, event_ids, user_event_matrix

    def train(self):
        """
        Train the recommendation model.
        """
        user_ids, event_ids, user_event_matrix = self.prepare_data()

        num_users = len(user_ids)
        num_events = len(event_ids)

        user_input = tf.keras.layers.Input(shape=(1,))
        event_input = tf.keras.layers.Input(shape=(1,))

        user_embedding = tf.keras.layers.Embedding(num_users, 50)(user_input)
        event_embedding = tf.keras.layers.Embedding(num_events, 50)(event_input)

        dot_product = tf.keras.layers.Dot(axes=2)([user_embedding, event_embedding])
        output = tf.keras.layers.Flatten()(dot_product)

        self.model = tf.keras.models.Model(inputs=[user_input, event_input], outputs=output)
        self.model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        user_indices, event_indices = np.where(user_event_matrix > 0)
        labels = user_event_matrix[user_indices, event_indices]

        self.model.fit(
            [user_indices, event_indices],
            labels,
            epochs=10,
            batch_size=32
        )

    def recommend(self, user_id, top_n=5):
        """
        Recommend top N events for a given user.
        """
        if not self.model:
            raise ValueError("Model is not trained yet.")

        user_ids, event_ids, _ = self.prepare_data()

        if user_id not in user_ids:
            raise ValueError(f"User ID {user_id} not found.")

        user_index = user_ids.index(user_id)
        event_scores = self.model.predict([np.array([user_index] * len(event_ids)), np.arange(len(event_ids))])

        top_event_indices = np.argsort(event_scores.flatten())[::-1][:top_n]
        recommended_event_ids = [event_ids[i] for i in top_event_indices]

        return recommended_event_ids


recommendation_model = RecommendationModel()

def train_recommendation_model():
    recommendation_model.train()
    return recommendation_model

def recommend_events(user_id, model, top_n=5):
    return model.recommend(user_id, top_n)
