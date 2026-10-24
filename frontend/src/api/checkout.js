import { api } from "./axios";

export const checkoutAPI = {
  addAddress: async (addressData) => {
    const response = await api.post("/addresses", addressData);
    return response.data;
  },
  getAddresses: async () => {
    const response = await api.get("/addresses");
    return response.data;
  },
  deleteAddress: async (addressId) => {
    await api.delete(`/addresses/${addressId}`);
  },
  createOrder: async (addressId) => {
    const response = await api.post("/orders", { address_id: addressId });
    return response.data;
  },
  getOrders: async () => {
    const response = await api.get("/orders");
    return response.data;
  },
  // Admin: saare orders
  getAllOrders: async () => {
    const response = await api.get("/orders/all");
    return response.data;
  },
  // Admin: status update
  updateOrderStatus: async (orderId, status) => {
    const response = await api.patch(`/orders/${orderId}/status`, { status });
    return response.data;
  }
};
