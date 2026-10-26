import { api } from "./axios";

export const reviewsAPI = {
  // Get all reviews for a product
  getReviews: async (productId) => {
    const response = await api.get(`/products/${productId}/reviews`);
    return response.data;
  },

  // Get average rating and count
  getRatingSummary: async (productId) => {
    const response = await api.get(`/products/${productId}/reviews/summary`);
    return response.data;
  },

  // Submit or update a review
  submitReview: async (productId, reviewData) => {
    const response = await api.post(`/products/${productId}/reviews`, reviewData);
    return response.data;
  },

  // Delete review
  deleteReview: async (reviewId) => {
    await api.delete(`/reviews/${reviewId}`);
  }
};
