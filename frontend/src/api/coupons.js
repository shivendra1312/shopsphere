import { api } from "./axios";

export const couponsAPI = {
  // Apply coupon code against cart amount
  applyCoupon: async (code, orderAmount) => {
    const response = await api.post("/coupons/apply", {
      code,
      order_amount: orderAmount
    });
    return response.data;
  },

  // Admin: get all coupons
  getCoupons: async () => {
    const response = await api.get("/coupons");
    return response.data;
  },

  // Admin: create coupon
  createCoupon: async (couponData) => {
    const response = await api.post("/coupons", couponData);
    return response.data;
  }
};
