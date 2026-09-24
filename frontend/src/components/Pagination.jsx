import React from 'react';
import './Pagination.css';

const Pagination = ({ page, setPage, hasMore }) => {
  const handlePrev = () => {
    if (page > 1) {
      setPage(page - 1);
    }
  };

  const handleNext = () => {
    if (hasMore) {
      setPage(page + 1);
    }
  };

  return (
    <div className="pagination-container">
      <button 
        className="pagination-btn" 
        onClick={handlePrev} 
        disabled={page === 1}
      >
        Previous
      </button>
      
      <span className="page-info">Page {page}</span>
      
      <button 
        className="pagination-btn" 
        onClick={handleNext} 
        disabled={!hasMore}
      >
        Next
      </button>
    </div>
  );
};

export default Pagination;
