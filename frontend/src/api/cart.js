import { api } from "./axios";

export const cartAPI = {
  // User ki cart lana
  getCart: async () => {
    const response = await api.get("/cart");
    return response.data;
  },

  // Product ko cart me daalna
  addToCart: async (product_id, quantity = 1) => {
    const response = await api.post("/cart", { product_id, quantity });
    return response.data;
  },

  // Cart item ki quantity update karna
  updateCartItem: async (item_id, quantity) => {
    const response = await api.put(`/cart/${item_id}`, { quantity });
    return response.data;
  },

  // Cart se ek item hatana
  removeFromCart: async (item_id) => {
    await api.delete(`/cart/${item_id}`);
  },

  // Poori cart khali karna
  clearCart: async () => {
    await api.delete("/cart");
  }
};

export const wishlistAPI = {
  // User ki wishlist lana
  getWishlist: async () => {
    const response = await api.get("/wishlist");
    return response.data;
  },

  // Wishlist me add karna
  addToWishlist: async (product_id) => {
    const response = await api.post("/wishlist", { product_id });
    return response.data;
  },

  // Wishlist se hatana
  removeFromWishlist: async (item_id) => {
    await api.delete(`/wishlist/${item_id}`);
  }
};
