import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { productsAPI } from '../api/products';
import { cartAPI, wishlistAPI } from '../api/cart';
import { reviewsAPI } from '../api/reviews';
import { useAuth } from '../context/AuthContext';
import { Heart, Star, Trash2 } from 'lucide-react';
import './ProductDetail.css';

const ProductDetail = () => {
  // 1. URL se ID nikalna
  const { id } = useParams();
  
  // 2. State variables
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [adding, setAdding] = useState(false);
  const [added, setAdded] = useState(false);
  const [wAdding, setWAdding] = useState(false);
  const [wAdded, setWAdded] = useState(false);
  const { user } = useAuth();

  // Reviews states
  const [reviews, setReviews] = useState([]);
  const [ratingSummary, setRatingSummary] = useState({ average_rating: 0, total_reviews: 0 });
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState('');
  const [submittingReview, setSubmittingReview] = useState(false);
  const [reviewError, setReviewError] = useState('');

  const fetchReviews = async () => {
    try {
      const [revs, sum] = await Promise.all([
        reviewsAPI.getReviews(id),
        reviewsAPI.getRatingSummary(id)
      ]);
      setReviews(revs);
      setRatingSummary(sum);
    } catch (err) {
      console.error("Reviews load error:", err);
    }
  };

  // 3. Data lana
  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const data = await productsAPI.getProduct(id);
        setProduct(data);
      } catch (error) {
        console.error("Product nahi mila", error);
      }
      setLoading(false);
    };

    fetchProduct();
    fetchReviews();
  }, [id]); // Agar ID badle toh naya data lao

  const handleSubmitReview = async (e) => {
    e.preventDefault();
    if (!comment.trim()) {
      setReviewError("Please write a review comment.");
      return;
    }
    setReviewError('');
    setSubmittingReview(true);
    try {
      await reviewsAPI.submitReview(id, { rating, comment });
      setComment('');
      fetchReviews();
    } catch (err) {
      const msg = err.response?.data?.detail || "Could not submit review.";
      setReviewError(msg);
    }
    setSubmittingReview(false);
  };

  const handleDeleteReview = async (reviewId) => {
    try {
      await reviewsAPI.deleteReview(reviewId);
      fetchReviews();
    } catch (err) {
      console.error("Delete review error:", err);
    }
  };

  // 4. Loading state
  if (loading) {
    return <div className="product-detail-page"><h2>Loading product details...</h2></div>;
  }

  // 5. Agar API ne error diya (e.g. invalid ID)
  if (!product) {
    return <div className="product-detail-page"><h2>Product not found!</h2></div>;
  }

  return (
    <div className="product-detail-page">
      <div className="detail-card">
        
        <span className="detail-category">
          {product.category ? product.category.name : 'Uncategorized'}
        </span>
        
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '10px' }}>
          <h1 className="detail-title">{product.title}</h1>
          {ratingSummary.total_reviews > 0 && (
            <div className="rating-badge">
              ⭐ {ratingSummary.average_rating} ({ratingSummary.total_reviews} {ratingSummary.total_reviews === 1 ? 'review' : 'reviews'})
            </div>
          )}
        </div>
        
        <div className="detail-description">
          {product.description}
        </div>
        
        <div className="detail-bottom">
          <div className="detail-price">${product.price.toFixed(2)}</div>
          
          <div style={{ display: 'flex', gap: '10px' }}>
            <button 
              className="add-to-cart-btn" 
              style={{ background: 'transparent', border: '1px solid #fc8181', color: '#fc8181', padding: '0 15px' }}
              disabled={wAdding || !user}
              onClick={async () => {
                setWAdding(true);
                try {
                  await wishlistAPI.addToWishlist(product.id);
                  setWAdded(true);
                  setTimeout(() => setWAdded(false), 2000);
                } catch (err) {
                  console.error("Wishlist error", err);
                }
                setWAdding(false);
              }}
              title="Add to Wishlist"
            >
              <Heart size={20} fill={wAdded ? "#fc8181" : "none"} />
            </button>

            <button 
              className="add-to-cart-btn" 
              disabled={product.stock === 0 || adding || !user}
            onClick={async () => {
              setAdding(true);
              try {
                await cartAPI.addToCart(product.id, 1);
                setAdded(true);
                setTimeout(() => setAdded(false), 2000);
              } catch (err) {
                console.error("Add to cart failed", err);
              }
              setAdding(false);
            }}
          >
            {product.stock === 0 ? "Out of Stock" : added ? "✓ Added!" : adding ? "Adding..." : !user ? "Login to Add" : "Add to Cart"}
            </button>
          </div>
        </div>
        
        <div style={{ color: product.stock < 5 ? '#ecc94b' : '#a0aec0', fontSize: '0.9rem' }}>
          {product.stock > 0 ? `${product.stock} items available in stock` : 'Currently unavailable'}
        </div>

        {/* ---- REVIEWS SECTION ---- */}
        <div className="reviews-container">
          <div className="reviews-header">
            <h2>
              Customer Reviews 
              {ratingSummary.total_reviews > 0 ? `(${ratingSummary.total_reviews})` : ''}
            </h2>
          </div>

          {/* Review submission form */}
          {user ? (
            <form className="review-form-card" onSubmit={handleSubmitReview}>
              <h3>Write a Review</h3>

              <div className="rating-stars-select">
                <span style={{ fontSize: '0.9rem', color: '#a0aec0', marginRight: '6px' }}>Rating:</span>
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    className={`star-btn ${star <= rating ? 'active' : ''}`}
                    onClick={() => setRating(star)}
                  >
                    ★
                  </button>
                ))}
                <span style={{ marginLeft: '10px', fontSize: '0.9rem', color: '#ecc94b', fontWeight: 600 }}>
                  {rating} / 5
                </span>
              </div>

              <textarea
                className="review-textarea"
                placeholder="Share your thoughts about this product..."
                value={comment}
                onChange={(e) => setComment(e.target.value)}
              />

              {reviewError && (
                <div style={{ color: '#fc8181', fontSize: '0.85rem' }}>⚠️ {reviewError}</div>
              )}

              <button
                type="submit"
                className="submit-review-btn"
                disabled={submittingReview}
              >
                {submittingReview ? "Submitting..." : "Submit Review"}
              </button>
            </form>
          ) : (
            <div style={{ color: '#a0aec0', fontSize: '0.95rem' }}>
              Please login to leave a review for this product.
            </div>
          )}

          {/* Reviews list */}
          <div className="reviews-list">
            {reviews.length === 0 ? (
              <div className="no-reviews">No reviews yet. Be the first to review this product!</div>
            ) : (
              reviews.map((rev) => (
                <div key={rev.id} className="review-card">
                  <div className="review-card-top">
                    <div>
                      <span className="review-author">
                        {rev.user ? (rev.user.first_name || rev.user.email) : 'Verified Buyer'}
                      </span>
                      <span className="review-date">
                        {new Date(rev.created_at).toLocaleDateString()}
                      </span>
                    </div>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <span className="review-stars">
                        {'★'.repeat(rev.rating)}{'☆'.repeat(5 - rev.rating)}
                      </span>

                      {user && (user.id === rev.user_id || user.role === 'ADMIN' || user.role === 'admin') && (
                        <button
                          className="delete-review-btn"
                          onClick={() => handleDeleteReview(rev.id)}
                          title="Delete review"
                        >
                          <Trash2 size={16} />
                        </button>
                      )}
                    </div>
                  </div>

                  <p className="review-comment">{rev.comment}</p>
                </div>
              ))
            )}
          </div>
        </div>

      </div>
    </div>
  );
};

export default ProductDetail;
