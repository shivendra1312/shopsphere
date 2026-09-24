import { api } from "./axios";

export const productsAPI = {
  // 1. Get all products with filters
  getProducts: async (params = {}) => {
    // params can be { search: "shirt", limit: 20, skip: 0, category_id: 4 }
    const response = await api.get("/products", { params });
    return response.data;
  },

  // 2. Get a single product by ID (Aage detail page me kaam aayega)
  getProduct: async (id) => {
    const response = await api.get(`/products/${id}`);
    return response.data;
  },

  // 3. Create a new product (Admin only)
  createProduct: async (productData) => {
    const response = await api.post("/products", productData);
    return response.data;
  },
};

export const categoriesAPI = {
  // Get all categories for the filter sidebar
  getCategories: async () => {
    const response = await api.get("/categories");
    return response.data;
  },

  // Create a new category (Admin only)
  createCategory: async (categoryData) => {
    const response = await api.post("/categories", categoryData);
    return response.data;
  }
};
